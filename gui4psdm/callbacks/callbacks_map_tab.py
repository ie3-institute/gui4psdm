import json
import os
import zipfile

import dash_leaflet as dl
import pandas as pd
from dash import ctx, html
from dash.dependencies import ALL, Input, Output

from gui4psdm.app import app
from gui4psdm.more_functions import baue_map, datatable_for_popup


@app.callback(
    Output("store-h", "data", allow_duplicate=True),
    Input("store-i", "data"),
    prevent_initial_call=True,
)
def weiter_weiter(data):
    return data


@app.callback(
    Output("store-a", "data"),
    Output("store-i", "data"),
    Input("upload-dateien-dropdown", "value"),
)
def initialisiere_map(value_dropdown):

    # Download-Karte Ordner erstellen, falls er nicht existiert
    if not os.path.exists("modified_networkmodels_folder"):
        os.makedirs("modified_networkmodels_folder")
    path = os.path.abspath("modified_networkmodels_folder")

    if value_dropdown == None:
        list_of_locations = {
            "ie3": {"lat": 51.490912, "lon": 7.403925},
        }

        fig = dl.Map(
            center=[51.499428, 7.446744],
            zoom=12,
            style={"height": "100vh"},
            children=[
                dl.TileLayer(
                    url="https://tiles.stadiamaps.com/tiles/alidade_smooth_dark/{z}/{x}/{y}{r}.png",
                    attribution='&copy; <a href="https://stadiamaps.com/">Stadia Maps</a> &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>',
                    maxZoom=20,
                ),
                dl.Circle(
                    center=[51.490912, 7.403925],  # Position des Punktes
                    radius=5,  # Größe des Punktes
                    color="red",  # Randfarbe
                    fill=True,
                    fillColor="red",  # Füllfarbe
                    fillOpacity=1,
                    children=[
                        dl.Tooltip("ie3", permanent=True, className="my-tooltip")
                    ],
                ),
            ],
        )

        return "letsgoooo", fig

    # Ab hier beginnt die Datentransformation, das map-objekt wird mit baue_map erzeugt

    upload_pfad = os.path.abspath("uploads") + "/" + value_dropdown
    with zipfile.ZipFile(upload_pfad) as z:
        with z.open("node_input.csv") as f:
            node_input_data = pd.read_csv(
                f, usecols=["geo_position", "id", "uuid", "slack"]
            )  # Funktioniert nur wenn die Spalten immer gleich benannt sind!!!

    geodaten_dict = {}
    zeilen = len(node_input_data)
    for i in range(zeilen):
        geodaten_dict[
            node_input_data.loc[i]["id"] + "#" + node_input_data.loc[i]["uuid"]
        ] = node_input_data.iloc[i]["geo_position"]

    for key in geodaten_dict:
        geodaten_dict[key] = json.loads(geodaten_dict[key])
        geodaten_dict[key] = {
            "lat": geodaten_dict[key]["coordinates"][1],
            "lon": geodaten_dict[key]["coordinates"][0],
        }  # Funktioniert nur wenn Lat und Lon immer die gleiche Reihenfolge haben

    uuid_to_latlon = {
        p.split("#")[1]: [geodaten_dict[p]["lat"], geodaten_dict[p]["lon"]]
        for p in geodaten_dict
    }

    slack_dict = {}
    zeilen = len(node_input_data)
    for i in range(zeilen):
        slack_dict[
            node_input_data.loc[i]["id"] + "#" + node_input_data.loc[i]["uuid"]
        ] = node_input_data.iloc[i]["slack"]

    with zipfile.ZipFile(upload_pfad) as z:
        with z.open("line_input.csv") as f:
            line_input_data = pd.read_csv(f, usecols=["node_a", "node_b", "id", "uuid"])

    geodaten_dict_lines = {}
    zeilen = len(line_input_data)
    for i in range(zeilen):
        geodaten_dict_lines[
            line_input_data.loc[i]["id"] + "#" + line_input_data.loc[i]["uuid"]
        ] = {
            "node_a": line_input_data.iloc[i]["node_a"],
            "node_b": line_input_data.iloc[i]["node_b"],
        }

    geodaten_dict_transformers = {}
    try:
        with zipfile.ZipFile(upload_pfad) as z:
            with z.open("transformer_2_w_input.csv") as f:
                transformer_2_w_input_data = pd.read_csv(
                    f, usecols=["node_a", "node_b", "id", "uuid"]
                )

        zeilen = len(transformer_2_w_input_data)
        for i in range(zeilen):
            geodaten_dict_transformers[
                transformer_2_w_input_data.loc[i]["id"]
                + "#"
                + transformer_2_w_input_data.loc[i]["uuid"]
            ] = {
                "node_a": transformer_2_w_input_data.iloc[i]["node_a"],
                "node_b": transformer_2_w_input_data.iloc[i]["node_b"],
            }
    except KeyError:
        pass

    geodaten_dict_3_w_transformers = {}
    try:
        with zipfile.ZipFile(upload_pfad) as z:
            with z.open("transformer_3_w_input.csv") as f:
                transformer_3_w_input_data = pd.read_csv(
                    f, usecols=["node_a", "node_b", "id", "uuid"]
                )

        zeilen = len(transformer_3_w_input_data)
        for i in range(zeilen):
            geodaten_dict_3_w_transformers[
                transformer_3_w_input_data.loc[i]["id"]
                + "#"
                + transformer_3_w_input_data.loc[i]["uuid"]
            ] = {
                "node_a": transformer_3_w_input_data.iloc[i]["node_a"],
                "node_b": transformer_3_w_input_data.iloc[i]["node_b"],
                "node_c": transformer_3_w_input_data.iloc[i]["node_c"],
            }
    except KeyError:
        pass

    geodaten_dict_switches = {}
    try:
        with zipfile.ZipFile(upload_pfad) as z:
            with z.open("switch_input.csv") as f:
                switch_input_data = pd.read_csv(
                    f, usecols=["node_a", "node_b", "id", "uuid", "closed"]
                )

        zeilen = len(switch_input_data)
        for i in range(zeilen):
            geodaten_dict_switches[
                switch_input_data.loc[i]["id"] + "#" + switch_input_data.loc[i]["uuid"]
            ] = {
                "node_a": switch_input_data.iloc[i]["node_a"],
                "node_b": switch_input_data.iloc[i]["node_b"],
                "closed": switch_input_data.iloc[i]["closed"],
            }
    except KeyError:
        pass

    fig_map = baue_map(
        geodaten_dict,
        uuid_to_latlon,
        slack_dict,
        geodaten_dict_lines,
        geodaten_dict_transformers,
        geodaten_dict_3_w_transformers,
        geodaten_dict_switches,
    )

    return "letsgo", fig_map


