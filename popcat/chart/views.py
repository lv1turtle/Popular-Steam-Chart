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


# https://www.highcharts.com/demo/highcharts/variable-radius-pie -> highchart 사용했습니다.
# https://dowtech.tistory.com/3 -> 참고했어요
# 태그 별 순위 기능 구현 (2-1)


# /api/tag -> 데이터를 보내주는 api 확인용
class RankByTagAPIView(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        topsellers_list = TopSellers.objects.all()

        # 리뷰 수에 비례하여 태그에 가중치를 부여한 {tag:value} dictionary
        tot_tag = {}  # 총 리뷰 수 기준
        pos_tag = {}  # 긍정 리뷰 수 기준

        for topseller in topsellers_list:
            # topsellers에 포함된 game을 선택
            game = Game.objects.get(id=topseller.game_id)
            # 선택한 game에 해당하는 리뷰 수를 조회
            reviewers = GameReviewers.objects.filter(
                game_id=game.id
            ) & GameReviewers.objects.filter(
                created_at__date=topseller.created_at.date()
            )
            reviewers = reviewers[0]

            categories = game.categories.split(",")
            for category in categories:
                category = category.replace(" ", "")
                # dict에 추가할 때, 리뷰 수에 비례한 가중치를 부여
                tot_tag[category] = tot_tag.get(category, 0) + reviewers.tot_reviews
                pos_tag[category] = pos_tag.get(category, 0) + reviewers.pos_reviews

        # 상위 10개만 추출하기 위해 value 기준 내림차순 정렬
        # sorted로 인해 list로 변환됨
        tot_tag = sorted(tot_tag.items(), key=lambda item: item[1], reverse=True)

        if len(tot_tag) > 10:
            tot_tag = tot_tag[0:10]

        # data 전달 형식
        pos = []
        neg = []

        for key, value in tot_tag:
            pos.append({"name": key, "y": value, "z": pos_tag[key]})
            neg.append({"name": key, "y": value, "z": value - pos_tag[key]})

        data = {"pos": pos, "neg": neg}

        return Response(data)


# /tag -> 실제로 chart를 그려줌
class TagView(View):
    def get(self, request, *args, **kwargs):
        return render(request, "chart/tag.html")


## 크롤 데이터 저장
def postreviewsData(request):
    data_Queue = GetReviewCount()
    topseller_data = TopSeller()
    today = timezone.now().date()
    # data[0]: 'id' / data[1] : 'game_name' / data[2] : 'pos_reviews' / data[3] : 'neg_reviews'
    # top_data[0] : 'game_name' / top_data[1] : 'tags' / top_data[2] : 'price' / top_data[3] : 'game_code'

    for data, top_data in zip(data_Queue, topseller_data):
        cleaned_tag_data = ", ".join(top_data[1])

        # game_name 순서 일치 여부 확인
        # print(f"data_Queue: {data[1]}")
        # print(f"topseller_data: {top_data[0]}")
        # game_name : 신규 -> 신규 저장
        if not Game.objects.filter(game_name=top_data[0]).exists():
            game = Game(
                game_name=top_data[0],
                price=top_data[2],
                categories=cleaned_tag_data,
                game_code=top_data[3],
            )
            game.save()
        else:
            game = Game.objects.get(game_name=top_data[0])
        # if not TopSellers.objects.filter(created_at__date=today).exists():
        TopSellers.objects.create(game_id=game.id, game_code=top_data[3])
        # if not GameReviewers.objects.filter(created_at__date=today).exists():
        GameReviewers.objects.create(
            game_id=game.id,
            pos_reviews=data[2],
            neg_reviews=data[3],
            tot_reviews=data[2] + data[3],
            game_code=top_data[3],
        )

    return HttpResponse(f"{topseller_data}")


def main(request):
    return render(request, "chart/main_page.html")
