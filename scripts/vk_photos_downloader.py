# -*- coding^ utf-8 -*-

import requests
import sys
sys.path.append('./')
import scripts.logger as log
log.Logging()

class Vk_Profile_Photo_Dowloader():

    @log.logger.catch()
    def __init__(self, token) -> None:
        self.token = token

    @log.logger.catch()
    def get_photos(self, owner_id: str, album_id: str = 'profile', count_photo: str = '5') -> list:
        url = 'https://api.vk.com/method/photos.get'
        params = {'access_token': self.token,
                'v': '5.131',
                'extended': '1',
                'owner_id': owner_id,
                'album_id': album_id,
                'count': count_photo}
        log.logger.info('Получение фотографий профиля из Вконтакте')
        response = requests.get(url, params=params).json()
        items = response['response']['items']

        return items

if __name__ == "__main__":
    access_token = ''
    vk = Vk_Profile_Photo_Dowloader(access_token)
    vk.get_photos(owner_id='52709815')