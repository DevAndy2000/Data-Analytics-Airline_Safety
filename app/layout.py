import dash_html_components as html
import dash_core_components as dcc
from data_loader import load_data
import dash_table
# Load data
data = load_data()

# Calculate statistical summary
summary = data.describe()

layout = html.Div([
    html.Div([
        html.Div([
            html.H1('Airline Safety Analytics Dashboard', style={'textAlign': 'center'}),
            html.Hr(),
        ]),

        html.Div([
            html.Div([
                html.Label('Select Year:'),
                dcc.Dropdown(
                    id='year-dropdown',
                    options=[
                        {'label': '1985-1999 Incidents', 'value': 'incidents_85_99'},
                        {'label': '1985-1999 Fatal Accidents', 'value': 'fatal_accidents_85_99'},
                        {'label': '1985-1999 Fatalities', 'value': 'fatalities_85_99'},
                        {'label': '2000-2014 Incidents', 'value': 'incidents_00_14'},
                        {'label': '2000-2014 Fatal Accidents', 'value': 'fatal_accidents_00_14'},
                        {'label': '2000-2014 Fatalities', 'value': 'fatalities_00_14'},
                    ],
                    value='fatalities_00_14',
                    multi=False,
                    placeholder='Select year range'
                ),
                html.Br(),
                html.Label('Select Airline(s):'),
                dcc.Dropdown(
                    id='airline-dropdown',
                    options=[{'label': airline, 'value': airline} for airline in data['airline'].unique()],
                    value=data['airline'].unique().tolist(),
                    multi=True,
                    placeholder='Select airline(s)'
                ),
            ], style={'width': '30%', 'display': 'inline-block', 'verticalAlign': 'top', 'padding': '10px'}),

            html.Div([
                dcc.Graph(id='airline-safety-graph'),
            ], style={'width': '65%', 'display': 'inline-block', 'padding': '0 20px'}),
        ]),

        html.Div([
            html.Div([
                html.Button("Export Data as CSV", id="export-button"),
                dcc.Download(id="download-data"),
            ], style={'padding': '20px 0'}),

            html.Div([
                html.H2('Airline Safety Data Table'),
                dash_table.DataTable(
                    id='data-table',
                    columns=[{"name": i, "id": i} for i in data.columns],
                    data=data.to_dict('records'),
                    page_size=10,
                    filter_action='native',
                    sort_action='native',
                    style_table={'overflowX': 'auto', 'marginTop': '20px'},
                    style_cell={'textAlign': 'left', 'padding': '5px', 'whiteSpace': 'normal'},
                    style_header={'backgroundColor': 'rgb(230, 230, 230)', 'fontWeight': 'bold'},
                    style_data_conditional=[{'if': {'row_index': 'odd'}, 'backgroundColor': 'rgb(248, 248, 248)'}],
                )
            ]),

            html.Div([
                html.H2('Statistical Summary'),
                html.P('Mean Incidents per Airline: {:.2f}'.format(summary.loc['mean', 'incidents_00_14'])),
                html.P('Median Incidents per Airline: {:.2f}'.format(summary.loc['50%', 'incidents_00_14'])),
                html.P('Standard Deviation of Incidents per Airline: {:.2f}'.format(summary.loc['std', 'incidents_00_14'])),
            ], style={'marginTop': '20px'}),

            html.Div([
                html.H2('Time Series Analysis'),
                dcc.Graph(id='time-series-graph'),
            ], style={'marginTop': '20px'}),
        ], style={'padding': '0 20px'}),
    ]),
])