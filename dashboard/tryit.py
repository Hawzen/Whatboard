import dash
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Output, Input, State

from app import app

# os.path.join(crntPath, "..", "data2/sample2.txt")
collapse_groups = ["Download WhatsApp data", "Run the analysis online", "Or run the analysis locally"]
collapse_content = [
    html.Div(
        html.H6([
            "You can follow ",
            html.A("this", href="https://faq.whatsapp.com/android/chats/how-to-save-your-chat-history/?lang=en" , target='_blank'),
            " for a guide to download your WhatsApp data",
            html.Br(),
            html.Br(),
            "After exporting the data, place it in an accessible storage where you can upload it unto the website"
        ])
    ),
    html.Div(
        html.H6([
            "Click ",
            html.Code("Load Sample"),
            " to see what the analysis looks like",
            html.Br(),
            html.Br(),
            "When you're ready to upload your own data, press (or drag and drop) the dotted box ",
            html.Code("Select Files"),
            html.Br(),
            html.Br(),
            "Note: It may take a while the first few refreshes, after that the website should be faster, since we're caching your data",
            html.Br(),
            "If your phone's system language is English (UK) or the data is formatted MM/DD/YYYY then click the checkbox beside the upload box"
        ])
    ),
    html.Div(
        html.H6([
            "1- Download python (version 3.6 and above should suffice) from ",
            html.A("here", href="https://www.python.org/" , target='_blank'),
            html.Br(),
            html.Br(),
            "2- Download the packages listed in requirements.txt in the source code. Follow ",
            html.A("this", href="https://stackoverflow.com/questions/7225900/how-to-install-packages-using-pip-according-to-the-requirements-txt-file-from-a#answer-15593865:~:text=I've%20read%20the%20above%2C%20realize%20this,pip%20install%20%2Dr%20%2Fpath%2Fto%2Frequirements.txt" , target="_blank"),
            html.Br(),
            " if you don't know how to install the packages, (or simply type ",
            html.Code("pip install"),
            " commands line by line)",
            html.Br(),
            html.Br(),
            "3- Download the source code linked in the bottom of the page.",
            html.Br(),
            "Then run app.py\index.py and go to the link it directs you to"
        ])
    ),
]


def make_item(i):
    return dbc.Card(
        [
            dbc.CardHeader(
                html.H2(
                    dbc.Button(
                        collapse_groups[i],
                        color="link",
                        outline=True,
                        id=f"group-{i}-toggle",
                        style={"color": "#243328"}
                    )
                )
            ),
            dbc.Collapse(
                dbc.CardBody(collapse_content[i]),
                id=f"collapse-{i}",
            ),
        ], className="jumbo-light"
    )


accordion = html.Div(
    [make_item(0), make_item(1), make_item(2)], className="accordion"
)

layout = html.Div([
    dbc.Row(
        dbc.Col(
            html.H2("Try it", className="display-5 mb-4 pt-3"),
        )
    ),
    accordion
], className="mt-3 mb-5")


@app.callback(
    [Output(f"collapse-{i}", "is_open") for i in range(3)],
    [Input(f"group-{i}-toggle", "n_clicks") for i in range(3)],
    [State(f"collapse-{i}", "is_open") for i in range(3)],
)
def toggle_accordion(n1, n2, n3, is_open1, is_open2, is_open3):
    ctx = dash.callback_context

    if not ctx.triggered:
        return False, False, False
    else:
        button_id = ctx.triggered[0]["prop_id"].split(".")[0]

    if button_id == "group-0-toggle" and n1:
        return not is_open1, False, False
    elif button_id == "group-1-toggle" and n2:
        return False, not is_open2, False
    elif button_id == "group-2-toggle" and n3:
        return False, False, not is_open3
    return False, False, False
