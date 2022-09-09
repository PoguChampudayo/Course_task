from VK_photos_getter import VKPhotoSaver
from Ya_photo_uploader import Ya_photo_uploader
from progress.bar import IncrementalBar
from logger import create_log
import os

def progress(mode, title=None, length=None):
    '''Initiates, continues and finishes progress bar'''
    if mode == 'create':
        global uploadbar
        uploadbar = IncrementalBar(title, max=length)
    elif mode == 'next':
        uploadbar.next()
    elif mode == 'finish':
        uploadbar.finish()
        
def launcher(VK_id, VK_token, ya_token, photo_quantity=5):
        if 'result.json' in os.listdir():
            os.remove('result.json')
        VK_photos = VKPhotoSaver(VK_id, VK_token, photo_quantity)
        Ya_uploads = Ya_photo_uploader(ya_token, 'Фото с ВК')
        photos = VK_photos.get_max_VK_photos()
        print(f'Всего: {len(photos)} фотографий')
        progress('create', 'Загрузка фотографий на ЯндексДиск', len(photos))
        Ya_uploads.create_YaDisk_folder()
        for photo in photos:
            Ya_uploads.upload_to_YaDisk(f'{Ya_uploads.folder}/{photos[photo][2]}.jpg', 
                                    photos[photo][0])
            create_log(photos[photo][2], photos[photo][1])
            progress('next')
        progress('finish')
        
if __name__ == '__main__':  
    with open('yatoken.txt', encoding='utf-8') as file:
        ya_token = file.read().split()  
    with open('VKtokenservice.txt', encoding='utf-8') as f: 
        VK_token= f.read().split()
    photo_count = 9
    launcher('1', *VK_token, *ya_token, photo_count)