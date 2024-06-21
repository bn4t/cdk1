import pandas as pd
import csv

rain_data_1 = pd.read_csv(r'C:\Users\Murat Kayhan\OneDrive - FHNW\Documents\FHNW\ckd\Data\rain_data_1.csv', sep =';')
rain_data_2 = pd.read_csv(r'C:\Users\Murat Kayhan\OneDrive - FHNW\Documents\FHNW\ckd\Data\rain_data_2.csv', sep=';')
rain_data_3 = pd.read_csv(r'C:\Users\Murat Kayhan\OneDrive - FHNW\Documents\FHNW\ckd\Data\rain_data_3.csv', sep=';')
rain_data_4 = pd.read_csv(r'C:\Users\Murat Kayhan\OneDrive - FHNW\Documents\FHNW\ckd\Data\rain_data_4.csv', sep=';')
rain_data_ch = pd.read_csv(r'C:\Users\Murat Kayhan\OneDrive - FHNW\Documents\FHNW\ckd\Data\rain_data_4.csv', sep=';')

rain_data_1['DAY'] = pd.to_datetime(rain_data_1['DAY'], format='%Y%m%d').dt.strftime('%d.%m.%Y')
rain_data_2['DAY'] = pd.to_datetime(rain_data_2['DAY'], format='%Y%m%d').dt.strftime('%d.%m.%Y')
rain_data_3['DAY'] = pd.to_datetime(rain_data_3['DAY'], format='%Y%m%d').dt.strftime('%d.%m.%Y')
rain_data_4['DAY'] = pd.to_datetime(rain_data_4['DAY'], format='%Y%m%d').dt.strftime('%d.%m.%Y')
rain_data_ch['DAY'] = pd.to_datetime(rain_data_4['DAY'], format='%Y%m%d').dt.strftime('%d.%m.%Y')

# Zusammenführen der DataFrames
rain_data = pd.concat([rain_data_1, rain_data_2, rain_data_3, rain_data_4, rain_data_ch])

# Reset des Index, um doppelte Indizes zu vermeiden
rain_data.reset_index(drop=True, inplace=True)

print(rain_data.head)


output_csv_path = r'C:/Users/Murat Kayhan/OneDrive - FHNW/Documents/FHNW/ckd/Data/rain_data_total.csv'



# CSV-Datei speichern
rain_data.to_csv(output_csv_path, index=False)