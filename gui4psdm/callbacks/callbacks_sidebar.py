import base64
import os
import uuid
import zipfile
from datetime import datetime

import pandas as pd
from dash import ALL, ctx, dcc
from dash.dependencies import Input, Output, State

from gui4psdm.app import app


def save_uploaded_file(data, filename, upload_folder="uploads"):
    """
    Speichert eine Datei, die über dcc.Upload hochgeladen wurde, im angegebenen Ordner.
    data: Hochgeladene Datei
    filename Name der Datei
    upload_folder: Ordner, in dem die Datei gespeichert wird
    """
    # Upload Ordner erstellen, falls er nicht existiert
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)

    # Datei speichern
    file_path = os.path.join(upload_folder, filename)
    with open(file_path, "wb") as f:
        f.write(data)


# Upload Reaktion (Überprüfe auf .zip Datei)
@app.callback(
    Output("upload-dateien-dropdown", "options"),
    Output("zip-output", "children"),
    Input("upload-data", "contents"),
    State("upload-data", "filename"),
)
def handle_zip_upload(contents, filename):
    workspace = os.getcwd()
    upload_folder = "uploads"
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)

    ordner = workspace + r"\uploads"

    # Alle Dateien und Ordner auflisten
    alle_dateien_und_ordner = os.listdir(ordner)

    options = {}

    if contents is None:
        if len(alle_dateien_und_ordner) == 0:
            options["Noch keine Datei hochgeladen."] = "Noch keine Datei hochgeladen."
            return options, "Noch keine Datei hochgeladen."
        else:
            for i in alle_dateien_und_ordner:
                options[i] = i
            return options, "Es gab schon mindestens einen Dateiupload"
    a = ""
    for i in range(len(contents)):
        # Base64 dekodieren
        content_type, content_string = contents[i].split(",")
        decoded = base64.b64decode(content_string)
        # decoded liegt jetzt als byte datei vor
        if not filename[i].lower().endswith(".zip"):
            a = a + f"'{filename[i]}' ist keine ZIP-Datei."
        else:
            save_uploaded_file(decoded, filename[i])
            options[filename[i]] = filename[i]  # Dropdown anpassen
            a = a + f"{filename[i]} erfolgreich hochgeladen"

    if len(options) == 0:
        options["Noch keine Datei hochgeladen."] = "Noch keine Datei hochgeladen."
        return options, a
    else:
        return options, a


@app.callback(
    Output("download-HTML", "data"),
    Input("download-button", "n_clicks"),
    State({"type": "csv-table", "key": ALL}, "data"),
    prevent_initial_call=True,
)
def func(value, all_tables):

    ids = [x["id"] for x in ctx.states_list[0]]

    neue_daten = {
        table_id["key"]: pd.DataFrame(table_data)
        for table_id, table_data in zip(ids, all_tables)
    }

    path = os.path.abspath("modified_networkmodels_folder") + "/"
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")  # keine : und Punkte
    zip_title = f"Version_{timestamp}.zip"
    zip_path = os.path.join(path, zip_title)

    with zipfile.ZipFile(zip_path, mode="w", compression=zipfile.ZIP_DEFLATED) as zf:
        for title, df in neue_daten.items():
            csv_name = f"{title}.csv"
            csv_bytes = df.to_csv(index=False).encode("utf-8")
            zf.writestr(csv_name, csv_bytes)
    path_2 = os.path.abspath("modified_networkmodels_folder") + "/" + zip_title
    return dcc.send_file(path_2)


# Knopf um UUID zu generieren


@app.callback(
    Output({"type": "meinInput", "index": "uuid"}, "value"),
    Input("generate-uuid", "n_clicks"),
    prevent_initial_call=True,
)
def generate_uuid(n_submit):
    u = uuid.uuid4()
    return u
