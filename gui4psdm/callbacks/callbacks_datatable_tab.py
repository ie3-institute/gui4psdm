import json
import os
import zipfile

import pandas as pd
from dash import ALL, dcc, html, no_update
from dash.dependencies import Input, Output, State

from gui4psdm.app import app
from gui4psdm.more_functions import baue_map, datatable_from_csv, has_real_values


@app.callback(
    Output("store-f", "data", allow_duplicate=True),
    Output("zip_vollstaendig", "children"),
    Output("store-b", "data"),
    Input("upload-dateien-dropdown", "value"),
    prevent_initial_call=True,
)
def build_data_table(value_dd):

    if value_dd == None:
        return html.Div(), html.Div(), "irgendwas"
    path = os.path.abspath("uploads") + "/" + value_dd
    with zipfile.ZipFile(path) as z:
        dateinnamen_liste = z.namelist()
        if not all(i.lower().endswith(".csv") for i in dateinnamen_liste):
            return [], "ZIP enthält Dateien, die keine CSV sind", "irgendwas"

    global data
    data = {}

    with zipfile.ZipFile(path) as z:
        a = z.namelist()
        for file_name in z.namelist():
            with z.open(file_name) as f:
                table_name = file_name.split(".")[0]
                data[table_name] = pd.read_csv(f)

    divs = [datatable_from_csv(data[key], key) for key in data]
    divs.append(html.Div(style={"height": "200px"}))

    return html.Div(divs), "Alles hat funktioniert", "irgendwas"


@app.callback(
    Output("auswahl_zeile_hinzufuegen", "options"),
    Input("store-b", "data"),
)
def set_zeile_hinzufuegen_uptions(data):
    options = {}
    if not "daten" in globals():
        options["Lade erst eine Datei hoch"] = "Lade erst eine Datei hoch"
        return options

    optionen = [
        "fixed_feed_in_input",
        "line_input",
        "line_type_input",
        "load_input",
        "node_input",
        "switch_input",
        "transformer_2_w_input",
        "transformer_2_w_type_input",
    ]
    for i in optionen:
        options[i] = i
    return options


@app.callback(
    Output("store-c", "data"),
    Output("store-e", "data"),
    Input("submit-val", "n_clicks"),
    State({"type": "meinInput", "index": ALL}, "value"),
    prevent_initial_call=True,
)
def update_output(n_submit, value):
    if has_real_values(value) == False:
        return no_update, no_update
    return "fertig", value


@app.callback(
    Output("store-f", "data", allow_duplicate=True),
    Output("store-g", "data", allow_duplicate=True),
    Output("kurzmalwarten", "children"),
    Input("store-e", "data"),
    State("store-k", "data"),
    prevent_initial_call=True,
)
def build_tabelle_new(
    data, value
):  # Mit store-g wird die funktion zur überarbeitung der map aufgerufen.

    pruefe_auf_vollstaendigkeit = (
        {  # wenn ein wert nötig ist dann ist er true, wenn nicht ist er false
            "fixed_feed_in_input": [
                True,
                True,
                True,
                True,
                False,
                False,
                False,
                True,
                True,
            ],
            "line_input": [
                True,
                True,
                False,
                False,
                False,
                True,
                True,
                True,
                True,
                True,
                True,
                True,
            ],
            "line_type_input": [True, True, True, True, True, True, True, True],
            "load_input": [
                True,
                True,
                True,
                True,
                True,
                True,
                False,
                False,
                False,
                True,
                True,
            ],
            "node_input": [
                True,
                True,
                True,
                True,
                False,
                False,
                False,
                True,
                True,
                True,
                True,
                True,
            ],
            "switch_input": [True, True, True, True, True, False, False, False],
            "transformer_2_w_input": [
                True,
                True,
                False,
                False,
                False,
                True,
                True,
                True,
                True,
                True,
                True,
            ],
            "transformer_2_w_type_input": [
                True,
                True,
                True,
                True,
                True,
                True,
                True,
                True,
                True,
                True,
                True,
                True,
                True,
                True,
                True,
            ],
        }
    )

    for i in range(len(pruefe_auf_vollstaendigkeit[value])):
        if pruefe_auf_vollstaendigkeit[value][i] == True and data[i] == None:
            return (
                no_update,
                no_update,
                "Es wurden nicht alle notwendigen Attribute ausgefüllt.",
            )

    if not all(
        x is None or (isinstance(x, float) and pd.isna(x)) for x in data
    ):  # Daten werden intern aktualisiert
        if data[6] == "True" or "False":
            geojson = '{{"type":"Point","coordinates":[{0},{1}],"crs":{{"type":"name","properties":{{"name":"EPSG:4326"}}}}}}'.format(
                data[2], data[1]
            )
            data.pop(2)
            data[1] = geojson
        data[value].loc[len(data[value])] = data
    divs = [
        datatable_from_csv(data[key], key) for key in data
    ]  # Neue tabelle wird gebaut
    divs.append(html.Div(style={"height": "200px"}))
    return divs, "letsgo", "Das Objekt wurde erfolgreich hinzugefügt!"


