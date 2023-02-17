import asyncio
from typing import List
from fastapi import Depends
from csvhelper.csvhelper import CsvFileHandler


class RentRepository:
    def __init__(self, csv_file_handler : CsvFileHandler = Depends(CsvFileHandler)):
        self.csv_file_handler: CsvFileHandler = csv_file_handler
        

    async def get_cities_by_dep(self, departement: int):
        cities = self.csv_file_handler.get_rent_indicator(str(departement))
        return cities

    async def get_city_note(self, city_names: List[str]) -> list:
        note = self.csv_file_handler.get_city_rate(city_names)
        return note


    
