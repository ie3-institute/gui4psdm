import dash_leaflet as dl
from dash import dcc, html

from gui4psdm.app import app

# Tab-Design
tabs_styles = {"height": "44px"}
tab_style = {
    "borderBottom": "1px solid #d6d6d6",
    "padding": "6px",
    "fontWeight": "bold",
    "backgroundColor": "#31302F",
}

tab_selected_style = {
    "borderTop": "1px solid #d6d6d6",
    "borderBottom": "1px solid #d6d6d6",
    "backgroundColor": "#1E1E1E",
    "color": "white",
    "padding": "6px",
}

app.title = "gui4psdm"
server = app.server


# Layout of Dash App
app.layout = html.Div(
    children=[
        html.Div(
            className="row",
            children=[
                # Column for user controls
                html.Div(
                    className="four columns div-user-controls",
                    children=[
                        html.A(
                            html.Img(
                                className="logo",
                                src=app.get_asset_url("dash-logo-new.png"),
                            ),
                        ),
                        html.H2("gui4psdm"),
                        html.P(
                            """Mit diesem Tool lassen sich Netzdaten hochladen, darstellen und verändern.""",
                            style={"margin-bottom": "30px"},  # Abstand nach unten
                        ),
                        dcc.Upload(
                            id="upload-data",
                            children=html.Div(
                                ["Drag and Drop or ", html.A("Select "), "Zip Files"]
                            ),
                            style={
                                "width": "100%",
                                "height": "60px",
                                "lineHeight": "60px",
                                "borderWidth": "1px",
                                "borderStyle": "dashed",
                                "borderRadius": "5px",
                                "textAlign": "center",
                                "margin": "10px",
                            },
                            # Allow multiple files to be uploaded
                            multiple=True,
                        ),
                        html.Div(id="zip-output", style={"marginLeft": "20px"}),
                        html.Div(
                            className="row",
                            children=[
                                html.Div(
                                    className="div-for-dropdown",
                                    children=[
                                        # Dropdown for locations on map
                                        dcc.Dropdown(
                                            id="upload-dateien-dropdown",
                                            options=[
                                                {
                                                    "label": "Noch keine Datei hochgeladen",
                                                    "value": "a",
                                                }
                                            ],
                                            placeholder="Wähle eine Datei aus zur Visualisierung aus...",
                                            className="spezifisches-dropdown",
                                        )
                                    ],
                                ),
                            ],
                        ),
                        # Hier wird angezeigt ob die Zip-Datei alle benötigten Elmenete besitzt
                        html.Div(id="zip_vollstaendig", style={"marginLeft": "20px"}),
                        dcc.Store(id="init", data=False),
                        html.Div(id="dropdown-output", style={"marginLeft": "20px"}),
                        html.Div(id="test-output", style={"marginLeft": "20px"}),
                        html.H2(id="dummy-output"),
                        dcc.Dropdown(
                            id="auswahl_zeile_hinzufuegen",
                            options=[{"label": "Zeile hinzufügen", "value": "a"}],
                            placeholder="Wähle eine Tabelle zum hinzufügen einer Zeile aus...",
                            style={"margin-top": "30px", "margin-bottom": "5px"},
                            className="spezifisches-dropdown",
                        ),
                        html.Div(
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
                        ),
                        html.Div(id="kurzmalwarten", style={"marginLeft": "20px"}),
                        html.Div(id="platzhalter", style={"height": "5vh"}),
                        html.Button(
                            "Download des aktualisierten Netzmodells",
                            id="download-button",
                            style={"width": "100%"},
                        ),
                        # dcc.Dropdown(
                        #     id="download-dateien-dropdown",
                        #     options=[{"label": "Noch keine Datei zum Download verfügbar", "value": "a"}],
                        #     placeholder="Wähle eine Datei zum Downloas aus..."
                        # ),
                        dcc.Download(id="download-HTML"),
                        dcc.Store(id="store-a"),
                        dcc.Store(id="store-b"),
                        dcc.Store(id="store-c"),
                        dcc.Store(id="store-d"),
                        dcc.Store(id="store-e"),
                        dcc.Store(id="store-f"),
                        dcc.Store(id="store-g"),
                        dcc.Store(id="store-h"),
                        dcc.Store(id="store-i"),
                        dcc.Store(id="store-k"),
                        # dcc.Store(id="store-l"),
                        html.A(
                            html.Img(
                                className="logo2",
                                src=app.get_asset_url("abb312.svg"),
                            ),
                        ),
                    ],
                ),
                html.Div(
                    className="eight columns div-for-charts bg-grey",
                    children=[
                        dcc.Tabs(
                            id="tabs-example-1",
                            value="tab1",
                            children=[
                                dcc.Tab(
                                    label="Karte",
                                    value="tab1",
                                    style=tab_style,
                                    selected_style=tab_selected_style,
                                    children=[
                                        html.Div(
                                            id="pop-up-data-table",
                                            style={"margin-top": "0px"},
                                        ),
                                        dl.Map(
                                            id="map-graph",
                                            scrollWheelZoom=True,
                                            style={"height": "100vh"},
                                        ),
                                    ],
                                ),
                                dcc.Tab(
                                    label="Netzwerkdaten Tabelle",
                                    value="tab2",
                                    style=tab_style,
                                    selected_style=tab_selected_style,
                                    children=[
                                        html.Div(
                                            id="table-container",
                                            style={"height": "100vh"},
                                        )
                                    ],
                                ),
                            ],
                            style=tabs_styles,
                        ),
                    ],
                ),
            ],
        )
    ]
)
