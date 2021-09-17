from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models


# Create your models here.

class User(AbstractUser):
    NORTH = "North"
    SOUTH = "South"
    EAST = "East"
    WEST = "West"

    FEMALE = "Female"
    MALE = "Male"

    INCOME_CHOICE = (
        ("0-$25K", "0-$25K"),
        ("$25K-$70k", "$25K-$70k"),
        (">$70K", ">$70K"),
    )
    REGION_CHOICE = (
        (NORTH, NORTH),
        (EAST, EAST),
        (SOUTH, SOUTH),
        (WEST, WEST),
    )

    GENDER_CHOICE = (
        (MALE, MALE),
        (FEMALE, FEMALE),
    )
    gender = models.CharField(max_length=200, choices=GENDER_CHOICE, )
    income_group = models.CharField(max_length=200, choices=INCOME_CHOICE, )
    region = models.CharField(max_length=200, choices=REGION_CHOICE, )
    marital_status = models.BooleanField(default=False)
    objects = UserManager()

    USERNAME_FIELD = "username"

    is_authenticated = True
    is_anonymous = False

    def __str__(self):
        return self.username
