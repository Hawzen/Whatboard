import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output

from app import app
from dashboard import report, dashboard
from scripts import analysis

general_statistics = [
    ("Count", "count"),
    ("Users In Group", "usrsIn"),
    ("No. Of Deleted Messages", "noDeleted"),
    ("No. Of Media Sent", "mediaSent"),
    ("No. Of Days", "noDays"),
    ("Messages Per Day", "msgsPerDay"),  # count / number of days
    ("Maximum Messages In One Day", "maxMsg"),
    ("Minimum Messages In One Day", "minMsg"),
]


def getLayout(df):

    def gen_card(stat, statid):
        return html.Div(
            dbc.Card(
                dbc.CardBody(
                    [
                        html.H5(f"{stat}:  ", className="card-title font-weight-lighter", id=f"stat-text-{statid}",
                                style={"display": "inline-block", "white-space": "pre"}),
                        html.H5("0", id=f"stat-num-{statid}", style={"display": "inline-block"})
                    ]
                ), className="mr-0 ml-1 mb-2 jumbo-light"
            ),
        )

    general_statistics_comp = dbc.CardDeck(
        [
            gen_card(stat, statid) for stat, statid in general_statistics
        ], className="mb-3"
    )

    toolTips = html.Div([
        dbc.Tooltip("Media includes: Images, Videos, Stickers or Voice Messages", target="stat-text-mediaSent"),
        dbc.Tooltip("This number can exceeds WhatsApp's limit since users join and leave."
                    " It is also limited by the users you select in the users table", target="stat-text-usrsIn"),
    ])

    layout = html.Div([
        *dashboard.createSpinner([
            dbc.Row([
                dbc.FormGroup([
                        html.P(
                            dbc.Label("Time Period", className="h4 ml-4"),
                            className="mb-0 mt-2"
                        ),
                    dbc.Col(
                        dcc.DatePickerRange(
                            id='df-datepicker',
                            persistence=True,
                            clearable=True,
                            day_size=30,
                        ), className="py-0 my-0"
                    ),
                    dbc.FormText("Filter the messages depending on a given period of time",
                                 className="ml-0")
                ], className="pb-0"),
                dbc.FormGroup([
                    html.P(
                        dbc.Label("Apply filters", className="h4 ml-3"),
                        className="mb-0 mt-2"
                    ),
                    dbc.Col(
                        dbc.Button("Refresh", id="report-refresh", color="primary", size="lg"), className="py-0 my-0"
                    ),
                    dbc.FormText("Filter the messages depending on a given period of time",
                                 className="ml-0")
                ], "mr-5 mb-4 pb-5"),
            ], justify="between"),
        ]),
        *dashboard.createSpinner([
            general_statistics_comp,
            toolTips
        ]),
    ])

    return layout


@app.callback(
    *[Output(f"stat-num-{statid}", "children") for stat, statid in general_statistics],
    report.getConstraints(),
    report.getDataStateFunctions(),
)
def update_general_statistics(n, user_row_ids, word_row_ids, start, end, reportDivType, content, filename, ukformat):
    df, *_ = report.sampleOrUploaded(content, filename, reportDivType, ukformat)

    dff = report.applyConstraints(df, user_row_ids, word_row_ids, start, end)

    if len(dff) == 0:
        return 0, 0, 0, 0, 0, 0, 0, 0

    usersDff = analysis.getUsers(dff)

    cnt, dlt, med = usersDff[["Count", "Deleted_Message", "Media_Sent"]].sum()
    usrsIn = len(usersDff)
    days = (dff.index[-1] - dff.index[0]).days
    msgsPerDay = round(cnt / max(days, 1))

    mx, mn = dff.groupby(dff.index.floor("d")).size().agg(["max", "min"])
    return cnt, usrsIn, dlt, med, days, msgsPerDay, mx, mn



