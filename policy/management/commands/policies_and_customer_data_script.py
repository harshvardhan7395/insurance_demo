import csv
import datetime

from django.core.management import BaseCommand, CommandError
from django.db import transaction

from policy.models import Policy
from users.models import User


class Command(BaseCommand):
    help = "load tags data"

    def handle(self, *args, **kwargs):
        with transaction.atomic():
            try:
                with open("Data Set - Insurance Client.csv", "r") as file:
                    next(file)
                    reader = csv.reader(file)

                    for row in reader:
                        policy_id = int(row[0])
                        customer_id = int(row[2])

                        date_of_purchase = None
                        if row[1] == "":
                            date_of_purchase = datetime.datetime.now()
                        else:
                            date_of_purchase = datetime.datetime.strptime(
                                row[1], "%m/%d/%Y"
                            )
                        fuel_segment = None
                        if row[3] == "CNG":
                            fuel_segment = Policy.CNG
                        elif row[3] == "Petrol":
                            fuel_segment = Policy.PETROL
                        else:
                            fuel_segment = Policy.DIESEL

                        vehicle_segment = None
                        if row[4] == "A":
                            vehicle_segment = Policy.A
                        elif row[4] == "B":
                            vehicle_segment = Policy.B
                        else:
                            vehicle_segment = Policy.C

                        premium = int(row[5])
                        bodily_injury_libality = True if int(row[6]) == 1 else False
                        personal_injury_protection = True if int(row[7]) == 1 else False
                        property_damage_liability = True if int(row[8]) == 1 else False
                        collision = True if int(row[9]) == 1 else False
                        comprehensive = True if int(row[10]) == 1 else False

                        gender = None
                        if row[11] == "Male":
                            gender = User.MALE
                        else:
                            gender = User.FEMALE
                        income_group = None
                        print(row[12])
                        if row[12] == "0- $25K":
                            income_group = "0-$25K"
                        elif row[12] == "$25-$70K":
                            income_group = "$25K-$70k"
                        else:
                            income_group = ">$70K"
                        region = None
                        if row[13] == "North":
                            region = User.NORTH
                        elif row[13] == "South":
                            region = User.SOUTH
                        elif row[13] == "East":
                            region = User.EAST
                        else:
                            region = User.WEST
                        marital_status = True if int(row[14]) == 1 else False
                        existing_user=0
                        user = User.objects.filter(id=customer_id)
                        if user:
                            existing_user=1
                            # print(user)
                        else:
                            new_user = User()
                            new_user.id = customer_id
                            new_user.username = customer_id
                            new_user.gender = gender
                            new_user.income_group = income_group
                            new_user.marital_status = marital_status
                            new_user.region = region
                            new_user.save()
                            # print(new_user)
                            user=new_user
                            print("created user")

                        policy = Policy()
                        policy.id = policy_id
                        policy.date_of_purchase = date_of_purchase
                        policy.bodily_injury_liability = bodily_injury_libality
                        policy.personal_injury_protection = personal_injury_protection
                        policy.property_damage_liability = property_damage_liability
                        policy.collision = collision
                        policy.comprehensive = comprehensive
                        policy.premium = premium
                        policy.vehicle_segment = vehicle_segment
                        policy.fuel = fuel_segment
                        policy.customer = user.first() if existing_user ==1 else user
                        policy.save()
            except Exception as e:
                raise CommandError(e)
