from django.http import HttpResponse
from django.shortcuts import render
from chart.models import *
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import F

def category_search(request):
    games = Game.objects.all()
    # 모든 게임의 카테고리 목록 가져오기
    categories_list = set()
    for game in games:
        categories_list.update(game.get_categories_list())
    categories_list = list(categories_list)

    selected_games = []
    selected_categories = None

    if "category" in request.GET:
        selected_categories = request.GET.getlist("category")
        # 선택한 각 카테고리에 해당하는 게임들 가져오기
        selected_games_lists = [
            set(
                Game.objects.filter(categories__icontains=category).values_list(
                    "game_name", flat=True
                )
            )
            for category in selected_categories
        ]
        # 선택한 카테고리들의 게임들을 모두 포함하는 게임 찾기
        if selected_games_lists:
            selected_games = selected_games_lists[0].intersection(*selected_games_lists)

    context = {
        "categories_list": categories_list,
        "selected_games": selected_games,
        "selected_categories": selected_categories,
    }
    return render(request, "category/category_search.html", context)


class average_price_by_categories(APIView):

    def get(self, request):
        return render(request, "category/categoryChart.html")


class Category_chart(APIView):
    def get(self, request, *args, **kwargs):
        date = kwargs.get("date")
        if not date:
            date = timezone.now().date()
        # 검색
        game_list = (
            TopSellers.objects.filter(created_at__contains=date)
            .annotate(
                game_name=F("game__game_name"),  # game의 game_name 필드를 가져옴
                game_price=F("game__price"),  # game의 price 필드를 가져옴
                game_categories=F(
                    "game__categories"
                ),  # game의 categories 필드를 가져옴
            )
            .values(
                "game_name",
                "game_price",
                "game_categories",  # 필요한 필드 선택
            )[:100]
        )
        # game_list =  Game.objects.filter(categories__contains=category)[:100]
        category_Total_price_dict = {}
        # 카테고리별 가격
        for i in game_list:
            categories = [
                category.strip() for category in i["game_categories"].split(",")
            ]
            for category in categories:
                category_Total_price_dict[category] = category_Total_price_dict.get(
                    category, [0, 0, 0]
                )
                category_Total_price_dict[category][0] += i["game_price"]
                category_Total_price_dict[category][1] += 1

        chart_data = []
        # 카테고리별 평균값 및 차트세팅
        if category_Total_price_dict:
            for category in category_Total_price_dict:
                category_Total_price_dict[category][2] = (
                    category_Total_price_dict[category][0]
                    // category_Total_price_dict[category][1]
                )
                chart_data.append(
                    {"name": category, "y": category_Total_price_dict[category][2]}
                )
        else:
            chart_data.append({"None": 0})

        data = {"chart_data": chart_data}
        return Response(data)


class Category_chart_by_game(APIView):
    def get(self, request, *args, **kwargs):
        category = kwargs.get("category")
        date = kwargs.get("date")
        # 검색
        game_list = (
            TopSellers.objects.filter(
                created_at__contains=date, game__categories__contains=category
            )
            .annotate(
                game_name=F("game__game_name"),  # game의 game_name 필드를 가져옴
                game_price=F("game__price"),  # game의 price 필드를 가져옴
                game_categories=F(
                    "game__categories"
                ),  # game의 categories 필드를 가져옴
            )
            .values(
                "game_name",
                "game_price",
                "game_categories",  # 필요한 필드 선택
            )[:10]
        )
        # 카테고리별 가격
        chart_data = []
        for i in game_list:
            chart_data.append({"name": i["game_name"], "y": i["game_price"]})

        data = {"chart_data": chart_data}
        return Response(data)
