import requests
from urllib.parse import urljoin
import time


TOKEN = ''
API_BASE_URL = 'http://api.vk.com/method/'
V = '5.21'


class VKUser:
    BASE_URL = API_BASE_URL

    def __init__(self, user_id, token=TOKEN, version=V):
        self.token = token
        self.version = version
        self.user_id = user_id
        self.first_name = ''
        self.last_name = ''
        self.user_link = 'http://www.vk.com/id' + str(self.user_id)
        self.get_user_info()

    def __create_method_url(self, method):
        return urljoin(self.BASE_URL, method)

    def __and__(self, other):
        res = self.get_mutual_friends(other.user_id)
        return res

    def __str__(self):
        return f'{self.first_name} {self.last_name} {self.user_link}'

    def get_user_info(self):
        res = requests.get(self.__create_method_url('users.get'), params={
            'access_token': self.token,
            'v': self.version,
            'user_ids': self.user_id
        })
        if 'error' not in res.json():
            user_info = res.json()['response'][0]
            self.first_name = user_info['first_name']
            self.last_name = user_info['last_name']
        else:
            user_info = ''
        return user_info

    def get_mutual_friends(self, target_user_id):
        res = requests.get(self.__create_method_url('friends.getMutual'), params={
            'access_token': self.token,
            'v': self.version,
            'source_uid': self.user_id,
            'target_uid': target_user_id
        })
        friends_list = []
        for elm in res.json()['response']:
            friend = VKUser(elm)
            friends_list.append(friend)
            time.sleep(1)
        return friends_list


if __name__ == '__main__':
    user1 = VKUser(2359003)
    user2 = VKUser(2116146)
    print(user1)
    print(user2)

    mutual_friends_list = user1 & user2
    i = 0
    print(f'Количество общих друзей - {len(mutual_friends_list)}:')
    for friend in mutual_friends_list:
        i += 1
        print(i, end='. ')
        print(friend)