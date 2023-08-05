"""
Class with DFI analytic methods, leveraging on the python api wrappers to gain analytical informations.
Composition of the class DFIConnection.
"""

import logging
from datetime import datetime, timedelta
from functools import partial
from typing import List, Optional, Tuple

import branca  # pylint: disable=import-error
import geopandas as gpd
import h3.api.numpy_int as h3
import numpy as np
import pandas as pd
from shapely.geometry import Polygon
from shapely.wkt import loads
from tqdm import tqdm

from dfi.connection import DFIConnect
from dfi.getters import DFIGet

logger = logging.getLogger(__name__)

# TODO: rename pings to records everywhere (records are used in colocated_records and pings
# everywhere else).
# TODO: remanme history to historical_records?
# TODO: remove ipython from the list of requirements, as not needed for the
# library, and can causes conflicts with colab.


class DFIAnalyse:
    """
    Class with analytical methods to build use cases on top of the DFI's queries.

    It must be instantiated with a DFIConnect instance as argument.

    Parameters
    ----------
    dfi_conn : DFIConnect
        Instance of a DFIConnect with the credentials and namespace of the DFI connection.

    Examples
    --------
    >>> dfi_conn = dfi.DFIConnect(api_token=api_token, namespace=namespace, instance_name=instance_name)
    >>> dfi_analyse = dfi.DFIAnalyse(dfi_conn)
    >>> dfi_analyse.pings_in_hexagons(uid, resolution, period)
    """

    def __init__(self, dfi_conn: DFIConnect) -> None:
        self.dfi_conn: DFIConnect = dfi_conn
        self.dfi_get: DFIGet = DFIGet(self.dfi_conn)

    def __repr__(self):
        return f"{self.__class__.__name__}({self.dfi_conn!r})({self.dfi_get!r}) {self.__dict__}"

    def __str__(self):
        return f"""DFI Python API: instance of {self.__class__.__name__}
                   composed with {self.dfi_conn!r} and instantiating {self.dfi_get!r}"""

    @staticmethod
    def summarise_by_day(df_history: pd.DataFrame) -> pd.DataFrame:
        """
        Aggregate the a dataframe of historical records by day.

         Parameters
        ----------
        df_history : pd.DataFrame
            Dataframe with a "timestamp" column.

        Returns
        -------
        df_summary : pd.DataFrame
            The input dataframe aggregated by number of events per day
        """
        # TODO: this method may be out of scope for this library and it may need to go.
        df_summary = df_history.copy()
        df_summary["time"] = df_summary["timestamp"].dt.time  # extract time only
        df_summary.set_index("timestamp", inplace=True)
        # group by 'group' column and apply aggregation functions
        df_summary = df_summary.groupby(pd.Grouper(freq="D")).agg(
            min_value=("time", "min"), max_value=("time", "max"), count=("time", "count")
        )
        # reset index to get the group column as a regular column again
        df_summary = df_summary.reset_index()
        return df_summary

    def pings_in_hexagons(
        self,
        uid: str,
        resolution: int,
        period: int,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
        vertices: Optional[List[List[float]]] = None,
    ) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """
        Binning the records of a device id by time (period) and space (H3 resolution)
        and with optional additional spatial and temporal constraints.

        Parameters
        ----------
        uid : str
            unique identifier of a device we want to analyse.
        resolution: int
            Uber's H3 resolution. Allowed numbers are > 1 and < 15.
        period: int
            Time interval in minutes for timestamp binning. Allowed values are 1, 5, 10, 15, 30.
        start_time: Optional[datetime] = None
            Lower bound for clipping the time interval of the historical records.
        end_time: Optional[datetime] = None
            Upper bound for clipping the time interval of the historical records.
        vertices: Optional[List[List[float]]] = None
            Sequence of vertices making a polygon with the geographical boundaries.

        Returns
        -------
        df_history : pd.DataFrame, df_hexagons : pd.DataFrame
            A tuple containing a dataframe with the historical records for the given uid with the specified
            time and space boundaries and a dataframe with the hexagon geometries, with time and space indexing.
        """
        # TODO: rename resolution and period to h3_resolution and time_resolution_min
        # TODO: allow for any number of minutes > 0
        # TODO: use a shapely polygon instead of a list of vertices (that may not constitute a valid polygon).
        # TODO (Robert): specify if the vertices as they are are (lat, lon) or (lon, lat)

        # TODO (Robert):
        # - the name of this function indicates it’s essentially the same as polygon_history but it’s doing a lot more
        # - return type indicates return of a single dataframe but it’s return a tuple of dataframes
        # - there’s no doc string to describe this function and it’s not clear from the code what it’s purpose is either

        # TODO: add an example with the output in the docstring.

        # TODO: this function does not do what the name promise, there should be only one output
        # TODO: rename function.

        if vertices is None:
            df_history = self.dfi_get.history(uid, start_time=start_time, end_time=end_time)
        else:
            df_history = self.dfi_get.polygon_history(
                include_list=[uid], vertices=vertices, start_time=start_time, end_time=end_time
            )
        if len(df_history) == 0:
            logger.warning("No history fund for entity %s", uid)
            return None, None
        if period not in [1, 5, 10, 15, 30]:
            raise ValueError("Period in minutes must be one of 1, 5, 10, 15, 30")
        if resolution < 1 or resolution > 15:
            raise ValueError("Resolution is incorrect")
        df_hexagons = df_history.copy()
        for row in range(len(df_hexagons)):
            hex_id = h3.geo_to_h3(
                df_hexagons.at[row, "latitude"],
                df_hexagons.at[row, "longitude"],
                resolution,
            )
            df_hexagons.at[row, "hex_id"] = hex(hex_id)[2:]
            df_hexagons.at[row, "hex_polygon"] = Polygon(h3.h3_to_geo_boundary(hex_id, geo_json=True))
            df_hexagons.at[row, "period_start"] = df_hexagons.at[row, "timestamp"].round(f"{period}min")
        df_hexagons["hex_polygon"] = df_hexagons["hex_polygon"].astype(str)
        df_hexagons["hex_id"] = df_hexagons["hex_id"].astype(str)
        # TODO: combine hex_id and period_start in a single index
        # TODO: agg and count instead of dropping duplicates, to have the number of pings per index in a column.
        df_hexagons = df_hexagons.drop_duplicates(subset=["hex_id", "period_start"])
        df_hexagons = df_hexagons.drop(["entity_id", "latitude", "longitude", "timestamp"], axis=1)
        # TODO: convert df_hexagons into a geodataframe, with geometry=hex_polygon
        df_hexagons = df_hexagons.assign(
            period_end=lambda df: df.period_start + timedelta(minutes=period),
        )
        df_hexagons = df_hexagons.sort_values(by="period_start", ascending=True)
        return df_history, df_hexagons

    def pings_in_hexagons_bbox(
        self,
        uid: str,
        resolution: int,
        period: int,
        min_lon: float,
        min_lat: float,
        max_lon: float,
        max_lat: float,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
    ) -> pd.DataFrame:
        """
        Binning the records of a device id by time (period) and space (H3 resolution)
        bounded by space with bounding box parameters, and with optional bounding box by time.

        Parameters
        ----------
        uid : str
            unique identifier of a device we want to analyse.
        resolution: int
            Uber's H3 resolution. Allowed numbers are > 1 and < 15.
        period: int
            Time interval in minutes for timestamp binning. Allowed values are 1, 5, 10, 15, 30.
        min_lon: float,  min_lat: float, max_lon: float, max_lat: float
            Bounding box parameters.
        start_time: Optional[datetime] = None
            Lower bound for clipping the time interval of the historical records.
        end_time: Optional[datetime] = None
            Upper bound for clipping the time interval of the historical records.

        Returns
        -------
        df_subset : pd.DataFrame
            Dataframe with columns "hex_id", "hex_polygon", "period_start", "period_end"
        min_time_range: int
            df_subset.period_start.min()
        max_time_range: int
            df_subset.period_start.max()
        """
        _, df_hexagons = self.pings_in_hexagons(uid, resolution, period, start_time=start_time, end_time=end_time)
        logger.warning("We found %i hexagons", len(df_hexagons))

        # TODO: be DRY and call instead pings_in_hexagons, passing the bounding_box as its vertices,
        # rather than filtering downstream. Use from_bbox_to_polygon_list and pass the values as vertices.
        # TODO: df_subset should have the number of pings per row.

        # Bounding box to Polygon
        bounding_box = Polygon(
            [
                (min_lon, min_lat),
                (max_lon, min_lat),
                (max_lon, max_lat),
                (min_lon, max_lat),
            ]
        )

        df_subset = pd.DataFrame(columns=["hex_id", "hex_polygon", "period_start", "period_end"])
        # Loop through the hexagons and check if they fit within the bounding box
        for _, row in tqdm(df_hexagons.iterrows(), total=len(df_hexagons)):
            # Convert the H3 hexagon to a Polygon object
            hexagon_polygon = loads(row["hex_polygon"])
            # Check if the Polygon object intersects with the bounding box
            if bounding_box.intersects(hexagon_polygon):
                new_row = {
                    "hex_id": row["hex_id"],
                    "hex_polygon": row["hex_polygon"],
                    "period_start": row["period_start"],
                    "period_end": row["period_end"],
                }
                df_subset = pd.concat([df_subset, pd.DataFrame([new_row])], ignore_index=True, axis=0)
        logger.warning("number of hexagons: %i", len(df_subset))
        min_time_range = df_subset.period_start.min()
        max_time_range = df_subset.period_start.max()
        logger.info("Min time range: %s", str(min_time_range))
        logger.info("Max time range: %s", str(max_time_range))
        # TODO: do not return min_time_range, max_time_range as the user can easily get them from df_subset.
        return df_subset, min_time_range, max_time_range

    def colocated_records(self, uid: str, df_hexagons: pd.DataFrame) -> pd.DataFrame:
        """
        Finds the devices that are co-located with the specified device id,
        bounded by the hexagons specified in the given dataframe.

        Parameters
        ----------
        uid : str
            unique identifier of a device we want to analyse.
        df_hexagons: pd.DataFrame
            Dataframe with hexagons polygon embedded in its column "hex_polygon".

        Returns
        -------
        df_records : pd.DataFrame
            Dataframe with columns "hex_id", "longitude", "latitude", "entity_id", "timestamp" with all the
            records of the devices co-located with uid at the specified hexagons.
        """
        # TODO: add sanity check for df_hexagons columns and types.
        # TODO: convert df_hexagons to geodataframe with hexagons encoded in the geometry column.
        # TODO (robert): colocated_records() requires a hexagons dataframe be passed into it, indicating
        # that another function needs to be called first.  Why not include all the relevant parts to
        # calculate collocations inside this function?  How is a user supposed to know they need to call
        # another function first?
        logger.info("Colocated records: querying hexagons ...")
        df_records = pd.DataFrame(columns=["hex_id", "longitude", "latitude", "entity_id", "timestamp"])
        for _, row in tqdm(df_hexagons.iterrows(), total=len(df_hexagons)):
            polygon_vertices = list(loads(row.hex_polygon).exterior.coords)  # pylint: disable=no-member
            data = self.dfi_get.neighbours(
                row.hex_id,
                polygon_vertices,
                min_time=row.period_start,
                max_time=row.period_end,
            )
            df_data = pd.DataFrame(data)
            if len(df_data) > 0:
                df_data = df_data[df_data["entity_id"] != uid]
            df_records = pd.concat([df_records, df_data], ignore_index=True, axis=0)
            # logger.info(f"    - HexId: {row.hex_id}, {row.period_start} found {len(df_data)} records")
        return df_records

    @staticmethod
    def from_bbox_to_polygon_list(min_lon: float, min_lat: float, max_lon: float, max_lat: float) -> List[List[float]]:
        """Convert a bounding box into a list of vertices"""
        return [[max_lon, max_lat], [max_lon, min_lat], [min_lon, min_lat], [min_lon, max_lat], [max_lon, max_lat]]

    @staticmethod
    def aggregate_h3_hexes(
        df_input: pd.DataFrame,
        resolution: int,
        colorscale_col: str = "num_pings",
        colorscale_log_transform: bool = True,
    ) -> gpd.GeoDataFrame:
        """
        Finds the devices that are co-located with the specified device id,
        bounded by the hexagons specified in the given dataframe.

        Parameters
        ----------
        df_input: pd.DataFrame
            unique identifier of a device we want to analyse.
        resolution: int
            Uber's H3 resolution. Allowed numbers are > 1 and < 15.
        colorscale_col: str = "num_pings"
            Name of the column with the colorscale for visualisation.
        colorscale_log_transform: bool = True,
            Log transform the colorscale.

        Returns
        -------
        df_input : pd.DataFrame
            Returns the given dataframe with two extra `hex_id` and `color` column. The operation happens in place.
        """
        return (
            df_input.assign(
                hex_id=lambda df: [
                    h3.geo_to_h3(lat, lon, resolution=resolution) for lat, lon in zip(df["latitude"], df["longitude"])
                ]
            )
            .pipe(_aggregate_pings, "hex_id")
            .assign(
                hex_id=lambda df: df.hex_id.map(hex).str[2:],
                color=lambda df: _assign_colors(df[colorscale_col], colorscale_log_transform=colorscale_log_transform),
            )
        )


