from django.contrib.auth import get_user_model
import random

User = get_user_model()


def create_username(email):
    username = email + '#' + str(random.randint(1000, 9999))

    if User.objects.filter(username=username).exists():
        create_username(email)

    return username
