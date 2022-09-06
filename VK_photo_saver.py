from datetime import datetime
import requests
import json
import time
from collections import Counter
from progress.bar import IncrementalBar
import os

#----------------------------------------------------------------------------------------------------------------------

class VKtoYaDiskPhotoSaver:
    
    def __init__(self, VK_id, ya_token = None) -> None:
        self.ya_token = ya_token
        self.VK_id = VK_id
        self.folder = 'Фото с VK'
        with open('VKtokenservice.txt', encoding='utf-8') as f: #Tested with service VK token
            self.VK_token= f.read().split()
        self.url = ('https://api.vk.com/method/')
        self.params = {
            'access_token' : self.VK_token,
            'v': '5.131'
        }
# Initialization: VKtoken is read from VKtoken.txt (or VKtokenservice.txt) in parent folder
   
    def get_VK_photo_info(self):
        self.VK_method = ('photos.get')
        get_VK_photo_info_params = {
            'owner_id': self.VK_id,
            'album_id': 'profile',
            'extended': '1'
        }
        req = requests.get(self.url + self.VK_method, params={**self.params, **get_VK_photo_info_params})
        with open('response.json', 'w') as f:
            json.dump(req.json(), f)
        return req.json()['response']['items']
#Input: class attrubutes (self.VK_id)
#Output: photos from VK profile info pulled from response -> items (extended = 1)

    def get_max_size(self, response_items):
        max_sizes = {}
        for photo in response_items:
            max_size = max([photo['sizes'][i]['width'] * photo['sizes'][i]['height'] 
                            for i,_ in enumerate(photo['sizes'])])
            max_sizes.setdefault(photo['id'], max_size)
        return max_sizes
# Get maximum size of each photo
    
    def progress(self, mode, length=None):
        if mode == 'create':
            global uploadbar
            uploadbar = IncrementalBar('Загрузка фотографий на яндекс диск', max= length)
        elif mode == 'next':
            uploadbar.next()
        elif mode == 'finish':
            uploadbar.finish()
# Progress bar initiator

    def get_max_VK_photos(self):
        response_items = self.get_VK_photo_info()
        result = {}
        unique_names = []
        for photo in response_items:
            for max_size_photo in photo['sizes']:
                if (max_size_photo['width'] * max_size_photo['height'] == self.get_max_size(response_items)[photo['id']]):
                    result.setdefault(photo['id'],[max_size_photo['url'], max_size_photo['type'], 
                                                   photo['likes']['count'], photo['date']])
            unique_names.append(photo['likes']['count'])
        counter = Counter(unique_names)
        for photo in result:
            if counter[result[photo][2]] > 1:
                photo_date = datetime.fromtimestamp(result[photo][3])
                result[photo][2] = str(result[photo][2]) + '_' + photo_date.strftime('%d-%m-%Y')
        print(f'Всего: {len(result)} фотографий')
        self.progress('create', len(result))
        return result
#Input: get_VK_photo_info result
#Output: dict ({id:[url, type, likes_count, date]})

    def get_one_photo_bytes(self, photo):
        time.sleep(0.2)
        return requests.get(photo)

#Input: url of a photo
#Output: bytes of photo for uploading to YaDisk
            
    def get_YaDisk_headers(self):
        return {
            'Content-Type': 'application/json',
            'Authorization': f'OAuth {self.ya_token}'
        }
        
    def check_for_folder(self):
        url = 'https://cloud-api.yandex.net/v1/disk/resources'
        params = {'path': self.folder}
        headers = self.get_YaDisk_headers()
        response = requests.get(url, params=params, headers=headers)
        return response
# Checks if folder exists, output - response 200 or 404
   
    def create_YaDisk_folder(self):
        if self.check_for_folder().status_code == 404:
            url = 'https://cloud-api.yandex.net/v1/disk/resources'
            params = {'path': self.folder}
            headers = self.get_YaDisk_headers()
            response = requests.put(url, params=params, headers=headers)
            return response
# Creates foled on YaDisk if it's not there
            
    def _get_YaDisk_upload_link(self, disc_file_path):
        url = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
        headers = self.get_YaDisk_headers()
        params = {'path': disc_file_path, 'overwrite': 'true'}
        response = requests.get(url, headers=headers, params=params)
        return response.json()
    
    def upload_to_YaDisk(self, file_path, url, size):
        href = self._get_YaDisk_upload_link(disc_file_path=file_path).get('href', '')
        response = requests.put(href, data=url)
        if response.status_code == 201:
            self.progress('next')
            self.create_log(file_path.split('/')[-1], size)
    
    def create_log(self, file_name, file_type):
        if 'result.json' in os.listdir():
            with open('result.json','r+') as f:
                data = json.load(f)
                data['files'].append({'file_name': file_name, 'size': file_type})
            with open('result.json','w') as f:
                json.dump(data, f)
        else:
            with open('result.json', 'x') as f:
                json.dump({'files': []}, f)
            self.create_log(file_name, file_type)
# Creates json file ({'files': [...]) or creates it if it's not here
           
    def launcher(self):
        if 'result.json' in os.listdir():
            os.remove('result.json')
        self.create_YaDisk_folder()
        photos = my_app.get_max_VK_photos()
        for photo in photos:
            my_app.upload_to_YaDisk(f'{my_app.folder}/{photos[photo][2]}.jpg', 
                                    my_app.get_one_photo_bytes(photos[photo][0]),photos[photo][1])
        self.progress('finish')
# Main controller: first cleares result.json, then creates a folder on YaDisk, then uploads each photo in the folder
       
with open('yatoken.txt', encoding='utf-8') as file:
    ya_token = file.read().split()   
my_app = VKtoYaDiskPhotoSaver('1', *ya_token)
my_app.launcher()