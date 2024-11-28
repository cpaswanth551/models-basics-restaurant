from django.contrib.auth.models import User
from core.models import Restaurant, Rating, Sale
from django.utils import timezone
from django.db import connection
from pprint import pprint
from django.db.models.functions import Lower


def run():
    # enter code below
    print(Restaurant.objects.count())
    print(Rating.objects.count())
    print(Sale.objects.count())

    chinese = Restaurant.TypeChoices.CHINESE
    indian = Restaurant.TypeChoices.INDIAN
    mexican = Restaurant.TypeChoices.MEXICAN
    check_choice = [chinese, indian, mexican]

    rest = Restaurant.objects.filter(restaurant_type__in=check_choice)

    rest = Restaurant.objects.filter(name__startswith="C")
    rest = Restaurant.objects.exclude(restaurant_type=chinese)
    rest = Restaurant.objects.exclude(restaurant_type__in=[indian, chinese])
    rest = Restaurant.objects.filter(name__lte="E")
    sale = Sale.objects.filter(income__range=(50, 60))
    rest = Restaurant.objects.order_by("-name")
    rest = Restaurant.objects.order_by(Lower("name"))
    rest = Restaurant.objects.order_by("date_opened")  

    print(rest, sale)

    pprint(connection.queries)
