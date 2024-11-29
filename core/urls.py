from django.urls import path
from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("order/", views.order_product, name="order-product"),
]
