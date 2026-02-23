from dash import dash

external_stylesheets = [
    "https://codepen.io/chriddyp/pen/bWLwgP.css",
    "https://stackpath.bootstrapcdn.com/bootswatch/4.5.2/darkly/bootstrap.min.css",
]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


app = dash.Dash(
    __name__,
    meta_tags=[{"name": "viewport", "content": "width=device-width"}],
)

app.config.suppress_callback_exceptions = True
