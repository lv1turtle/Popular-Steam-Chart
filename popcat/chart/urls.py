from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("api/tag/", views.RankByTagAPIView.as_view(), name="tag_api"),
    path("tag/", views.TagView.as_view(), name="tag"),
    path("buyers/", views.NumOfBuyers, name="NumOfBuyers"),
    path("api/barchart/", views.BarChartAPIView.as_view(), name="barchart_api"),
    path("test/", views.postreviewsData, name="get_data"),
    path("main/", views.main, name="main_page")
]
