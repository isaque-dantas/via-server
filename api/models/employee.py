from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models


class EmployeeManager(BaseUserManager):
    @staticmethod
    def create_user(name: str, email: str, password: str):
        user = Employee.objects.model(
            email=Employee.objects.normalize_email(email),
            name=name
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


class Employee(AbstractBaseUser):
    name = models.CharField(max_length=128, blank=False)
    email = models.EmailField(unique=True, blank=False)

    objects = EmployeeManager()
    USERNAME_FIELD = 'email'
