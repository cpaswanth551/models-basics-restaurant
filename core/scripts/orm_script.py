from django.contrib.auth.models import User
from core.models import Restaurant, Rating, Sale, Staff
from django.utils import timezone
from django.db import connection
from pprint import pprint
import random


def run():
    staff, created = Staff.objects.get_or_create(name="Tony Stark")

    print(staff)

    staff.restaurants.set(
        Restaurant.objects.all()[:10],
        through_defaults={"salary": random.randint(20_000, 80_000)},
    )
