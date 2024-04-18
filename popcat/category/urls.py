from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("categorysearch/", views.category_search, name="category_search"),
    path("test/", views.average_price_by_categories.as_view(), name="average_price_by_categories"),
    path("api_chart/<str:category>/<str:date>",views.Category_chart_by_game.as_view(),name="category_chart_by_game"),
    path("api_chart/<str:date>",views.Category_chart.as_view(),name="category_chart_by_search_api"),
]
