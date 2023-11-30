from rest_framework.authentication import BaseAuthentication
from vendors.models import UserAutenticate
from django.http import JsonResponse


class HeaderAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get("Token")

        if not request.method == "GET":
            try:
                user, token = auth_header.split()
                user = UserAutenticate.objects.get(username=user, token=token)
            except:
                # raise AuthenticationFailed('Invalid token')
                return JsonResponse(
                    {"status": "error", "message": "autherozation required"}
                )

            return user, None

        return None
