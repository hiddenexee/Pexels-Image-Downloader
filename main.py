from string import ascii_lowercase, digits
from random import choice, randint
import requests

class PexelsAPI:
    def __init__(self, api_key: str, keyword: str) -> None:
        self.api_url = 'https://api.pexels.com/v1/'
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': api_key
        })
        
        self.keyword = keyword 

    def search_photo(self, page = '1') -> dict:
        return self.session.get(f"{self.api_url}search?query={self.keyword}&page={page}&per_page=50").json()

class Downloading:
    def __init__(self) -> None:
        pass
    
    @staticmethod
    def get_random_string(lenght = randint(8, 12)):
        return ''.join(choice(ascii_lowercase + digits) for _ in range(lenght))
    
    @staticmethod
    def downloand(photo_arr: list) -> None:
        for src in photo_arr:
            response = requests.get(src)
            if response.status_code == 200:
                with open(f"images/{Downloading.get_random_string()}.jpg", 'wb') as f:
                    f.write(response.content)

if __name__ == '__main__':
    api_key = open("api_key.txt", "r", encoding="utf-8").read()

    input_keyword = input("[*] Keyword giriniz: ")
    max_page = int(input("[*] Kaç sayfa indirilsin: "))
    
    photo_api = PexelsAPI(api_key, input_keyword)
    downloading = Downloading()
    next_page = "1"

    for _ in range(max_page):
        photo_dict = photo_api.search_photo(next_page)
        #print(photo_dict)
        photo_src = []
        for photo in photo_dict["photos"]:
            photo_src.append(photo["src"]["original"])
        print(f"[+] {next_page}. sayfada {len(photo_src)} adet resim çekildi\n[+] Resimler indiriliyor")
        downloading.downloand(photo_src)
        next_page = photo_dict["next_page"].split('page=')[1].split('&')[0]

        print(f"[+] {next_page}. sayfa taranıyor")

    input(f"\n[*] {max_page} sayfa gezildi, işlemler bitmiştir")



