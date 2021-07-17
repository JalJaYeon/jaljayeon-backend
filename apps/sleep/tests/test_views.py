from datetime import datetime, date, time
from apps.user.models import User
from rest_framework.test import APITestCase
from apps.common.test import create_sample_user_and_get_token
from apps.sleep.models import Sleep


class TestReportingSleep(APITestCase):
    ENDPOINT = '/api/sleep'
    """
    The Sleep Report should be created only when:
    1. the requested user is authenticated
    2. following parameters exist
        - time_slept: formatted string(%H:%M)
        - is_enough_sleep: boolean
        - tiredness_level: integer(1 <= tiredness_level <= 5)
    3. if user already reported sleep, then the other creation request should be blocked
    
    and the response should contain:
    1. the submitted values (mentioned above)
    2. ai_advice
    """
    access_token_1: str
    access_token_2: str

    def setUp(self):
        _, self.access_token_1 = create_sample_user_and_get_token(
            self.client, 'test_user')
        _, self.access_token_2 = create_sample_user_and_get_token(
            self.client, 'another_user')

    def test_create_sleep_report_should_success_1(self):
        response = self.client.post(
            self.ENDPOINT,
            {
                'slept_time': '20:30',
                'is_enough_sleep': True,
                'tiredness_level': 1
            },
            HTTP_AUTHORIZATION='Bearer ' + self.access_token_1,
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['slept_time'], '20:30')
        self.assertEqual(response.data['is_enough_sleep'], True)
        self.assertEqual(response.data['tiredness_level'], 1)
        self.assertIn('slept_date', response.data)
        self.assertIn('ai_advice', response.data)

    def test_create_sleep_report_should_success_2(self):
        response = self.client.post(
            self.ENDPOINT,
            {
                'slept_time': '20:30',
                'is_enough_sleep': True,
                'tiredness_level': 5
            },
            HTTP_AUTHORIZATION='Bearer ' + self.access_token_2,
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['slept_time'], '20:30')
        self.assertEqual(response.data['is_enough_sleep'], True)
        self.assertEqual(response.data['tiredness_level'], 5)
        self.assertIn('slept_date', response.data)
        self.assertIn('ai_advice', response.data)

    def test_two_users_create_sleep_report_should_success(self):
        response = self.client.post(
            self.ENDPOINT,
            {
                'slept_time': '20:30',
                'is_enough_sleep': True,
                'tiredness_level': 5
            },
            HTTP_AUTHORIZATION='Bearer ' + self.access_token_1,
        )
        self.assertEqual(response.status_code, 201)
        response = self.client.post(
            self.ENDPOINT,
            {
                'slept_time': '20:30',
                'is_enough_sleep': True,
                'tiredness_level': 5
            },
            HTTP_AUTHORIZATION='Bearer ' + self.access_token_2,
        )
        self.assertEqual(response.status_code, 201)

    def test_create_sleep_report_twice_should_fail(self):
        response = self.client.post(
            self.ENDPOINT,
            {
                'slept_time': '20:30',
                'is_enough_sleep': True,
                'tiredness_level': 5
            },
            HTTP_AUTHORIZATION='Bearer ' + self.access_token_1,
        )
        self.assertEqual(response.status_code, 201)
        response = self.client.post(
            self.ENDPOINT,
            {
                'slept_time': '20:30',
                'is_enough_sleep': True,
                'tiredness_level': 5
            },
            HTTP_AUTHORIZATION='Bearer ' + self.access_token_1,
        )
        self.assertEqual(response.status_code, 400)

    def test_wrong_formatted_slept_time_should_fail(self):
        response = self.client.post(
            self.ENDPOINT,
            {
                'slept_time': '20:30',
                'is_enough_sleep': 'abc',
                'tiredness_level': 3
            },
            HTTP_AUTHORIZATION='Bearer ' + self.access_token_1,
        )
        self.assertEqual(response.status_code, 400)

    def test_wrong_formatted_tiredness_level_should_fail_1(self):
        response = self.client.post(
            self.ENDPOINT,
            {
                'slept_time': '20:30',
                'is_enough_sleep': 'abc',
                'tiredness_level': -1
            },
            HTTP_AUTHORIZATION='Bearer ' + self.access_token_1,
        )
        self.assertEqual(response.status_code, 400)

    def test_wrong_formatted_tiredness_level_should_fail_2(self):
        response = self.client.post(
            self.ENDPOINT,
            {
                'slept_time': '20:30',
                'is_enough_sleep': 'abc',
                'tiredness_level': 8
            },
            HTTP_AUTHORIZATION='Bearer ' + self.access_token_1,
        )
        self.assertEqual(response.status_code, 400)

    def test_empty_string_request_should_fail(self):
        response = self.client.post(
            self.ENDPOINT,
            {
                'slept_time': '',
                'is_enough_sleep': '',
                'tiredness_level': '',
            },
            HTTP_AUTHORIZATION='Bearer ' + self.access_token_1,
        )
        self.assertEqual(400, response.status_code)

    def test_empty_body_request_should_fail(self):
        response = self.client.post(
            self.ENDPOINT,
            HTTP_AUTHORIZATION='Bearer ' + self.access_token_1,
        )
        self.assertEqual(400, response.status_code)

    def test_unauthorized_request_should_fail(self):
        response = self.client.post(self.ENDPOINT, {
            'slept_time': '20:30',
            'is_enough_sleep': True,
            'tiredness_level': 3
        })
        self.assertEqual(response.status_code, 401)


