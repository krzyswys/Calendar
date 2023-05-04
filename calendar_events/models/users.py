from django.db import models
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
import calendar_events.models as md
import exceptions as e


class Users(models.Model):
    user_id = models.BigAutoField(primary_key=True)
    login = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.login

    @staticmethod
    def create_user(login: str):
        if login is None:
            raise e.NoDataGiven("Login cannot be None")

        user = Users()
        user.login = login

        try:
            user.save()
            return user
        except IntegrityError:
            raise e.EntityAlreadyExists("User with specified login already exists")

    @staticmethod
    def get_user(user_id: int = None, login: str = None):
        if user_id is None and login is None:
            raise e.NoDataGiven("Need to specify id or login")

        try:
            if user_id is not None:
                return Users.objects.get(user_id=user_id)
            else:
                return Users.objects.get(login=login)
        except ObjectDoesNotExist:
            raise e.EntityNotFound("Cannot find specified user")

    def modify(self, new_login: str):
        if new_login is None:
            raise e.NoDataGiven("Login cannot be None")

        self.login = new_login

        try:
            self.save()
            return self
        except IntegrityError:
            raise e.EntityAlreadyExists("User with specified login already exists!")
