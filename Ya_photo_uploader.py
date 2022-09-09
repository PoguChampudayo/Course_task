import requests

class Ya_photo_uploader:    
    
    def __init__(self, ya_token:str, folder:str) -> None:
        self.ya_token = ya_token
        self.folder = folder
    def get_YaDisk_headers(self):
        return {
            'Content-Type': 'application/json',
            'Authorization': f'OAuth {self.ya_token}'
        }
        
    def check_for_folder(self):
        '''Checks if folder exists. Output: response 200 or 404'''
        
        url = 'https://cloud-api.yandex.net/v1/disk/resources'
        params = {'path': self.folder}
        headers = self.get_YaDisk_headers()
        response = requests.get(url, params=params, headers=headers)
        return response
   
    def create_YaDisk_folder(self):
        '''Creates folder on YaDisk if it's not there.'''
        
        if self.check_for_folder().status_code == 404:
            url = 'https://cloud-api.yandex.net/v1/disk/resources'
            params = {'path': self.folder}
            headers = self.get_YaDisk_headers()
            response = requests.put(url, params=params, headers=headers)
            return response

    def _get_YaDisk_upload_link(self, disc_file_path:str, file_url:str):
        '''Recieves upload link for put request.'''
        
        upload_link = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
        headers = self.get_YaDisk_headers()
        params = {'path': disc_file_path, 'overwrite': 'true', 'url': file_url}
        response = requests.post(upload_link, headers=headers, params=params)
        return response.json()
    
    def upload_to_YaDisk(self, file_path:str, file_url:str):
        href = self._get_YaDisk_upload_link(disc_file_path=file_path, file_url=file_url).get('href', '')
        req = requests.post(href, data=file_url)
        print(req.json())

    