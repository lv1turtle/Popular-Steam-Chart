from django.http import HttpResponse
from .Crawler.GetReviewCount import GetReviewCount
from .Crawler.SteamTopSeller import TopSeller
from .models import *
from django.utils import timezone
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from django.views.generic import View
import pandas as pd
import matplotlib.pyplot as plt
from django.db.models import Sum
from django.shortcuts import render
from io import BytesIO
import base64


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




# 2-4 태그별 구매자수(리뷰수)
def NumOfBuyers_graph():
    # Django QuerySet을 사용하여 데이터 가져오기
    data = GameReviewers.objects.values_list('game__game_name', 'game__categories', 'tot_reviews')

    # DataFrame으로 변환
    df = pd.DataFrame(list(data), columns=['Game Name', 'Categories', 'Total Reviews'])

    # 카테고리 분리 및 데이터 정규화
    # 'FPS, Shooting, Arcade' 같은 문자열을 ','로 분리
    df = df.drop('Categories', axis=1).join(df['Categories'].str.split(', ', expand=True).stack().reset_index(level=1, drop=True).rename('Category'))

    # 카테고리별 리뷰 수 합계 계산
    category_reviews = df.groupby('Category')['Total Reviews'].sum()
    category_reviews = category_reviews.sort_values(ascending=False).head(15) # 데이터 정렬

    # 막대그래프로 표시
    category_reviews.plot(kind='bar', color='skyblue')
    #plt.title('Total Reviews by Category')
    plt.xlabel('Category')
    plt.ylabel('Total Buyers')
    plt.xticks(rotation=82, fontsize=7)  # x축 라벨의 폰트 크기를 조정
    plt.tight_layout()
    #plt.show() #그래프 새창으로 보기

    # 그래프를 BytesIO 객체에 저장
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    graph = base64.b64encode(image_png)
    graph = graph.decode('utf-8')
    buffer.close()

    # 그래프 이미지 데이터를 반환
    return graph

def NumOfBuyers(request):
    graph = NumOfBuyers_graph()
    context = {'graph': graph}
    return render(request, 'chart/buyers_test.html', context)


def main(request):
    return render(request, "chart/main_page.html")