@app.callback(
    Output("dummy-output", "children"), Input("upload-dateien-dropdown", "value")
)
def daten_bereitstellen(value_dd):

    if value_dd == None:
        return " "
    pfad = os.path.abspath("uploads") + "/" + value_dd

    global daten
    daten = {}

    with zipfile.ZipFile(pfad) as z:
        a = z.namelist()
        for dateiname in z.namelist():
            with z.open(dateiname) as f:
                tabellenname = dateiname.split(".")[0]
                daten[tabellenname] = pd.read_csv(f)


@app.callback(
    Output("pop-up-data-table", "children"),
    Output("test-output", "children"),
    Input({"type": "geo-marker", "id": ALL}, "n_clicks"),
    prevent_initial_call=True,
)
def marker_clicked(n_clicks_list):

    if not n_clicks_list or not any(n_clicks_list):
        return None, ""

    uuid_clicked_node = ctx.triggered_id["id"]

    tabelle_feed = daten["fixed_feed_in_input"][
        daten["fixed_feed_in_input"]["node"] == uuid_clicked_node
    ]  # Funktioniert nur wenn die gegebenen Dateien aus dem PSDM immer die gleichen Namen haben!!!
    tabelle_feed.insert(0, "Anschlussart", "Einspeisung")
    tabelle_feed.pop("node")

    tabelle_load = daten["load_input"][
        daten["load_input"]["node"] == uuid_clicked_node
    ]  # Funktioniert nur wenn die gegebenen Dateien aus dem PSDM immer die gleichen Namen haben!!!
    tabelle_load.insert(0, "Anschlussart", "Last")
    tabelle_load.pop("node")

    fertige_tabelle = html.Div(
        [datatable_for_popup(tabelle_feed), datatable_for_popup(tabelle_load)]
    )
    return fertige_tabelle, "Top"
