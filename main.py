# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
import json
import sys
sys.path.append('./')
from scripts.vk_photos_downloader import Vk_Profile_Photo_Dowloader
from scripts.yandex_upload import Yandex_Uploader
import scripts.logger as log
log.Logging()

@log.logger.catch()
def main():
    with open('./data/vk_token.txt', 'r', encoding='utf-8') as file:
        vk_token = file.readline().strip()

    with open('./data/yandex_token.txt', 'r', encoding='utf-8') as file:
        yandex_token = file.readline().strip()

    vk_result = vk(vk_token)
    result = yandex(yandex_token, vk_result)

    log.logger.info('Сохранение json файла')
    with open('result.json', 'w', encoding='utf8') as file: json.dump(result, file, indent='\t', ensure_ascii=False)
    ...

@log.logger.catch()
def vk(vk_token) -> list:
    vk = Vk_Profile_Photo_Dowloader(vk_token)
    id_profile = input('Введите id профиля из которого необходимо получить фото\n-> ').strip()
    count_photo = input('Укажите количество фотографий для скачивания\nОставьте пустым для сохранения стандартного количества изображений\n-> ').strip()

    if count_photo == '' and id_profile != '':
        items = vk.get_photos(owner_id=id_profile)
    elif count_photo != '' and id_profile != '':
        items = vk.get_photos(owner_id=id_profile, count_photo=count_photo)
    else:
        log.logger.info('Не указан профиль')
        exit()

    result_json = []

    for item in items:
        largest_photo(result_json, item=item)

    return result_json

@log.logger.catch()
def yandex(yandex_token, vk_result) -> list:
    yandex = Yandex_Uploader(yandex_token)
    time_now = datetime.now().strftime('%d-%m-%Y %H_%M_%S')
    path = f'coursework_{time_now}'
    yandex.create_folder(path=path)
    result = []
    check_lst = []
    for item in vk_result:
        if item['likes'] not in check_lst: file_name = f'{item["likes"]}.jpg'
        else: file_name = f'{item["likes"]}_{item["date"]}.jpg'

        result.append({'file_name': file_name,
                        'size': item['size']['type']})
        
        yandex.upload(file_path=f'{path}/{file_name}', url_image=item['size']['url'])

    return result

@log.logger.catch()
def convert_unix_time_to_date(unix_time: int, time_delta: int = 3) -> int:
    date = (datetime.utcfromtimestamp(unix_time) + timedelta(hours=time_delta)).strftime('%Y-%m-%d %H-%M-%S')

    return date

@log.logger.catch()
def largest_photo(result: list, item: dict):
    pixels = 0
    image_for_upload = None
    for size in item['sizes']:
        count_pixels = int(size['width']) * int(size['height'])
        if count_pixels > pixels:
            pixels = count_pixels
            image_for_upload = size
    d = {'size': {'type': image_for_upload['type'],
                'url': image_for_upload['url']},
        'likes': item['likes']['count'],
        'date': convert_unix_time_to_date(unix_time=item['date'])
        }

    result.append(d)


if __name__ == "__main__":
    main()