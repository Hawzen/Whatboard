from datetime import datetime

import numpy as np
import pandas as pd
import plotly.express as px
from plotly.graph_objs import *

days = ["Mon", "Tues", "Wed", "Thurs", "Fri", "Sat", "Sun"]
months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'June', 'July', 'Aug', 'Sept', 'Oct', 'Nov', 'Dec']

hoursColor = "#d4ebd5"
weeksColor = "Viridis"
yearsColor = "Viridis"
allColor = "#d4ebd5"

paper_bgcolor = "#F3FFF2"
plot_bgcolor = "#F3FFF2"


def plotMessagesOverTime(data: pd.DataFrame, mode: str):
    if mode.lower() == 'hours' or mode.lower() == 'days':
        return plotHours(data)
    elif mode.lower() == 'weeks':
        return plotWeeks(data)
    elif mode.lower() == 'years':
        return plotYears(data)
    elif mode.lower() == "all":
        return plotAll(data)
    else:
        raise Exception(f"No mode {mode} exist")


def plotHours(data: pd.DataFrame):
    # DataFrame For Hour
    hours = np.arange(24)
    messages = pd.Series(np.zeros(24), hours, dtype="int64")
    hist_df = pd.DataFrame({'Hour Of Day': hours, 'Messages': messages + data.groupby(data.index.hour).size()})

    # Plotting Hist
    fig = px.histogram(hist_df, x="Hour Of Day", y="Messages", color_discrete_sequence=[hoursColor])

    # Layout adjustment
    fig.update_traces(xbins_size="M1")
    # fig.update_xaxes(ticklabelmode="instant", dtick="M1", tickformat="h")
    fig.update_layout(bargap=0.1)
    fig.update_layout(
        yaxis_title="No. Of Messages",
        font=dict(
            family="Courier New, monospace",
            size=18,
            color="RebeccaPurple"
        ),
        autosize=True,
        margin=dict(t=0, b=0, l=0, r=0),
        paper_bgcolor=paper_bgcolor,
        plot_bgcolor=plot_bgcolor
    )

    fig.update_traces(hovertemplate="Hour: %{x}<br>No. Of Messages: %{y}<br>")
    return fig


def plotWeeks(data: pd.DataFrame):
    week_day_list = []
    hours_list = []
    num_msg_list = []

    # enumerating the groupby DataFrame
    for ((day, hour), num_msg) in data.groupby([data.index.dayofweek, data.index.hour]).size().items():
        week_day_list.append(days[day])
        hours_list.append(hour)
        num_msg_list.append(num_msg)

    # Creat DataFrame for heatmap
    heat_df = pd.DataFrame({'Day': week_day_list, 'Hours': hours_list, 'No. of messages': num_msg_list})

    # Plotting heatmap
    fig = px.density_heatmap(heat_df, x='Hours', y='Day', z='No. of messages',
                             color_continuous_scale=weeksColor, nbinsx=24, nbinsy=24)

    # Layout adjustment
    fig.update_layout(
        xaxis_title="Hours",
        yaxis_title="Day",
        font=dict(
            family="Courier New, monospace",
            size=18,
            color="RebeccaPurple"
        ),
        coloraxis_colorbar=dict(
            title="No. Of Messages",
            thicknessmode="pixels", thickness=50,
            yanchor="top", y=1,
            ticks="outside",
        ),
        autosize=True,
        margin=dict(t=0, b=0, l=0, r=0),
        paper_bgcolor=paper_bgcolor,
        plot_bgcolor=plot_bgcolor
    )

    fig.update_traces(hovertemplate="Hour: %{x}<br>Day: %{y}<br>No. Of Messages: %{z}")

    return fig


