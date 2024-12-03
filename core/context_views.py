from django.shortcuts import render

from django.contrib.contenttypes.models import ContentType

from core.models import Rating

from django.shortcuts import render
from django.contrib.contenttypes.models import ContentType
from core.models import (
    Rating,
)  # Replace 'core.models' with your actual app's path if different


def index(request):
    """
    View to demonstrate the usage of Django's ContentType framework.

    This function showcases:
    - Retrieving all ContentType objects.
    - Filtering ContentType objects for a specific app.
    - Accessing a model class dynamically from a ContentType object.
    - Querying data and retrieving specific instances of a model using ContentType.
    - Getting the ContentType for a specific model.

    ContentType is a powerful tool for creating generic, dynamic, and reusable code
    across Django models. It is especially useful for generic relationships, dynamic
    querying, and building custom permission systems.


    """
    context = {}

    # Retrieve all ContentType objects (each represents a model in project)
    context_text = ContentType.objects.all()
    print("All ContentType objects:", context_text)

    # Filter ContentType objects for models within the 'core' app
    context_text = ContentType.objects.filter(app_label="core")
    print("ContentType objects in the 'core' app:", context_text)

    # Get a specific ContentType object for the 'restaurant' model in the 'core' app
    context_text = ContentType.objects.get(app_label="core", model="restaurant")
    print("ContentType for 'core.restaurant':", context_text)

    # Access the actual model class from the ContentType object
    rst_model = context_text.model_class()
    print("All objects of the 'Restaurant' model:", rst_model.objects.all())

    # Retrieve a specific object of the 'Restaurant' model using ContentType
    rst_model = context_text.get_object_for_this_type(name="Bombay Bustle")
    print("Restaurant object retrieved dynamically:", rst_model)
    print("Latitude of the restaurant:", rst_model.latitude)

    # Get the ContentType object for the 'Rating' model
    rating_context_text = ContentType.objects.get_for_model(Rating)
    print("ContentType for the 'Rating' model:", rating_context_text)
    print("App label of 'Rating':", rating_context_text.app_label)
    print("Model name for 'Rating':", rating_context_text.model)

    return render(request, "index.html", context)
