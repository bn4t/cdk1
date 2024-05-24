import dash
from dash import dcc, html, dash_table
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import plotly.graph_objects as go

# Load data
flood_data = pd.read_csv('./flood_data.csv', sep=',')
rain_data = pd.read_csv('./rain_data.csv', sep=',')
regions_data = pd.read_csv('./regions_ch.csv', sep=',')

# Print column names to verify them
print("Flood Data Columns:", flood_data.columns)
print("Rain Data Columns:", rain_data.columns)
print("Regions Data Columns:", regions_data.columns)

# Display the first few rows of the flood_data
print(flood_data.head())

# Convert 'DAY' column to datetime
rain_data['DAY'] = pd.to_datetime(rain_data['DAY'], format='%d.%m.%Y')

# Extract Latitude and Longitude from the 'regions' column in flood_data
flood_data[['Latitude', 'Longitude']] = flood_data['regions'].str.strip('[]()').str.split(',', expand=True)
flood_data['Latitude'] = flood_data['Latitude'].astype(float)
flood_data['Longitude'] = flood_data['Longitude'].astype(float)

# Extract Latitude and Longitude from the 'Coordinates' column in regions_data
regions_data[['Latitude', 'Longitude']] = regions_data['Coordinates'].str.strip('[]()').str.split(',', expand=True)
regions_data['Latitude'] = regions_data['Latitude'].astype(float)
regions_data['Longitude'] = regions_data['Longitude'].astype(float)

# Merge flood_data with regions_data based on Latitude and Longitude
flood_data = pd.merge(flood_data, regions_data, on=['Latitude', 'Longitude'], how='left', suffixes=('', '_region'))

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
                html.Br(),  # Add a line break for spacing
                dcc.Slider(
                    id='year-slider',
                    min=flood_data['Year'].min(),
                    max=flood_data['Year'].max(),
                    value=flood_data['Year'].max(),
                    marks={str(year): {'label': str(year), 'style': {'transform': 'rotate(45deg)', 'white-space': 'nowrap'}} for year in flood_data['Year'].unique()},
                    step=None
                ),
                html.Br(),  # Add another line break for more spacing
                dash_table.DataTable(
                    id='flood-table',
                    columns=[
                        {'name': 'Location', 'id': 'location'},
                        {'name': 'Start Date', 'id': 'Start date'},
                        {'name': 'End Date', 'id': 'End date'},
                        {'name': 'Precipitation (mm)', 'id': 'precipitation'}
                    ],
                    style_table={'overflowX': 'auto'},
                    style_cell={'textAlign': 'left'}
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
                ),
                dbc.Row(
                    dbc.Col(dcc.Graph(id='boxplot-plot'), width=12),
                )
            ], width=6, lg=6)  # Grafen rechts
        ])
    ], fluid=True)
])

@app.callback(
    Output('map-plot', 'figure'),
    Output('flood-table', 'data'),
    Input('year-slider', 'value')
)
def update_map(year):
    # Filter data only by the selected year
    filtered_data = flood_data[flood_data['Year'] == year]
    
    # Check if there is data to plot
    if (filtered_data.empty) or ('Name' not in filtered_data.columns):
        fig = go.Figure()
        fig.update_layout(mapbox_style="carto-darkmatter")
        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
        fig.add_annotation(
            x=0.5, y=0.5, text="No data available for this selection",
            showarrow=False, font=dict(size=20, color="white"),
            xref="paper", yref="paper"
        )
        table_data = []
    else:
        # Plot data if available
        fig = px.scatter_mapbox(
            filtered_data, 
            lat="Latitude", 
            lon="Longitude", 
            hover_name="Name",  # Use the region name for hover info
            color_discrete_sequence=["fuchsia"], 
            zoom=3, 
            height=500
        )
        # Remove latitude and longitude from hover data
        fig.update_traces(hovertemplate='<b>%{hovertext}</b>')
        fig.update_layout(mapbox_style="carto-positron")
        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
        
        # Prepare table data
        table_data = filtered_data[['Name', 'Start date', 'End date']].copy()  # Adjusted column names
        table_data['precipitation'] = table_data.apply(lambda row: rain_data[(rain_data['DAY'] >= row['Start date']) & (rain_data['DAY'] <= row['End date'])]['PRECIPITATION'].sum(), axis=1)
        table_data = table_data.rename(columns={'Name': 'location', 'Start date': 'Start date', 'End date': 'End date', 'precipitation': 'precipitation'}).to_dict('records')
    
    return fig, table_data

@app.callback(
    Output('precipitation-plot', 'figure'),
    Output('temperature-plot', 'figure'),
    Output('boxplot-plot', 'figure'),
    Input('year-slider', 'value')
)
def update_charts(year):
    filtered_data = rain_data[rain_data['DAY'].dt.year == year]
    
    # Ensure only one data point per day
    filtered_data = filtered_data.groupby('DAY').mean().reset_index()
    
    precipitation_fig = px.histogram(filtered_data, x='DAY', y='PRECIPITATION', title='Niederschlag', color_discrete_sequence=['#00ccff'])
    temperature_fig = px.line(filtered_data, x='DAY', y='TEMPERATURE_AVG', title='Durchschnittstemperatur', color_discrete_sequence=['#ff3300'])
    boxplot_fig = px.box(filtered_data, y='PRECIPITATION', title='Precipitation Boxplot', color_discrete_sequence=['#00ccff'])
    
    return precipitation_fig, temperature_fig, boxplot_fig

if __name__ == '__main__':
    app.run_server(debug=True)
