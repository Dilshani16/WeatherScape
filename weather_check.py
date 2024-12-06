from threading import Thread
from multiprocessing import Process

import json
import time
import requests 

class weatherCheck(Process):

    def __init__(self, api_key, lat, lon, queries ,delay =5):
        super(weatherCheck, self).__init__()
        self.api_key = api_key
        self.lat = lat
        self.lon = lon
        self.queries = queries
        self.delay = delay
       


    def run(self):
        
        while True:
        
            weather = self.__get_weather_report(self.api_key,self.lat,self.lon)
            # self.__upate_weather_obj(weather)
            self.queries.put(weather)

            # print("weather is ",weather)

            time.sleep(self.delay)


    def __upate_weather_obj(self,weather):
        for attr in ['id','main','description','icon']:
            self.weather[attr] = weather[attr]



    def __get_weather_report(self, api_key, lat, lon):
        url =f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}'
        response = requests.get(url)
        if response.status_code == 200:
            json_content = json.loads(response.content)
            weather = json_content['weather']
            if weather:
                return weather[0]
     