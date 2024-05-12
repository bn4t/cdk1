from dash import Dash, html, dcc, callback, Output, Input, dash_table
import plotly.express as px
import pandas as pd
from datetime import datetime

global_mean_temp = pd.read_csv('../data/source/global_mean_temp.csv', sep=',')
agri4cast = pd.read_csv('../data/source/df_ch.csv', sep=';', parse_dates=['DAY'], date_format='%Y%m%d')
agri4cast_resampled = agri4cast.resample('ME', on='DAY').sum().reset_index()
agri4cast_yearly = agri4cast.resample('YE', on='DAY').sum().reset_index().assign(YEAR=lambda x: x['DAY'].dt.year)

# calculate delta for the precipitation data
agri4cast_yearly_global_temp = pd.merge(agri4cast_yearly, global_mean_temp, left_on='YEAR', right_on='YEAR')


agri4cast_yearly_global_temp['PRECIPITATION_DELTA'] = agri4cast_yearly_global_temp.PRECIPITATION.diff()

# calculate the correlation between the global mean temperature and the precipitation
# TODO: visualize this
agri4cast_yearly_global_temp['CORR_PRECIPITATION_MEAN_TEMP'] = agri4cast_yearly_global_temp['PRECIPITATION'].corr(agri4cast_yearly_global_temp['No_Smoothing'])

# calculate the sliding window average
agri4cast_resampled['precipitation_moving_avg_48_months'] = agri4cast_resampled['PRECIPITATION'].rolling(48).mean()
agri4cast_resampled['precipitation_moving_avg_36_months'] = agri4cast_resampled['PRECIPITATION'].rolling(36).mean()
agri4cast_resampled['precipitation_moving_avg_24_months'] = agri4cast_resampled['PRECIPITATION'].rolling(24).mean()
agri4cast_resampled['precipitation_moving_avg_12_months'] = agri4cast_resampled['PRECIPITATION'].rolling(12).mean()
agri4cast_resampled['precipitation_moving_avg_6_months'] = agri4cast_resampled['PRECIPITATION'].rolling(6).mean()

app = Dash(__name__)

app.layout = html.Div([
    html.H1(children='Klimawandel und Fluten in der Schweiz', style={'textAlign': 'center'}),
    html.H2(children='Einführung', style={'textAlign': 'center'}),
    html.P(children='Lässt sich ein Zusammenhang finden zwischen Klimawandel und Fluten in der Schweiz?'),

    dcc.Graph(figure=px.line(global_mean_temp, x='YEAR', y='No_Smoothing', title='Global Mean Temperature')),

    html.P(children='Observation Chart', style={'textAlign': 'center'}),

    dcc.Graph(figure=px.line(agri4cast_resampled, x='DAY', y=[
        'PRECIPITATION',
        'precipitation_moving_avg_48_months',
        'precipitation_moving_avg_36_months',
        'precipitation_moving_avg_24_months',
        'precipitation_moving_avg_12_months',
        'precipitation_moving_avg_6_months'], title='Niederschlagsdaten')),
    html.P(children='Erklärung Chart + button to move through the different averages starting with the raw data visualizing how it becomes only obvious when having a larger rolling average', style={'textAlign': 'center'}),


    dcc.Graph(figure=px.line(agri4cast_yearly_global_temp, x='YEAR', y=['PRECIPITATION', 'No_Smoothing'], title='Niederschlagsdaten und Klimadaten', log_y=True)),
    # scatterplot with the same data
    dcc.Graph(figure=px.scatter(agri4cast_yearly_global_temp, x='No_Smoothing', y='PRECIPITATION', title='Scatterplot Niederschlagsdaten und Klimadaten', color='YEAR')),

    # Einführung
    # - chart mit global mean temp
    # Fragestellung: Lässt sich ein Zusammenhang finden zwischen Klimawandel und Fluten in der Schweiz?

    # 1. Daten
    # - Chart mit Niederschlagsdaten und Klimadaten + map with grid_no selection
    # Erklärung Chart
    #
    # - mit Flutdaten + Niederchlagsdaten + Klimadaten + map with grid_no selection
    # Erklärung Chart

    # 2. Analyse
    # Observations
    # Explanation for results

    dcc.Dropdown(agri4cast_resampled.GRID_NO.unique(), '0', id='dropdown-selection'),
    dcc.Graph(id='graph-content')
])


@callback(
    Output('graph-content', 'figure'),
    Input('dropdown-selection', 'value')
)
def update_graph(value):
    dff = agri4cast[agri4cast_resampled.GRID_NO == value]
    return px.line(dff, x='DAY', y='PRECIPITATION')


if __name__ == '__main__':
    app.run(debug=True)
