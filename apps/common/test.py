from datetime import time
import typing
from apps.user.models import User


def create_sample_user_and_get_token(api_client, username) -> typing.List:
    user: User = User.objects.create_user(username=username,
                                          name="홍길동",
                                          weight_kg=0,
                                          average_sleep_time=time(00, 00),
                                          bedtime_starts_at=time(00, 00),
                                          password='thePas123Q')
    response = api_client.post(
        '/api/token',
        {
            'username': username,
            'password': 'thePas123Q',
        },
    )
    return (user, response.data['access'])