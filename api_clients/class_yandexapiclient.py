import requests
from datetime import datetime
import logging
from colorama import Fore, Back, Style
import time

DATE_FORMAT = '%d-%m-%Y at %Hh.%Mm.%Ss'

def date_today(format=DATE_FORMAT):
    return datetime.today().strftime(format)


class YandexAPIClient:
    API_BASE_URL = 'https://cloud-api.yandex.net/v1/disk/resources'
    _FOLDER_S = "Yandex folder was created"
    _FOLDER_F = "Yandex folder wasn't created"

    _C_FOLDER_F = Fore.RED + _FOLDER_F + Style.RESET_ALL
    _C_FOLDER_S = Fore.GREEN + _FOLDER_S  + Style.RESET_ALL

    _INFO_S = Fore.GREEN + "Request: SUCCESS!" + Style.RESET_ALL
    _INFO_F = Fore.RED + "Request: FAILURE!" + Style.RESET_ALL

    def __init__(self, access_token:str):
        self.__headers = {'Authorization':access_token}
    
    def get_status(self, status_link:str):
        response = requests.get(status_link, headers=self.__headers)
        return response.json()['status']

    def create_folder(self, name:str=date_today()):
        folder_path = '/' + name
        params = {'path':folder_path}
        response = requests.put(self.API_BASE_URL, params=params,  headers=self.__headers)
        status = response.status_code
        if status != 201:
            if 200 <= status < 300:
                message = response.json()['description']
            else:
                message = f"Status code: {status}"
            logging.critical(f"{self._C_FOLDER_F} {message}")
            return 1
        logging.info(self._C_FOLDER_S)
        return 0
    
    def _get_params_for_downloading(self, download_url:str, download_path:str):
        return {
            'url':download_url,
            'path':download_path
        }

    def downloading_file(self, download_url:str, download_path:str='/name', file_name:str='name'):
        post_url = f"{self.API_BASE_URL}/upload?"
        path = download_path + '/' + file_name
        response = requests.post(post_url, 
                                params=self._get_params_for_downloading(download_url,
                                                                        path),
                                headers=self.__headers
        )
        if 202 != response.status_code:
            logging.critical(f"{self._INFO_F} Status code: {response.status_code}")
            return 2
        status_link = response.json()['href']
        if self.get_status(status_link) == 'failed':
            logging.warning(f"{self._INFO_F}: photo wasn't downloaded on Yandex")
            return 1
        logging.info(f"{self._INFO_S} {file_name} was downloaded on Yandex")
        return 0
