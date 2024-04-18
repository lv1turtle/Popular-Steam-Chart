from django.http import HttpResponse
from django.shortcuts import render
from chart.models import *
from rest_framework.views import APIView

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
        return render(request, 'category_results.html', context)
    else:
        return render(request, 'category_results.html', {})

# class average_price_by_categories(APIView):

def average_price_by_categories(request):
    print(request)
    category = "salad"
    # 검색 조건
    
    # 검색
    game_list =  Game.objects.filter(categories__contains=category)[:100]
    category_Total_price_dict = {}
    
    # 카테고리별 가격
    for i in game_list :
        categories = [category.strip() for category in i.categories.split(',')]
        for category in categories :
            category_Total_price_dict[category] = category_Total_price_dict.get(category, [0,0,0])
            category_Total_price_dict[category][0] += i.price
            category_Total_price_dict[category][1] += 1
    
    labels = []
    sizes = []
    # 카테고리별 평균값 및 차트세팅
    if category_Total_price_dict :
        for category in category_Total_price_dict :
            category_Total_price_dict[category][2] = category_Total_price_dict[category][0] // category_Total_price_dict[category][1]
            labels.append(category)
            sizes.append(category_Total_price_dict[category][2])
    else :
        labels.append('NONE')
        sizes.append(1)
    # 원형 차트 생성
    

    data = {
        "games" : game_list,
        "dict" : category_Total_price_dict,
        "labels" : labels,
        "sizes" : sizes,
        # "chart" : image_png
    }
    return render(request, 'category/categoryChart.html', data)
        
