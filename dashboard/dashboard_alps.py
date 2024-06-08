import dash
from dash import dcc, html, dash_table
import plotly.express as px
import pandas as pd
import geopandas as gpd
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

# Load data
flood_data = pd.read_csv('flood_data_fixed.csv', sep=',')
rain_data = pd.read_csv('rain_data_alps.csv', sep=',')
regions_data = pd.read_csv('regionswithcords.csv', sep=',')

# Load country boundaries using geopandas
countries = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

# Function to parse dates with multiple formats
def parse_dates(date_series, formats):
    for fmt in formats:
        try:
            parsed_dates = pd.to_datetime(date_series, format=fmt, errors='coerce', dayfirst=True)
            if parsed_dates.notna().all():
                return parsed_dates
        except (ValueError, TypeError):
            continue
    return pd.to_datetime(date_series, errors='coerce', dayfirst=True)  # Fallback to default parsing

# Parse 'Start date' and 'End date' columns in flood_data with multiple formats
flood_data['Start date'] = parse_dates(flood_data['Start date'], ['%d.%m.%Y', '%Y-%m-%d'])
flood_data['End date'] = parse_dates(flood_data['End date'], ['%d.%m.%Y', '%Y-%m-%d'])

# Parse 'DAY' column in rain_data with mixed formats
rain_data['DAY'] = parse_dates(rain_data['DAY'], ['%d.%m.%Y', '%Y-%m-%d', '%Y%m%d'])

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

