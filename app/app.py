import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import dash_table
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from layout import layout
from callbacks import register_callbacks

app = dash.Dash(__name__)
app.title = 'Airline Safety Analytics Dashboard'
app.layout = layout

register_callbacks(app)

if __name__ == '__main__':
    app.run_server(debug=True)