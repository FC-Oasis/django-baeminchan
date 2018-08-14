import random
import string

from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

User = get_user_model()
user_fields = [
    'username',
    'password',
    'fullname',
]


def get_dummy_user_info():
    """
    무작위 유저 정보를 생성해 딕셔너리 타입으로 리턴
    :return: dummy_user_info
    """
    dummy_user_info = {
        # 무작위 문자열 생성
        field: ''.join(random.choices(string.ascii_uppercase + string.digits, k=10)) for field in user_fields
    }
    dummy_user_info['email'] = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10)) + '@a.com'

    # 무작위 핸드폰 번호 생성(str 인스턴스)
    dummy_user_info['contact_phone'] = '010-{}-{}'.format(
        str(random.randint(1111, 9999)),
        str(random.randint(1111, 9999))
    )

    # 무작위 날짜 생성(datetime 형식의 str 인스턴스)
    dummy_user_info['birthday'] = '{}-{}-{}'.format(
        str(random.randint(1950, 2018)),
        format(random.randint(1, 12), '02'),
        format(random.randint(1, 30), '02'),
    )

    return dummy_user_info


def get_dummy_user():
    return User.objects.create_user(**get_dummy_user_info())


class MembersTest(APITestCase):
    """
    Member 요청에 대한 테스트
    """
    URL = '/api/users/'

    def test_user_create_status_code(self):
        """
        User 생성 요청 결과의 HTTP 상태코드가 201인지 확인
        :return:
        """
        URL = self.URL + 'create/'
        response = self.client.post(
            URL,
            data=get_dummy_user_info(),  # 무작위 유저 정보 사용
            format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_email_change(self):
        """
        User의 이메일 변경 API 테스트
        :return:
        """
        user_info = get_dummy_user_info()
        user = User.objects.create_user(**user_info)

        # # 테스트 코드 내에서 토큰 받아오기
        # response = self.client.post(
        #     self.URL + 'auth-token/',
        #     data={
        #         'username': user_info['username'],
        #         'password': user_info['password'],
        #     },
        # )
        #
        # token = response.json()['token']
        #
        # # 테스트 코드 내에서 토큰 인증하기
        # self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)

        # 강제로 인증하기
        self.client.force_authenticate(user=user)

        URL = self.URL + f'change/email/{user.id}/'

        response = self.client.patch(
            URL,
            data={
                'email': 'a@a.com',
            },
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['email'], 'a@a.com')
