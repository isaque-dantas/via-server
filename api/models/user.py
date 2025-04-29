from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models


class UserManager(BaseUserManager):
    @staticmethod
    def create_user(name: str, email: str, password: str, role: str):
        user = User.objects.model(
            email=User.objects.normalize_email(email),
            name=name,
            role=role
        )

        user.set_password(password)
        user.is_active = True
        user.is_staff = False

        user.save()

        return user

    def create_superuser(self, **data):
        user = self.create_user(**data)

        user.is_staff = True
        user.is_superuser = True
        user.save()

        return user


class User(AbstractBaseUser):
    class Role(models.TextChoices):
        SELLER = 'vendedor'
        CLIENT = 'cliente'

    name = models.CharField(max_length=128, blank=False)
    email = models.EmailField(max_length=128, unique=True, blank=False)
    role = models.CharField(max_length=8, choices=Role)

    objects = UserManager()
    USERNAME_FIELD = 'email'
