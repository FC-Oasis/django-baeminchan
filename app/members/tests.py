import random
import string

from django.contrib.auth import get_user_model
from django.test import Client
from rest_framework import status
from rest_framework.exceptions import ValidationError
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
        format(random.randint(1, 28), '02'),
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

        # 테스트 코드 내에서 토큰 받아오기
        response = self.client.post(
            self.URL + 'auth-token/',
            data={
                'username': user_info['username'],
                'password': user_info['password'],
            },
        )

        token = response.json()['token']

        # 테스트 코드 내에서 토큰 인증하기
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)

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

    def test_password_change(self):
        """
        User의 비밀번호 변경 API 테스트
        :return:
        """
        user_info = get_dummy_user_info()
        user = User.objects.create_user(**user_info)

        self.client.force_authenticate(user=user)

        URL = self.URL + f'change/password/{user.id}/'
        new_password = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))  # 새로운 비밀번호

        response = self.client.patch(
            URL,
            data={
                'new_password': new_password,
                'check_new_password': new_password,
            },
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.json(),
            {
                'new_password': new_password,
                'check_new_password': new_password,
            },
        )

        # new_password, check_new_password 서로 다를 때
        response = self.client.patch(
            URL,
            data={
                'new_password': new_password,
                'check_new_password': 'abcd1234',
            },
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.json(),
            {
                "non_field_errors": [
                    "비밀번호가 맞지 않습니다"
                ]
            },
        )

    # # Phone 관련 테스트 사용시 실제 청기와랩 API 호출됨
    # # 필요할 때만 주석 해제해서 사용할 것
    # def test_get_phone_auth_key(self):
    #     URL = self.URL + 'phone/'
    #     response = self.client.post(
    #         URL,
    #         data={
    #             'contact_phone': '01012345678',
    #         }
    #     )
    #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    #
    #     response = self.client.post(
    #         URL,
    #         data={
    #             'contact_phone': '010-1234-5678',
    #         }
    #     )
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    #
    #     auth_key_prev = response.json()['auth_key']
    #     self.assertIsNotNone(auth_key_prev)
    #
    #     response = self.client.patch(
    #         URL,
    #         data={
    #             'contact_phone': '010-1234-5678',
    #         }
    #     )
    #
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #
    #     auth_key = response.json()['auth_key']
    #     self.assertIsNotNone(auth_key_prev)
    #     self.assertNotEqual(auth_key_prev, auth_key)
    #
    # def test_duplicated_phone(self):
    #     URL = self.URL + 'phone/'
    #
    #     response = self.client
    #     for __ in range(2):
    #         response = self.client.post(
    #             URL,
    #             data={
    #                 'contact_phone': '010-1234-5678',
    #             }
    #         )
    #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    #
    # def test_phone_auth(self):
    #     import pprint
    #     URL = self.URL + 'phone/'
    #     response = self.client.post(
    #         URL,
    #         data={
    #             'contact_phone': '010-1234-5678',
    #         }
    #     )
    #     auth_key = response.json()['auth_key']
    #
    #     response = self.client.post(
    #         URL + 'auth/',
    #         data={
    #             'contact_phone': '010-1234-5678',
    #             'auth_key': '000',
    #         }
    #     )
    #     self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    #
    #     response = self.client.post(
    #         URL + 'auth/',
    #         data={
    #             'contact_phone': '010-1234-5678',
    #             'auth_key': auth_key,
    #         }
    #     )
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #
    #     response = self.client.post(
    #         URL + 'auth/',
    #         data={
    #             'contact_phone': '010-1234-5678',
    #             'auth_key': auth_key,
    #         }
    #     )
    #     self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_duplicate_email_validation(self):
        """
        check@duplicate.com 이메일을 A 라는 유저가 등록했을 때
        B 유저가 check@duplicate.com 이라는 이메일을 가지지 못하도록 테스트 설정
        :return:
        """
        user_info = get_dummy_user_info()
        user = User.objects.create_user(**user_info)

        self.client.force_authenticate(user=user)

        # /api/users/change/email/1/
        URL = self.URL + f'change/email/{user.id}/'

        # response 받는 유저데이터의 email 과 비교하기 위한 test data 를 생성
        compare_with_response_data = User.objects.create_user(
            username='test',
            password='pass1122',
            email='check@duplicate.com',
        )

        response = self.client.patch(
            URL,
            data={
                'email': 'check@duplicate.com',
            },
        )

        self.assertRaises(ValidationError)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.json(),
            {
                "email": [
                    "이미 사용중인 이메일입니다"
                ]
            },
        )
