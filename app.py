
import numpy as np
import pandas as pd

import plotly.express as px
import plotly.graph_objs as go

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output



###############################
###        Load Data        ###
###############################

# Summary data
summary = pd.read_csv(
    "https://raw.githubusercontent.com/nychealth/coronavirus-data/master/summary.csv",
    names=["VALUE"]
).iloc[:4,:]
summary.VALUE = summary.VALUE.astype("int")
# Tests data
tests = pd.read_csv(
    "https://raw.githubusercontent.com/nychealth/coronavirus-data/master/tests.csv",
    parse_dates=True
)
tests.DATE = pd.to_datetime(tests.DATE)
# Case / Hospital / Deaths
case_hosp_death = pd.read_csv(
    "https://raw.githubusercontent.com/nychealth/coronavirus-data/master/case-hosp-death.csv",
    parse_dates=True
)
# Borough
by_boro = pd.read_csv(
    "https://raw.githubusercontent.com/nychealth/coronavirus-data/master/by-boro.csv"
).iloc[:5]
# Sex
by_sex = pd.read_csv(
    "https://raw.githubusercontent.com/nychealth/coronavirus-data/master/by-sex.csv"
).iloc[:2]
# Race
by_race = pd.read_csv(
    "https://raw.githubusercontent.com/nychealth/coronavirus-data/master/by-race.csv"
).sort_values("CASE_RATE_ADJ")
# Poverty
by_poverty = pd.read_csv(
    "https://raw.githubusercontent.com/nychealth/coronavirus-data/master/by-poverty.csv"
)
# Age
by_age = pd.read_csv(
    "https://raw.githubusercontent.com/nychealth/coronavirus-data/master/by-age.csv"
).iloc[:5]


###############################
###       Make Plots        ###
###############################

tests_fig = go.Figure()
tests_fig.add_trace(go.Scatter(
    x=tests.DATE,
    y=tests.TOTAL_TESTS,
    name="Total Tests"
))
tests_fig.add_trace(go.Scatter(
    x=tests.DATE,
    y=tests.POSITIVE_TESTS,
    name="Positive Tests"
))
tests_fig.update_layout(
    title="Number of Cases Performed vs Number of New COVID-19 Cases",
    showlegend=False,
    yaxis_title="Number of People",
    annotations=[
        dict(
            x=tests.DATE.max(),
            y=tests.TOTAL_TESTS.iloc[-1],
            xref="x",
            yref="y",
            text="Total Tests",
            align="left",
            showarrow=True,
            ax=30,
            ay=0
        ),
        dict(
            x=tests.DATE.max(),
            y=tests.POSITIVE_TESTS.iloc[-1],
            xref="x",
            yref="y",
            text="Positive Tests",
            align="left",
            showarrow=True,
            ax=40,
            ay=0
        )
    ]
)

def make_boro_graph(number,case_rate):
    col = f"{number.upper()}_{case_rate.upper()}"

    if number == "CASE":
        axlabel = "Cases"
    elif number == "HOSPITALIZED":
        axlabel = "Hospitalizations"
    else:
        axlabel = "Deaths"

    if case_rate == "RATE":
        axlabel += " (per 100,000 People)"

    boro_fig = px.bar(
        by_boro.sort_values(col,ascending=True),
        x=col,
        y="BOROUGH_GROUP",
        orientation='h')

    boro_fig.update_layout(
        title="COVID-19 Cases by Borough",
        xaxis_title=axlabel,
        yaxis_title=None)

    return boro_fig

boro_fig = make_boro_graph(
    "CASE",
    "RATE"
)

