import asyncio
import aiohttp
import json
from typing import List
from fastapi import Depends
import numpy as np
from entities.city import City
from entities.note import Note
from entities.rent import Rent
from repositories.city import RentRepository

class RentService:
    def __init__(self, rent_repository: RentRepository = Depends(RentRepository)):
        self.rent_repository: RentRepository = rent_repository
        self.base_url = "https://geo.api.gouv.fr/communes/"
        self.headers = {"Content-Type": "application/json"}
    
    
    #get every city note in a departement
    async def get_city_note(self, *city_names: List[str]) -> List[Note]:
        try:
            notes = await self.rent_repository.get_city_note(city_names)
            note_dict = {note["Villes"]: note["Notes"] for note in notes}
            note_data = [Note(city, note_dict.get(city, 0.0)) for city in city_names]
            return note_data
        except Exception as e:
            print(e)
                
    #get average city average rent in a departement
    async def get_avg_rent_by_dep(self, renting_data) -> list:

        dep=renting_data['dep']
        data = await self.rent_repository.get_cities_by_dep(dep)
        
        for i in range(len(data)):
            data = [d for d in data if float(data[i]["loypredm2"]) * float(renting_data['area']) <= int(renting_data['price'])]
        
        result_list: list = []
        
        for n in range(len(data)):
           result_list.append(Rent(data[n]["id_zone"], data[n]["INSEE"], data[n]["LIBGEO"], data[n]["DEP"], data[n]["loypredm2"]))
        return result_list

    #get every city info in a departement
    async def get_city_info_by_insee(self, *insee: List[str]) -> List[str]:
        async with aiohttp.ClientSession(headers=self.headers) as session:
            tasks = [session.get(self.base_url + insee_item) for insee_item in insee]
            responses = await asyncio.gather(*tasks)
            return [await r.text() for r in responses]

    async def search_rent(self, renting_data: dict) -> list:
        cities = await self.get_avg_rent_by_dep(renting_data)
        city_names = [city.ville for city in cities]
        insee_codes = [city.insee for city in cities]
        
        # Execute get_city_note() and get_city_info_by_insee() with asyncio
        notes, infos = await asyncio.gather(self.get_city_note(*city_names),self.get_city_info_by_insee(*insee_codes))      

        infos = list(map(lambda x: x.replace('Not Found', '{"nom":"NaN","code":"NaN","codeDepartement":"NaN","siren":"NaN","codeEpci":"NaN","codeRegion":"NaN","codesPostaux":["NaN"],"population":0}'), infos))
        # convert infos to a list of dictionaries
        infos = json.loads(json.dumps([json.loads(JSON_STRING) for JSON_STRING in infos]))

        # Extract relevant information from infos
        codes_postaux = [info["codesPostaux"][0] for info in infos]
        population = [info["population"] for info in infos]

        # Create a new list of City objects
        city_list = [
            City(city.avg_rent, note.rate, city.ville, code_postal, pop)
            for city, note, code_postal, pop in zip(cities, notes, codes_postaux, population)
        ]

        return city_list


    def save_rent_to_database():

        df = pd.read_csv("average_rent.csv", encoding = 'latin-1',delimiter=";", decimal=",")
        result = df.to_json(orient = 'records')
        parsed = json.loads(result)
        print(rent_model)
        #rs=json.dumps(parsed, indent=4) 
        result2= []
        for row in parsed:
            
            if int(row['DEP'])==int(rent_model['departement']) and float(row['upr.IPm2']*rent_model['space'])<=rent_model['amount']:
                result2.append(row)
                
        for row in parsed:
            keys =  self.get_keys(row)   
            values = self.get_values(row)

            print(f"INSERT INTO infos_rent ({keys}) VALUES ({values})")
            query_put(
                        """
                        INSERT INTO infos_rent (
                                                    id_zone, 
                                                    INSEE, 
                                                    LIBGEO,
                                                    DEP, 
                                                    REG, 
                                                    TYPPRED,
                                                    loypredm2,
                                                    lwr_IPm2,
                                                    upr_IPm2,
                                                    R2adj,
                                                    NBobs_maille,
                                                    NBobs_commune
                                                )
                        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                        """,
                        (
                            row['id_zone'], 
                            row['INSEE'], 
                            row['LIBGEO'],
                            row['DEP'], 
                            row['REG'], 
                            row['TYPPRED'],
                            row['loypredm2'],
                            row['lwr.IPm2'],
                            row['upr.IPm2'],
                            row['R2adj'],
                            row['NBobs_maille'],
                            row['NBobs_commune']
                        )
                    )
            print(query_put)
        print(result2)
        return result2

    def get_keys(self,data_json):
        rs = list()
        for key in data_json.keys():
            #print(key)
            rs.append(key)

        for char in rs:
            rs=str(rs).replace("'","").replace("[","").replace("]","").replace("\"","").replace(".","_")
        return rs

    def get_values(self,data_json):
        rs = list()
        for value in data_json.values():
            #print(value)
            rs.append(value)

        for char in rs:
            rs=str(rs).replace("'","").replace("[","").replace("]","").replace("\"","")
        return rs