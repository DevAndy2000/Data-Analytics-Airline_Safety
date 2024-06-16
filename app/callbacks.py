from dash.dependencies import Input, Output
from layout import data
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px

def register_callbacks(app):
    @app.callback(
        [Output('airline-safety-graph', 'figure'),
         Output('data-table', 'data'),
         Output('time-series-graph', 'figure')],
        [Input('year-dropdown', 'value'),
         Input('airline-dropdown', 'value')]
    )
    def update_graph_table_and_time_series(selected_year, selected_airlines):
        if not selected_airlines:
            return {}, [], {}

        filtered_data = data[data['airline'].isin(selected_airlines)]

        # Update the bar graph
        bar_fig = px.bar(filtered_data, x='airline', y=selected_year,
                         title=f'{selected_year.replace("_", " ").capitalize()} by Airline',
                         hover_data={'airline': True, selected_year: True})
        bar_fig.update_layout(xaxis={'categoryorder': 'total descending'})

        # Update the table
        table_data = filtered_data.to_dict('records')

        # Dummy time series analysis
        # Replace this with your actual time series analysis function
        trend = filtered_data[selected_year].rolling(window=3).mean()
        seasonal = filtered_data[selected_year].rolling(window=12).mean()
        residual = filtered_data[selected_year] - trend - seasonal

        # Plot time series graph
        time_series_fig = make_subplots(rows=3, cols=1, shared_xaxes=True, subplot_titles=('Trend', 'Seasonal', 'Residual'))
        time_series_fig.add_trace(go.Scatter(x=filtered_data['airline'], y=trend, mode='lines', name='Trend'), row=1, col=1)
        time_series_fig.add_trace(go.Scatter(x=filtered_data['airline'], y=seasonal, mode='lines', name='Seasonal'), row=2,
                                  col=1)
        time_series_fig.add_trace(go.Scatter(x=filtered_data['airline'], y=residual, mode='lines', name='Residual'), row=3,
                                  col=1)

        time_series_fig.update_layout(height=600, title_text="Time Series Analysis", showlegend=False)
        time_series_fig.update_xaxes(title_text="Airline")
        time_series_fig.update_yaxes(title_text="Value", row=1, col=1)
        time_series_fig.update_yaxes(title_text="Value", row=2, col=1)
        time_series_fig.update_yaxes(title_text="Value", row=3, col=1)

        return bar_fig, table_data, time_series_fig

    @app.callback(
        Output("download-data", "data"),
        [Input("export-button", "n_clicks")],
        [Input('year-dropdown', 'value'),
         Input('airline-dropdown', 'value')]
    )
    def export_data_to_csv(n_clicks, selected_year, selected_airlines):
        if not n_clicks:
            return None

        filtered_data = data[data['airline'].isin(selected_airlines)]
        csv_string = filtered_data.to_csv(index=False, encoding='utf-8-sig')

        return dict(content=csv_string, filename="airline_safety_data.csv")