class TestRetrievingSleep(APITestCase):
    ENDPOINT = '/api/sleep'
    """
    The requesting endpoint should return response successfully only when:
    1. the user is authenticated

    and the response should contain following parameters:
    - id
    - owner(username)
    - slept_date
    - slept_time (with the format of %H:%M)
    - is_enough_sleep
    - used_phone_30_mins_before_sleep
    - tiredness_level
    - ai_advice
    """

    user_1: User
    access_token_1: str

    user_2: User
    access_token_2: str

    def setUp(self):
        self.user_1, self.access_token_1 = create_sample_user_and_get_token(
            self.client, 'test_user')
        self.user_2, self.access_token_2 = create_sample_user_and_get_token(
            self.client, 'another_user')

        # create fixtures
        Sleep.objects.create(owner=self.user_1,
                             slept_date=date(2021, 8, 27),
                             slept_time=time(8, 30),
                             is_enough_sleep=True,
                             used_phone_30_mins_before_sleep=True,
                             tiredness_level=1)

        Sleep.objects.create(owner=self.user_1,
                             slept_date=date(2021, 8, 28),
                             slept_time=time(8, 30),
                             is_enough_sleep=True,
                             used_phone_30_mins_before_sleep=True,
                             tiredness_level=3)

        Sleep.objects.create(owner=self.user_1,
                             slept_date=date(2021, 8, 29),
                             slept_time=time(8, 30),
                             is_enough_sleep=False,
                             used_phone_30_mins_before_sleep=True,
                             tiredness_level=5)

        Sleep.objects.create(owner=self.user_1,
                             slept_date=date(2021, 8, 30),
                             slept_time=time(8, 30),
                             is_enough_sleep=False,
                             used_phone_30_mins_before_sleep=False,
                             tiredness_level=4)

        Sleep.objects.create(owner=self.user_1,
                             slept_date=date(2021, 8, 27),
                             slept_time=time(8, 30),
                             is_enough_sleep=True,
                             used_phone_30_mins_before_sleep=True,
                             tiredness_level=1)

        Sleep.objects.create(owner=self.user_2,
                             slept_date=date(2021, 8, 28),
                             slept_time=time(8, 30),
                             is_enough_sleep=True,
                             used_phone_30_mins_before_sleep=True,
                             tiredness_level=3)

        Sleep.objects.create(owner=self.user_2,
                             slept_date=date(2021, 8, 29),
                             slept_time=time(8, 30),
                             is_enough_sleep=False,
                             used_phone_30_mins_before_sleep=True,
                             tiredness_level=5)

        Sleep.objects.create(owner=self.user_2,
                             slept_date=date(2021, 8, 30),
                             slept_time=time(8, 30),
                             is_enough_sleep=False,
                             used_phone_30_mins_before_sleep=False,
                             tiredness_level=4)

    def test_retreiving_sleep_should_success(self):
        sleep = Sleep.objects.filter(owner=self.user_1)[0]
        response = self.client.get(self.ENDPOINT + f"/{sleep.pk}",
                                   HTTP_AUTHORIZATION='Bearer ' +
                                   self.access_token_1)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['id'], sleep.pk)
        self.assertEqual(response.data['owner'], self.user_1.username)
        self.assertEqual(response.data['slept_time'], "08:30")
        self.assertIn('slept_date', response.data)
        self.assertIn('is_enough_sleep', response.data)
        self.assertIn('used_phone_30_mins_before_sleep', response.data)
        self.assertIn('tiredness_level', response.data)
        self.assertIn('ai_advice', response.data)

    def test_other_user_try_to_retrieve_sleep_should_fail(self):
        sleep = Sleep.objects.filter(owner=self.user_1)[0]
        response = self.client.get(self.ENDPOINT + f"/{sleep.pk}",
                                   HTTP_AUTHORIZATION='Bearer ' +
                                   self.access_token_2)
        self.assertEqual(response.status_code, 404)

    def test_unauthorized_request_should_fail(self):
        sleep = Sleep.objects.filter(owner=self.user_1)[0]
        response = self.client.get(self.ENDPOINT + f"/{sleep.pk}")
        self.assertEqual(response.status_code, 401)


