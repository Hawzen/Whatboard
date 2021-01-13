import os
import re
import sys

import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, State

from app import cache
from dashboard import dashboard
from scripts import analysis

crntPath = os.path.dirname(__file__)
sys.path.insert(1, os.path.join(crntPath, "report_components"))
samplePath = os.path.join(crntPath, "..", "data2/beeSample.txt")


# Dataframes
def getDf(data, ukformat=False):
    df = analysis.getDataFrame(data, ukformat=ukformat)
    return df


def getUsersDf(df, commands):
    usersDf = analysis.getUsers(df, commands)
    usersDf["AvgPerDay"] = usersDf["AvgPerDay"].round(1)
    usersDf = usersDf.reset_index()
    usersDf['id'] = usersDf['Sender']
    usersDf.set_index('id', inplace=True, drop=False)
    return usersDf


def getWordsDf(df):
    wordsDf = analysis.getWords(df)
    wordsDf = wordsDf.reset_index()
    wordsDf.columns = ["Word", "Frequency"]
    wordsDf["id"] = wordsDf["Word"]
    wordsDf.set_index('id', inplace=True, drop=False)
    return wordsDf


def getLinksDf(df):
    linksDf = analysis.getLinks(df)
    # linksDf = linksDf.reset_index()
    linksDf.columns = ["Sender", "Message"]
    return linksDf


def getAllDf(text, isPath=False, ukformat=False):
    data, commands = analysis.filterData(text, isPath)
    df = getDf(data, ukformat=ukformat)
    usersDf = getUsersDf(df, commands)
    wordsDf = getWordsDf(df)
    linksDf = getLinksDf(df)
    return df, commands, usersDf, wordsDf, linksDf


# Getters
@cache.memoize(24 * 60 * 60)
def getSampleDf():
    return getAllDf(samplePath, isPath=True)


def getLayout(data, isSample=False, isDataframes=None, name="Analyze"):
    if isDataframes:
        df, commands, usersDf, wordsDf, linksDf = data
    elif isSample:
        df, commands, usersDf, wordsDf, linksDf = getSampleDf()
    else: # This shouldn't usually be called, since uploaded data have isDataframes and sample data have isSample
        print("getLayout got data with isSample=False, isDataframes=False")
        df, commands, usersDf, wordsDf, linksDf = getAllDf(data)

    layout = html.Div([
        dbc.Row(
            dbc.Col(
                html.H2(name.capitalize(), className="display-5 mb-3 pt-5"),
            )
        ),
        dbc.Row(general_statistics.getLayout(df)),
        *dashboard.createSpinner(dbc.Row(tabels.getLayout(df, commands, usersDf, wordsDf, linksDf)),),
        *dashboard.createSpinner(dbc.Row(msgs_to_time_plot.getLayout()),),
        dbc.Row(other_plots.getLayout(usersDf)),
    ], className="mb-5 mt-0 pt-0")

    return layout


def getConstraints(w_refresh=True):
    """ Outputs the following parameters
        user_row_ids
        word_row_ids
        start
        end
    """
    constraints = [
        State('users-Datatable', 'selected_row_ids'),
        State('words-Datatable', 'selected_row_ids'),
        *[State("df-datepicker", val) for val in ["start_date", "end_date"]]
    ]

    if w_refresh:
        constraints.insert(0, Input("report-refresh", "n_clicks"))

    return constraints


def getDataStateFunctions():
    return [
        State("report-div-type", "children"),
        State('upload-data', 'contents'),
        State('upload-data', 'filename'),
        State("month-formatting", "checked")
    ]


# Convenience
@cache.memoize(30 * 60)
def applyConstraints(df, user_row_ids=None, word_row_ids=None, start=None, end=None):
    """ Applies the constraints in the following order
        date constraint
        user constraint word constraint
    """
    df = datePickerFilter(df, start, end)

    if len(df) == 0:
        return df

    if user_row_ids:
        df = df[df["Sender"].isin(user_row_ids)]

    if word_row_ids:
        word_row_ids = [re.escape(m) for m in word_row_ids]
        df = df[df["Message"].str.contains("|".join(word_row_ids))]

    return df


def sampleOrUploaded(content, filename, reportDivType, ukformat=False):
    if reportDivType == "uploaded":
        return parse_contents(content, filename, returnDataframe=True, ukformat=ukformat)
    elif reportDivType == "sample":
        return getSampleDf()


def datePickerFilter(df, start, end):
    if start is not None:
        df = df[df.index > start]
    if end is not None:
        df = df[df.index < end]
    return df


# Import after adding the directory to path, and after all function definitions
import general_statistics, tabels, msgs_to_time_plot, other_plots
from options import parse_contents
