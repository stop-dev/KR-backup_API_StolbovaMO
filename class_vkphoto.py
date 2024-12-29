class VKPhoto:

    def __init__(self, likes:int, url:str, size:str, date):
        self._likes = likes
        self._url = url
        self._size = size
        self._date = date
    
    def __repr__(self):
        return (f"likes: {self._likes}\n " + f"url: {self._url}\n "
            + f"size: {self._size}\n " + f"date: {self._date}\n")

    def create_photo_name(self, add_date:bool = 0):
        name = f"{self._likes}"
        if add_date:
            name += f" {self._date}"
        return f'{name}.jpg'

    def save_to_yandex_disk(self, folder_name:str, date_in_name:bool):
        name = self.create_photo_name(date_in_name)
        pass

    def get_likes(self):
        return self._likes
    
    def get_url(self):
        return self._url

    def get_size(self):
        return self._size

    def get_date(self):
        return self._date