class TestListingSleep(APITestCase):
    ENDPOINT = '/api/sleep'
    """
    The Sleep listing should return success fully only when:
    1. the user is authenticated

    and the response should contain following parameters:
    - id
    - owner(username)
    - slept_time (with the format of %H:%M)
    - is_enough_sleep
    - used_phone_30_mins_before_sleep
    - tiredness_level
    - ai_advice
    """

    user_1: User
    access_token_1: str

    user_2: User
    access_token_2: str

    def setUp(self):
        self.user_1, self.access_token_1 = create_sample_user_and_get_token(
            self.client, 'test_user')
        self.user_2, self.access_token_2 = create_sample_user_and_get_token(
            self.client, 'another_user')

        # create fixtures
        ## user 1 data

        Sleep.objects.create(owner=self.user_1,
                             slept_date=date(2021, 8, 21),
                             slept_time=time(8, 30),
                             is_enough_sleep=True,
                             used_phone_30_mins_before_sleep=True,
                             tiredness_level=1)

        Sleep.objects.create(owner=self.user_1,
                             slept_date=date(2021, 8, 22),
                             slept_time=time(8, 30),
                             is_enough_sleep=True,
                             used_phone_30_mins_before_sleep=True,
                             tiredness_level=1)

        Sleep.objects.create(owner=self.user_1,
                             slept_date=date(2021, 8, 23),
                             slept_time=time(8, 30),
                             is_enough_sleep=True,
                             used_phone_30_mins_before_sleep=True,
                             tiredness_level=1)

        Sleep.objects.create(owner=self.user_1,
                             slept_date=date(2021, 8, 24),
                             slept_time=time(8, 30),
                             is_enough_sleep=True,
                             used_phone_30_mins_before_sleep=True,
                             tiredness_level=3)

        Sleep.objects.create(owner=self.user_1,
                             slept_date=date(2021, 8, 25),
                             slept_time=time(8, 30),
                             is_enough_sleep=False,
                             used_phone_30_mins_before_sleep=True,
                             tiredness_level=5)

        Sleep.objects.create(owner=self.user_1,
                             slept_date=date(2021, 8, 26),
                             slept_time=time(8, 30),
                             is_enough_sleep=False,
                             used_phone_30_mins_before_sleep=False,
                             tiredness_level=4)

        Sleep.objects.create(owner=self.user_1,
                             slept_date=date(2021, 8, 27),
                             slept_time=time(8, 30),
                             is_enough_sleep=True,
                             used_phone_30_mins_before_sleep=True,
                             tiredness_level=1)

        Sleep.objects.create(owner=self.user_1,
                             slept_date=date(2021, 8, 28),
                             slept_time=time(8, 30),
                             is_enough_sleep=True,
                             used_phone_30_mins_before_sleep=True,
                             tiredness_level=3)

        Sleep.objects.create(owner=self.user_1,
                             slept_date=date(2021, 8, 29),
                             slept_time=time(8, 30),
                             is_enough_sleep=False,
                             used_phone_30_mins_before_sleep=True,
                             tiredness_level=5)

        Sleep.objects.create(owner=self.user_1,
                             slept_date=date(2021, 8, 30),
                             slept_time=time(8, 30),
                             is_enough_sleep=False,
                             used_phone_30_mins_before_sleep=False,
                             tiredness_level=4)

        ## user 2 data

        Sleep.objects.create(owner=self.user_2,
                             slept_date=date(2021, 8, 25),
                             slept_time=time(8, 30),
                             is_enough_sleep=True,
                             used_phone_30_mins_before_sleep=True,
                             tiredness_level=1)

        Sleep.objects.create(owner=self.user_2,
                             slept_date=date(2021, 8, 27),
                             slept_time=time(8, 30),
                             is_enough_sleep=True,
                             used_phone_30_mins_before_sleep=True,
                             tiredness_level=1)

        Sleep.objects.create(owner=self.user_2,
                             slept_date=date(2021, 8, 28),
                             slept_time=time(8, 30),
                             is_enough_sleep=True,
                             used_phone_30_mins_before_sleep=True,
                             tiredness_level=3)

        Sleep.objects.create(owner=self.user_2,
                             slept_date=date(2021, 8, 29),
                             slept_time=time(8, 30),
                             is_enough_sleep=False,
                             used_phone_30_mins_before_sleep=True,
                             tiredness_level=5)

        Sleep.objects.create(owner=self.user_2,
                             slept_date=date(2021, 8, 30),
                             slept_time=time(8, 30),
                             is_enough_sleep=False,
                             used_phone_30_mins_before_sleep=False,
                             tiredness_level=4)

    def test_list_sleep_should_success_1(self):
        sleeps_cnt = Sleep.objects.filter(owner=self.user_1).count()
        response = self.client.get(self.ENDPOINT,
                                   HTTP_AUTHORIZATION='Bearer ' +
                                   self.access_token_1)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), sleeps_cnt)

    def test_list_sleep_should_success_2(self):
        sleeps_cnt = Sleep.objects.filter(owner=self.user_2).count()
        response = self.client.get(self.ENDPOINT,
                                   HTTP_AUTHORIZATION='Bearer ' +
                                   self.access_token_2)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), sleeps_cnt)


