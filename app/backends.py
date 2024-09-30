""""
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model

from myretrogamelist import settings

User = get_user_model()


class AuthBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(username=username)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None


class AuthenticationBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None):
            login_valid = settings.ADMIN_LOGIN == username
            pwd_valid = User.check_password(password, settings.ADMIN_PASSWORD)
            if login_valid and pwd_valid:
                try:
                    user = User.objects.get(username=username)
                except User.DoesNotExist:
                    # Create a new user. There's no need to set a password
                    # because only the password from settings.py is checked.
                    user = User(username=username)
                    user.is_staff = True
                    user.is_superuser = True
                    user.save()
                return user
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

"""