app.layout = html.Div(
    style={'position': 'relative', 'height': '100vh', 'width': '100vw', 'overflow': 'hidden'},
    children=[
        html.Div(
            style={
                'position': 'absolute', 'top': '0', 'left': '0', 'width': '100%', 'height': '100%', 'z-index': '-1',
                'overflow': 'hidden', 'filter': 'grayscale(100%)'
            },
            children=[
                html.Iframe(
                    src="https://www.youtube.com/embed/oDK0FNisfDg?autoplay=1&loop=1&playlist=oDK0FNisfDg&controls=0&mute=1",
                    style={
                        'position': 'absolute', 'top': '0', 'left': '0', 'width': '100vw', 'height': '100vh', 'border': 'none',
                        'transform': 'scale(1.5)', 'transform-origin': 'center'
                    }
                )
            ]
        ),
        dbc.Container([
            dbc.Row([
                dbc.Col(html.H1("Klimakrise und Flutgefahr: Die Unterschätzte Bedrohung der Erderwärmung", className="text-center mt-3", style={'color': '#fef3c7'}), width=12),
                dbc.Col(html.H3("Klimadaten Challenge 2024", className="text-center text-muted", style={'color': '#fef3c7'}), width=12),
                dbc.Col(html.H4("Benjamin, Boran und Murat", className="text-center text-muted mb-4", style={'color': '#fef3c7'}), width=12)
            ]),
            dbc.Row([
                dbc.Col([
                    dcc.Dropdown(
                        id='country-dropdown',
                        options=[],
                        value=None,  # No default value
                        clearable=True,
                        placeholder="Select a country",
                        style={'background-color': '#fef3c7'}
                    ),
                ], width=6),
                dbc.Col([
                    dcc.Dropdown(
                        id='timeframe-dropdown',
                        options=[
                            {'label': 'Täglich', 'value': 'D'},
                            {'label': 'Wöchentlich', 'value': 'W'},
                            {'label': 'Monatlich', 'value': 'M'}
                        ],
                        value='D',  # Standardwert
                        clearable=False,
                        style={'background-color': '#fef3c7'}
                    ),
                ], width=6)
            ]),
            dbc.Row([
                dbc.Col(
                    dcc.Slider(
                        id='year-slider',
                        min=flood_data['Year'].min(),
                        max=flood_data['Year'].max(),
                        value=flood_data['Year'].max(),
                        marks={str(year): {'label': str(year), 'style': {'transform': 'rotate(45deg)', 'white-space': 'nowrap', 'color': '#fef3c7'}} for year in flood_data['Year'].unique()},
                        step=None
                    ),
                width=12),
            ]),
            dbc.Row([
                dbc.Col(dcc.Graph(id='precipitation-plot', style={'background-color': '#fef3c7', 'border-radius': '10px', 'padding': '10px', 'height': '60vh'}), width=12),
            ]),
            dbc.Row([
                dbc.Col(
                    html.Div(
                        dcc.Graph(id='cumulative-precipitation-plot', style={'background-color': '#fef3c7', 'border-radius': '10px', 'padding': '10px', 'height': '60vh', 'width': '800vw', 'display': 'inline-block'}),
                        style={'overflowX': 'scroll', 'width': '100%'}
                    ), width=12),
            ]),
            dbc.Row([
                dbc.Col(dcc.Graph(id='map-plot', style={'background-color': '#fef3c7', 'border-radius': '10px', 'padding': '10px', 'height': '60vh'}), width=12),
            ]),
            dbc.Row([
                dbc.Col([
                    html.H5("Überschwemmungen", style={'color': '#fef3c7'}),
                    dash_table.DataTable(
                        id='flood-table',
                        columns=[
                            {'name': 'Location', 'id': 'location'},
                            {'name': 'Start Date', 'id': 'Start date'},
                            {'name': 'End Date', 'id': 'End date'}
                        ],
                        style_table={'overflowX': 'auto', 'border': '1px solid black'},
                        style_cell={'textAlign': 'left', 'backgroundColor': '#fef3c7', 'color': 'black', 'border': '1px solid black'},
                        style_header={'backgroundColor': '#fef3c7', 'border': '1px solid black'},
                        style_data={'backgroundColor': '#fef3c7', 'border': '1px solid black'},
                        style_as_list_view=True
                    ),
                ], width=6),
                dbc.Col([
                    html.H5("Schäden und Verluste", style={'color': '#fef3c7'}),
                    dash_table.DataTable(
                        id='damage-table',
                        columns=[
                            {'name': 'Location', 'id': 'location'},
                            {'name': 'Fatalities', 'id': 'Fatalities', 'type': 'numeric'},
                            {'name': 'Losses (EUR, 2020)', 'id': 'Losses (EUR, 2020)', 'type': 'numeric'}
                        ],
                        style_table={'overflowX': 'auto', 'border': '1px solid black'},
                        style_cell={'textAlign': 'center', 'backgroundColor': '#fef3c7', 'color': 'black', 'border': '1px solid black'},
                        style_header={'backgroundColor': '#fef3c7', 'border': '1px solid black'},
                        style_data_conditional=[
                            {'if': {'column_id': 'Fatalities'}, 'textAlign': 'center'},
                            {'if': {'column_id': 'Losses (EUR, 2020)'}, 'textAlign': 'center'},
                            {'if': {'column_id': 'location'}, 'border-left': '1px solid black', 'border-right': '1px solid black'},
                            {'if': {'column_id': 'Fatalities'}, 'border-left': '1px solid black', 'border-right': '1px solid black'},
                            {'if': {'column_id': 'Losses (EUR, 2020)'}, 'border-left': '1px solid black', 'border-right': '1px solid black'}
                        ],
                        style_header_conditional=[
                            {'if': {'column_id': 'location'}, 'border-left': '1px solid black', 'border-right': '1px solid black'},
                            {'if': {'column_id': 'Fatalities'}, 'border-left': '1px solid black', 'border-right': '1px solid black'},
                            {'if': {'column_id': 'Losses (EUR, 2020)'}, 'border-left': '1px solid black', 'border-right': '1px solid black'}
                        ]
                    )
                ], width=6)
            ]),
            dbc.Row([
                dbc.Col(
                    html.Div(
                        [
                            html.H6("Sources:", style={'color': '#fef3c7'}),
                            html.A("Natural Hazards Europe", href="https://naturalhazards.eu/", target="_blank", style={'color': '#fef3c7'}),
                            html.Br(),
                            html.A("European Commission Authentication Service", href="https://ecas.ec.europa.eu/cas/login?loginRequestId=ECAS_LR-22393326-Lssax9p7FwCWzIt1zx7JwFBWmUqNZEJaTzzfKZNbKRV0rVaStudi9zdBPQsZ7Xkw58VlITEgaf8rpeXfGnUHvXZ-yntOf97TTHqxVxzLXeLDP6-Jb1Kl6AzMyAzXYuaIzmyg5uCkZSpbzezx2Big1GzIcQetJDGTrumP0hQcm7SdYfHO8ao5HDpjJDY6zsTrcbCXrN8", target="_blank", style={'color': '#fef3c7'})
                        ],
                        className="text-center mt-3"
                    )
                )
            ])
        ], fluid=True, style={'height': '90vh', 'overflowY': 'auto'})
    ]
)

@app.callback(
    Output('country-dropdown', 'options'),
    Input('year-slider', 'value')
)
def update_country_options(selected_year):
    filtered_data = flood_data[flood_data['Year'] == selected_year]
    countries = filtered_data['Country name'].unique()
    return [{'label': country, 'value': country} for country in countries]

