
import json

import weather_check
import image_downloaer
import engine


from multiprocessing import Queue

city = 'colombo'
api_key = "60c9b65ed07f5050a0bf1c6de810f8d8"
lat = '44.3'
lon = '10.99'

queries = Queue()
images = Queue()
weather = {}
queries.get()

if __name__ == "__main__":
    print("Starting dynamic Wallpaer.")

    queries = Queue()
    images = Queue()
    weather = {}
   

    weather_city = weather_check.weatherCheck(api_key, lat, lon, queries)
    weather_city.start()

    downloader = image_downloaer.ImageDownloader(queries, images)
    downloader.start()

    engine = engine.Engine(images)
    engine.start()

    weather_city.join()
    downloader.join()
    engine.join()
    