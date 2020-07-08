from configparser import ConfigParser
import requests
import random
import string
import csv
import json


class StarnaviBot:

    STARNAVI_REQS = {
        'register': 'http://127.0.0.1:8000/api/accounts/register/',
        'get_jwt': 'http://127.0.0.1:8000/api/token/',
        'posts': 'http://127.0.0.1:8000/api/posts/',
    }

    def __init__(self, conf_data: dict, file_name='users.csv'):
        """
        :param conf_data: parsed dict with starnavi settings
        """
        if not conf_data:
            raise AttributeError('Should be data')
        self.data = conf_data
        self.file_name = file_name
        self.users = []

    def save_user_data_to_file(self, username, password, *args, **kwargs):
        """
            Save user info (username, password) to csv.file
        """
        with open(self.file_name, 'a') as f:
            writer = csv.writer(f, quoting=csv.QUOTE_ALL)
            writer.writerow([username, password])
        print('User {} are saved into file!'.format(username))

    def register_user(self):
        """
            Create and register user
        """
        url = self.STARNAVI_REQS.get('register')
        # gen random username
        username = ''.join([random.choice(string.ascii_letters) for _ in range(10)])
        password = 'keudlqwwnd123'

        response = requests.post(url, data={
            'username': username,
            'password': password,
            'password_confirm': password

        })
        if response.status_code != 201:
            raise ValueError(response.status_code, response.content)
        print('User {} are created!'.format(username))
        user = {
            'username': username,
            'password': password,
            'jwttoken': ''
        }
        self.users.append(user)
        self.save_user_data_to_file(*user.values())

    def login_user(self, user: dict):
        """
            Get JWT-token for user and save it to user dict
        """
        url = self.STARNAVI_REQS.get('get_jwt')
        response = requests.post(url, data={
            'username': user.get('username'),
            'password': user.get('password')
        })
        jwt_token = response.content.decode('utf-8')
        user['jwttoken'] = json.loads(jwt_token).get('access')
        print('{} user are login with {} token'.format(user.get('username'), user.get('jwttoken')))

    def create_post(self, user: dict):
        """
         Create post for user
        """
        url = self.STARNAVI_REQS.get('posts')

        random_title = ''.join([random.choice(string.ascii_letters) for _ in range(10)])
        random_text = ''.join([random.choice(string.ascii_letters) for _ in range(10)])

        response = requests.post(url, data={
                                                'title': random_title,
                                                'text': random_text
                                            },
                                         headers={
                                             'Authorization': 'Bearer ' + user.get('jwttoken')
                                         })
        print('{} user create response with {} status code'.format(user.get('username'), response.status_code))

    def create_posts_per_user(self, max_post_number: int):
        """
            Create post from each user
        """
        for user in self.users:
            if not user.get('jwttoken'):
                self.login_user(user)

            posts_per_user = random.randint(0, max_post_number)
            print('{} user can make {} posts'.format(user.get('username'), posts_per_user))
            for _ in range(posts_per_user):
                self.create_post(user)

    def get_all_posts_ids(self, user: dict):
        """
            Get all posts and return list of ids

            NOTE: I understand that i send get request for each user. But i do it because
            i understand that if i pass get request only once - my db can change while i working with likes
        """
        url = self.STARNAVI_REQS.get('posts')
        response = requests.get(url, headers={
                                     'Authorization': 'Bearer ' + user.get('jwttoken')
                                 })
        data = json.loads(response.content)
        return [post.get('id') for post in data]

    def like_post(self, user: dict, post_id: int):
        url = self.STARNAVI_REQS.get('posts') + str(post_id) + '/like/'
        response = requests.post(url,  headers={
                                     'Authorization': 'Bearer ' + user.get('jwttoken')
                                 })
        print('{} user are like {} post'.format(user.get('username'), post_id))

    def like_posts_per_user(self, max_likes_per_user: int):
        for user in self.users:
            if not user.get('jwttoken'):
                self.login_user(user)

            like_per_user = random.randint(0, max_likes_per_user)
            # todo: for test
            like_per_user = 3
            posts_ids = self.get_all_posts_ids(user)

            for _ in range(like_per_user):
                self.like_post(user, random.choice(posts_ids))

    def launch(self):
        """
            Launch bot

            i separate user signup, post creation and post like. I know that i duplicate cycles but make this decision
            because i check is max_posts_number/max_likes_per_user are not equal zero

            Like i understand i can make request func, which will take a url via parameter.
            When i choose it my code will be much more shorter but i think the split will be better
            because i make make code more readble

            NOTE: i see that my like_posts_per_user and create_posts_per_user are equal, and i understand that
            maybe will be better if i use one func for several tasks with different params. But i think this desicion
            make my code more readable
        """
        number_of_users = int(self.data.get('number_of_users', 0))
        print('Get {} users'.format(number_of_users))
        for _ in range(number_of_users):
            self.register_user()

        max_posts_number = int(self.data.get('max_posts_per_user', 0))
        print('Get {} max posts number'.format(max_posts_number))
        if max_posts_number != 0:
            self.create_posts_per_user(max_posts_number)

        max_likes_per_user = int(self.data.get('max_likes_per_user', 0))
        print('Get {} max likes number'.format(max_likes_per_user))
        if max_likes_per_user != 0:
            self.like_posts_per_user(max_likes_per_user)

        print('DONE')

if __name__ == '__main__':

    config = ConfigParser()
    config.read('config_for_bot.ini')

    confdict = {section: dict(config.items(section)) for section in config.sections()}

    StarnaviBot(confdict.get('starnavi')).launch()


