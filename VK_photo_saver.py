# TODO:
#     1) Добавить проверку на одинаковое количество лайков
#     2) Добавить проверку на наличие папки на ЯДиске
#     3) Причесать код (пихнуть все выполнение в один метод)
#     4) Добавить логирование
    
import requests
import json
import time

class VKtoYaDiskPhotoSaver:
    
    def __init__(self, VK_id, ya_token = None) -> None:
        self.ya_token = ya_token
        self.VK_id = VK_id
        self.folder = 'Фото с VK'
        with open('Course_task/VKtokenservice.txt', encoding='utf-8') as f:
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
        with open('Course_task/response.json', 'w') as f:
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
                if max_size_photo['type'] == 'z':
                    result.setdefault(photo['likes']['count'],[max_size_photo['url'], max_size_photo['type']])
        return result
    
#Input: get_VK_photo_info result
#Output: dict ({likes_count:[url, type]})

    def get_one_photo_bytes(self, photo):
        time.sleep(0.33)
        return requests.get(photo)
                                    # with open(f'Course_task/{photo}.jpg', 'wb') as handle:
                                    #     response = requests.get(photos_info[photo][0], stream=True)
                                    #     handle.write(response.content)
#Input: url of a photo
#Output: bytes of photo for upload to YaDisk
            
    def get_YaDisk_headers(self):
        return {
            'Content-Type': 'application/json',
            'Authorization': f'OAuth {self.ya_token}'
        }
    def create_YaDisk_folder(self):
        url = 'https://cloud-api.yandex.net/v1/disk/resources'
        params = {'path': self.folder}
        headers = self.get_YaDisk_headers()
        response = requests.put(url, params=params, headers=headers)
        return response
            
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
        
my_app = VKtoYaDiskPhotoSaver('1', 'y0_AgAAAAA4hChgAADLWwAAAADM50-I2qtAW1OlQKqpjmm8JEt9Bs-Ow58') #int(input('Введите ID VK: ')))
photos = my_app.get_max_VK_photos()

for photo in photos:
    my_app.upload_to_YaDisk(f'{my_app.folder}/{photo}.jpg', my_app.get_one_photo_bytes(photos[photo][0]))
# print(my_app.create_YaDisk_folder('Фото с VK'))