race_rate_fig = go.Figure(data=[
    go.Bar(
        name='Deaths',
        x=by_race.DEATH_RATE_ADJ,
        y=by_race.RACE_GROUP,
        orientation='h',
        marker_color="#d62728"),
    go.Bar(
        name='Hospitalizations',
        x=by_race.HOSPITALIZED_RATE_ADJ,
        y=by_race.RACE_GROUP,
        orientation='h',
        marker_color="#ff7f0e"),
    go.Bar(
        name='Cases',
        x=by_race.CASE_RATE_ADJ,
        y=by_race.RACE_GROUP,
        orientation='h',
        marker_color="#1f77b4")
    
])
race_rate_fig.update_layout(
    title="Age-Adjusted COVID-19 Rate by Race (per 100,000 People)",
    xaxis_title=None
)

###############################
###      Make the App       ###
###############################
app = dash.Dash(
    __name__
)
server = app.server

app.title = "COVID-19 Dashboard"
app.layout = html.Div(
    id="app-container",
    children=[
        # Title and blurb
        html.H1(
            id="title",
            children="NYC COVID-19 Dashboard"
            ),
        html.P(
            children=html.I(children="by Austin Poor")
        ),
        html.P(
            children="Information on the COVID-19 outbreak in NYC."
        ),
        html.P(
            children=[
                "Data courtesy of the NYC Department of Health and Mental Hygiene. ",
                "GitHub repo can be found ",
                html.A(children="here",href="https://github.com/nychealth/coronavirus-data"),
                "."
            ]
        ),
        
        # Key numbers table
        html.H2(children="At a Glance"),
        html.Table(children=[
            html.Tr(children=[
                html.Td(children=[
                    html.Span(className="big-number",children=f"{summary.loc['NYC_CASE_COUNT'][0]:,}"),
                    html.Br(),
                    html.Span(className="num-text",children="Cases"),
                    ]),
                html.Td(children=[
                    html.Span(className="big-number",children=f"{summary.loc['NYC_HOSPITALIZED_COUNT'][0]:,}"),
                    html.Br(),
                    html.Span(className="num-text",children="Hospitalized"),
                    ]),
                html.Td(children=[
                    html.Span(className="big-number",children=f"{summary.loc['NYC_CONFIRMED_DEATH_COUNT'][0]:,}"),
                    html.Br(),
                    html.Span(className="num-text",children="Confirmed Deaths"),
                    ]),
                html.Td(children=[
                    html.Span(className="big-number",children=f"{summary.loc['NYC_PROBABLE_DEATH_COUNT'][0]:,}"),
                    html.Br(),
                    html.Span(className="num-text",children="Probable Deaths"),
                    ])
            ])
        ]),

        # Testing graph
        html.H2(children="Testing"),
        html.P(
            children=""
        ),
        dcc.Graph(
            id="tests-graph",
            figure=tests_fig
        ),

        # By borough
        html.H2(children="Cases by Borough"),
        html.P(children=""),
        dcc.Graph(
            id="borough-graph",
            figure=boro_fig
        ),
        dcc.RadioItems(
                id='boro-graph-number',
                options=[
                    {"label":"Cases","value":"CASE"},
                    {"label":"Hospitalizations","value":"HOSPITALIZED"},
                    {"label":"Deaths","value":"DEATH"}
                ],
                value='CASE',
                labelStyle={'display': 'inline-block'}
        ),
        dcc.RadioItems(
                id='boro-case-rate',
                options=[
                    {"label":"Count","value":"COUNT"},
                    {"label":"Rate","value":"RATE"}
                ],
                value='RATE',
                labelStyle={'display': 'inline-block'}
        ),

        # By race / ethnicity
        html.H2(children="Cases by Race"),
        html.P(
            children=""
        ),
        dcc.Graph(
            id="race-rate-graph",
            figure=race_rate_fig
        ),
    ]
)



###############################
###        Callbacks        ###
###############################

@app.callback(
    Output(component_id='borough-graph', component_property='figure'),
    [Input(component_id='boro-graph-number', component_property='value'),
     Input(component_id='boro-case-rate', component_property='value')]
)
def update_boro_plot(number,case_rate):
    return make_boro_graph(number,case_rate)



if __name__ == '__main__':
    app.run_server(debug=True)
