import dash
from dash import dcc, html
import plotly.express as px
import pandas as pd

# Initialize the Dash app
app = dash.Dash(__name__)

global_mean_temp_df = pd.read_csv('../data/source/global_mean_temp.csv', sep=',')

agri4cast_df = pd.read_csv('../data/source/df_ch.csv', sep=';', parse_dates=['DAY'], date_format='%Y%m%d')

# resample the agri4cast data to monthly and yearly data
agri4cast_monthly_df = agri4cast_df.resample('ME', on='DAY').sum().reset_index()
agri4cast_yearly_df = agri4cast_df.resample('YE', on='DAY').sum().reset_index().assign(YEAR=lambda x: x['DAY'].dt.year)

# merge the yearly agri4cast data with the global mean temperature data
agri4cast_yearly_global_mean_temp_df = pd.merge(agri4cast_yearly_df, global_mean_temp_df, left_on='YEAR',
                                                right_on='YEAR')

# calculate the yearly delta for the precipitation data
agri4cast_yearly_global_mean_temp_df['PRECIPITATION_DELTA'] = agri4cast_yearly_global_mean_temp_df.PRECIPITATION.diff()

# calculate rolling averages for the precipitation data over different timeframes
agri4cast_monthly_df['precipitation_moving_avg_48_months'] = agri4cast_monthly_df['PRECIPITATION'].rolling(48).mean()
agri4cast_monthly_df['precipitation_moving_avg_36_months'] = agri4cast_monthly_df['PRECIPITATION'].rolling(36).mean()
agri4cast_monthly_df['precipitation_moving_avg_24_months'] = agri4cast_monthly_df['PRECIPITATION'].rolling(24).mean()
agri4cast_monthly_df['precipitation_moving_avg_12_months'] = agri4cast_monthly_df['PRECIPITATION'].rolling(12).mean()
agri4cast_monthly_df['precipitation_moving_avg_6_months'] = agri4cast_monthly_df['PRECIPITATION'].rolling(6).mean()

# get the precipitation data for August 2005 for whole switzerland
agri4cast_disaster_switzerland_df = agri4cast_df.loc[
    (agri4cast_df['DAY'] >= '2005-08-01') & (agri4cast_df['DAY'] <= '2005-08-31')]
agri4cast_disaster_switzerland_df = agri4cast_disaster_switzerland_df.groupby('DAY').sum().reset_index()

agri4cast_disaster_individual_df = agri4cast_df.loc[
    (agri4cast_df['DAY'] >= '2005-08-01') & (agri4cast_df['DAY'] <= '2005-08-31')]
agri4cast_disaster_individual_df = agri4cast_disaster_individual_df.groupby(['DAY', 'GRID_NO']).sum().reset_index()

# bar chart for the precipitation data in August 2005
precipitation_august_2005_bar_chart = px.line(
    agri4cast_disaster_individual_df,
    x='DAY',
    y='PRECIPITATION',
    color='GRID_NO',
    title='Niederschlagsdaten August 2005 (ganze Schweiz)',
    labels={'DAY': 'Datum', 'PRECIPITATION': 'Niederschlag (mm)'}
)

# add the sum of the precipitation data for whole switzerland
precipitation_august_2005_bar_chart.add_scatter(
    x=agri4cast_disaster_switzerland_df['DAY'],
    y=agri4cast_disaster_switzerland_df['PRECIPITATION'],
    mode='lines',
    name='Whole Switzerland'
)

# scatter plot of precipitation data and global mean temperature
precipitation_global_mean_temp_scatter_chart = px.scatter(
    agri4cast_yearly_global_mean_temp_df,
    x='No_Smoothing',
    y='PRECIPITATION',
    title='Scatterplot Niederschlagsdaten und Klimadaten',
    color='YEAR',
    trendline='ols',
    labels={'No_Smoothing': 'Global Mean Temperature', 'PRECIPITATION': 'Jährlicher Regenfall (mm)'}
)

precipitation_moving_avg_chart = px.line(
    agri4cast_monthly_df,
    x='DAY',
    y=[
        'PRECIPITATION',
        'precipitation_moving_avg_48_months',
        'precipitation_moving_avg_36_months',
        'precipitation_moving_avg_24_months',
        'precipitation_moving_avg_12_months',
        'precipitation_moving_avg_6_months',
    ],
    title='Niederschlagsdaten',
)

