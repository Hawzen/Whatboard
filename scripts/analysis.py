import os
import re
from collections import Counter
import numpy as np
import pandas as pd
import phonenumbers

crntPath = os.path.dirname(__file__)
patternsPath = os.path.join(crntPath, "..", "data2", "patterns.txt")
with open(patternsPath, "r+", encoding="utf-8") as file:
    command_patterns, command_patterns_w_colon = [ln.split(";") for ln in file.readlines()]

time_stamp_pattern = '(\\d{0,4})/(\\d{0,4})/(\\d{0,4}), (\\d{1,2}):(\\d{1,2})\\:?(\\d{0,2})( am| pm| AM| PM)?'

user_patterns = ["<Media omitted>|media omitted|‎sticker omitted",
                 "This message was deleted|You deleted this message"]
media_patt, deleted_patt = user_patterns


def registerOutlier(text):
    """Registers a new outlier and updates the command patterns"""
    global command_patterns_w_colon
    text = text.strip()
    command_patterns_w_colon.append(text)
    with open(patternsPath, "a+", encoding="utf-8") as file:
        file.write(f";{text}")


def getData(name: str):
    with open(name, "r", encoding="utf-8") as file:
        data = file.readlines()
    return data


def isNewLine(line):
    # Detects weather the line is a new line or a continuation of a line
    # Examples of new lines contain:
    #   00/00/0000, 0:00 pm
    #   [00/00/0000, 00:00:00 PM]
    return re.search(r'\[?(\d{0,4})/(\d{0,4})/(\d{0,4}), (\d{1,2}):(\d{1,2}):?(\d{0,2}) (\D{2})\]?', line)


def removeGroupMsgs(data: list) -> (list, list):
    removed_list = []
    for line in data:
        end = re.search(time_stamp_pattern, line).end()
        if line[end + 1:].find(":") != -1:
            for pattern in command_patterns_w_colon:
                if re.search(pattern, line):
                    removed_list.append(line)
                    break
            continue

        removed_list.append(line)

    data = [el for el in data if el not in removed_list]
    return data, removed_list


def filterData(data, load=False) -> (list, list):
    if isinstance(data, str) and load:
        data = getData(data)

    newData = []
    for line in data:
        if isNewLine(line):
            newData.append(line)
        else:
            newData[-1] += line
    return removeGroupMsgs(newData)


def getDataFrame(data, ukformat=False) -> pd.DataFrame:
    name = data
    if isinstance(data, str):
        data = getData(data)
        data, _ = filterData(data)

    time_stamp_list = []
    senders_list = []
    messages_list = []

    for text in data:
        time_stamp = re.search(time_stamp_pattern, text)
        time_stamp_list.append(time_stamp.group())

        text = text[time_stamp.end():]

        try:
            sender = text[:text.index(":")].replace("-", "").replace("]", "").strip()
        except ValueError:  # New outlier detected
            print("registered a new outlier: ", text)
            registerOutlier(text)
            return getDataFrame(name)
        message = text[text.index(":") + 2:-1]  # +2 for ": " and -1 for "\n"
        senders_list.append(sender)
        messages_list.append(message)

    df = pd.DataFrame({'Sender': senders_list, 'Message': messages_list},
                      index=pd.to_datetime(time_stamp_list, dayfirst=not ukformat))

    return df


@np.vectorize
def getCountry(phoneNum: str):
    try:
        return phonenumbers.region_code_for_number(phonenumbers.parse(phoneNum))
    except phonenumbers.NumberParseException:
        return None


@np.vectorize
def getUserFromCommand(joinedStr: str) -> str:
    joined = re.search("joined using", joinedStr).end()
    if joined:
        end = re.search(time_stamp_pattern, joinedStr).end()
        return joinedStr[end + 1:joined].replace("-", "").replace("]", "")


def getUsers(df: pd.DataFrame, commands: list = None) -> pd.DataFrame:
    userDayGroup = df.groupby(
        ["Sender", df.index.floor("d")]).size()  # Group by user and day, values are count msgs each day
    out = userDayGroup.groupby("Sender").agg(["sum", "mean", "max", "min"])
    out.columns = ["Count", "AvgPerDay", "MaxADay", "MinADay"]

    userGroup = df.groupby("Sender")["Message"]
    out["Media_Sent"] = userGroup.apply(lambda g: g.str.contains(media_patt, regex=True).sum())
    out["Deleted_Message"] = userGroup.apply(lambda g: g.str.contains(deleted_patt, regex=True).sum())

    names = df["Sender"].unique()
    countries = getCountry(names)
    out["Country"] = pd.Series(countries, index=names)

    # Refactor later
    if commands:
        for command in commands:
            joined = re.search("joined using", command)
            if joined:
                end = re.search(time_stamp_pattern, command).end()
                user = command[end + 1:joined.start() - 1].replace("-", "").replace("]", "").strip()
                user = re.sub("(?!:[^+])[^\w+]", ' ', user).strip()
                if user not in out.index and user != "You":
                    out.loc[user] = [0, 0, 0, 0, 0, 0, getCountry(user)]

    return out


def testMsg(msg: str):
    # msg = msg.replace(u'\u200e', "").replace(u'\u200e', "")
    return all(not re.match(pat, msg) for pat in user_patterns)


def getWords(df: pd.DataFrame) -> pd.DataFrame:
    """
    df: pd.DataFrame, Index=Date Column=(Sender, Message)
    users: list of users to filter df with, None is no filter
    Returns a DataFrame, Index=Words Values=Frequency
    """
    msgs = df["Message"].values

    words = " ".join(filter(testMsg, msgs))
    counter = Counter(words.split())
    wordsDF = pd.DataFrame(counter.values(), index=counter.keys(), columns=["Frequency"])
    wordsDF.index.rename("Word")
    return wordsDF


def getLinks(df: pd.DataFrame) -> pd.DataFrame:
    link_pattern = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)" \
                   r"(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]" \
                   r"+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
    linksDf = df[df["Message"].str.match(link_pattern)]
    linksDf.index = linksDf.index.floor("d")
    return linksDf
