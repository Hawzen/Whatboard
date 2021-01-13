import dash_bootstrap_components as dbc
import dash_table


def getLayout(df, commands, usersDf, wordsDf, linksDf):
    layout = dbc.Container([
        dbc.Row([
            dbc.Col([
                dash_table.DataTable(
                    id='users-Datatable',
                    columns=[{"name": col, "id": col} for col in usersDf.columns if col != "id"],
                    data=usersDf.to_dict('records'),
                    page_size=300,
                    row_selectable='multi',
                    filter_action='native',
                    sort_action='native',
                    fixed_rows={'headers': True},
                    style_table={'overflowY': 'auto', 'overflowX': 'scroll'},
                    export_format="csv",

                    tooltip_header={
                        "Sender": "Name of sender",
                        "Count": "Number of recorded messages (excludes commands)",
                        'AvgPerDay': 'Only considers days where they sent a message',
                        "MaxADay": "Maximum number of messages in any given day where sender sent a message",
                        "MinADay": "Minimum number of messages in any given day where sender sent a message",
                        "Media_Sent": "Media Sent, includes Photos, Videos, Voice Messages and stickers",
                        "Delete_Messages": "Number of deleted messages",
                        'Country': "Users with no country code in their number (such contacts) have None values",
                    },

                    style_header_conditional=[
                        *[{
                            'if': {'column_id': col},
                            'textDecoration': 'underline',
                            'textDecorationStyle': 'dotted',
                        } for col in ["AvgPerDay", "Country"]],

                        *[{
                            'if': {'column_id': col},
                            'backgroundColor': '#CDE9CB',
                            'fontWeight': 'bold'
                        } for col in usersDf.columns if col != "id"]

                    ],

                    style_cell_conditional=[
                        *[{'if': {'column_id': col},
                           'backgroundColor': '#EFFBEE',
                           'color': 'black',
                           'textAlign': 'center'
                           } for col in usersDf.columns if col != "id"],

                        {'if': {'column_id': "Sender"},
                         "editable": "True",
                         },
                    ],

                    style_data_conditional=[
                        {
                            'if': {'row_index': 'odd'},
                            'backgroundColor': '#ecfaea'
                        }
                    ],
                )
            ], className="mb-2"),
        ]),
        dbc.Row([
            dbc.Col([
                dash_table.DataTable(
                    id='words-Datatable',
                    columns=[{"name": col, "id": col} for col in wordsDf.columns if col != "id"],
                    data=wordsDf.to_dict('records'),
                    page_size=300,
                    row_selectable='multi',
                    filter_action='native',
                    sort_action='native',
                    fixed_rows={'headers': True},
                    style_table={'overflowY': 'auto', 'overflowX': 'auto'},
                    export_format="csv",
                    export_headers = "display",

                    style_header_conditional=[
                        *[{
                            'if': {'column_id': col},
                            'backgroundColor': '#CDE9CB',
                            'fontWeight': 'bold'
                        } for col in wordsDf.columns if col != "id"]

                    ],

                    style_cell_conditional=[
                        *[{'if': {'column_id': col},
                           'backgroundColor': '#EFFBEE',
                           'color': 'black',
                           'textAlign': 'center',
                           "font-size": "large",
                           'minWidth': '180px', 'width': '180px', 'maxWidth': '180px',
                           } for col in wordsDf.columns if col != "id"],

                    ],

                    style_data_conditional=[
                        {
                            'if': {'row_index': 'odd'},
                            'backgroundColor': '#ecfaea'
                        }
                    ],

                )
            ], xl=6, width=12),
            dbc.Col([
                dash_table.DataTable(
                    id='links-Datatable',
                    columns=[{"name": col, "id": col} for col in linksDf.columns if col != "id"],
                    data=linksDf.to_dict('records'),
                    page_size=300,
                    fixed_rows={'headers': True},
                    style_table={'overflowY': 'auto', 'overflowX': 'auto'},
                    export_format="csv",

                    style_header_conditional=[
                        *[{
                            'if': {'column_id': col},
                            'backgroundColor': '#CDE9CB',
                            'fontWeight': 'bold',
                            "color": "black"
                        } for col in linksDf.columns if col != "id"]

                    ],

                    style_cell_conditional=[

                        *[{'if': {'column_id': col},
                           'backgroundColor': '#EFFBEE',
                           'color': 'black',
                           'textAlign': 'center',
                           'minWidth': '180px', 'width': '180px', 'maxWidth': '180px',
                           } for col in linksDf.columns if col != "id"],


                        {"if": {"column_id": "Message"},
                         'whiteSpace': 'normal',
                         'height': 'auto',
                         "color": "blue",
                         'minWidth': '260px', 'width': '260px', 'maxWidth': '260px',
                         },

                    ],

                    style_data_conditional=[
                        {
                            'if': {'row_index': 'odd'},
                            'backgroundColor': '#ecfaea'
                        }
                    ],
                )
            ], xl=6, width=12)
        ])

    ])
    return layout