# Define the layout of the app
app.layout = html.Div(children=[
    # Adding Tailwind CSS from CDN
    html.Link(rel='stylesheet', href='https://cdnjs.cloudflare.com/ajax/libs/tailwindcss/2.2.19/tailwind.min.css'),

    html.Div(children=[
        html.H1(children='Die Flutkatastrophe von 2005 – Ursachen, Auswirkungen und der Einfluss des Klimawandels',
                className='text-4xl font-bold text-center my-8'),

        html.H2(children='Einleitung', className='text-2xl font-semibold my-4'),
        html.Div(children=[
            html.P(children='''
            Im August 2005 ereignete sich in der Schweiz eine der schwersten Hochwasserkatastrophen der letzten Jahrhunderte. 
            Zwischen dem 21. und 23. August brachten schwere Regenfälle weite Teile des Alpennordhangs von Waadt bis Graubünden zum Überlaufen. 
            Dieser Bericht untersucht die Ursachen, Auswirkungen und den Einfluss des Klimawandels auf die Flutkatastrophe von 2005.
        ''', className='text-lg'),
            html.Img(src=dash.get_asset_url('meteo.png'), alt='Meteorologische Lage', className='w-5/6'),
        ], className='flex justify-between items-start mx-auto my-9'),

        html.H2(children='Die Ereignisse im August 2005', className='text-2xl font-semibold my-4'),
        html.P(children='''
            Vom 19. bis 23. August 2005 kam es zu intensiven und langanhaltenden Niederschlägen, die zu schweren Überschwemmungen und Erdrutschen führten.
            Ein Tiefdruckgebiet verlagerte sich vom Golf von Genua über die Alpen, was zu einem Stau feuchtwarmer Luftmassen führte. 
            Diese Luftmassen trafen auf kühlere Luft aus dem Norden, was heftige Regenfälle auslöste. 
            Die Regenmenge erreichte örtlich über 300 mm innerhalb von zwei Tagen, und 
            in einigen Regionen fielen diese Mengen sogar innerhalb von 24 Stunden.
        ''', className='text-lg mb-4'),

        # TODO: map grid_no to cantons -> will be done by boran
        dcc.Graph(figure=precipitation_august_2005_bar_chart, className='my-8'),

        html.H2(children='Auswirkungen der Flut', className='text-2xl font-semibold my-4'),
        html.P(children='''            
            Die Hochwasserereignisse führten zu massiven Schäden in mehreren Bereichen:
            ''', className='text-lg mb-4'),
        html.Ol(children=[
            html.Li(
                children='Menschenleben und Infrastruktur: Sechs Menschen verloren ihr Leben, und die Gesamtschadenssumme belief sich auf etwa 2,5 Milliarden Franken. Besonders stark betroffen waren die Kantone Bern, Luzern und Obwalden, wo Infrastrukturschäden von über 500 Millionen Franken entstanden.'),
            html.Li(
                children='TODO: graph von seepegelständen? Wasserstände der Seen: Mehrere Seen, darunter der Brienzersee und der Sarnersee, erreichten die höchsten je gemessenen Wasserstände, was zu umfangreichen Überschwemmungen führte.'),
            html.Li(
                children='Dynamische Schäden: Überschwemmungen, Erosionen und Murgänge verursachten schwere Schäden an Gebäuden und Straßen. Besonders betroffen waren Gebiete entlang der Aare, Reuss und Emme, wo Abflussmengen weit über den bisherigen Höchstwerten gemessen wurden.')
        ], className='text-lg mb-4 list-disc'),

        html.Div(children=[
            html.Img(src=dash.get_asset_url('flood-1.webp'), alt='Flood 1', className='my-8'),
            html.Img(src=dash.get_asset_url('flood-2.webp'), alt='Flood 2', className='my-8'),
        ], className='grid grid-cols-2 gap-4'),

        html.H2(children='Der Einfluss des Klimawandels', className='text-2xl font-semibold my-4'),
        html.P(children='''
            Während kein direkter Einfluss des Klimawandels auf das Hochwasserereignis von 2005 nachgewiesen werden kann mit den verfügbaren Daten,
            ist es klar herauszulesen, dass es mit geringeren Mengen an Regenfällen nicht zu dem Ereignis gekommen wäre.
            
            Da die globale Durchschnittstemperatur und die jährlich gemesse Niederschlagsmenge in der Schweiz stark korrelieren,
            ist es wahrscheinlich, dass der Klimawandel die Häufigkeit und Intensität von Extremwetterereignissen wie Hochwasser in der Schweiz erhöhen kann.
        ''', className='text-lg mb-4'),

        dcc.Graph(figure=precipitation_global_mean_temp_scatter_chart, className='my-8'),
        dcc.Graph(figure=precipitation_moving_avg_chart, className='my-8'),

        html.H2(children='Fazit', className='text-2xl font-semibold my-4'),
        html.P(children='''
            Die Flutkatastrophe von 2005 war ein Weckruf für die Schweiz. 
            Sie zeigte die zerstörerische Kraft von Naturereignissen und die Bedeutung effektiver Präventionsstrategien. 
            Mit Blick auf den Klimawandel müssen diese Massnahmen kontinuierlich weiterentwickelt werden, um zukünftigen Herausforderungen gewachsen zu sein, 
            speziell im Bezug auf die steigenden globalen Temperaturen und die damit einhergehende steigende Niederschlagsmenge.
        ''', className='text-lg mb-4')
    ], className='container mx-auto px-4')
])

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