@app.callback(
    Output('map-plot', 'figure'),
    Output('flood-table', 'data'),
    Output('damage-table', 'data'),
    Input('year-slider', 'value'),
    Input('country-dropdown', 'value')
)
def update_map(year, country):
    # Filter data only by the selected year
    filtered_data = flood_data[flood_data['Year'] == year]
    
    # Check if a country is selected and filter accordingly
    if country:
        filtered_data = filtered_data[filtered_data['Country name'] == country]
    
    # Define map center and zoom level based on the selected country
    country_centers = {
        'Switzerland': {'lat': 46.8182, 'lon': 8.2275},
        'Italy': {'lat': 41.8719, 'lon': 12.5674},
        'Germany': {'lat': 51.1657, 'lon': 10.4515},
        'Austria': {'lat': 47.5162, 'lon': 14.5501},
        'France': {'lat': 46.6034, 'lon': 1.8883},
        'Liechtenstein': {'lat': 47.166, 'lon': 9.5554},
        'Slovenia': {'lat': 46.1512, 'lon': 14.9955}
    }
    
    country_zoom_levels = {
        'Switzerland': 7,
        'Italy': 5,
        'Germany': 5,
        'Austria': 6,
        'France': 5,
        'Liechtenstein': 10,
        'Slovenia': 8
    }
    
    map_center = country_centers.get(country, {'lat': 50.1109, 'lon': 8.6821})
    zoom_level = country_zoom_levels.get(country, 3)
    
    # Replace NaN values in 'Losses (mln EUR, 2020)' with 0 for losses under 1 million EUR
    filtered_data['Losses (EUR, 2020)'] = filtered_data['Losses (mln EUR, 2020)'].fillna(0)
    
    # Determine marker size based on losses
    filtered_data['marker_size'] = filtered_data.apply(lambda row: max(10, row['Losses (EUR, 2020)'] / 10) if row['Losses (EUR, 2020)'] != 0 else 10, axis=1)

    # Plot data if available, otherwise show a message
    fig = px.scatter_mapbox(
        filtered_data, 
        lat="Latitude", 
        lon="Longitude", 
        hover_name="Name",  # Use the region name for hover info
        size='marker_size' if country else None,  # Adjust size only if a country is selected
        size_max=30,
        color_discrete_sequence=["black"], 
        zoom=zoom_level, 
        height=500
    )
    fig.update_traces(marker=dict(opacity=0.5 if country else 1.0))  # Adjust opacity only if a country is selected
    fig.update_traces(hovertemplate='<b>%{hovertext}</b>')
    fig.update_layout(mapbox_style="carto-positron")
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    fig.update_layout(mapbox=dict(center=map_center, zoom=zoom_level))
    
    # Prepare flood table data
    flood_table_data = filtered_data[['Name', 'Start date', 'End date']].copy()
    flood_table_data['Start date'] = flood_table_data['Start date'].dt.strftime('%d.%m.%Y')
    flood_table_data['End date'] = flood_table_data['End date'].dt.strftime('%d.%m.%Y')
    flood_table_data = flood_table_data.rename(columns={'Name': 'location', 'Start date': 'Start date', 'End date': 'End date'}).to_dict('records')
    
    # Prepare damage table data
    damage_data = filtered_data[['Name', 'Fatalities', 'Losses (EUR, 2020)']].copy()
    damage_data['Fatalities'] = damage_data['Fatalities'].fillna('None')
    damage_data['Losses (EUR, 2020)'] = damage_data['Losses (EUR, 2020)'].apply(lambda x: '{:,.0f}'.format(x).replace(',', "'") if isinstance(x, (int, float)) else x)
    damage_data['Name'] = damage_data['Name'].fillna('').astype(str)
    damage_grouped = damage_data.groupby(['Fatalities', 'Losses (EUR, 2020)']).agg({'Name': ', '.join}).reset_index()
    damage_grouped = damage_grouped.rename(columns={'Name': 'location'})
    damage_table_data = damage_grouped.to_dict('records')
    
    return fig, flood_table_data, damage_table_data

