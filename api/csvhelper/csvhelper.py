import json
from pathlib import Path
from typing import Any, Dict, List
import pandas as pd
import chardet


class CsvFileHandler:
    def __init__(self):
        pass

    def get_rent_indicator(self, departement: str) -> List[Dict[str, Any]]: 
        with open("indicateurs-loyers-appartements.csv", encoding="ISO-8859-1") as file:
            data = pd.read_csv(file, sep=";", decimal=",")
        
        data = data[data['DEP'] == departement]
        return json.loads(self.df_to_json(data))

    def get_city_rate(self, ville: List[str]) -> List[Dict[str, Any]]: 
        #Data frame from csv
        with open("cities_rate.csv") as file:
            data = pd.read_csv(file, sep=",", decimal=",")
            data = data[data['Villes'].isin(ville)]
            return json.loads(self.df_to_json(data))

    #convert dataframe to json in format records
    def df_to_json(self,df):
        return df.to_json(orient="records")

    #Detect encoding of a file
    def detect_encoding(self,file_path):
        with open(file_path, 'rb') as f:
            rawdata = f.read()
        return chardet.detect(rawdata)['encoding']