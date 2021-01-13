import dash_bootstrap_components as dbc
import dash_html_components as html
from dashboard import header, report, tryit, faq
import options


def createSpinner(children):
    return dbc.Spinner(children,
                       type='None',
                       fullscreen=False,
                       spinnerClassName="loader"
                       ),


layout = dbc.Container([
    header.layout,
    tryit.layout,
    *[
        options.getLayout(),
        *createSpinner(html.Div(children=[], id="report_div"))
    ],
    html.Hr(className=""),
    faq.layout,
    dbc.Row(
        dbc.Col(

        )
    ),
    dbc.Row(
        dbc.Col(
            html.H4("Source code", className="display-5"),
        )
    ),
    dbc.Row([
        dbc.Col([
            html.P([
                "The source code can be found ",
                html.A("here", href="https://github.com/Hawzen/Whatboard", target="_blank")
            ])
        ])
    ])
], className="text-monospace")
