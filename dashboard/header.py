from random import random

import dash_bootstrap_components as dbc
import dash_html_components as html

credit1, credit2 = ["Hawzen", "D7miiz"] if random() > 0.5 else ["D7miiz", "Hawzen"]
name = "Whatboard"

layout = html.Div([
    dbc.Row(
        dbc.Col(
            html.H1(name, className="display-4 mb-5 pt-5"),
        )
    ),
    dbc.Row(
        dbc.Col([
            dbc.Jumbotron([
                html.P([
                    html.I("Whatboard"),
                    " is a tool to analyze your WhatsApp chats",
                    html.Br(),
                    "You can use it to find out statistics about your conversations, activity plots and much more",
                    html.Br(),
                    "See the sample included below",
                    html.Br(),
                    html.Br(),
                    html.P([
                        "Done by: ",
                        html.A(credit1, className="list-inline-item", href=f"https://github.com/{credit1}", target='_blank'),
                        html.A(credit2, className="list-inline-item", href=f"https://github.com/{credit2}", target='_blank'),
                    ],
                        className="list-inline text-black-50 font-italic", id="credits")
                ], className="text-justify h5 lead")
            ], id="jumboIntro", className="mx-auto shadow jumbo"),
        ],
            width=12
        )
    ),
])