def plotYears(data: pd.DataFrame):
    week_day_list = []
    month_list = []
    num_msg_list = []

    for ((year, month, day), num_msg) in data.groupby(
            [data.index.year, data.index.month, data.index.day]).size().items():
        dt = datetime(year, month, day)

        week_day_list.append(dt.day)
        month_list.append(months[dt.month - 1])
        num_msg_list.append(num_msg)

    # Creat DataFrame for heatmap
    heat_df = pd.DataFrame({'Day': week_day_list, 'Month': month_list, 'No. of messages': num_msg_list})
    df2 = pd.DataFrame([[29, 'Feb', 0], [30, 'Feb', 0], [31, 'Feb', 0]
                           , [31, 'Apr', 0], [31, 'Jun', 0], [31, 'Sept', 0]
                           , [31, 'Nov', 0]], columns=['Day', 'Month', 'No. of messages'])

    heat_df = heat_df.append(df2, ignore_index=True)

    # Plotting heatmap
    fig = px.density_heatmap(heat_df, x='Month', y='Day', z='No. of messages', nbinsy=32,
                             color_continuous_scale=yearsColor)
    # Layout adjustment
    fig.update_layout(
        font=dict(
            family="Courier New, monospace",
            size=18,
            color="RebeccaPurple"
        ),
        coloraxis_colorbar=dict(
            title="No. Of Messages",
            thicknessmode="pixels", thickness=50,
            yanchor="top", y=1,
            ticks="outside"
        ),
        autosize=True,
        margin=dict(t=0, b=0, l=0, r=0),
        paper_bgcolor=paper_bgcolor,
        plot_bgcolor=plot_bgcolor
    )

    fig.update_traces(hovertemplate="Month: %{x}<br>Day: %{y}<br>No. Of Messages: %{z} <extra></extra> ")

    fig.add_trace(
        Heatmap(x=df2["Month"], y=df2["Day"], z=df2["No. of messages"], showscale=False, colorscale="Greys",
                hoverinfo='skip'))
    return fig


def plotAll(data: pd.DataFrame):
    time_stamp_list = []
    num_msg_list = []

    for time_stamp, num_msg in data.groupby(data.index).size().items():
        time_stamp_list.append(time_stamp)
        num_msg_list.append(num_msg)

    hist_dict = {'TimeStamp': time_stamp_list, 'No. of messages': num_msg_list}
    hist_df = pd.DataFrame(hist_dict)

    fig = px.histogram(hist_df, x="TimeStamp", y="No. of messages", color_discrete_sequence=[allColor])
    fig.update_xaxes(
        ticklabelmode="period",
        ticks='outside',
        tickformat="%B\n%Y")

    fig.update_layout(
        yaxis_title="No. Of Messages",
        font=dict(
            family="Courier New, monospace",
            size=18,

            color="RebeccaPurple"
        ),
        bargap=0.1,
        autosize=True,
        margin=dict(t=0, b=0, l=0, r=0),
        paper_bgcolor=paper_bgcolor,
        plot_bgcolor=plot_bgcolor
    )

    return fig