def _aggregate_pings(df_input: pd.DataFrame, hex_id: str) -> pd.DataFrame:
    return (
        df_input.groupby(hex_id)
        .agg(
            num_pings=("entity_id", "count"),
            num_devices=("entity_id", "nunique"),
            first_ping=("timestamp", "min"),
            last_ping=("timestamp", "max"),
        )
        .reset_index()
    )


def _assign_colors(df_input: pd.Series, colorscale_log_transform: bool) -> pd.Series:
    if not df_input.empty:
        if colorscale_log_transform:
            df_input = _transform_to_log(df_input)
        colormap = _create_colormap(df_input)
        return df_input.map(partial(_count_to_rgb_tuple, colormap=colormap))
    else:
        return df_input


def _transform_to_log(df_input: pd.Series) -> pd.Series:
    """normalise and transform a series to log scale"""
    return pd.Series(np.log(1 + df_input / 2))


def _create_colormap(df_input: pd.Series) -> branca.colormap.StepColormap:
    legend_steps = np.linspace(0, df_input.max(), 100)
    colormap = branca.colormap.linear.YlOrRd_09.scale(0, 100)  # pylint: disable=no-member
    return colormap.to_step(index=legend_steps)


def _count_to_rgb_tuple(count: int, colormap: branca.colormap.StepColormap) -> str:
    hex_color = colormap(count).lstrip("#")
    return tuple(int(hex_color[i : i + 2], base=16) for i in (0, 2, 4))
