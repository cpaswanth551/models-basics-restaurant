from datetime import timezone, datetime, timedelta
import itertools
import random
from django.shortcuts import render
from django.db.models.functions import Lower, Length, Concat, Coalesce
from django.db.models import (
    Count,
    Avg,
    Max,
    Min,
    Sum,
    CharField,
    Value,
    F,
    Q,
    Case,
    When,
)
from .forms import RestaurantForm
from core.models import Restaurant, Rating, Sale, Staff, StaffRestaurant
from django.utils import timezone as tz


# Create your views here.
def index_form(request):
    if request.method == "POST":
        form = RestaurantForm(request.POST or None)
        if form.is_valid():
            print(form.cleaned_data)
        else:
            return render(request, "index.html", {"form": form})
    context = {"form": RestaurantForm()}
    return render(request, "index.html", context)


def index_prefect_related(request):
    rest_ = Restaurant.objects.all()  # will take 15 queries
    rest__ = Restaurant.objects.prefetch_related("ratings")  # takes 2 queries.
    rest = Restaurant.objects.filter(name__istartswith="P").prefetch_related("ratings")
    context = {"restaurant": rest}
    return render(request, "index.html", context)


def index_select_related(request):
    rating = Rating.objects.all()  # taking 31 queries
    rating_sr = Rating.objects.only("rating", "restaurant__name").select_related(
        "restaurant"
    )  # only took 1 query
    context = {"ratings": rating_sr}
    return render(request, "index.html", context)


def index_m2m(request):
    staff, created = Staff.objects.get_or_create(name="Aswanth CP")
    print(staff.restaurant.all())
    staff.restaurant.add(Restaurant.objects.first())  # adding new m2m relations
    staff.restaurant.set(Restaurant.objects.all()[0:10])  # slicing 0 to <10
    print(staff.restaurant.all())
    staff.restaurant.remove(Restaurant.objects.first())  # removing new m2m relations
    staff.restaurant.set(Restaurant.objects.all())  # sets all restaurant to the staff
    staff.restaurant.clear()  # remove all relations
    italian = staff.restaurant.filter(
        restaurant_type=Restaurant.TypeChoices.ITALIAN
    )  # filtering
    print(staff.restaurant.count())  # counts of all relations

    rest = Restaurant.objects.first()  # reverse accessing
    staff = rest.staff_set.all()
    return render(request, "index.html")


def index_m2m_through(request):
    context = {}
    staff = Staff.objects.first()
    rest = Restaurant.objects.first()
    rest2 = Restaurant.objects.last()
    staff_rest = StaffRestaurant.objects.create(
        staff=staff, restaurant=rest, salary=24_000
    )  # adding element to m2m through staffRestaurant model
    staff.restaurants.add(
        rest, through_defaults={"salary": 28_000}
    )  # alternate way to add staff restaurant

    return render(request, "index.html", context)


def index_m2m_query(request):
    context = {}
    jobs = (
        StaffRestaurant.objects.all()
    )  # here we are having total of 23 queries when try to use this query technique

    for job in jobs:
        print(job.restaurant)
        print(job.staff)

    # same thing will optimized using prefetch query
    jobs = StaffRestaurant.objects.prefetch_related("restaurant", "staff")

    for job in jobs:
        print(job.restaurant)
        print(job.staff)

    return render(request, "index.html", context)


def index_values(request):
    context = {}
    restaurant = Restaurant.objects.values("name")  # here the values will a dict output
    restaurant2 = Restaurant.objects.values(name_lower=Lower("name"))[:5]
    rst3 = Restaurant.objects.values("name", "date_opened")

    IT = Restaurant.TypeChoices.ITALIAN
    rating = Rating.objects.filter(restaurant__restaurant_type=IT).values(
        "rating", "restaurant__name"
    )  # here we can access the related restaurant element of rating  model using values.
    print(rating)
    return render(request, "index.html", context)


def index_values_list(request):
    context = {}
    restaurant = Restaurant.objects.values_list(
        "name"
    )  # her the values are given in tuples.

    restaurant = Restaurant.objects.values_list(
        "name", flat=True
    )  # here the values are given in list

    print(restaurant)
    return render(request, "index.html", context)


