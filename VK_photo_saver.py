import requests
import json

class VKPhotoSaver:
    
    def __init__(self, VK_id, ya_token = None) -> None:
        self.VK_id = VK_id
        self.ya_token = ya_token
        self.url = ('https://api.vk.com/method/')
    
    def get_VK_user_info(self):
        self.VK_method = ('users.get')
        params = {'user_ids': self.VK_id}
        req = requests.get(self.url + self.VK_method, params=params)
        return req
    
my_app = VKPhotoSaver('1')
print(my_app.get_VK_user_info().text)