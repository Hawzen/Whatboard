import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input

from app import app
from dashboard import report
from scripts import whatPlot

modes = ["days", "weeks", "years", "all"]


def getLayout():
    layout = \
        dbc.Container([
            html.H3("Distribution of messages over time", className="mb-2 p-2"),
            dbc.Row([
                dbc.ButtonGroup([
                    dbc.Col([
                        dbc.DropdownMenu([
                            dbc.DropdownMenuItem("Days", id="report-dropdownlist-days"),
                            dbc.DropdownMenuItem("Weeks", id="report-dropdownlist-weeks"),
                            dbc.DropdownMenuItem("Years", id="report-dropdownlist-years"),
                            dbc.DropdownMenuItem("All-time", id="report-dropdownlist-all"),
                        ],
                            id="report-dropdownlist'",
                            label="Graphing Mode",
                            color="primary",
                            bs_size="lg",
                            direction="right",
                            className="mr-3 pr-2 mb-1"),
                        html.Div(
                            dbc.Button(
                                "Generate Plot",
                                size="lg",
                                color="primary",

                                id="report-msgsOverTimeGraph-generate",
                            ),
                            hidden=True,
                        )
                    ], width=3, className="mr-0 mt-1"),
                ], size="lg", vertical=True),
            ], justify="between", no_gutters=True, className="mb-3"),
            dbc.Row(
                dbc.Col([
                    dcc.Graph(
                        id="report-msgsOverTimeGraph-plot",
                        config={"displaylogo": False,
                                'modeBarButtonsToRemove': ['pan2d', 'lasso2d'],
                                "editable": True},
                        className="mt-1"
                    ),
                ]), no_gutters=True
            )
        ], className="mt-3 pt-3"
        )

    return layout


def getMode(timestamps):
    maxMode = (0, "no mode")
    for clicks, mode in zip(timestamps, modes):
        if clicks is not None:
            maxMode = maxMode if maxMode[0] > clicks else (clicks, mode)
    return maxMode[1]


@app.callback(
    Output("report-msgsOverTimeGraph-plot", "figure"),
    Input("report-msgsOverTimeGraph-generate", "n_clicks"),
    *[Input(f"report-dropdownlist-{mode}", "n_clicks_timestamp") for mode in modes],
    report.getConstraints(w_refresh=False),
    report.getDataStateFunctions(),
)
def generatePlot(n, days, weeks, years, alltime, user_row_ids, word_row_ids, start, end, reportDivType, content,
                 filename, ukformat):
    if not any([days, weeks, years, alltime]):
        df, *_ = report.sampleOrUploaded(content, filename, reportDivType, ukformat)
        return whatPlot.plotMessagesOverTime(df, "days")

    mode = getMode([days, weeks, years, alltime])
    if mode == "no mode":
        return dash.no_update

    df, *_ = report.sampleOrUploaded(content, filename, reportDivType, ukformat)
    df = report.applyConstraints(df, user_row_ids, word_row_ids, start, end)

    return whatPlot.plotMessagesOverTime(df, mode)


# doesnt work?
# @app.callback(
#     Output("report-dropdownlist", "children"),
#     Input("report-msgsOverTimeGraph-generate", "n_clicks"),
#     *[State(f"report-dropdownlist-{mode}", "n_clicks_timestamp") for mode in modes],
# )
# def updateLabel(n, days, weeks, years, alltime):
#     if n:
#         return getMode([days, weeks, years, alltime])


# Optimize at globe and animation
