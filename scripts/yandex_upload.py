# -*- coding: utf-8 -*-

import requests
from datetime import datetime
import sys
sys.path.append('./')
import scripts.logger as log
log.Logging()

class Yandex_Uploader:

    @log.logger.catch()
    def __init__(self, token: str):
        self.token = token

    def create_folder(self, path: str):
        """Метод создает папку по указанному пути"""
        url = 'https://cloud-api.yandex.net/v1/disk/resources?path={path}'.format(path=path)
        header = {'Authorization': f'OAuth {self.token}'}
        response = requests.put(url, headers=header).json()
        log.logger.info('Создание папки по указанному пути на яндекс диске\n{}'.format(response))

    @log.logger.catch()
    def upload(self, file_path: str, url_image: str):
        """Метод загружает файлы по списку file_list на яндекс диск"""
        url = 'https://cloud-api.yandex.net/v1/disk/resources/upload?path={file_path}'.format(file_path=file_path.split("\\")[-1])
        header = {'Authorization': f'OAuth {self.token}'}
        response = requests.get(url, headers=header).json()
        image = requests.get(url_image)
        try:
            log.logger.info('Попытка загрузки файла на яндекс диск')
            requests.put(response['href'], files={'file': image.content})
        except KeyError:
            log.logger.info(response)


if __name__ == '__main__':
    token = ''
    uploader = Yandex_Uploader(token)