@app.callback(
    Output("table-container", "children"),
    Input("store-f", "data"),
    prevent_initial_call=True,
)
def weitergeben(data):
    return data


@app.callback(
    Output("store-d", "data", allow_duplicate=True),
    Output("store-k", "data"),
    Input("auswahl_zeile_hinzufuegen", "value"),
    prevent_initial_call=True,
)
def daten_hinzufuegen(value):
    attribute_aller_tabellen_standard = {
        "fixed_feed_in_input": [
            "uuid",
            "cos_phi_rated",
            "id",
            "node",
            "operates_from",
            "operates_until",
            "operator",
            "q_characteristics",
            "s_rated",
        ],
        "line_input": [
            "uuid",
            "id",
            "operates_from",
            "operates_until",
            "operator",
            "node_a",
            "node_b",
            "parallel_devices",
            "length",
            "geo_position",
            "olm_characteristic",
            "type",
        ],
        "line_type_input": ["uuid", "id", "r", "x", "b", "g", "i_max", "v_rated"],
        "load_input": [
            "uuid",
            "cos_phi_rated",
            "e_cons_annual",
            "id",
            "load_profile",
            "node",
            "operates_from",
            "operates_until",
            "operator",
            "q_characteristics",
            "s_rated",
        ],
        "node_input": [
            "uuid",
            "Lat",
            "Lon",
            "id",
            "operates_from",
            "operates_until",
            "operator",
            "slack",
            "subnet",
            "v_rated",
            "v_target",
            "volt_lvl",
        ],
        "switch_input": [
            "uuid",
            "closed",
            "id",
            "node_a",
            "node_b",
            "operates_from",
            "operates_until",
            "operator",
        ],
        "transformer_2_w_input": [
            "uuid",
            "id",
            "operates_from",
            "operates_until",
            "operator",
            "node_a",
            "node_b",
            "parallel_devices",
            "tap_pos",
            "auto_tap",
            "type",
        ],
        "transformer_2_w_type_input": [
            "uuid",
            "id",
            "r_sc",
            "x_sc",
            "g_m",
            "b_m",
            "s_rated",
            "v_rated_a",
            "v_rated_b",
            "d_v",
            "d_phi",
            "tap_side",
            "tap_neutr",
            "tap_min",
            "tap_max",
        ],
    }
    p = data[value].columns
    liste_zum_iterieren = attribute_aller_tabellen_standard[value]
    input_div = html.Div(
        [
            html.Div(
                [
                    dcc.Input(
                        id={"type": "meinInput", "index": i},
                        placeholder="Gebe " + i + " ein...",
                        style={"width": "50vh", "margin-top": "5px"},
                    )
                ]
                + (
                    [
                        html.Button(
                            "generate_uuid",
                            id="generate-uuid",
                            n_clicks=0,
                            style={"margin-left": "10px", "margin-top": "5px"},
                        )
                    ]
                    if i == "uuid"
                    else []
                ),
                style={"display": "flex", "alignItems": "center"},
            )
            for i in liste_zum_iterieren
        ]
        + [
            html.Div(style={"height": "10px"}),
            html.Button("Submit", id="submit-val", n_clicks=0, style={"width": "20vh"}),
        ]
    )
    return input_div, value


