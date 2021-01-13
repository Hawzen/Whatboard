import dash_bootstrap_components as dbc
import dash_html_components as html

layout = html.Div([
    dbc.Row(
        dbc.Col(
            html.H2("FAQ", className="display-5 mb-4 pt-3"),
        )
    ),
    dbc.Row([
        dbc.Col([
            dbc.Jumbotron([
                html.H4("There's a bug in the code"),
                html.H6([
                    "If you spot bugs you can open an issue in ",
                    html.A("this", href="https://github.com/Hawzen/Whatboard/issues", target='_blank'),
                    " github repository listed below."
                ]),
                html.H6("Or you can fix it and do a pull request and we'll handle it")
            ], className="shadow-sm jumbo-light mx-auto")
        ], xl=4, lg=12, md=12, sm=12, xs=12),
        dbc.Col([
            dbc.Jumbotron([
                html.H4("How is my data processed?"),
                html.H6("Since we're using a python backend your data will have to be sent to our server when you upload a file"),
                html.H6('We recommend running the application locally (see "Run the analysis locally"), '
                        'that way all processing never leave your computer')
            ], className="shadow-sm jumbo-light mx-auto")
        ], xl=4, lg=12, md=12, sm=12, xs=12),
        dbc.Col([
            dbc.Jumbotron([
                html.H4("Is my data saved?"),
                html.H6("Your data will be temporarily cached (and deleted automatically later)."),
                html.H6("This allows the website to function much faster than if we were to process the file in every request"),
            ], className="shadow-sm jumbo-light mx-auto")
        ], xl=4, lg=12, md=12, sm=12, xs=12),
    ])
])