def plotGlobe(usersDf: pd.DataFrame):
    countries = {'Afghanistan': 'AF',
                 'Albania': 'AL',
                 'Algeria': 'DZ',
                 'American Samoa': 'AS',
                 'Andorra': 'AD',
                 'Angola': 'AO',
                 'Anguilla': 'AI',
                 'Antarctica': 'AQ',
                 'Antigua and Barbuda': 'AG',
                 'Argentina': 'AR',
                 'Armenia': 'AM',
                 'Aruba': 'AW',
                 'Australia': 'AU',
                 'Austria': 'AT',
                 'Azerbaijan': 'AZ',
                 'Bahamas': 'BS',
                 'Bahrain': 'BH',
                 'Bangladesh': 'BD',
                 'Barbados': 'BB',
                 'Belarus': 'BY',
                 'Belgium': 'BE',
                 'Belize': 'BZ',
                 'Benin': 'BJ',
                 'Bermuda': 'BM',
                 'Bhutan': 'BT',
                 'Bolivia, Plurinational State of': 'BO',
                 'Bonaire, Sint Eustatius and Saba': 'BQ',
                 'Bosnia and Herzegovina': 'BA',
                 'Botswana': 'BW',
                 'Bouvet Island': 'BV',
                 'Brazil': 'BR',
                 'British Indian Ocean Territory': 'IO',
                 'Brunei Darussalam': 'BN',
                 'Bulgaria': 'BG',
                 'Burkina Faso': 'BF',
                 'Burundi': 'BI',
                 'Cambodia': 'KH',
                 'Cameroon': 'CM',
                 'Canada': 'CA',
                 'Cape Verde': 'CV',
                 'Cayman Islands': 'KY',
                 'Central African Republic': 'CF',
                 'Chad': 'TD',
                 'Chile': 'CL',
                 'China': 'CN',
                 'Christmas Island': 'CX',
                 'Cocos (Keeling) Islands': 'CC',
                 'Colombia': 'CO',
                 'Comoros': 'KM',
                 'Congo': 'CG',
                 'Congo, the Democratic Republic of the': 'CD',
                 'Cook Islands': 'CK',
                 'Costa Rica': 'CR',
                 'Country name': 'Code',
                 'Croatia': 'HR',
                 'Cuba': 'CU',
                 'Curaçao': 'CW',
                 'Cyprus': 'CY',
                 'Czech Republic': 'CZ',
                 "Côte d'Ivoire": 'CI',
                 'Denmark': 'DK',
                 'Djibouti': 'DJ',
                 'Dominica': 'DM',
                 'Dominican Republic': 'DO',
                 'Ecuador': 'EC',
                 'Egypt': 'EG',
                 'El Salvador': 'SV',
                 'Equatorial Guinea': 'GQ',
                 'Eritrea': 'ER',
                 'Estonia': 'EE',
                 'Ethiopia': 'ET',
                 'Falkland Islands': 'FK',
                 'Faroe Islands': 'FO',
                 'Fiji': 'FJ',
                 'Finland': 'FI',
                 'France': 'FR',
                 'French Guiana': 'GF',
                 'French Polynesia': 'PF',
                 'French Southern Territories': 'TF',
                 'Gabon': 'GA',
                 'Gambia': 'GM',
                 'Georgia': 'GE',
                 'Germany': 'DE',
                 'Ghana': 'GH',
                 'Gibraltar': 'GI',
                 'Greece': 'GR',
                 'Greenland': 'GL',
                 'Grenada': 'GD',
                 'Guadeloupe': 'GP',
                 'Guam': 'GU',
                 'Guatemala': 'GT',
                 'Guernsey': 'GG',
                 'Guinea': 'GN',
                 'Guinea-Bissau': 'GW',
                 'Guyana': 'GY',
                 'Haiti': 'HT',
                 'Heard Island and McDonald Islands': 'HM',
                 'Holy See (Vatican City State)': 'VA',
                 'Honduras': 'HN',
                 'Hong Kong': 'HK',
                 'Hungary': 'HU',
                 'ISO 3166-2:GB': '(.uk)',
                 'Iceland': 'IS',
                 'India': 'IN',
                 'Indonesia': 'ID',
                 'Iran, Islamic Republic of': 'IR',
                 'Iraq': 'IQ',
                 'Ireland': 'IE',
                 'Isle of Man': 'IM',
                 'Israel': 'IL',
                 'Italy': 'IT',
                 'Jamaica': 'JM',
                 'Japan': 'JP',
                 'Jersey': 'JE',
                 'Jordan': 'JO',
                 'Kazakhstan': 'KZ',
                 'Kenya': 'KE',
                 'Kiribati': 'KI',
                 "Korea, Democratic People's Republic of": 'KP',
                 'Korea, Republic of': 'KR',
                 'Kuwait': 'KW',
                 'Kyrgyzstan': 'KG',
                 "Lao People's Democratic Republic": 'LA',
                 'Latvia': 'LV',
                 'Lebanon': 'LB',
                 'Lesotho': 'LS',
                 'Liberia': 'LR',
                 'Libya': 'LY',
                 'Liechtenstein': 'LI',
                 'Lithuania': 'LT',
                 'Luxembourg': 'LU',
                 'Macao': 'MO',
                 'Macedonia, the former Yugoslav Republic of': 'MK',
                 'Madagascar': 'MG',
                 'Malawi': 'MW',
                 'Malaysia': 'MY',
                 'Maldives': 'MV',
                 'Mali': 'ML',
                 'Malta': 'MT',
                 'Marshall Islands': 'MH',
                 'Martinique': 'MQ',
                 'Mauritania': 'MR',
                 'Mauritius': 'MU',
                 'Mayotte': 'YT',
                 'Mexico': 'MX',
                 'Micronesia, Federated States of': 'FM',
                 'Moldova, Republic of': 'MD',
                 'Monaco': 'MC',
                 'Mongolia': 'MN',
                 'Montenegro': 'ME',
                 'Montserrat': 'MS',
                 'Morocco': 'MA',
                 'Mozambique': 'MZ',
                 'Myanmar': 'MM',
                 'Namibia': 'NA',
                 'Nauru': 'NR',
                 'Nepal': 'NP',
                 'Netherlands': 'NL',
                 'New Caledonia': 'NC',
                 'New Zealand': 'NZ',
                 'Nicaragua': 'NI',
                 'Niger': 'NE',
                 'Nigeria': 'NG',
                 'Niue': 'NU',
                 'Norfolk Island': 'NF',
                 'Northern Mariana Islands': 'MP',
                 'Norway': 'NO',
                 'Oman': 'OM',
                 'Pakistan': 'PK',
                 'Palau': 'PW',
                 'Palestine, State of': 'PS',
                 'Panama': 'PA',
                 'Papua New Guinea': 'PG',
                 'Paraguay': 'PY',
                 'Peru': 'PE',
                 'Philippines': 'PH',
                 'Pitcairn': 'PN',
                 'Poland': 'PL',
                 'Portugal': 'PT',
                 'Puerto Rico': 'PR',
                 'Qatar': 'QA',
                 'Romania': 'RO',
                 'Russian Federation': 'RU',
                 'Rwanda': 'RW',
                 'Réunion': 'RE',
                 'Saint Barthélemy': 'BL',
                 'Saint Helena, Ascension and Tristan da Cunha': 'SH',
                 'Saint Kitts and Nevis': 'KN',
                 'Saint Lucia': 'LC',
                 'Saint Martin': 'MF',
                 'Saint Pierre and Miquelon': 'PM',
                 'Saint Vincent and the Grenadines': 'VC',
                 'Samoa': 'WS',
                 'San Marino': 'SM',
                 'Sao Tome and Principe': 'ST',
                 'Saudi Arabia': 'SA',
                 'Senegal': 'SN',
                 'Serbia': 'RS',
                 'Seychelles': 'SC',
                 'Sierra Leone': 'SL',
                 'Singapore': 'SG',
                 'Sint Maarten': 'SX',
                 'Slovakia': 'SK',
                 'Slovenia': 'SI',
                 'Solomon Islands': 'SB',
                 'Somalia': 'SO',
                 'South Africa': 'ZA',
                 'South Georgia and the South Sandwich Islands': 'GS',
                 'South Sudan': 'SS',
                 'Spain': 'ES',
                 'Sri Lanka': 'LK',
                 'Sudan': 'SD',
                 'Suriname': 'SR',
                 'Svalbard and Jan Mayen': 'SJ',
                 'Swaziland': 'SZ',
                 'Sweden': 'SE',
                 'Switzerland': 'CH',
                 'Syrian Arab Republic': 'SY',
                 'Taiwan, Province of China': 'TW',
                 'Tajikistan': 'TJ',
                 'Tanzania, United Republic of': 'TZ',
                 'Thailand': 'TH',
                 'Timor-Leste': 'TL',
                 'Togo': 'TG',
                 'Tokelau': 'TK',
                 'Tonga': 'TO',
                 'Trinidad and Tobago': 'TT',
                 'Tunisia': 'TN',
                 'Turkey': 'TR',
                 'Turkmenistan': 'TM',
                 'Turks and Caicos Islands': 'TC',
                 'Tuvalu': 'TV',
                 'Uganda': 'UG',
                 'Ukraine': 'UA',
                 'United Arab Emirates': 'AE',
                 'United Kingdom': 'GB',
                 'United States': 'US',
                 'United States Minor Outlying Islands': 'UM',
                 'Uruguay': 'UY',
                 'Uzbekistan': 'UZ',
                 'Vanuatu': 'VU',
                 'Venezuela, Bolivarian Republic of': 'VE',
                 'Viet Nam': 'VN',
                 'Virgin Islands, British': 'VG',
                 'Virgin Islands, U.S.': 'VI',
                 'Wallis and Futuna': 'WF',
                 'Western Sahara': 'EH',
                 'Yemen': 'YE',
                 'Zambia': 'ZM',
                 'Zimbabwe': 'ZW',
                 'Åland Islands': 'AX'}

    iso_code = {val: key for key, val in countries.items()}
    usersDf['Country Name'] = [iso_code.get(str(cnt), "Unspecified") for cnt in usersDf["Country"].values]

    users_country = []
    country_count = []
    for Country_Name, num_persons in usersDf.groupby('Country Name').size().items():
        if Country_Name == 'Unspecified':
            users_country.append(str(num_persons) + " " + Country_Name)
            country_count.append(num_persons)
            continue
        users_country.append(Country_Name)
        country_count.append(num_persons)

    globe_df = pd.DataFrame({'Country': users_country, 'No. Users': country_count})

    fig = px.scatter_geo(globe_df, locations="Country",
                         color="Country",  # which column to use to set the color of markers
                         hover_name="Country",  # column added to hover information
                         locationmode='country names',
                         size='No. Users',
                         size_max=60,
                         projection="natural earth",
                         )

    fig.update_layout(
        geo=dict(bgcolor='rgb(243, 255, 242)'),
        paper_bgcolor=paper_bgcolor,
        autosize=True,
        margin=dict(t=0, b=0, l=0, r=0),
        showlegend=False,
        plot_bgcolor=plot_bgcolor
    )
    return fig


def plotUsersAnimation(data: pd.DataFrame, users):
    # Number of messages indexed by user and month
    msgsByUserAndMonth = pd.DataFrame(data.groupby([data['Sender'], data.index.month]).size())

    newIndex = pd.MultiIndex.from_product(msgsByUserAndMonth.index.levels)
    msgsByUserAndMonth = msgsByUserAndMonth.reindex(newIndex).fillna(0)

    # Make index columns
    animationDf = msgsByUserAndMonth.reset_index()
    animationDf.columns = ["User", "Month", "No. Of Messages"]

    # Filter by given users
    animationDf = animationDf[animationDf["User"].isin(users)]

    # Change from month numbers to names
    animationDf["Month"] = [months[m - 1] for m in animationDf["Month"]]

    upper = max(animationDf["No. Of Messages"])

    fig = px.bar(animationDf, x="User", y="No. Of Messages", color="User",
                 animation_frame="Month", animation_group="User", range_y=[0, max(animationDf["No. Of Messages"])])

    fig.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 1500

    fig.update_layout(
        paper_bgcolor=paper_bgcolor,
        plot_bgcolor=plot_bgcolor,
        autosize=True,
        margin=dict(t=0, b=0, l=0, r=0),
    )

    return fig
