from django.http import HttpResponse
from django.shortcuts import render
from chart.models import *
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import F


# 테스트 용, 마음대로 수정해주세요.
def index(request):
    game_list = Game.objects.all()
    topsellers_list = TopSellers.objects.all()
    reviewers_list = GameReviewers.objects.all()
    
    context = {
        'games': game_list,
        'topsellers': topsellers_list,
        'reviewers': reviewers_list
    }
    
    return render(request,'category/index.html',context)

def category_search(request):
    if 'category' in request.GET:
        category = request.GET['category']
        # 해당 카테고리를 가진 게임 가져오기
        games = Game.objects.filter(categories__icontains=category)
        # 해당 게임들의 TopSellers 정보 가져오기
        top_sellers = TopSellers.objects.filter(game__in=games).order_by('created_at')
        game_rank = [(ts.game, i + 1) for i, ts in enumerate(top_sellers)]
        context = {
            'games': game_rank,  # TopSellers에서 가져온 게임들만 표시
            'category': category
        }
        return render(request, 'category/category_search.html', context)
    else:
        return render(request, 'category/category_search.html', {})

class average_price_by_categories(APIView):

    def get(self, request):
        return render(request, 'category/categoryChart.html')
        
class Category_chart(APIView) :
    def get(self, request, *args, **kwargs) :
        date = kwargs.get('date')
        if not date :
            date = timezone.now().date()
        # 검색
        game_list = TopSellers.objects.filter(
            created_at__contains=date
        ).annotate(
            game_name=F('game__game_name'),  # game의 game_name 필드를 가져옴
            game_price=F('game__price'),  # game의 price 필드를 가져옴
            game_categories=F('game__categories'),  # game의 categories 필드를 가져옴
        ).values(
            'game_name', 'game_price', 'game_categories',  # 필요한 필드 선택
        )[:100]
        # game_list =  Game.objects.filter(categories__contains=category)[:100]
        category_Total_price_dict = {}
        # 카테고리별 가격
        for i in game_list :
            categories = [category.strip() for category in i["game_categories"].split(',')]
            for category in categories :
                category_Total_price_dict[category] = category_Total_price_dict.get(category, [0,0,0])
                category_Total_price_dict[category][0] += i["game_price"]
                category_Total_price_dict[category][1] += 1
        
        chart_data = []
        # 카테고리별 평균값 및 차트세팅
        if category_Total_price_dict :
            for category in category_Total_price_dict :
                category_Total_price_dict[category][2] = category_Total_price_dict[category][0] // category_Total_price_dict[category][1]
                chart_data.append({'name':category, 'y':category_Total_price_dict[category][2]})
        else :
            chart_data.append({"None":0})

        data = {
            "chart_data": chart_data
        }
        return Response(data)

class Category_chart_by_game(APIView) :
    def get(self, request, *args, **kwargs) :
        category = kwargs.get('category')
        date = kwargs.get('date')
        # 검색
        game_list = TopSellers.objects.filter(
            created_at__contains=date,
            game__categories__contains=category
        ).annotate(
            game_name=F('game__game_name'),  # game의 game_name 필드를 가져옴
            game_price=F('game__price'),  # game의 price 필드를 가져옴
            game_categories=F('game__categories'),  # game의 categories 필드를 가져옴
        ).values(
            'game_name', 'game_price', 'game_categories',  # 필요한 필드 선택
        )[:10]
        # 카테고리별 가격
        chart_data = []
        for i in game_list :
            chart_data.append({'name':i["game_name"], 'y':i["game_price"]})

        data = {
            "chart_data": chart_data
        }
        return Response(data)