@app.callback(
    Output("store-d", "data", allow_duplicate=True),
    Input("store-c", "data"),
    prevent_initial_call=True,
)
def output(
    value,
):  # Mit dieser Funktion werden der Button und die Input-Felder ausgeblendet
    if all(x is not None for x in value):
        return html.Div(
            id="dateneingabe",
            children=[
                dcc.Input(
                    id={"type": "meinInput", "index": "abc"},
                    placeholder="Enter a value...",
                    type="text",
                    value="",
                    style={"display": "none"},
                ),
                html.Button(
                    "Submit",
                    id="submit-val",
                    n_clicks=0,
                    style={"display": "none"},
                ),
            ],
        )


@app.callback(
    Output("dateneingabe", "children"),
    Input("store-d", "data"),
    prevent_initial_call=True,
)
def gebe_daten_weiter(data):
    return data


@app.callback(
    Output("store-h", "data", allow_duplicate=True),
    Input("store-g", "data"),
    prevent_initial_call=True,
)
def aktualisiere_map(data):

    geodaten_dict = {}
    zeilen = len(data["node_input"])
    for i in range(zeilen):
        geodaten_dict[
            data["node_input"].loc[i]["id"] + "#" + data["node_input"].loc[i]["uuid"]
        ] = data["node_input"].iloc[i]["geo_position"]

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
    zeilen = len(data["node_input"])
    for i in range(zeilen):
        slack_dict[
            data["node_input"].loc[i]["id"] + "#" + data["node_input"].loc[i]["uuid"]
        ] = data["node_input"].iloc[i]["slack"]

    geodaten_dict_lines = {}
    zeilen = len(data["line_input"])
    for i in range(zeilen):
        geodaten_dict_lines[
            data["line_input"].loc[i]["id"] + "#" + data["line_input"].loc[i]["uuid"]
        ] = {
            "node_a": data["line_input"].iloc[i]["node_a"],
            "node_b": data["line_input"].iloc[i]["node_b"],
        }

    geodaten_dict_transformers = {}
    try:
        zeilen = len(data["transformer_2_w_input"])
        for i in range(zeilen):
            geodaten_dict_transformers[
                data["transformer_2_w_input"].loc[i]["id"]
                + "#"
                + data["transformer_2_w_input"].loc[i]["uuid"]
            ] = {
                "node_a": data["transformer_2_w_input"].iloc[i]["node_a"],
                "node_b": data["transformer_2_w_input"].iloc[i]["node_b"],
            }
    except KeyError:
        pass

    geodaten_dict_3_w_transformers = {}
    try:
        zeilen = len(data["transformer_3_w_input"])
        for i in range(zeilen):
            geodaten_dict_3_w_transformers[
                data["transformer_3_w_input"].loc[i]["id"]
                + "#"
                + data["transformer_3_w_input"].loc[i]["uuid"]
            ] = {
                "node_a": data["transformer_3_w_input"].iloc[i]["node_a"],
                "node_b": data["transformer_3_w_input"].iloc[i]["node_b"],
                "node_c": data["transformer_3_w_input"].iloc[i]["node_c"],
            }
    except KeyError:
        pass

    geodaten_dict_switches = {}
    try:
        zeilen = len(data["switch_input"])
        for i in range(zeilen):
            geodaten_dict_switches[
                data["switch_input"].loc[i]["id"]
                + "#"
                + data["switch_input"].loc[i]["uuid"]
            ] = {
                "node_a": data["switch_input"].iloc[i]["node_a"],
                "node_b": data["switch_input"].iloc[i]["node_b"],
                "closed": data["switch_input"].iloc[i]["closed"],
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

    return "map wird aktualisiert", fig_map


@app.callback(
    Output("map-graph", "children"), Input("store-h", "data"), prevent_initial_call=True
)
def gebe_map_daten_weiter(data):
    return data
