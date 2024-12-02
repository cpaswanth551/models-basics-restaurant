from django.contrib import admin
from core.models import (
    Restaurant,
    Sale,
    Rating,
    Staff,
    StaffRestaurant,
    Product,
    Order,
    Comment,
)


# Register your models here.
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]


class RatingAdmin(admin.ModelAdmin):
    list_display = ["id", "rating"]


class CommentAdmin(admin.ModelAdmin):
    list_display = ["id", "content_type", "object_id"]


admin.site.register(Restaurant, RestaurantAdmin)
admin.site.register(Sale)
admin.site.register(Rating, RatingAdmin)
admin.site.register(Staff)
admin.site.register(StaffRestaurant)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(Comment, CommentAdmin)
