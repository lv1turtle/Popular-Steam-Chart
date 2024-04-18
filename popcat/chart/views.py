from django.http import HttpResponse
from .Crawler.GetReviewCount import GetReviewCount
from .Crawler.SteamTopSeller import TopSeller
from .models import *
from django.utils import timezone
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from django.views.generic import View

def index(request):
    return HttpResponse("Pop Category Chart, in here")

# https://codepen.io/pen -> highchart 사용했습니다.
# https://dowtech.tistory.com/3 -> 참고했어요
# 태그 별 순위 기능 구현 (2-1)
class RankByTagAPIView(APIView):
    authentication_classes = []
    permission_classes = []
    
    def get(self, request):
        topsellers_list = TopSellers.objects.all()
        
        # 리뷰 수에 비례하여 태그에 가중치를 부여한 {tag:value} dictionary
        tot_tag = {} # 총 리뷰 수 기준
        pos_tag = {} # 긍정 리뷰 수 기준
        neg_tag = {} # 부정 리뷰 수 기준
        
        for topseller in topsellers_list :
            # topsellers에 포함된 game을 선택
            game = Game.objects.get(id = topseller.game_id)
            # 선택한 game에 해당하는 리뷰 수를 조회
            reviewers = GameReviewers.objects.filter(game_id = game.id) & GameReviewers.objects.filter(created_at = topseller.created_at)
            reviewers = reviewers[0]
            
            categories = game.categories.split(',')
            for category in categories :
                category = category.replace(" ","")
                # dict에 추가할 때, 리뷰 수에 비례한 가중치를 부여
                tot_tag[category] = tot_tag.get(category, 0) + reviewers.tot_reviews
                pos_tag[category] = pos_tag.get(category, 0) + reviewers.pos_reviews
                neg_tag[category] = neg_tag.get(category, 0) + reviewers.neg_reviews
        
        # data 전달 형식
        tag = []
        for key, value in tot_tag.items() :
            tag.append({ 'name' : key, 'y' : value})
        
        data = {
            'tags': tag
        }
        
        return Response(data)

class TagView(View):
    def get(self, request, *args, **kwargs):
        return render(request,'chart/tag.html')

## 크롤 데이터 저장
def postreviewsData(request):
    data_Queue = GetReviewCount()
    topseller_data = TopSeller()
    # data[0]: 'id' / data[1] : 'game_name' / data[2] : 'pos_reviews' / data[3] : 'neg_reviews'
    # top_data[0] : 'game_name' / top_data[1] : 'tags' / top_data[2] : 'price'
    for data, top_data in zip(data_Queue, topseller_data):
        # game_name 순서 일치 여부 확인
        # print(f"data_Queue: {data[1]}")
        # print(f"topseller_data: {top_data[0]}")
        # game_name : 신규 -> 신규 저장
        if not Game.objects.filter(game_name=data[1]).exists():
            game = Game(game_name=data[1], price=top_data[2], categories=top_data[1])
            game.save()

            top_sellers = TopSellers(game_id=game.id)
            top_sellers.save()

            reviewers = GameReviewers(
                game_id=game.id,
                pos_reviews=data[2],
                neg_reviews=data[3],
                tot_reviews=data[2] + data[3],
            )
            reviewers.save()
    
    return HttpResponse(f"{topseller_data}")


#2-4
def NumOfBuyers():
    #test