
import numpy as np
import pandas as pd

import plotly.express as px
import plotly.graph_objs as go

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output



###############################
### Load Data & Make Graphs ###
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

# Boro data
boro = pd.read_csv(
    "https://raw.githubusercontent.com/nychealth/coronavirus-data/master/boro.csv"
).iloc[:5]

def make_boro_graph(actual_count=False):
    if actual_count:
        boro_fig = px.bar(
            boro.sort_values("COVID_CASE_COUNT",ascending=True),
            x="COVID_CASE_COUNT",
            y="BOROUGH_GROUP",
            orientation='h')
        boro_fig.update_layout(
            title="COVID-19 Cases by Borough",
            xaxis_title="Number of Cases",
            yaxis_title=None)
    else:
        boro_fig = px.bar(
            boro.sort_values("COVID_CASE_RATE",ascending=True),
            x="COVID_CASE_RATE",
            y="BOROUGH_GROUP",
            orientation='h')
        boro_fig.update_layout(
            title="COVID-19 Cases by Borough",
            xaxis_title="Case Rate (per 100,000 People)",
            yaxis_title=None)
    return boro_fig

boro_fig = make_boro_graph(False)

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
        dcc.RadioItems(
                id='boro-graph-val',
                options=[
                    {"label":"Actual Cases","value":"COVID_CASE_COUNT"},
                    {"label":"Cases per 100,000","value":"COVID_CASE_RATE"}
                ],
                value='COVID_CASE_RATE',
                labelStyle={'display': 'inline-block'}
            ),
        dcc.Graph(
            id="borough-graph",
            figure=boro_fig
        ),

        # Source information
        html.H2(children="Source"),
        html.P(children="Data courtesy of the NYC Department of Health and Mental Hygiene."),
        html.P(children=[
            "Repo can be found ",
            html.A(children="here",href="https://github.com/nychealth/coronavirus-data"),
            "."
        ])
    ]
)

###############################
###        Callbacks        ###
###############################

@app.callback(
    Output(component_id='borough-graph', component_property='figure'),
    [Input(component_id='boro-graph-val', component_property='value')]
)
def update_boro_plot(actual_or_rate):
    if actual_or_rate == "COVID_CASE_RATE":
        return make_boro_graph(False)
    else:
        return make_boro_graph(True)



if __name__ == '__main__':
    app.run_server(debug=True)
