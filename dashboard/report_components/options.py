import base64
import io

import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input, State

from app import app, cache
from dashboard import report
from dashboard.report import getAllDf, samplePath

options = dbc.Container([
    dbc.Card([
        dbc.Row([
            dbc.Col(
                dbc.FormGroup([
                    html.P(
                        dbc.Label("View Demo", className="h4 ml-4"),
                        className="mt-2"
                    ),
                    dbc.Col(
                        dbc.Button(
                            "Load Sample",
                            size="lg",
                            color="primary",
                            id="load-sample",
                        ), className="py-0 my-0"
                    ),
                    dbc.FormText("Load a pre-set sample and see the app's capabilities",
                                 className="ml-3 mt-2")
                ]), lg=6, md=12
            ),
            dbc.Col(
                dbc.FormGroup([
                    html.P(
                        dbc.Label("Upload File", className="h4 ml-4 mb-1 mt-2"),
                    ),
                    dcc.Upload(
                        id='upload-data',
                        children=html.Div([
                            html.A('Select File', style={"overflow": "hidden"})
                        ]),
                        style={
                            'width': '100%',
                            'height': '50px',
                            'lineHeight': '50px',
                            'borderWidth': '1px',
                            'borderStyle': 'dashed',
                            'borderRadius': '5px',
                            'textAlign': 'center',
                            'margin': '10px'
                        },
                        className="mt-0 pt-0"
                    ),
                    dbc.Checkbox(id="month-formatting", className="mb-3 ml-3 d-inline"),
                    dbc.FormText("Format is MM/DD/YYYY", className="ml-3 mt-2 d-inline"),
                ], className="mr-5"), lg=6, md=12
            )
        ]),
    ], className="shadow-sm jumbo-light p-3 mb-0 pb-0"),
    html.Div(id="garbage", hidden=True)
], className="mb-5 mt-5 pt-2")


def getLayout():
    return options


@cache.memoize(30 * 60)
def parse_contents(contents, filename, returnDataframe=False, ukformat=False):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
        if 'txt' in filename:
            if returnDataframe:
                return getAllDf(io.StringIO(decoded.decode('utf-8')), ukformat=ukformat)
            else:
                return io.StringIO(decoded.decode('utf-8'))
    except Exception as e:
        print(e)
        return dash.no_update


@app.callback(
    Output("report_div", "children"),
    Input("load-sample", "n_clicks"),
    Input('upload-data', 'contents'),
    State('upload-data', 'filename'),
    State("report_div", "children"),
    State("month-formatting", "checked"),
    prevent_initial_call=True
)
def loadFiles(n, contents, filename, children, ukformat):
    ctx = dash.callback_context

    if not ctx.triggered:
        return []
    elif ctx.triggered[0]["prop_id"] == "load-sample.n_clicks":
        if n:
            if children and children[1]["props"]["children"] == "sample": # Prevents mashing the button
                return dash.no_update
            # The sample name here is just for show, it isnt the path
            return [report.getLayout(samplePath, isSample=True, name="Sample.txt"), html.Div("sample", id="report-div-type", hidden=True)]

    elif ctx.triggered[0]["prop_id"] == "upload-data.contents":
        dataframes = parse_contents(contents, filename, returnDataframe=True, ukformat=ukformat)
        return [report.getLayout(dataframes, name=filename, isDataframes=True), html.Div("uploaded", id="report-div-type", hidden=True)]

    else:
        print("Error reached end of load sample")


app.clientside_callback(
    """
    function(clicks, click2, elemid) {
        document.getElementById(elemid).scrollIntoView({
          behavior: 'smooth'
        });
    }
    """,
    Output('garbage', 'children'),
    Input('upload-data', 'contents'),
    Input("load-sample", "n_clicks"),
    State('report_div', 'id'),
    prevent_initial_call=True
)
