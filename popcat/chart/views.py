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


# https://codepen.io/pen -> highchart 사용했습니다.
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
        neg_tag = {}  # 부정 리뷰 수 기준

        for topseller in topsellers_list:
            # topsellers에 포함된 game을 선택
            game = Game.objects.get(id=topseller.game_id)
            # 선택한 game에 해당하는 리뷰 수를 조회
            reviewers = GameReviewers.objects.filter(
                game_id=game.id
            ) & GameReviewers.objects.filter(created_at=topseller.created_at)
            reviewers = reviewers[0]

            categories = game.categories.split(",")
            for category in categories:
                category = category.replace(" ", "")
                # dict에 추가할 때, 리뷰 수에 비례한 가중치를 부여
                tot_tag[category] = tot_tag.get(category, 0) + reviewers.tot_reviews
                pos_tag[category] = pos_tag.get(category, 0) + reviewers.pos_reviews
                neg_tag[category] = neg_tag.get(category, 0) + reviewers.neg_reviews

        # 상위 10개만 추출하기 위해 value 기준 내림차순 정렬
        tot_tag = sorted(tot_tag.items(), key=lambda item: item[1], reverse=True)
        # data 전달 형식
        tag = []
        # sort로 인해 list로 변환됐으므로 itmes()를 사용하지 않음
        for key, value in tot_tag[0:10]:
            tag.append({"name": key, "y": value})

        data = {"tags": tag}

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
    # top_data[0] : 'game_name' / top_data[1] : 'tags' / top_data[2] : 'price'
    for data, top_data in zip(data_Queue, topseller_data):
        # game_name 순서 일치 여부 확인
        # print(f"data_Queue: {data[1]}")
        # print(f"topseller_data: {top_data[0]}")
        # game_name : 신규 -> 신규 저장
        if not Game.objects.filter(game_name=top_data[0]).exists():
            game = Game(
                game_name=top_data[0], price=top_data[2], categories=top_data[1]
            )
            game.save()
        else:
            game = Game.objects.get(game_name=top_data[0])
        # if not TopSellers.objects.filter(created_at__date=today).exists():
        TopSellers.objects.create(game_id=game.id)
        # if not GameReviewers.objects.filter(created_at__date=today).exists():
        GameReviewers.objects.create(
            game_id=game.id,
            pos_reviews=data[2],
            neg_reviews=data[3],
            tot_reviews=data[2] + data[3],
        )
    return HttpResponse(f"{topseller_data}")
















# 기능 2-4 태그별 구매자수
def NumOfBuyers_graph():
    # 게임 리뷰어 모델에서 게임명, 카테고리, 총 리뷰어 수 데이터 가져오기
    game_data = GameReviewers.objects.values_list(
        'game__game_name', 
        'game__categories', 
        'tot_reviews'
    )

    # DataFrame 생성, 'Game Name'을 인덱스로 설정
    df = pd.DataFrame(list(game_data), columns=['Game Name', 'Category', 'Total Reviews'])
    df.set_index('Game Name', inplace=True)
    
    # 카테고리별로 Total Reviews 집계
    category_reviews = df.groupby('Category')['Total Reviews'].sum()
        
    # 막대그래프 그리기
    plt.figure(figsize=(3, 3))  # 그래프 사이즈 조절
    ax = category_reviews.plot(kind='bar', color='skyblue')

    # 그래프 제목과 라벨 설정
    # plt.title('Buyers by Category') # 기존의 xlabel을 비활성화 하고, 새로운 텍스트를 x축의 끝에 배치
    plt.xlabel('')  # 기존 xlabel 제거
    ax.text(x=len(category_reviews)-0.5, y=-5, s='Category', horizontalalignment='right', verticalalignment='top')
    plt.ylabel('Buyers')# Y축 라벨 설정
    plt.xticks(rotation=45)  # 카테고리 이름이 길 경우 회전시키기
    plt.tight_layout()  # 레이아웃 설정으로 라벨이 잘리는 것 방지
    
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

