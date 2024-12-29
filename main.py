import json
import configparser # For settings.ini
from pprint import pprint
from datetime import datetime
from colorama import Fore, Back, Style
from api_clients.class_vkapiclient import VKAPIClient
from api_clients.class_yandexapiclient import YandexAPIClient, DATE_FORMAT
from api_clients.class_yandexapiclient import date_today
from class_vkphoto import VKPhoto
import logging
from dialog_with_user import dialog_with_user

def creat_json_file(dict1):
    _INFO = Fore.GREEN + "JSON file was created" + Style.RESET_ALL
    with open('photos_info.json', 'w') as f:
        json.dump(dict1, f, ensure_ascii=False, indent=2)
    logging.info(_INFO)


def get_big_photo_url_and_type(photo_sizes: dict) -> list:
    TYPES_PIORITY = {'w':1, 'z':2, 'y':3, 'x':4, 'r':5, 'q':6,
                    'p':7, 'm':8, 'o':9, 's':10}
    result_list = []
    for photo in photo_sizes:
        if not result_list or (result_list and TYPES_PIORITY[photo['type']] <
                                            TYPES_PIORITY[result_list[0]]):
            result_list = [photo['type'], photo['url']]
    return result_list


def make_photos_infolist(file_json) -> list:
    photos_list = []
    for item in file_json['response']['items']:
        likes = item['likes']['count']
        date = datetime.fromtimestamp(item["date"]).strftime(DATE_FORMAT)
        r = get_big_photo_url_and_type(item["sizes"])
        photos_list.append(VKPhoto(likes=likes, date=date, size=r[0],
                                    url=r[1]))
    return photos_list


def download_vkphotos_to_yandex(folder_name, photos_json, yandex_client:YandexAPIClient):
    unique_likes_list = []
    info_for_json_file = []

    vk_photos_list = make_photos_infolist(photos_json)
    if yandex_client.create_folder(folder_name):
        return
    for photo_info in vk_photos_list:
        if photo_info.get_likes() in unique_likes_list:
            add_date = True
        else:
            unique_likes_list.append(photo_info.get_likes())
            add_date = False
        photo_name = photo_info.create_photo_name(add_date=add_date)
        download_path = f"/{folder_name}"
        status_code = yandex_client.downloading_file(
            photo_info.get_url(),
            download_path,
            photo_name
        )
        if status_code == 1:
            continue 
        elif status_code == 2: 
            return
        info_for_json_file.append({"file_name":photo_name, "size":photo_info.get_size()})
    creat_json_file({"downloaded_files":info_for_json_file})


def initial_program() -> tuple:
    user_id, download_photos_number = dialog_with_user()
    if user_id == None:
        return None, None, None

    # set logging format
    logging.basicConfig(level=logging.INFO,  format="%(levelname)s: %(message)s")

    # read tokens from .ini file
    config = configparser.ConfigParser()
    config.read("settings.ini")
    vk_client = VKAPIClient(config['Tokens']['access_token_vk'], user_id)
    yandex_client = YandexAPIClient(config['Tokens']['access_token_yandex_disk'])
    return vk_client, yandex_client, download_photos_number


if __name__ == '__main__':
    vk_client, yandex_client, download_photos_number = initial_program()

    photos_json = vk_client.get_photos_json(download_photos_number)
    if photos_json:
        folder_name = f"Photos_from_VK {date_today()}"
        download_vkphotos_to_yandex(folder_name, photos_json, yandex_client)
