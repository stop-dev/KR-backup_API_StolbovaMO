from pprint import pprint, pformat
import requests
from colorama import Fore, Back, Style
import logging


class VKAPIClient:
    API_BASE_URL = 'https://api.vk.com/method/'
    _INFO_SUCCESS = Fore.GREEN + "Request: SUCCESS!" + Style.RESET_ALL
    _INFO_FAILURE = Fore.RED + "Request: FAILURE!" + Style.RESET_ALL
    _INFO_PHOTOS = Back.YELLOW + "Getting information about photos from vk.com..." + Style.RESET_ALL

    def __init__(self, access_token, user_id, vertion='5.199'):
        self.__token = access_token
        self.user_id = user_id
        self.version = vertion
        self.__params = {'access_token': self.__token, 'v': self.version}

    def _get_params_for_photos(self, number:int, album_id:str):
        return {
            'owner_id':self.user_id,
            'album_id':album_id,
            'extended':1,
            'photo_sizes':1,
            'count':number
        }

    def get_photos_json(self, number:int=5, album_id:str='profile'):
        METHOD = 'photos.get'
        get_url = f"{self.API_BASE_URL}{METHOD}?"
        params = {**self.__params, **self._get_params_for_photos(number, album_id)}
        logging.info(self._INFO_PHOTOS)
        response = requests.get(get_url, params=params)
        result = response.json()
        if not 200 <= response.status_code < 300 or list(result.keys())[0] == 'error':
            if response.status_code == 200:
                massage = f"{result['error']['error_msg']}"
            else:
                massage = f"Status code: {response.status_code}"
            logging.critical(f"{self._INFO_FAILURE} {massage}")
            return None
        else:
            logging.info(self._INFO_SUCCESS)
            return response.json()
