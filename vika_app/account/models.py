import datetime

from django.contrib.auth.models import (
    AbstractBaseUser,
    AbstractUser,
    BaseUserManager,
    Permission,
    PermissionsMixin,
)
from django.db import models
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumber, PhoneNumberField


class UserManager(BaseUserManager):
    def create_user(
        self, phone, password=None, is_staff=False, is_active=True, **extra_fields
    ):
        extra_fields.pop("username", None)
        extra_fields.pop("email", None)

        user = self.model(
            phone=phone, is_active=is_active, is_staff=is_staff, **extra_fields
        )

        if password:
            user.set_password(password)
        user.save()

        return user

    def create_superuser(self, phone, password=None, **extra_fields):
        return self.create_user(
            phone, password, is_staff=True, is_superuser=True, **extra_fields
        )

    def staff(self):
        return self.get_queryset().filter(is_staff=True)


class User(AbstractBaseUser, PermissionsMixin):
    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    class UserType:
        USER = "0"
        TRAINER = "1"
        MANAGER = "2"

        choices = (
            (USER, "Пользователь"),
            (TRAINER, "Тренер"),
            (MANAGER, "Управляющий"),
        )

    class UserGender:
        MAN = "0"
        WOMAN = "1"

        choices = (
            (MAN, "Мужской"),
            (WOMAN, "Женский"),
        )

    username = None
    name = models.CharField("Имя пользователя", max_length=100, blank=True, null=True)
    phone = PhoneNumberField("Номер телефона", db_index=True, unique=True)
    user_type = models.CharField(
        "Тип пользователя",
        max_length=1,
        choices=UserType.choices,
        default=UserType.USER,
    )
    gender = models.CharField(
        "Пол", max_length=1, blank=True, choices=UserGender.choices, null=True
    )
    age = models.IntegerField("Возраст", null=True, blank=True)
    is_staff = models.BooleanField("Статус персонала", default=False)
    is_active = models.BooleanField("Активный", default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        if self.user_type == User.UserType.MANAGER:
            return f"Управляющий {self.name}"
        elif self.user_type == User.UserType.TRAINER:
            return f"Тренер {self.name}"
        elif self.user_type == User.UserType.USER:
            return f"{self.name}"