class TestRetrievingToday(APITestCase):
    ENDPOINT = '/api/sleep/today'

    user_1: User
    access_token_1: str
    user_2: User
    access_token_2: str

    def setUp(self):
        self.user_1, self.access_token_1 = create_sample_user_and_get_token(
            self.client, 'test_user')
        self.user_2, self.access_token_2 = create_sample_user_and_get_token(
            self.client, 'another_user')

        # create fixtures
        ## user 1 data

        Sleep.objects.create(owner=self.user_1,
                             slept_date=datetime.today().date(),
                             slept_time=time(8, 30),
                             is_enough_sleep=True,
                             used_phone_30_mins_before_sleep=True,
                             tiredness_level=1)

    def test_is_today_reported_should_return_200(self):
        response = self.client.get(
            self.ENDPOINT,
            HTTP_AUTHORIZATION='Bearer ' + self.access_token_1,
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['owner'], self.user_1.username)
        self.assertEqual(response.data['is_enough_sleep'], True)
        self.assertEqual(response.data['used_phone_30_mins_before_sleep'],
                         True)
        self.assertEqual(response.data['tiredness_level'], 1)

    def test_is_today_reported_should_return_400(self):
        response = self.client.get(
            self.ENDPOINT,
            HTTP_AUTHORIZATION='Bearer ' + self.access_token_2,
        )
        self.assertEqual(response.status_code, 400)

    def test_is_today_reported_should_return_401(self):
        response = self.client.get(self.ENDPOINT)
        self.assertEqual(response.status_code, 401)