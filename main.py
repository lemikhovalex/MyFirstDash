# -*- coding: utf-8 -*-

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.
import transformer
import data_samples_creator
import styles
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
import base64
import io
from dash.dependencies import Input, Output

data_samples_creator.generate_circle()

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = 'MyFirstDash'
# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
df1 = pd.DataFrame({
    "x": [1, 2, 3, 4, 5, 6, 7],
    "y": [1, 2, 3, 4, 5, 6, 7],
})

fig1 = px.scatter(df1, x="x", y="y", title='Before transform')
df2 = transformer.transform(df1)
fig2 = px.scatter(df2, x="x", y="y", title='After transform')

empt_fig1 = px.scatter(title='Before transform')
empt_fig2 = px.scatter(title='After transform')

app.layout = html.Div(children=[
    html.H1(
        children='Guess quadratic func',
        style={
            'textAlign': 'center',
        }
    ),

    html.H2(children='With given x and y, y got transformed', style={
        'textAlign': 'center',
    }),
    html.H3(children='Here is simple example', style={
        'textAlign': 'center',
    }),
    html.Div(children=[
        html.Div([
            html.H3('Before'),
            dcc.Graph(id='before_1', figure=fig1)
        ], className="six columns"),

        html.Div([
            html.H3('After'),
            dcc.Graph(id='after_1', figure=fig2)
        ], className="six columns"),
    ]),

    html.Div([
        html.H5('You are free do upload your own data as pandas.DataFrame with 2 columns "x" and "y"'),
        dcc.Upload(
            id='upload-data',
            children=html.Div([
                'Drag and Drop or ',
                html.A('Select Files')
            ]),
            style=styles.drag_drop_styles,
            multiple=True
        ),
    ], className="container"),
    html.Div(children=[
        html.Div([
            html.H3('Before'),
            dcc.Graph(id='before_upl', figure=empt_fig1)
        ], className="six columns"),

        html.Div([
            html.H3('After'),
            dcc.Graph(id='after_upl', figure=empt_fig2)
        ], className="six columns"),
    ])
])


def parse_data(contents, filename):
    content_type, content_string = contents.split(',')
    df = pd.DataFrame()
    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV or TXT file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))
        elif 'xls' in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
        elif 'txt' or 'tsv' in filename:
            # Assume that the user upl, delimiter = r'\s+'oaded an excel file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')), delimiter=r'\s+')
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])

    return df


@app.callback(
    [Output(component_id='before_upl', component_property='figure'),
     Output(component_id='after_upl', component_property='figure')
     ],
    [Input(component_id='upload-data', component_property='contents'),
     Input(component_id='upload-data', component_property='filename')]
)
def update_graph(contents, filename):
    _fig1 = px.scatter()
    _fig2 = px.scatter()

    if contents:
        contents = contents[0]
        filename = filename[0]
        df = parse_data(contents, filename)
        df = df.set_index(df.columns[0])
        _fig1 = px.scatter(df, x="x", y="y", title='Before transform')
        _fig2 = px.scatter(transformer.transform(df), x="x", y="y", title='After transform')

    return _fig1, _fig2


if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0')
