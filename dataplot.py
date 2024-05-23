import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

# Daten laden
flood_data = pd.read_csv('CDK/flood_data.csv', sep=',')
rain_data = pd.read_csv('CDK/rain_data.csv', sep=',')
rain_data['DAY'] = pd.to_datetime(rain_data['DAY'], format='%d.%m.%Y')

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div([
    dbc.Container([
        dbc.Row([
            dbc.Col(html.H1("Dashboard", className="text-center mt-3", style={'color': 'white'}), width=12),
            dbc.Col(html.H3("Klimadaten Challenge 2024", className="text-center text-muted", style={'color': 'white'}), width=12),
            dbc.Col(html.H4("Benjamin, Boran und Murat", className="text-center text-muted mb-4", style={'color': 'white'}), width=12)
        ]),
        dbc.Row([
            dbc.Col([
                dcc.Graph(id='map-plot'),
                dcc.Slider(
                    id='year-slider',
                    min=flood_data['Year'].min(),
                    max=flood_data['Year'].max(),
                    value=flood_data['Year'].max(),
                    marks={str(year): str(year) for year in flood_data['Year'].unique()},
                    step=None
                )
            ], width=6, lg=6),  # Karte und Slider links
            dbc.Col([
                dbc.Row(
                    dbc.Col(
                        dcc.Dropdown(
                            id='country-dropdown',
                            options=[{'label': country, 'value': country} for country in flood_data['Country name'].unique()],
                            value='Germany',  # Standardwert
                            clearable=False
                        ),
                        width=12
                    ),
                ),
                dbc.Row(
                    dbc.Col(dcc.Graph(id='precipitation-plot'), width=12),
                ),
                dbc.Row(
                    dbc.Col(dcc.Graph(id='temperature-plot'), width=12),
                )
            ], width=6, lg=6)  # Grafen rechts
        ])
    ], fluid=True)
])

@app.callback(
    Output('map-plot', 'figure'),
    Input('country-dropdown', 'value'),
    Input('year-slider', 'value')
)
def update_map(country, year):
    filtered_data = flood_data[(flood_data['Country name'] == country) & (flood_data['Year'] == year)]
    fig = px.scatter_mapbox(filtered_data, lat="Latitude", lon="Longitude", hover_name="ID",
                            color_discrete_sequence=["fuchsia"], zoom=3, height=500)
    fig.update_traces(marker=dict(size=15, symbol='marker'))
    fig.update_layout(mapbox_style="carto-darkmatter")
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    return fig

@app.callback(
    Output('precipitation-plot', 'figure'),
    Output('temperature-plot', 'figure'),
    Input('year-slider', 'value')
)
def update_charts(year):
    filtered_data = rain_data[rain_data['DAY'].dt.year == year]
    precipitation_fig = px.line(filtered_data, x='DAY', y='PRECIPITATION', title='Niederschlag', color_discrete_sequence=['#00ccff'])
    temperature_fig = px.line(filtered_data, x='DAY', y='TEMPERATURE_AVG', title='Durchschnittstemperatur', color_discrete_sequence=['#ff3300'])
    return precipitation_fig, temperature_fig

if __name__ == '__main__':
    app.run_server(debug=True)