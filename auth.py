import sys, os
from uuid import uuid4
from django.conf import settings
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "vendor_management_system.settings")
django.setup()

from vendors.models import UserAutenticate


def create_user(username):
    token = str(uuid4())

    try:
        obj = UserAutenticate.objects.get(username=username)
        return obj.token
    except UserAutenticate.DoesNotExist:
        obj = UserAutenticate.objects.create(username=username, token=token)
        obj.save()

        return token


if __name__ == "__main__":
    token = create_user(sys.argv[1])
    print(token)
