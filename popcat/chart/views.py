from django.http import HttpResponse
from .Crawler.GetReviewCount import GetReviewCount
from .models import *
from django.utils import timezone


def index(request):
    return HttpResponse("Pop Category Chart, in here")


## 오늘 날짜에 해당하는 TopSeller 저장
def postCrawlData(request):
    data_Queue = GetReviewCount()
    for data in data_Queue:
        # game_name : 신규 -> 신규 저장
        if not Game.objects.filter(game_name=data[1]).exists():
            game = Game(game_name=data[1])
            game.save()

            top_sellers = TopSellers(game_id=game.id)
            top_sellers.save()

            reviewers = GameReviewers(game_id=game.id, reviewers=data[2])
            reviewers.save()
    return HttpResponse(f"{data_Queue}")
