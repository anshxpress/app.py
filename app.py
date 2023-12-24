import pandas as pd
import dash
import plotly.graph_objs as go
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output

external_stylesheets = [
    {
        'href': 'https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css',
        'rel': 'stylesheet',
        'integrity': 'sha384-MCw98/SFnGE8FJT3GXwEOngsV72t27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO',
        'crossorigin': 'anonymous'
    }
]

patients = pd.read_csv('IndividualDetails.csv')
total = patients.shape[0]
active = patients[patients['current_status'] == 'Hospitalized'].shape[0]
Recovered = patients[patients['current_status'] == 'recovered'].shape[0]
deaths = patients[patients['current_status'] == 'Deceased'].shape[0]
options = [
             {'label': 'All', 'value': 'All'},
             {'label': 'Hospitalized', 'value': 'Hospitalized'},
             {'label': 'Deceased', 'value': 'Deceased'},
             {'label': 'Recovers', 'value': 'Recovers'},
          ]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# Define the layout
app.layout = html.Div([
 html.H1("COVID-19 Analysis", style={'text-align': 'center'}),
    # First part with 4 square blocks
    html.Div([
        html.Div([
            html.H3("Total Cases", style={'color': 'black', 'text-align': 'center', 'padding-top': '40px','font-weight': 'bold'}),
            html.H4(total, style={'color': 'black', 'text-align': 'center'})
        ], style={'backgroundColor': 'blue', 'height': '200px', 'width': '25%', 'float': 'left'}),

        html.Div([
            html.H3("Active Cases", style={'color': 'black', 'text-align': 'center', 'padding-top': '40px','font-weight': 'bold'}),
            html.H4(active, style={'color': 'black', 'text-align': 'center'})
        ], style={'backgroundColor': 'red', 'height': '200px', 'width': '25%', 'float': 'left'}),

        html.Div([
            html.H3("Recovers",style={'color': 'black', 'text-align': 'center', 'padding-top': '40px','font-weight': 'bold'}),
            html.H4(Recovered, style={'color': 'black', 'text-align': 'center'})
        ], style={'backgroundColor': 'green', 'height': '200px', 'width': '25%', 'float': 'left'}),

        html.Div([
            html.H3("Deaths",style={'color': 'black', 'text-align': 'center', 'padding-top': '40px','font-weight': 'bold'}),
            html.H4(deaths, style={'color': 'black', 'text-align': 'center'})
        ], style={'backgroundColor': 'yellow', 'height': '200px', 'width': '25%', 'float': 'left'})
    ], style={'width': '100%', 'height': '200px', 'borderBottom': '2px solid #ccc', 'paddingBottom': '10px'}),

    html.Div(style={'height': '20px'}),
    html.Div([
        html.Div([
            html.Div([
                html.Div([
                    dcc.Dropdown(id='picker', options=options, value='All'),
                    dcc.Graph(id='bar')
                ],className='card-body')
            ],className='col-md-12')
        ],className='row')
    ],className='container')
])


@app.callback(Output('bar', 'figure'), [Input('picker', 'value')])
def update_graph(type):

    if type == 'All':
        pbar = patients['detected_state'].value_counts().reset_index()
        return {'data': [go.Bar(x=pbar['detected_state'], y=pbar['count'])],
                'layout': go.Layout(title='State Total Count')}
    else:
        npat = patients[patients['current_status'] == type]
        pbar = npat['detected_state'].value_counts().reset_index()
        return {'data': [go.Bar(x=pbar['detected_state'], y=pbar['count'])],
                'layout': go.Layout(title='State Total Count')}


if __name__ == '__main__':
    app.run_server(debug=True, port=5000)