@app.callback(
    Output('precipitation-plot', 'figure'),
    Output('cumulative-precipitation-plot', 'figure'),
    Input('year-slider', 'value'),
    Input('timeframe-dropdown', 'value'),
    Input('country-dropdown', 'value')
)
def update_charts(year, timeframe, country):
    filtered_data = rain_data[rain_data['DAY'].dt.year == year]
    cumulative_data = rain_data[(rain_data['DAY'].dt.year >= 1979) & (rain_data['DAY'].dt.year <= year)]

    # Falls ein Land ausgewählt wurde, filtern Sie die Daten nach diesem Land
    if country:
        selected_country = countries[countries['name'] == country]
        gdf = gpd.GeoDataFrame(
            filtered_data, geometry=gpd.points_from_xy(filtered_data.LONGITUDE, filtered_data.LATITUDE))
        filtered_data = gpd.sjoin(gdf, selected_country, how="inner", op='within')
        filtered_data = pd.DataFrame(filtered_data.drop(columns=['geometry', 'index_right']))
        
        gdf_cumulative = gpd.GeoDataFrame(
            cumulative_data, geometry=gpd.points_from_xy(cumulative_data.LONGITUDE, cumulative_data.LATITUDE))
        cumulative_data = gpd.sjoin(gdf_cumulative, selected_country, how="inner", op='within')
        cumulative_data = pd.DataFrame(cumulative_data.drop(columns=['geometry', 'index_right']))

    # Berechnung von Mittelwerten für Niederschlag, gruppiert nach dem gewünschten Zeitrahmen
    if timeframe == 'D':
        filtered_data = filtered_data.groupby('DAY').mean(numeric_only=True).reset_index()
        cumulative_data = cumulative_data.groupby('DAY').mean(numeric_only=True).reset_index()
        y_label = 'Niederschlag (mm/Tag)'
    elif timeframe == 'W':
        filtered_data = filtered_data.resample('W', on='DAY').mean(numeric_only=True).reset_index()
        cumulative_data = cumulative_data.resample('W', on='DAY').mean(numeric_only=True).reset_index()
        y_label = 'Niederschlag (mm/Woche)'
    elif timeframe == 'M':
        filtered_data = filtered_data.resample('M', on='DAY').mean(numeric_only=True).reset_index()
        cumulative_data = cumulative_data.resample('M', on='DAY').mean(numeric_only=True).reset_index()
        y_label = 'Niederschlag (mm/Monat)'

    # Add a column to indicate if the date falls within any flood event
    if country:
        flood_periods = flood_data[(flood_data['Year'] == year) & (flood_data['Country name'] == country)][['Start date', 'End date']].dropna()
    else:
        flood_periods = flood_data[flood_data['Year'] == year][['Start date', 'End date']].dropna()

    filtered_data['In_Flood_Period'] = filtered_data['DAY'].apply(lambda day: any((day >= start) and (day <= end) for start, end in zip(flood_periods['Start date'], flood_periods['End date'])))
    cumulative_data['In_Flood_Period'] = cumulative_data['DAY'].apply(lambda day: any((day >= start) and (day <= end) for start, end in zip(flood_periods['Start date'], flood_periods['End date'])))

    # Map True/False to 'Überschwemmung'/'Niederschläge'
    filtered_data['In_Flood_Period'] = filtered_data['In_Flood_Period'].map({True: 'Überschwemmung', False: 'Niederschläge'})
    cumulative_data['In_Flood_Period'] = cumulative_data['In_Flood_Period'].map({True: 'Überschwemmung', False: 'Niederschläge'})

    # Precipitation bar plot for selected year
    precipitation_fig = px.bar(
        filtered_data, 
        x='DAY', 
        y='PRECIPITATION', 
        title=f'{timeframe}-Niederschlag', 
        labels={'PRECIPITATION': y_label},
        color='In_Flood_Period',
        color_discrete_map={'Überschwemmung': '#E69F00', 'Niederschläge': '#56B4E9'}
    )

    # Add moving average as a line
    precipitation_fig.add_trace({
        'x': filtered_data['DAY'],
        'y': filtered_data['PRECIPITATION'].rolling(window=5, min_periods=1).mean(),
        'mode': 'lines',
        'line': {'color': '#800080', 'width': 2},
        'name': 'Gleitender Durchschnitt (5 Tage)',
        'hovertemplate': 'Gleitender Durchschnitt: %{y:.2f} mm<extra></extra>'
    })

    precipitation_fig.update_layout(
        plot_bgcolor='#FFFFFF', 
        paper_bgcolor='#fef3c7',
        xaxis=dict(showgrid=True, gridcolor='grey'),
        yaxis=dict(showgrid=True, gridcolor='grey')
    )
    
    # Cumulative precipitation bar plot
    cumulative_precipitation_fig = px.bar(
        cumulative_data, 
        x='DAY', 
        y='PRECIPITATION', 
        title=f'Kumulativer Niederschlag (1979-{year})', 
        labels={'PRECIPITATION': y_label},
        color='In_Flood_Period',
        color_discrete_map={'Überschwemmung': '#E69F00', 'Niederschläge': '#56B4E9'}
    )

    # Add moving average as a line
    cumulative_precipitation_fig.add_trace({
        'x': cumulative_data['DAY'],
        'y': cumulative_data['PRECIPITATION'].rolling(window=5, min_periods=1).mean(),
        'mode': 'lines',
        'line': {'color': '#800080', 'width': 2},
        'name': 'Gleitender Durchschnitt (5 Tage)',
        'hovertemplate': 'Gleitender Durchschnitt: %{y:.2f} mm<extra></extra>'
    })

    cumulative_precipitation_fig.update_layout(
        plot_bgcolor='#FFFFFF', 
        paper_bgcolor='#fef3c7',
        xaxis=dict(showgrid=True, gridcolor='grey'),
        yaxis=dict(showgrid=True, gridcolor='grey')
    )

    return precipitation_fig, cumulative_precipitation_fig

if __name__ == '__main__':
    app.run_server(debug=True, port=8051)