def index_aggregate(request):
    context = {}
    ret_count = Restaurant.objects.count()
    print(ret_count)

    rest = Restaurant.objects.aggregate(total=Count("id"))
    print(rest)

    rest_avg = Rating.objects.aggregate(avg=Avg("rating"))
    print(rest_avg)

    rest_avg1 = Rating.objects.filter(restaurant__name__startswith="p").aggregate(
        avg=Avg("rating")
    )
    print(rest_avg1)

    sale_icome_max = Sale.objects.aggregate(max=Max("income"))
    sale_icome_min = Sale.objects.aggregate(min=Min("income"))
    sale_icome = Sale.objects.aggregate(
        min=Min("income"), max=Max("icome"), avg=Avg("income"), sum=Sum("income")
    )
    print(sale_icome_max, sale_icome_min)

    one_month_ago = datetime.now() - timedelta(days=31)
    sales = Sale.objects.filter(datetime__gte=one_month_ago)
    sale_icome = sales.aggregate(
        min=Min("income"), max=Max("income"), avg=Avg("income"), sum=Sum("income")
    )
    print(sale_icome)

    return render(request, "index.html", context)


def index_annotate(request):
    context = {}
    restaurant = Restaurant.objects.annotate(name_len=Length("name"))
    restaurant1 = Restaurant.objects.annotate(name_len=Length("name")).filter(
        name_len__gte=10
    )
    print(restaurant1.values("name", "name_len"))

    return render(request, "index.html", context)


def index_annotate_ex(request):
    context = {}
    concatenation = Concat(
        "name",
        Value(" [Rating: "),
        Avg("ratings__rating"),
        Value("]"),
        output_field=CharField(),
    )
    rest = Restaurant.objects.annotate(
        message=concatenation
    )  #  addes {"message" : "Pizzeria 2 [Rating: 3.0]"}
    for r in rest:
        print(r.message)

    rest_total_sales = Restaurant.objects.annotate(
        total_sales=Sum("sales__income")
    ).values("name", "total_sales")

    rest_count = Restaurant.objects.annotate(
        num_rating=Count("ratings__rating")
    ).values("name", "num_rating")

    rest_count_with_avg = Restaurant.objects.annotate(
        num_rating=Count("ratings__rating"), avg_rating=Avg("ratings__rating")
    ).values("name", "num_rating", "avg_rating")

    rest_count_with_groupby_rest_type = Restaurant.objects.values(
        "restaurant_type"
    ).annotate(
        num_rating=Count("ratings__rating")
    )  # This will give distinct restaurant_type rating count

    print([r["total_sales"] for r in rest_count])
    rest_sales_total = Restaurant.objects.annotate(
        total_sales=Sum("sales__income")
    ).order_by("total_sales")

    for r in rest_sales_total:
        print(r.total_sales)

    rest_sales_total = Restaurant.objects.annotate(
        total_sales=Sum("sales__income")
    ).order_by("total_sales")

    print(rest_sales_total.aggregate(avg_sales=Avg("total_sales")))

    return render(request, "index.html", context)


def index_F_object(request):
    context = {}
    rating = Rating.objects.filter(rating=2).first()
    rating.rating += 1
    rating.rating = F("rating") + 1
    rating_ = Rating.objects.update(rating=F("rating") * 2)  # multiplying rating by 2

    sales = Sale.objects.filter(expenditure__gt=F("income"))  # filter

    sales = (
        Sale.objects.annotate(profit=F("income") - F("expenditure"))
        .values("profit")
        .order_by("-profit")
    )  # using annotate

    sales = Sale.objects.aggregate(
        profit=Count("id", filter=Q(income__gt=F("expenditure"))),
        loss=Count("id", filter=Q(income__lt=F("expenditure"))),
    )  # aggregate

    return render(request, "index.html", context)


def index_bulk_update(request):
    context = {}

    sales = Sale.objects.all()
    for sale in sales:
        sale.expenditure = random.uniform(5, 100)

    Sale.objects.bulk_update(sales, ["expenditure"])

    return render(request, "index.html", context)


def index_Q(request):
    context = {}
    print
    sales = Sale.objects.aggregate(
        profit=Count("id", filter=Q(income__gt=F("expenditure"))),
        loss=Count("id", filter=Q(income__lt=F("expenditure"))),
    )

    print(Restaurant.objects.filter(name__icontains="1"))

    print(Restaurant.objects.filter(name__iendswith="1"))

    it_or_max = Q(name__icontains="italian") | Q(name__icontains="mexican")
    recently_opened = Q(date_opened__gt=tz.now() - tz.timedelta(days=40))
    restaurant = Restaurant.objects.filter(it_or_max | recently_opened)

    #  not  coditions
    it_or_max = Q(name__icontains="italian") | Q(name__icontains="mexican")
    not_recently_opened = ~Q(date_opened__gt=tz.now() - tz.timedelta(days=40))
    restaurant = Restaurant.objects.filter(it_or_max | not_recently_opened)

    # complex
    # 1 - name containing number  (or/and)
    # 2 - profit - income - expediture

    name_has_num = Q(restaurant__name__regex=r"[0-9]+")
    profited = Q(income__gt=F("expenditure"))

    sales1 = Sale.objects.filter(name_has_num | profited)
    sales2 = Sale.objects.select_related("restaurant").filter(
        name_has_num | profited
    )  # if have any related objects
    for sale in sales:
        print(sale.restaurant.name)

    return render(request, "index.html", context)


