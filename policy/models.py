from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.db import models


# Create your models here.

def validate_premium(value):
    if value > 1000000:
        raise ValidationError(
            _('Premium cannot be more than 1 million')
        )


class Policy(models.Model):
    CNG = "CNG"
    PETROL = "Petrol"
    DIESEL = "Diesel"

    A = "A"
    B = "B"
    C = "C"

    FEMALE = "Female"
    MALE = "Male"

    NORTH = "North"
    SOUTH = "South"
    EAST = "East"
    WEST = "West"

    GENDER_CHOICE = (
        (MALE, MALE),
        (FEMALE, FEMALE),
    )

    FUEL_CHOICES = (
        (CNG, CNG),
        (PETROL, PETROL),
        (DIESEL, DIESEL),
    )
    SEGMENT_CHOICE = (
        (A, A),
        (B, B),
        (C, C),
    )
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

    customer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="customer",
        on_delete=models.CASCADE,
    )
    bodily_injury_liability = models.BooleanField()
    personal_injury_protection = models.BooleanField()
    property_damage_liability = models.BooleanField()
    collision = models.BooleanField()
    comprehensive = models.BooleanField()
    premium = models.IntegerField(validators=[validate_premium])
    vehicle_segment = models.CharField(max_length=200, choices=SEGMENT_CHOICE)
    fuel = models.CharField(max_length=200, choices=FUEL_CHOICES)
    date_of_purchase = models.DateTimeField()
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.premium)
