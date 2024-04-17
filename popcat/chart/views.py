from django.http import HttpResponse
from .Crawler.GetReviewCount import GetReviewCount
from .Crawler.SteamTopSeller import TopSeller
from .models import *
from django.utils import timezone


def index(request):
    return HttpResponse("Pop Category Chart, in here")


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


def test_graph():
    
    print('hello 안녕하세요 ')
    이건 그냥 테스트 하는 겁니다
    
    
    return 

test_graph()
