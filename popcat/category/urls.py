from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("categorysearch", views.category_search, name="category_search"),
    path("test/", views.average_price_by_categories, name="average_price_by_categories"),
]
