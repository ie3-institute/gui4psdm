import json
import os
import zipfile

import folium
import pandas as pd

from definitions import ROOT_DIR

input_path = os.path.join(ROOT_DIR, "input", "simbench_example.zip")
with zipfile.ZipFile(input_path) as z:
    with z.open("node_input.csv") as f:
        node_input_data = pd.read_csv(
            f, usecols=["geo_position", "id", "uuid", "slack"]
        )

geodata_dict = {}
rows = len(node_input_data)
for i in range(rows):
    geodata_dict[
        node_input_data.loc[i]["id"] + "#" + node_input_data.loc[i]["uuid"]
    ] = node_input_data.iloc[i]["geo_position"]

for key in geodata_dict:
    geodata_dict[key] = json.loads(geodata_dict[key])
    geodata_dict[key] = {
        "lat": geodata_dict[key]["coordinates"][1],
        "lon": geodata_dict[key]["coordinates"][0],
    }

fig = folium.Map(location=[51.499428, 7.446744], zoom_start=12)

circles = [
    folium.Circle(
        location=[geodata_dict[p]["lat"], geodata_dict[p]["lon"]],
        radius=8,
        color="#FF0000",
        fill=True,
        fill_color="#FF0000",
        fill_opacity=1,
        tooltip=p.split("#")[0],
    ).add_to(fig)
    for p in geodata_dict
]

uuid_to_latlon = {
    p.split("#")[1]: [geodata_dict[p]["lat"], geodata_dict[p]["lon"]]
    for p in geodata_dict
}

with zipfile.ZipFile(input_path) as z:
    with z.open("line_input.csv") as f:
        line_input_data = pd.read_csv(f, usecols=["node_a", "node_b", "id", "uuid"])

geodata_dict_lines = {}
rows = len(line_input_data)
for i in range(rows):
    geodata_dict_lines[
        line_input_data.loc[i]["id"] + "#" + line_input_data.loc[i]["uuid"]
    ] = {
        "node_a": line_input_data.iloc[i]["node_a"],
        "node_b": line_input_data.iloc[i]["node_b"],
    }

lines = [
    folium.PolyLine(
        locations=[
            uuid_to_latlon[geodata_dict_lines[p]["node_a"]],
            uuid_to_latlon[geodata_dict_lines[p]["node_b"]],
        ],
        color="#FF0000",
    ).add_to(fig)
    for p in geodata_dict_lines
]

# save Map
fig.save("map.html")
