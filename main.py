import requests, json, random
from tokens import *

class VK:
    URL_VK = 'https://api.vk.com/method/photos.get?'

    def __init__(self, id_VK):
        self.id_VK = id_VK

    def vk_photos(self):
        params = {
            'owner_id': self.id_VK,
            'v': '5.131',
            'access_token': TOKEN_VK,
            'album_id': 'profile',
            'extended': '1'
        }

        res = requests.get(self.URL_VK, params=params)
        if res.status_code == 200:
            photos = res.json()['response']['items']
            big_photos = {}
            for item in photos:
                sizes = [item['sizes'][i]['height'] * item['sizes'][i]['width'] for i in range(len(item['sizes']))]
                if str(item['likes']['count']) not in big_photos:
                    big_photos[f'{item["likes"]["count"]}'] = [item['sizes'][sizes.index(max(sizes))]['url'],
                                                               item['sizes'][sizes.index(max(sizes))]['type']]
                else:
                    big_photos[f'{item["likes"]["count"]}_'] = [item['sizes'][sizes.index(max(sizes))]['url'],
                                                                item['sizes'][sizes.index(max(sizes))]['type']]
            return big_photos
        else:
            print('Ошибка')


class Yndex:
    base_host = 'https://cloud-api.yandex.net/'

    def __init__(self, token, dict_):
        self.token = token
        self.dict_photos = dict_

    def headers(self):
        return {
            'Content-Type': 'application/json',
            'Authorization': f'OAuth {self.token}'
        }

    def upload_photos(self):
        uri = 'v1/disk/resources/upload/'
        URL_y = self.base_host + uri
        photos_json = {
            'photos': []
        }

        folder = f'Папка № {random.randint(100000, 999999)}'
        res = requests.put(self.base_host + 'v1/disk/resources/', params={'path': folder}, headers=self.headers())
        for key, val in self.dict_photos.items():
            params = {
                'path': f'/{folder}/{key}',
                'url': val[0],
                'overwrite': True}
            result = requests.post(URL_y, params=params, headers=self.headers())

            if result.status_code == 202:
                photos_json['photos'].append({
                    'file_name': f'{key}.jpg',
                    'size': val[1]
                })
                print('Загрузка фото произошла успешно!')
            else:
                print('Ошибка')
                break

        with open('upload_photo.json', 'w') as file:
            json.dump(photos_json, file, indent=4)

if __name__ == '__main__':
    object_1 = VK(60185737)
    dict_photos = object_1.vk_photos()

    object_2 = Yndex(TOKEN_YanD, dict_photos)
    object_2.upload_photos()