"""
Class with DFI getters, srappers of the DFI python API.
Composition of the class DFIConnection.
"""

import json
import logging
from datetime import datetime
from typing import List, Optional

import pandas as pd
import requests
from requests.exceptions import ConnectionError as RequestsConnectionError
from tqdm import tqdm

from dfi import stream
from dfi.connection import DFIConnect

logger = logging.getLogger(__name__)


# TODO: rename uid to device_id and uid to list_device_ids?

# TODO (Robert): count() & entities() - these functions only take as parameters, start_time and end_time,
# there’s no argument for polygon or vertices or bbox.  There are polygon_count() and polygon_entities()
# which appear to be the same but can add a polygon filter.
# TODO: possibly reduce duplicates and have only a single function with optional polygon or bbox as shapely.

# TODO (Robert): Would be helpful to have some functions for adding/retrieving polygons
# to the PostGIS instance

# TODO (Robert): There’s no bbox() function to query data given a bounding box,
# isn’t there an endpoint for this?


class DFIGet:
    """
    Class responsible to call the HTTP API and submit queries.

    It must be instantiated with a DFIConnect instance as argument.

    Parameters
    ----------
    dfi_conn : DFIConnect
        Instance of a DFIConnect with the credentials and namespace of the DFI connection.

    Examples
    --------
    >>> dfi_conn = dfi.DFIConnect(api_token=api_token, namespace=namespace, instance_name=instance_name)
    >>> dfi_get = dfi.DFIGet(dfi_conn)
    >>> dfi_get.entities(start_time, end_time)

    """

    def __init__(self, dfi_conn: DFIConnect) -> None:
        self.dfi_conn: DFIConnect = dfi_conn

    def __repr__(self):
        return f"{self.__class__.__name__}({self.dfi_conn!r}) {self.__dict__}"

    def __str__(self):
        return f"DFI Python API: instance of {self.__class__.__name__} composed with {self.dfi_conn!r}."

    @staticmethod
    def _check_response(
        response: requests.Response,
        url: str,
        headers: dict,
        params: dict,
        my_payload: Optional[dict] = None,
    ) -> None:
        """Log the response of a request with the given parameters. Raise an error if status code is not 20x."""
        # prevent from showing the user token to terminal and logs
        headers = headers.copy()
        headers["X-API-TOKEN"] = "Bearer XXX"

        msg = f"""Response status code {response.status_code}.
Query URL: {url},
HEADER: {json.dumps(headers, sort_keys=True, indent=4)},
PARAMS: {json.dumps(params, sort_keys=True, indent=4)}
"""
        if my_payload is not None:
            msg += f"PAYLOAD: {json.dumps(my_payload, sort_keys=True, indent=4)}"

        if int(response.status_code / 10) != 20:
            logger.error(msg)
            raise RequestsConnectionError(msg)
        else:
            logger.debug(msg)

    def api_version(self) -> str:
        """
        Version of the Data Flow Index.
        """
        my_url = f"{self.dfi_conn.base_url}/version"
        my_headers = self.dfi_conn.streaming_headers

        with requests.get(
            url=my_url,
            headers=my_headers,
            timeout=self.dfi_conn.query_timeout,
            stream=True,
        ) as response:
            self._check_response(response, my_url, my_headers, {})
            return response.text

    def count(self, start_time: Optional[datetime] = None, end_time: Optional[datetime] = None) -> int:
        """
        Returns the number of records stored in the DFI engine with an optional time constraint.

        Parameters
        ----------
        start_time: Optional[datetime] = None
            Lower bound for the time constraint.

        end_time: Optional[datetime] = None
            Upper bound for the time constraint.

        Returns
        -------
            The number of records stored in the DFI engine.
        """

        # TODO: verify output type.

        my_params = {"instance": self.dfi_conn.qualified_instance_name}
        if start_time is not None:
            my_params["startTime"] = start_time.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        if end_time is not None:
            my_params["endTime"] = end_time.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        my_url = f"{self.dfi_conn.base_url}/count"
        my_headers = self.dfi_conn.streaming_headers

        with requests.get(
            url=my_url,
            headers=my_headers,
            params=my_params,
            timeout=self.dfi_conn.query_timeout,
            stream=True,
        ) as response:
            self._check_response(response, my_url, my_headers, my_params)
            return stream.receive_count(response, self.dfi_conn.progress_bar)

    def entities(self, start_time: Optional[datetime] = None, end_time: Optional[datetime] = None) -> int:
        """
        Returns the number of entities stored in the DFI engine with an optional time constraint.

        Parameters
        ----------
        start_time: Optional[datetime] = None
            Lower bound for the time constraint.

        end_time: Optional[datetime] = None
            Upper bound for the time constraint.

        Returns
        -------
            The number of entities stored in the DFI engine.
        """

        # TODO: verify output type.

        my_params = {"instance": self.dfi_conn.qualified_instance_name}
        if start_time is not None:
            my_params["startTime"] = start_time.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        if end_time is not None:
            my_params["endTime"] = end_time.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        my_url = f"{self.dfi_conn.base_url}/entities"
        my_headers = self.dfi_conn.streaming_headers

        with requests.get(
            my_url,
            headers=my_headers,
            params=my_params,
            timeout=self.dfi_conn.query_timeout,
            stream=True,
        ) as response:
            self._check_response(response, my_url, my_headers, my_params)
            return stream.receive_entities(response, self.dfi_conn.progress_bar)

    def entity_count(self, uid: str, start_time: Optional[datetime] = None, end_time: Optional[datetime] = None) -> int:
        """
        Count the records for a given uid, with the optional time interval constraint.

        Parameters
        ----------
        uid: str
            Entity unique id.

        start_time: Optional[datetime] = None
            Lower bound for the time constraint.

        end_time: Optional[datetime] = None
            Upper bound for the time constraint.

        Returns
        -------
            Number of records for the given uid, and within the optional time interval constraint.
        """
        # TODO: rename to records_count_by_id?
        # TODO: this function counts the records (pings) for a uid not the entities (deivice ids.)
        my_params = {"instance": self.dfi_conn.qualified_instance_name}
        if start_time is not None:
            my_params["startTime"] = start_time.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        if end_time is not None:
            my_params["endTime"] = end_time.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        my_url = f"{self.dfi_conn.base_url}/entities/{uid}/count"
        my_headers = self.dfi_conn.streaming_headers

        with requests.get(
            my_url,
            headers=my_headers,
            params=my_params,
            timeout=self.dfi_conn.query_timeout,
            stream=True,
        ) as response:
            self._check_response(response, my_url, my_headers, my_params)
            return stream.receive_count(response, self.dfi_conn.progress_bar)

    def polygon_count(
        self,
        polygon: Optional[str] = None,
        vertices: Optional[List[List[float]]] = None,
        include_list: Optional[List[any]] = None,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
    ) -> int:
        """
        Get the number of elements within a polygon.
        The polygon can be passed by name from the persistent database or by vertices.
        Optional lower and upper bounds for the time constraints can be added.

        Parameters
        ----------
        polygon: Optional[str] = None
            Name of a polygon already stored in the database.

        vertices: Optional[List[List[float]]] = None
            List of vertices of a polygon

        include_list: Optional[List[any]] = None
            Set of entity_ids that results will be further filtered by.

        start_time: Optional[datetime] = None
            Lower bound for the time constraint.

        end_time: Optional[datetime] = None
            Upper bound for the time constraint.

        Returns
        -------
            Number of points in the polygon, given the input constraints.
        """
        # TODO: rename to records_count_by_polygon?
        # TODO: refactor to take a shapely.Polyogn instead of a list of vertices, that may not be a valid polygon?
        # TODO: Not clear what include_list is intended for by the name.
        # Find a better name here and in previous functions?
        # TODO: Split into two function, one by vertices, one by polygon name? This should be done at API level.
        # Alternatively join the variables into one and distinguish by the type.
        # TODO: specify if the vertices as they are are (lat, lon) or (lon, lat)

        my_params = {"instance": self.dfi_conn.qualified_instance_name}
        my_payload = {}
        if start_time is not None:
            my_payload["startTime"] = start_time.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        if end_time is not None:
            my_payload["endTime"] = end_time.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        if include_list is not None:
            my_payload["include"] = include_list
        if polygon is not None and vertices is not None:
            logger.warning("You cannot specify both Polygon and Vertices. Pick one")
            return
        if polygon is not None:
            my_payload["name"] = polygon
        if vertices is not None:
            my_payload["vertices"] = vertices
        my_url = f"{self.dfi_conn.base_url}/polygon/count"
        my_headers = self.dfi_conn.streaming_headers

        with requests.post(
            my_url,
            headers=my_headers,
            json=my_payload,
            params=my_params,
            timeout=self.dfi_conn.query_timeout,
            stream=True,
        ) as response:
            self._check_response(response, my_url, my_headers, my_params)
            return stream.receive_count(response, self.dfi_conn.progress_bar)

    def polygon_entities(
        self,
        polygon: str = None,
        vertices: List[List[float]] = None,
        include_list: List[any] = None,
        start_time: datetime = None,
        end_time: datetime = None,
    ) -> List[any]:
        """
        Get the number of entities within a polygon.
        The polygon can be passed by name from the persistent database or by vertices.
        Optional lower and upper bounds for the time constraints can be added.

        Parameters
        ----------
        polygon: Optional[str] = None
            Name of a polygon already stored in the database.

        vertices: Optional[List[List[float]]] = None
            List of vertices of a polygon

        include_list: Optional[List[any]] = None
            Set of entity_ids that results will be further filtered by.

        start_time: Optional[datetime] = None
            Lower bound for the time constraint.

        end_time: Optional[datetime] = None
            Upper bound for the time constraint.

        Returns
        -------
            List of unique entities in polygon given, the input constraints.
        """

        # TODO: rename to entities_count_by_polygon?
        # TODO: refactor to take a shapely.Polyogn instead of a list of vertices, that may not be a valid polygon?
        # TODO: should include_list be documented on the API as well?
        # TODO: Split into two function, one by vertices, one by polygon name? This should be done at API level.
        # Alternatively join the variables into one and distinguish by the type.
        # TODO: specify if the vertices as they are are (lat, lon) or (lon, lat)

        my_params = {"instance": self.dfi_conn.qualified_instance_name}
        my_payload = {}
        if start_time is not None:
            my_payload["startTime"] = start_time.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        if end_time is not None:
            my_payload["endTime"] = end_time.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        if include_list is not None:
            my_payload["include"] = include_list
        if polygon is not None and vertices is not None:
            logger.warning("You cannot specify both Polygon and Vertices. Pick one")
            return
        if polygon is not None:
            my_payload["name"] = polygon
        if vertices is not None:
            my_payload["vertices"] = vertices
        my_url = f"{self.dfi_conn.base_url}/polygon/entities"
        my_headers = self.dfi_conn.streaming_headers

        with requests.post(
            my_url,
            headers=my_headers,
            json=my_payload,
            params=my_params,
            timeout=self.dfi_conn.query_timeout,
            stream=True,
        ) as response:
            self._check_response(response, my_url, my_headers, my_params, my_payload)
            return stream.receive_entities(response, self.dfi_conn.progress_bar)

    def polygon_history(
        self,
        polygon: str = None,
        vertices: List[List[float]] = None,
        include_list: List[any] = None,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
        parse_payload_as_json: bool = False,
    ) -> pd.DataFrame:
        """
        Get the trajectories of the entities appearing within a polygon.
        The polygon can be passed by name from the persistent database or by vertices.
        Optional lower and upper bounds for the time constraints can be added.

        Parameters
        ----------
        polygon: Optional[str] = None
            Name of a polygon already stored in the database.

        vertices: Optional[List[List[float]]] = None
            List of vertices of a polygon

        include_list: Optional[List[any]] = None
            Set of entity_ids that results will be further filtered by.

        start_time: Optional[datetime] = None
            Lower bound for the time constraint.

        end_time: Optional[datetime] = None
            Upper bound for the time constraint.

        parse_payload_as_json: bool = False
            If True it parses the payload as a JSON string into the column payload.

        Returns
        -------
            Dataframe with the trajectories of the entities found in polygon, given the input constraints.
        """
        # TODO: verify output type is correct
        # TODO: are we returning the list of entities or the records? Not clear from the name.
        # TODO: confirm that we get the full trajectory and not only the points within
        # the polygon divide by type id.
        # In alpha, we treat TAI in a different way. We take ALL the pings in the database that
        # have appeared at least once in the polygon.
        # AFAIK it can be done with DFI, but only with two queries? Is it worth adding a new endpoint
        # to query all the pings that have appeared at least once in the given poly?
        # TODO: specify if the vertices as they are are (lat, lon) or (lon, lat)
        # TODO: Function names not standard - polygon_history() and history()
        # (I have to read the function parameters to understand this is for entities)
        my_params = {"instance": self.dfi_conn.qualified_instance_name}
        my_payload = {}
        if start_time is not None:
            my_payload["startTime"] = start_time.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        if end_time is not None:
            my_payload["endTime"] = end_time.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        if include_list is not None:
            my_payload["include"] = include_list
        if polygon is not None and vertices is not None:
            logger.warning("You cannot specify both Polygon and Vertices. Pick one")
            return
        if polygon is not None:
            my_payload["name"] = polygon
        if vertices is not None:
            my_payload["vertices"] = vertices
        my_url = f"{self.dfi_conn.base_url}/polygon/history"

        with requests.post(
            my_url,
            headers=self.dfi_conn.streaming_headers,
            json=my_payload,
            params=my_params,
            timeout=self.dfi_conn.query_timeout,
            stream=True,
        ) as response:
            self._check_response(response, my_url, self.dfi_conn.streaming_headers, my_params, my_payload)
            data = stream.receive_history(response, self.dfi_conn.progress_bar)

        data_formatted = []
        for item in data:
            if parse_payload_as_json:
                try:
                    payload = json.loads(item["payload"])
                except Exception as err:
                    payload = {}
                    logger.debug("Failed to parse payload to JSON: %s", err)
            else:
                payload = item["payload"]
            data_formatted.append(
                [
                    item["id"],
                    datetime.strptime(item["time"], "%Y-%m-%dT%H:%M:%S.%fZ"),
                    item["coordinate"][0],
                    item["coordinate"][1],
                    payload,
                ]
            )
        df_uids = pd.DataFrame(data_formatted, columns=["entity_id", "timestamp", "longitude", "latitude", "payload"])
        if start_time is not None and end_time is not None:
            # TODO: error here if only one of the two constraints is passed. This shoud be split in two.
            # Also verify that the type of start_time and end_time are sane and can be compared w df_uid["timestamp"].
            # If the API does not allow for only one constraint (why not) then we should have the constraints passed as
            # a tuple and not a single entities.
            # TODO: also this is done already when querying the data, and so it is a duplicate
            return df_uids[(df_uids["timestamp"] >= start_time) & (df_uids["timestamp"] <= end_time)]
        return df_uids

    def history(
        self,
        uid: str,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
        parse_payload_as_json: bool = False,
    ) -> pd.DataFrame:
        """
        Get the trajectory of one entity, with optional time interval.

        Parameters
        ----------
        uid: str
            Entity unique id.

        start_time: Optional[datetime] = None
            Lower bound for the time constraint.

        end_time: Optional[datetime] = None
            Upper bound for the time constraint.

        parse_payload_as_json: bool = False
            If True it parses the payload as a JSON string into the column payload.

        Return
        -------
            Dataframe with columns "entity_id", "timestamp", "longitude", "latitude", "payload"
            The last column is empty if parse_payload_as_json is False.
        """
        # TODO: history to trajectory?
        # TODO: suppress the payload column entirely if the parse_payload_as_json is False,
        # instead of leaving the column with empty dictionaries, which has some cost.
        my_params = {"instance": self.dfi_conn.qualified_instance_name}
        if start_time is not None:
            my_params["startTime"] = start_time.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        if end_time is not None:
            my_params["endTime"] = end_time.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        my_url = f"{self.dfi_conn.base_url}/entities/{uid}/history"
        my_headers = self.dfi_conn.streaming_headers

        with requests.get(
            my_url,
            headers=my_headers,
            params=my_params,
            timeout=self.dfi_conn.query_timeout,
            stream=True,
        ) as response:
            self._check_response(response, my_url, my_headers, my_params)
            data = stream.receive_history(response, self.dfi_conn.progress_bar)

        logger.debug("Uid: %s \nHistory length: %i", uid, len(data))
        data_formatted = []
        for item in data:
            if parse_payload_as_json:
                try:
                    payload = json.loads(item["payload"])
                except Exception as err:
                    payload = {}
                    logger.debug("Failed to parse payload to JSON: %s for item %s", err, str(item))
            else:
                payload = item["payload"]
            data_formatted.append(
                [
                    item["id"],
                    datetime.strptime(item["time"], "%Y-%m-%dT%H:%M:%S.%fZ"),
                    item["coordinate"][0],
                    item["coordinate"][1],
                    payload,
                ]
            )
        return pd.DataFrame(data_formatted, columns=["entity_id", "timestamp", "longitude", "latitude", "payload"])

    def histories(
        self,
        uids: List[str],
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
        parse_payload_as_json: bool = False,
    ) -> pd.DataFrame:
        """
        Get the trajectories of a list of entities by their device_ids, with optional time interval.

        Parameters
        ----------
        uids: List[str]
            List of entities unique ids.

        start_time: Optional[datetime] = None
            Lower bound for the time constraint.

        end_time: Optional[datetime] = None
            Upper bound for the time constraint.

        parse_payload_as_json: bool = False
            If True it parses the payload as a JSON string into the column payload.

        Return
        -------
            Dataframe with columns "entity_id", "timestamp", "longitude", "latitude", "payload"
            The last column is empty if parse_payload_as_json is False.
        """
        # TODO uids to list_device_ids?
        # TODO: histories or trajectories?
        # TODO: suppress the payload column entirely if the parse_payload_as_json is False,
        # instead of leaving the column with empty dictionaries, which has some cost.
        df_records = pd.DataFrame(columns=["entity_id", "timestamp", "longitude", "latitude", "payload"])
        progress_bar_status = self.dfi_conn.progress_bar
        # TODO: bypass the hack of progress bar status with a decorator embedding the progress bar in
        # every method consideered?
        self.dfi_conn.progress_bar = False
        for uid in tqdm(uids, total=len(uids)):
            df_history = self.history(uid, start_time, end_time, parse_payload_as_json)
            df_records = pd.concat([df_records, df_history], ignore_index=True, axis=0)
        self.dfi_conn.progress_bar = progress_bar_status
        return df_records

    def neighbours(
        self,
        hex_id: str,
        polygon_vertices: List[List[float]],
        min_time: Optional[datetime] = None,
        max_time: Optional[datetime] = None,
    ) -> List[any]:
        """
        Method under development.
        """
        # TODO: min_time and max_time to start_time and end_time for coherence with the rest of the other methods?
        # TODO: "polygon_vertices" to "vertices" for coherence with the other methods?
        # TODO: BUG here as the `hex_id` is not passed to the query, so it has no effect.
        # This method, as it is, is identical topolygon_history, with less value input.
        # TODO: docstring to address after the hex_id is passed to the API if needed.
        # TODO: specify if the polygon_vertices as they are are (lat, lon) or (lon, lat)
        # TODO: better naming needed?

        my_url = f"{self.dfi_conn.base_url}/polygon/history"
        my_payload = {
            "vertices": polygon_vertices,
            "startTime": min_time.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
            "endTime": max_time.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
        }
        my_headers = self.dfi_conn.streaming_headers
        my_params = {"instance": f"{self.dfi_conn.namespace}.{self.dfi_conn.instance_name}"}

        with requests.post(
            my_url,
            json=my_payload,
            headers=my_headers,
            params=my_params,
            timeout=self.dfi_conn.query_timeout,
            stream=True,
        ) as response:
            self._check_response(response, my_url, my_headers, my_params, my_payload)
            data = stream.receive_history(response, self.dfi_conn.progress_bar)

        if data is None:
            logger.warning("Query Error. Vertices: %s", str(polygon_vertices))
            data = []
        data = [
            {
                "hex_id": hex_id,
                "entity_id": x["id"],
                "timestamp": datetime.strptime(x["time"], "%Y-%m-%dT%H:%M:%S.%fZ"),
                "longitude": x["coordinate"][0],
                "latitude": x["coordinate"][1],
            }
            for x in data
        ]
        return data

    def retrieve_saved_polygon(self, polygon_name: str) -> List[List[float]]:
        """
        Get the list of a polygon saved in the polygon database from its name.

        Parameters
        ----------
        polygon_name: str
            Name of the polygon the user wants to retrieve from database.

        Return
        -------
            List of the polygon coordinates.
        """
        # TODO: check if it is (lat, lon) or (lon, lat) and add to the docstring.
        # It should be lon, lat. Make sure this is the convention we want the user to be
        # exposed to.
        url = self.dfi_conn.base_url + "/polygons/" + polygon_name
        headers = self.dfi_conn.synchronous_headers

        response = requests.get(
            url,
            headers=headers,
            timeout=self.dfi_conn.query_timeout,
        )
        self._check_response(response, url, headers, params={})
        vertices = response.json().get("vertices")

        if vertices is not None:
            return vertices

        msg = f"Polygon vertices can not be retrieved from the json response: {response.json()}"
        logger.error(msg)
        raise IOError(msg)
