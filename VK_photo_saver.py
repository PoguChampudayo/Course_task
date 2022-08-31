from dataclasses import fields
import requests
from pprint import pprint
import json
import time



class VKtoYaDiskPhotoSaver:
    
    def __init__(self, VK_id, ya_token = None) -> None:
        self.ya_token = ya_token
        self.VK_id = VK_id
        with open('VKtoken.txt', encoding='utf-8') as f:
            self.VK_token= f.read().split()
        self.url = ('https://api.vk.com/method/')
        self.params = {
            'access_token' : self.VK_token,
            'v': '5.131'
        }
       
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
    
    def get_max_VK_photos(self):
        response_items = self.get_VK_photo_info()
        result = {}
        max_photo = 0
        for photo in response_items:
            for max_size_photo in photo['sizes']:
                if max_size_photo['height'] * max_size_photo['width'] < max_photo:
                    result.setdefault(photo['likes']['count'],[max_size_photo['url'], max_size_photo['type']])
                else:
                    max_photo = max_size_photo['height'] * max_size_photo['width']
        print(max_size_photo)
        return result
#Input: get_VK_photo_info result
#Output: dict ({likes_count:[url, type]})
    
    def get_YaDisk_headers(self):
        return {
            'Content-Type': 'application/json',
            'Authorization': f'OAuth {self.ya_token}'
        }
        
    def _get_YaDisk_upload_link(self, disc_file_path):
        url = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
        headers = self.get_YaDisk_headers()
        params = {'path': disc_file_path, 'overwrite': 'true'}
        response = requests.get(url, headers=headers, params=params)
        return response.json()
    
    def upload_to_YaDisk(self, file_path, url):
        href = self._get_YaDisk_upload_link(disc_file_path=file_path).get('href', '')
        response = requests.put(href, data=url)
        if response.status_code == 201:
            print('Success!')
    
    # def save_photo_to_YaDisk(self, Ya_destination, url, filename):
        
my_app = VKtoYaDiskPhotoSaver('1') #int(input('Введите ID VK: ')))
photos_info = my_app.get_max_VK_photos()
for photo in photos_info:
    time.sleep(0.33)
    with open(f'{photo}.jpg', 'wb') as handle:
        response = requests.get(photos_info[photo][0], stream=True)
        handle.write(response.content)


