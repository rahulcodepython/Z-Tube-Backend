from django.conf import settings
from django.shortcuts import redirect
from django.core.exceptions import ValidationError
from urllib.parse import urlencode
from typing import Dict, Any
import requests
from . import models, create_username

GOOGLE_ACCESS_TOKEN_OBTAIN_URL = 'https://oauth2.googleapis.com/token'
GOOGLE_USER_INFO_URL = 'https://www.googleapis.com/oauth2/v3/userinfo'
LOGIN_URL = f'{settings.BASE_APP_URL}/auth/login'


def google_get_access_token(code: str, redirect_uri: str) -> str:
    try:
        data = {
            'code': code,
            'client_id': settings.GOOGLE_OAUTH2_CLIENT_ID,
            'client_secret': settings.GOOGLE_OAUTH2_CLIENT_SECRET,
            'redirect_uri': redirect_uri,
            'grant_type': 'authorization_code'
        }

        response = requests.post(GOOGLE_ACCESS_TOKEN_OBTAIN_URL, data=data)

        access_token = response.json()['access_token']

        return access_token

    except Exception as e:
        raise ValidationError('Could not get access token from Google.')


def google_get_user_info(access_token: str) -> Dict[str, Any]:
    response = requests.get(
        GOOGLE_USER_INFO_URL,
        params={'access_token': access_token}
    )

    if not response.ok:
        raise ValidationError('Could not get user info from Google.')

    return response.json()


def get_user_data(validated_data):
    redirect_uri = f'{settings.BASE_API_URL}/auth/google/'

    code = validated_data.get('code')
    error = validated_data.get('error')

    if error or not code:
        params = urlencode({'error': error})
        return redirect(f'{LOGIN_URL}?{params}')

    access_token = google_get_access_token(
        code=code, redirect_uri=redirect_uri)
    user_data = google_get_user_info(access_token=access_token)

    if models.User.objects.filter(email=user_data['email']).exists():
        return user_data['email']

    models.User.objects.create(
        username=create_username.create_username(user_data['email'].split(
            '@')[0]),
        email=user_data['email'],
        first_name=user_data.get('given_name'),
        last_name=user_data.get('family_name')
    )
    models.Profile.objects.create(
        user=models.User.objects.get(email=user_data['email']),
        tags=[]
    )

    return user_data['email']
