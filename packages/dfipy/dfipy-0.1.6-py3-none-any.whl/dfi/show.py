"""
Class with methods to show DFI results.
Composition of the class DFIConnection.
"""

import json
import logging
from typing import List, Optional

import pandas as pd
import pydeck as pdk
import pyperclip
from IPython.display import IFrame  # pylint: disable=import-error

from dfi.connection import DFIConnect
from dfi.getters import DFIGet

logger = logging.getLogger(__name__)


# TODO: find a way to avoid importing IPython and removing
# ipython from requirements.
# TODO: why not using KeplerGl as industry standard? Passing polygons via copy paste
# is not ideal, or via passing html code is not ideal. Kepler has the methods to draw
# map out of the box. A lightweigth alternative to kepler is https://leafmap.org/
# also having the draw polygon option out of the box.


VIEW_STATE_LONDON = pdk.ViewState(
    longitude=-0.1,
    latitude=51.5,
    zoom=10,
    min_zoom=5,
    max_zoom=15,
    pitch=0,
    bearing=0,
)


class DFIShow:
    """
    Visualisation methods to build use case on top of the queries from DFI.
    Not part of the DFI API wrapper, but handy to have it embedded there for demo and functionalities.
    """

    def __init__(self, dfi_conn: DFIConnect) -> None:
        self.dfi_conn: DFIConnect = dfi_conn
        self.dfi_get: DFIGet = DFIGet(self.dfi_conn)

    def __repr__(self):
        return f"{self.__class__.__name__}({self.dfi_conn!r}){self.__dict__}"

    def __str__(self):
        return f"""DFI Python API: instance of {self.__class__.__name__} composed with {self.dfi_conn!r}"""

    def heatmap(
        self,
        query_polygons: List[str] = None,  # TODO: maybe calling this polygon_names could help.
        vertices: List[List[float]] = None,
        df_history: pd.DataFrame = None,
        df_hexagons: pd.DataFrame = None,
        df_colocs: pd.DataFrame = None,
        view_state=None,
        color_gradient: bool = True,
    ) -> pdk.Deck:
        """
        Helper method to create a heatmap from the components of a range of queries.
        """
        layers = []

        if query_polygons is not None:
            for query_polygon in query_polygons:
                list_vertices = self.dfi_get.retrieve_saved_polygon(query_polygon)
                geojson_poly = _create_geojson_from_coordinates(list_vertices)

                # return geoJSON
                geojson_pdk = pdk.Layer(
                    "GeoJsonLayer",
                    geojson_poly,
                    opacity=0.2,
                    stroked=True,
                    filled=True,
                    extruded=False,
                    wireframe=True,
                    get_elevation="0",
                    get_fill_color="[255, 255, 0]",
                    get_line_color="[191, 64, 192]",
                    line_width_min_pixels=3,
                    pickable=True,
                )
                layers.append(geojson_pdk)

        if vertices is not None:
            geo_json_poly = _create_geojson_from_coordinates(vertices)
            geo_json_poly_pdk = pdk.Layer(
                "GeoJsonLayer",
                geo_json_poly,
                opacity=0.5,
                stroked=False,
                filled=True,
                extruded=False,
                wireframe=True,
                get_elevation="0",
                get_fill_color="[255, 255, 0]",
                get_line_color="[255, 255, 0]",
                pickable=True,
            )
            layers.append(geo_json_poly_pdk)

        if df_hexagons is not None:
            pdk_hexagons = pdk.Layer(
                "H3HexagonLayer",
                df_hexagons,
                pickable=True,
                stroked=True,
                filled=True,
                extruded=False,
                get_hexagon="hex_id",
                get_fill_color="color" if color_gradient else "[255, 255, 0, 50]",
                get_line_color="color" if color_gradient else "[255, 255, 0, 50]",
                line_width_min_pixels=3,
            )
            layers.append(pdk_hexagons)

        if df_history is not None:
            history_pdk = pdk.Layer(
                "ScatterplotLayer",  # ScatterplotLayer HexagonLayer
                df_history,
                get_position=["longitude", "latitude"],
                auto_highlight=True,
                elevation_scale=500,
                pickable=True,
                elevation_range=[0, 300],
                extruded=True,
                filled=True,
                opacity=0.8,
                radius_scale=6,
                radius_min_pixels=1,
                radius_max_pixels=100,
                line_width_min_pixels=1,
                get_fill_color=[255, 0, 0],
                get_line_color=[255, 0, 0],
                coverage=1,
            )
            layers.append(history_pdk)

        if df_hexagons is not None:
            pdk_hexagons = pdk.Layer(
                "H3HexagonLayer",
                df_hexagons,
                pickable=True,
                stroked=True,
                filled=True,
                extruded=False,
                get_hexagon="hex_id",
                get_fill_color="color" if color_gradient else "[255, 255, 0, 50]",
                get_line_color="color" if color_gradient else "[255, 255, 0, 50]",
                line_width_min_pixels=3,
            )
            layers.append(pdk_hexagons)

        if df_colocs is not None:
            if len(df_colocs) > 0:
                colocs_pdk = pdk.Layer(
                    "ScatterplotLayer",  # ScatterplotLayer HexagonLayer
                    df_colocs,
                    get_position=["longitude", "latitude"],
                    auto_highlight=True,
                    elevation_scale=500,
                    pickable=True,
                    elevation_range=[0, 300],
                    extruded=True,
                    filled=True,
                    opacity=0.8,
                    radius_scale=6,
                    radius_min_pixels=1,
                    radius_max_pixels=100,
                    line_width_min_pixels=1,
                    get_fill_color=[0, 0, 255],
                    get_line_color=[0, 0, 255],
                    coverage=1,
                )
                layers.append(colocs_pdk)
        # Set the viewport location if not given
        if view_state is None:
            view_state = VIEW_STATE_LONDON

        return pdk.Deck(layers=layers, initial_view_state=view_state)

    def map(
        self,
        query_polygons: List[str] = None,
        vertices: List[List[float]] = None,
        history: List[List[float]] = None,
        df_history: pd.DataFrame = None,
        view_state=None,
        tooltip: Optional[dict] = None,
    ) -> pdk.Deck:
        """
        Helper method to create a map from the components obtained from a range of queries.
        """
        # TODO (Robert):
        # has both history and df_history.  This is confusing as it’s the same data but different forms.
        # I believe all the function calls return histories into a dataframe,
        # why is the history argument needed here?
        # should plot the polygon first then the pings on top
        layers = []

        if history is not None:
            pdk_history = pdk.Layer(
                "ScatterplotLayer",
                pd.DataFrame(history, columns=["longitude", "latitude"]),
                get_position=["longitude", "latitude"],
                auto_highlight=True,
                elevation_scale=500,
                pickable=True,
                elevation_range=[0, 300],
                extruded=True,
                filled=True,
                opacity=0.8,
                radius_scale=6,
                radius_min_pixels=1,
                radius_max_pixels=100,
                line_width_min_pixels=1,
                get_fill_color=[255, 0, 0],
                get_line_color=[255, 0, 0],
                coverage=1,
            )
            layers.append(pdk_history)

        if df_history is not None:
            pdk_df_history = pdk.Layer(
                "ScatterplotLayer",
                df_history,
                get_position=["longitude", "latitude"],
                auto_highlight=True,
                elevation_scale=500,
                pickable=True,
                elevation_range=[0, 300],
                extruded=True,
                filled=True,
                opacity=0.8,
                radius_scale=6,
                radius_min_pixels=1,
                radius_max_pixels=100,
                line_width_min_pixels=1,
                get_fill_color=[255, 0, 0],
                get_line_color=[255, 0, 0],
                coverage=1,
            )
            layers.append(pdk_df_history)

        if query_polygons is not None:
            for query_polygon in query_polygons:
                list_vertices = self.dfi_get.retrieve_saved_polygon(query_polygon)
                geojson_poly = _create_geojson_from_coordinates(list_vertices)

                # return geoJSON
                geojson_pdk = pdk.Layer(
                    "GeoJsonLayer",
                    geojson_poly,
                    opacity=0.2,
                    stroked=True,
                    filled=True,
                    extruded=False,
                    wireframe=True,
                    get_elevation="0",
                    get_fill_color="[255, 255, 0]",
                    get_line_color="[191, 64, 192]",
                    line_width_min_pixels=3,
                    pickable=True,
                )
                layers.append(geojson_pdk)

        if vertices is not None:
            geo_json_poly = _create_geojson_from_coordinates(vertices)
            geo_json_poly_pdk = pdk.Layer(
                "GeoJsonLayer",
                geo_json_poly,
                opacity=0.5,
                stroked=False,
                filled=True,
                extruded=False,
                wireframe=True,
                get_elevation="0",
                get_fill_color="[255, 255, 0]",
                get_line_color="[255, 255, 0]",
                pickable=True,
            )
            layers.append(geo_json_poly_pdk)

        # Set the viewport location
        if view_state is None:
            view_state = VIEW_STATE_LONDON

        # Combined all of it and render a viewport
        if tooltip is not None:
            return pdk.Deck(layers=layers, initial_view_state=view_state, tooltip=tooltip)
        else:
            return pdk.Deck(layers=layers, initial_view_state=view_state)

    @staticmethod
    def ask_user_polygon(
        mapbox_api_token: str, width_pc: int = 100, height_px: int = 400, zoom: int = 8, long: float = 0, lat: float = 0
    ) -> IFrame:
        """
        Helper to input a polygon.
        """
        srcdoc = """
<!DOCTYPE html>
<html>
<head>
<title>mapboxgl-jupyter viz</title>
<meta charset='UTF-8' />
<meta name='viewport' content='initial-scale=1,maximum-scale=1,user-scalable=no' />
<script src='https://api.mapbox.com/mapbox-gl-js/v2.14.1/mapbox-gl.js'></script>
<link href='https://api.mapbox.com/mapbox-gl-js/v2.14.1/mapbox-gl.css' rel='stylesheet' />

<script src='https://api.mapbox.com/mapbox-gl-js/plugins/mapbox-gl-draw/v1.4.1/mapbox-gl-draw.js'></script>
<link rel='stylesheet'
      href='https://api.mapbox.com/mapbox-gl-js/plugins/mapbox-gl-draw/v1.4.1/mapbox-gl-draw.css' type='text/css' />


<style type='text/css'>
    body { margin:0; padding:0; }
    #map { position: absolute; top:0; bottom:0; width:100%; }
</style>
</head>


<body>


<div id='map' class='map'></div>

<script type='text/javascript'>

    mapboxgl.accessToken = '<<MAPBOX_KEY>>';
    var map = new mapboxgl.Map({
        container: 'map',
        style: 'mapbox://styles/mapbox/dark-v11?optimize=true',
        center: [<<LONGITUDE>>, <<LATITUDE>>],
        zoom: <<ZOOM>>,
        pitch: 0,
        bearing: 0,
    });

    const draw_nav_ctrl = new mapboxgl.NavigationControl();
    map.addControl(draw_nav_ctrl, 'top-right');

    const draw_poly_ctrl = new MapboxDraw({
        displayControlsDefault: false,
        defaultMode: 'draw_polygon',
        controls: {
            polygon: true,
            trash: true
        }
    });
    map.addControl(draw_poly_ctrl, 'top-right');

    map.on('draw.create', GetPolygonVertices);
    map.on('draw.delete', GetPolygonVertices);
    map.on('draw.update', GetPolygonVertices);


    function GetPolygonVertices(e) {
        const data = draw_poly_ctrl.getAll();

        if (data.features.length > 0) {
            // Get the coordinates of the polygon
            var polygon = e.features[0];
            var coordinates = polygon.geometry.coordinates;
            var jsonString = JSON.stringify(coordinates[0]);
            const input = document.createElement('textarea');
            input.value = jsonString;
            document.body.appendChild(input);
            input.select();
            document.execCommand('copy'); // copy to clipboard
            document.body.removeChild(input); // Remove the input field from the document
        }
    }



</script>
</body>
</html>
"""

        frame_id = "map"
        srcdoc = srcdoc.replace("<<MAPBOX_KEY>>", mapbox_api_token)
        srcdoc = srcdoc.replace("<<ZOOM>>", str(zoom))
        srcdoc = srcdoc.replace("<<LONGITUDE>>", str(long))
        srcdoc = srcdoc.replace("<<LATITUDE>>", str(lat))
        iframe_template = (
            f'<iframe id="{frame_id}", srcdoc="{srcdoc}" style="width: {width_pc}%; height: {height_px}px;"></iframe>'
        )
        return IFrame(iframe_template, height_px, height_px)

    @staticmethod
    def get_user_polygon() -> List[List[float]]:
        """Helper to create a polygon via copy paste"""
        polygon_text = pyperclip.paste()
        try:
            polygon_coordinates = json.loads(polygon_text)
        except Exception as err:
            logger.error("Could not parse content of clipboard: '%s', Error %s", polygon_text, err)
            return
        return polygon_coordinates


def _create_geojson_from_coordinates(coordinates: List[List[float]]) -> dict:
    """
    Helper function to display a polygon on a map.
    """
    return {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "properties": {},
                "geometry": {"coordinates": [coordinates], "type": "Polygon"},
            }
        ],
    }