def index_coalesce(request):
    context = {}
    print(Restaurant.objects.aggregate(total_sum=Coalesce(Sum(F("capacity")), 0)))

    print(
        Rating.objects.filter(rating__lt=0).aggregate(
            total=Coalesce(Avg("rating"), 0.0)
        )
    )

    # using with annotate
    print(
        Restaurant.objects.annotate(
            name_value=Coalesce(F("nickname"), F("name"))
        ).values("name_value")
    )

    return render(request, "index.html", context)


def index_conditional_case_when(request):
    context = {}

    italian = Restaurant.TypeChoices.ITALIAN

    rests = Restaurant.objects.annotate(
        is_italian=Case(When(restaurant_type=italian, then=True), default=False)
    )
    for rest in rests:
        if rest.is_italian:
            print(rest)

    # more complex queries

    # - taking counts of sales from Sale table to Restaurant object and annotating it to get count of sales
    # - then checking if restaurant is popular or not

    restaurant = Restaurant.objects.annotate(nsales=Count("sales"))

    restaurants = restaurant.annotate(
        is_popular=Case(When(nsales__gte=8, then=True), default=False)
    ).values("nsales", "is_popular")

    print(restaurants.filter(is_popular=True))

    # multiple conditions

    # - ratings > 3.5 and num_rating > 1

    restaurants = Restaurant.objects.annotate(
        avg=Avg("ratings__rating"), num_ratings=Count("ratings__pk")
    )

    restaurants = restaurants.annotate(
        highly_rated=Case(
            When(avg__gt=3.5, num_ratings__gt=1, then=True), default=False
        )
    )
    print(restaurants.filter(highly_rated=True))

    # complex - query to generate restaurant based on continents
    restaurants = Restaurant.objects.annotate(
        avg=Coalesce(Avg("ratings__rating"), 0.0), num_ratings=Count("ratings__pk")
    )
    print(restaurants.values("avg"))

    restaurants = restaurants.annotate(
        rating_bucket=Case(
            When(avg__gt=3.5, then=Value("Highly rated")),
            When(avg__range=(2.5, 3.5), then=Value("Average rated")),
            When(avg__lt=2.5, then=Value("Low rated")),
        )
    )
    print(restaurants.filter(rating_bucket="Average rated"))

    # complex

    type = Restaurant.TypeChoices
    asian = Q(restaurant_type=type.CHINESE) | Q(restaurant_type=type.INDIAN)
    mexican = Q(restaurant_type=type.MEXICAN)
    europe = Q(restaurant_type=type.ITALIAN) | Q(restaurant_type=type.GREEK)

    restaurants = Restaurant.objects.annotate(
        continent=Case(
            When(
                asian,
                then=Value("asian"),
            ),
            When(mexican, then=Value("north america")),
            When(
                europe,
                then=Value("europe"),
            ),
            default=Value("N/A"),
        )
    )

    print(restaurants.filter(continent="europe"))

    #  total sales of 10 days interval  (1-10,11-20,21-30)
    first_sales = Sale.objects.aggregate(first_sale_date=Min("datetime"))[
        "first_sale_date"
    ]
    last_sales = Sale.objects.aggregate(last_sale_date=Max("datetime"))[
        "last_sale_date"
    ]

    dates = []
    count = itertools.count()

    while (
        dt := first_sales + tz.timedelta(days=10 * next(count))
    ) <= last_sales:  # Walrus opertions
        dates.append(dt)

    whens = [
        When(datetime__range=(dt, dt + tz.timedelta(days=10)), then=Value(dt.date()))
        for dt in dates
    ]

    case = Case(*whens, output_field=CharField())

    print(
        Sale.objects.annotate(daterange=case)
        .values("daterange")
        .annotate(total_sales=Sum("income"))
    )

    return render(request, "index.html", context)


def index(request):
    context = {}

    return render(request, "index.html", context)
