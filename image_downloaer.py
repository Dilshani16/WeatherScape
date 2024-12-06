from threading import Thread
from multiprocessing import Process
import requests
import json

class ImageDownloader(Process):
    def __init__(self,queries,images):
        super(ImageDownloader, self).__init__()
        self.queries = queries
        self.prev_queries = None
        self.images = images

    def run(self):

        query = self.queries.get()
        print("Query", query)
        while query is not None:
            # if self.prev_queries == query:
            #     print("same query")
            #     query = self.queries.get()
            #     continue

            url = f"https://unsplash.com/napi/search/photos?page=1&query={query}"

            r = requests.get(url)

            if r.status_code == 200:
               
                response_json = json.loads(r.content)
                result = response_json['results']
                for image in result:
                    self.__download_image(image)
            else:
                print("Unsucessfully")

            
            query = self.queries.get()
            self.prev_queries = query


    def __download_image(self,image):
        urls = image['urls']
        raw = urls['raw']
        print(raw)

        res = requests.get(raw, stream = True)
        if res.status_code == 200:
               
           res.raw.decode_content = True

           x = raw.split('?')
           image_name = x[0].split('/')[-1]


           file_name = f'images/{image_name}.jpg'

           with open(file_name,'wb') as f:
               f.write(res.content)

           self.images.put(file_name)

           print("image downloaded sucessfully", file_name)
        else:
            print("unsucessfully")

        