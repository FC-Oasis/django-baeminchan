import json

import requests
from django.contrib.auth import get_user_model

from config.settings.production import secrets

User = get_user_model()


class KakaoBackend:

    def authenticate(self, request, access_token):

        # def get_access_token(code):
        #     url = 'https://kauth.kakao.com/oauth/token'
        #     data = {
        #         'grant_type': 'authorization_code',
        #         'client_id': secrets["KAKAO_REST_API_KEY"],
        #         'redirect_uri': 'https://server.yeojin.me/api/users/kakao',
        #         'code': code,
        #     }
        #     response = requests.post(url, data=data)
        #     response_dict = json.loads(response.text)
        #     access_token = response_dict['access_token']
        #     return access_token
        #
        # def connect_app(access_token):
        #     url = 'https://kapi.kakao.com/v1/user/signup'
        #     headers = {
        #         'Authorization': f'Bearer {access_token}',
        #         'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8',
        #     }
        #     response = requests.post(url, headers=headers)
        #     response_dict = response.json()
        #     kakao_user_id = response_dict['id']
        #     return kakao_user_id

        def get_user_info(access_token):
            url = 'https://kapi.kakao.com/v2/user/me'
            headers = {
                'Authorization': f'Bearer {access_token}',
                'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8',
                # 연령대와 생일을 알기 위해서는 kakao_account.age_range, kakao_account.birthday 추가
                'property_keys': '["properties.nickname", "kakao_account.email"]',
            }
            response = requests.post(url, headers=headers)
            return response.json()

        def create_user_from_kakao_user_info(user_info):
            kakao_user_id = user_info['id']
            fullname = user_info['properties']['nickname']
            email = user_info['kakao_account']['email']
            return User.objects.get_or_create(
                username=kakao_user_id,
                defaults={
                    'username': kakao_user_id,
                    'fullname': fullname,
                    'email': email,
                },
            )

        # access_token = get_access_token(code)
        # connect_app(access_token)
        user_info = get_user_info(access_token)
        user, user_created = create_user_from_kakao_user_info(user_info)
        return user
