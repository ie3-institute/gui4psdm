import dash_leaflet as dl
import pandas as pd
from dash import dash_table, html


def datatable_from_csv(data, title):
    return html.Div(
        [
            html.P(title + ":", style={"margin-top": "30px", "fontWeight": "bold"}),
            dash_table.DataTable(
                id={"type": "csv-table", "key": title},
                columns=[{"name": col, "id": col} for col in data.columns],
                data=data.to_dict("records"),
                page_size=10,  # Anzahl der Zeilen pro Seite
                filter_action="native",
                sort_action="native",
                filter_options={"placeholder_text": "Tabelle filtern..."},
                export_format="csv",
                editable=True,
                export_headers="display",
                style_table={
                    "border": "2px solid #f9f9f9",
                    "border-radius": "1px",
                    "overflowX": "auto",
                },
                style_header={
                    "backgroundColor": "#252725",
                    "color": "white",
                    "fontWeight": "bold",
                    "textAlign": "center",
                },
                style_cell={
                    "padding": "10px",
                    "textAlign": "left",
                    "backgroundColor": "#909193C7",
                },
                style_data_conditional=[
                    {
                        "if": {"state": "selected"},  # Zustand: ausgewählt
                        "backgroundColor": "#00FB3F",  # rote Hintergrundfarbe
                        "color": "black",
                    }
                ],
            ),
        ]
    )


def datatable_for_popup(data):
    return html.Div(
        [
            dash_table.DataTable(
                columns=[{"name": col, "id": col} for col in data.columns],
                data=data.to_dict("records"),
                page_size=10,  # Anzahl der Zeilen pro Seite
                style_table={
                    "border": "2px solid #f9f9f9",
                    "border-radius": "1px",
                    "overflowX": "auto",
                },
                style_header={
                    "backgroundColor": "#252725",
                    "color": "white",
                    "fontWeight": "bold",
                    "textAlign": "center",
                },
                style_cell={
                    "padding": "10px",
                    "textAlign": "left",
                    "backgroundColor": "#909193C7",
                },
                style_data_conditional=[
                    {"if": {"row_index": "odd"}, "backgroundColor": "#A19C9CF6"}
                ],
            )
        ]
    )


def baue_map(
    geodaten_dict,
    uuid_to_latlon,
    slack_dict,
    geodaten_dict_lines,
    geodaten_dict_transformers,
    geodaten_dict_3_w_transformers,
    geodaten_dict_switches,
):
    marker = [
        dl.Circle(
            center=[geodaten_dict[p]["lat"], geodaten_dict[p]["lon"]],
            id={"type": "geo-marker", "id": p.split("#")[1]},
            radius=5,
            color="#FF0000",
            fill=True,
            fillColor="#FF0000",
            fillOpacity=1,
            children=[
                dl.Tooltip(p.split("#")[0], permanent=False, className="my-tooltip")
            ],
        )
        for p in geodaten_dict
    ]

    slack_marker = []

    for i in slack_dict:
        if slack_dict[i] is True:
            slack_marker = [
                dl.Circle(
                    center=[geodaten_dict[i]["lat"], geodaten_dict[i]["lon"]],
                    id=i.split("#")[1],
                    radius=10,
                    color="#ffff00",
                    fill=True,
                    fillColor="#ffff00",
                    fillOpacity=1,
                    children=[
                        dl.Tooltip(
                            i.split("#")[0], permanent=False, className="my-tooltip"
                        )
                    ],
                )
            ]

    leitungen = [
        dl.Polyline(
            positions=[
                uuid_to_latlon[geodaten_dict_lines[p]["node_a"]],
                uuid_to_latlon[geodaten_dict_lines[p]["node_b"]],
            ],
            color="#FF0000",
        )
        for p in geodaten_dict_lines
    ]

    transformatoren_marker = [
        dl.Circle(
            center=uuid_to_latlon[geodaten_dict_transformers[p]["node_a"]],
            id=p.split("#")[1],
            radius=5,
            color="#0000FF",
            fill=True,
            fillColor="#0000FF",
            fillOpacity=1,
            children=[
                dl.Tooltip(p.split("#")[0], permanent=False, className="my-tooltip2")
            ],
        )
        for p in geodaten_dict_transformers
    ]

    drei_w_transformatoren_marker = [
        dl.Circle(
            center=uuid_to_latlon[geodaten_dict_3_w_transformers[p]["node_a"]],
            id=p.split("#")[1],
            radius=5,
            color="#0000FF",
            fill=True,
            fillColor="#0000FF",
            fillOpacity=1,
            children=[
                dl.Tooltip(p.split("#")[0], permanent=False, className="my-tooltip2")
            ],
        )
        for p in geodaten_dict_3_w_transformers
    ]

    schalter_closed = [
        dl.Circle(
            center=uuid_to_latlon[geodaten_dict_switches[p]["node_a"]],
            id=p.split("#")[1],
            radius=5,
            color="#00FF00",
            fill=True,
            fillColor="#00FF00",
            fillOpacity=1,
            children=[
                dl.Tooltip(p.split("#")[0], permanent=False, className="my-tooltip3")
            ],
        )
        for p in geodaten_dict_switches
        if geodaten_dict_switches[p]["closed"] is False
    ]

    schalter_opened = [
        dl.Circle(
            center=uuid_to_latlon[geodaten_dict_switches[p]["node_a"]],
            id=p.split("#")[1],
            radius=5,
            color="#00FF00",
            fill=True,
            fillColor="#FFFFFF",
            fillOpacity=1,
            children=[
                dl.Tooltip(p.split("#")[0], permanent=False, className="my-tooltip3")
            ],
        )
        for p in geodaten_dict_switches
        if geodaten_dict_switches[p]["closed"] is True
    ]

    first_key = next(iter(geodaten_dict))
    latInitial = geodaten_dict[first_key]["lat"]
    lonInitial = geodaten_dict[first_key]["lon"]
    zoom = 12

    fig_map = dl.Map(
        center=[latInitial, lonInitial],
        zoom=zoom,
        style={"height": "100vh"},
        children=[
            dl.TileLayer(
                url="https://tiles.stadiamaps.com/tiles/alidade_smooth_dark/{z}/{x}/{y}{r}.png",
                attribution='&copy; <a href="https://stadiamaps.com/">Stadia Maps</a> &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>',
                maxZoom=20,
            ),
            dl.LayerGroup(leitungen),
            dl.LayerGroup(marker),
            dl.LayerGroup(slack_marker),
            dl.LayerGroup(transformatoren_marker),
            dl.LayerGroup(drei_w_transformatoren_marker),
            dl.LayerGroup(schalter_opened),
            dl.LayerGroup(schalter_closed),
        ],
    )

    return fig_map


def has_real_values(lst):
    """
    True  → Liste enthält mindestens einen echten Wert
    False → Liste ist None, leer oder besteht nur aus None/NaN
    """
    if lst is None:
        return False

    for x in lst:
        if x is not None and not (isinstance(x, float) and pd.isna(x)):
            return True

    return False
