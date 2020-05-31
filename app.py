
import datetime

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

# Syndromic
syndromic_data = pd.read_csv(
    "https://raw.githubusercontent.com/nychealth/coronavirus-data/master/syndromic_data.csv"
)
syndromic_data.Date = pd.to_datetime(syndromic_data.Date)


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

poverty_rate_fig = go.Figure(data=[
    go.Bar(
        name='Deaths',
        x=by_poverty.DEATH_RATE_ADJ,
        y=by_poverty.POVERTY_GROUP,
        orientation='h',
        marker_color="#d62728"),
    go.Bar(
        name='Hospitalizations',
        x=by_poverty.HOSPITALIZED_RATE_ADJ,
        y=by_poverty.POVERTY_GROUP,
        orientation='h',
        marker_color="#ff7f0e"),
    go.Bar(
        name='Cases',
        x=by_poverty.CASE_RATE_ADJ,
        y=by_poverty.POVERTY_GROUP,
        orientation='h',
        marker_color="#1f77b4")
    
])
poverty_rate_fig.update_layout(
    title="Age-Adjusted COVID-19 Rate by Poverty Level (per 100,000 People)",
    xaxis_title=None
)

# Age rate
age_rate_fig = go.Figure(data=[
    go.Bar(
        name='Deaths',
        x=by_age.DEATH_RATE,
        y=by_age.AGE_GROUP,
        orientation='h',
        marker_color="#d62728"),
    go.Bar(
        name='Hospitalizations',
        x=by_age.HOSPITALIZED_RATE,
        y=by_age.AGE_GROUP,
        orientation='h',
        marker_color="#ff7f0e"),
    go.Bar(
        name='Cases',
        x=by_age.CASE_RATE,
        y=by_age.AGE_GROUP,
        orientation='h',
        marker_color="#1f77b4")
    
])
age_rate_fig.update_layout(
    title="COVID-19 Rate by Age Group (per 100,000 People)",
    xaxis_title=None
)


vis_admit_fig = go.Figure(data=[
    go.Scatter(
        x=syndromic_data.Date,
        y=syndromic_data['Admit All ages'],
        name="Admissions"
    ),
    go.Scatter(
        x=syndromic_data.Date,
        y=syndromic_data['Visit All ages'],
        name="Visits"
    )
])
vis_admit_fig.update_layout(
    title="COVID-19 Rate of Hospital Visits vs Admissions (per 100,000 People)",
    showlegend=True,
    xaxis_title=None,
    yaxis_title=None
)
vis_admit_fig_ymax = max(
    syndromic_data["Admit All ages"].max(),
    syndromic_data["Visit All ages"].max()
)
vis_admit_fig.add_shape(
    # Line reference to the axes
        type="line",
        xref="x",
        yref="y",
        x0=datetime.datetime(2020,3,7),
        y0=vis_admit_fig_ymax,
        x1=datetime.datetime(2020,3,7),
        y1=0,
        line=dict(
            color="gray",
            width=3,
        ),
        opacity=0.5
    )
vis_admit_fig.add_shape(
    # Line reference to the axes
        type="line",
        xref="x",
        yref="y",
        x0=datetime.datetime(2020,3,22),
        y0=vis_admit_fig_ymax,
        x1=datetime.datetime(2020,3,22),
        y1=0,
        line=dict(
            color="gray",
            width=3,
        ),
        opacity=0.5
    )
vis_admit_fig.update_layout(
    annotations=[
        dict(
            x=datetime.datetime(2020,3,7),
            y=vis_admit_fig_ymax,
            xref="x",
            yref="y",
            text="Cuomo Declares State of Emergency",
            align="right",
            showarrow=True,
            ax=-85,
            ay=-20
        ),
        dict(
            x=datetime.datetime(2020,3,22),
            y=vis_admit_fig_ymax,
            xref="x",
            yref="y",
            text="State-Wide Stay-at-Home Order",
            align="left",
            showarrow=True,
            ax=90,
            ay=-15
        ),
    ]
)

hosp_visit_age_fig = go.Figure(data=[
    go.Scatter(
        x=syndromic_data.Date,
        y=syndromic_data['Visit 0-17'],
        name="0-17"
    ),
    go.Scatter(
        x=syndromic_data.Date,
        y=syndromic_data['Visit 18-44'],
        name="18-44"
    ),
    go.Scatter(
        x=syndromic_data.Date,
        y=syndromic_data['Visit 45-64'],
        name="45-64"
    ),
    go.Scatter(
        x=syndromic_data.Date,
        y=syndromic_data['Visit 65-74'],
        name="65-74"
    ),
    go.Scatter(
        x=syndromic_data.Date,
        y=syndromic_data['Visit 75+'],
        name="75+"
    )
])
hosp_visit_age_fig.update_layout(
    title="COVID-19 Rate of Hospital Visits by Age Group (per 100,000 People)",
    showlegend=True,
    xaxis_title=None,
    yaxis_title=None
)

hosp_admit_age_fig = go.Figure(data=[
    go.Scatter(
        x=syndromic_data.Date,
        y=syndromic_data['Admit 0-17'],
        name="0-17"
    ),
    go.Scatter(
        x=syndromic_data.Date,
        y=syndromic_data['Admit 18-44'],
        name="18-44"
    ),
    go.Scatter(
        x=syndromic_data.Date,
        y=syndromic_data['Admit 45-64'],
        name="45-64"
    ),
    go.Scatter(
        x=syndromic_data.Date,
        y=syndromic_data['Admit 65-74'],
        name="65-74"
    ),
    go.Scatter(
        x=syndromic_data.Date,
        y=syndromic_data['Admit 75+'],
        name="75+"
    )
])
hosp_admit_age_fig.update_layout(
    title="COVID-19 Rate of Hospital Admissions by Age Group (per 100,000 People)",
    showlegend=True,
    xaxis_title=None,
    yaxis_title=None
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

        # By poverty level
        html.H2(children="Cases by Poverty Level"),
        html.P(
            children=""
        ),
        dcc.Graph(
            id="poverty-rate-graph",
            figure=poverty_rate_fig
        ),

        # By age group
        html.H2(children="Cases by Age Group"),
        html.P(
            children=""
        ),
        dcc.Graph(
            id="age-rate-graph",
            figure=age_rate_fig
        ),

        # Hospital Visit & Admissions
        html.H2(children="Hospital Visits and Admissions"),
        html.P(
            children=""
        ),
        dcc.Graph(
            id="hosp-vis-admit-graph",
            figure=vis_admit_fig
        ),
        dcc.Graph(
            id="hosp-vis-age-graph",
            figure=hosp_visit_age_fig
        ),
        dcc.Graph(
            id="hosp-admit-age-graph",
            figure=hosp_admit_age_fig
        ),

        # Source information
        html.H2(children="Source"),
        html.P(
            children=[
                "Data courtesy of the NYC Department of Health and Mental Hygiene. "
            ]
        ),
        html.P(
            children=[
                "GitHub repo can be found ",
                html.A(children="here",href="https://github.com/nychealth/coronavirus-data"),
                "."
            ]
        ),
        html.Br()
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
