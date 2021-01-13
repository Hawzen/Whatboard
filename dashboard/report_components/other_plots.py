import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
from dash.dependencies import Output, Input

from app import app
from dashboard import report
from scripts import whatPlot


def getLayout(usersDf):

    layout = dbc.Container([
        html.H3("Globe", className="mb-5 mt-5 pt-4 pb-1"),
        dbc.Row([
            dbc.Col([
                dcc.Graph(
                    id="report-globe-plot",
                    config={"displaylogo": False,
                            'modeBarButtonsToRemove': ['pan2d', 'lasso2d'],
                            "editable": True},
                    figure=whatPlot.plotGlobe(usersDf)
                )
            ])
        ]),
        html.H3("Animation plot", className="mb-3 mt-5 pt-4 pb-1"),
        dbc.Button(
            "Generate Animation",
            size="lg",
            color="primary",
            className="mb-5",
            id="report-animation-generate",
        ),
        dbc.Row([
            dbc.Col([
                dcc.Graph(
                    id="report-animation-plot",
                    config={"displaylogo": False,
                            'modeBarButtonsToRemove': ['pan2d', 'lasso2d'],
                            "editable": True},
                ),
                dbc.FormText("The order of months may not be correct", className="ml-3 mt-2 d-inline"),
            ])
        ])
    ])

    return layout


@app.callback(Output("report-animation-plot", "figure"),
              Input("report-animation-generate", "n_clicks"),
              report.getDataStateFunctions(),
              report.getConstraints(w_refresh=False),
              )
def generateAnimation(n, reportDivType, content, filename, ukformat, user_row_ids, word_row_ids, start, end):
    if not n or not user_row_ids:
        return empty_plot("Choose up to 10 people from the table above then hit Generate Animation")

    df, *_ = report.sampleOrUploaded(content, filename, reportDivType, ukformat)
    df = report.applyConstraints(df, user_row_ids, word_row_ids, start, end)
    if len(user_row_ids) <= 10:
        return whatPlot.plotUsersAnimation(df, user_row_ids)


def empty_plot(label_annotation):
    trace1 = go.Scatter(
        x=[],
        y=[]
    )

    data = [trace1]

    layout = go.Layout(
        showlegend=False,
        xaxis=dict(
            autorange=True,
            showgrid=False,
            zeroline=False,
            showline=False,
            ticks='',
            showticklabels=False
        ),
        yaxis=dict(
            autorange=True,
            showgrid=False,
            zeroline=False,
            showline=False,
            ticks='',
            showticklabels=False
        ),
        annotations=[
            dict(
                x=0,
                y=0,
                xref='x',
                yref='y',
                text=label_annotation,
                showarrow=True,
                arrowhead=7,
                ax=0,
                ay=0
            )
        ]
    )

    fig = go.Figure(data=data, layout=layout)
    return fig
