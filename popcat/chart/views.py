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
    for data in data_Queue:
        # game_name : 신규 -> 신규 저장
        if not Game.objects.filter(game_name=data[1]).exists():
            game = Game(game_name=data[1], price=0, categories="default")
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
    return HttpResponse(f"{data_Queue}")
