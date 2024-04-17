from django.db import models
from datetime import datetime


class Game(models.Model):
    game_name = models.CharField(max_length=255)  # 게임 이름
    price = models.IntegerField(default=0)
    categories = models.CharField(max_length=1000, default="")  # 카데고리

    def __str__(self):
        return f"게임 이름:{self.game_name}"


class TopSellers(models.Model):
    game = models.ForeignKey(
        Game, related_name="topsellers", on_delete=models.CASCADE
    )  # 게임 id
    created_at = models.DateTimeField(
        auto_now_add=True
    )  # TopSellers에 올라와있던 해당 날짜

    def __str__(self):
        return f"생성 날짜:{self.created_at}"


class GameReviewers(models.Model):
    game = models.ForeignKey(
        Game, related_name="gamereviewers", on_delete=models.CASCADE
    )  # 게임 id
    pos_reviews = models.IntegerField(default=0)  # 긍정 리뷰어 수
    neg_reviews = models.IntegerField(default=0)  # 부정 리뷰어 수
    tot_reviews = models.IntegerField(default=0)  # 리뷰어 수 총합

    def __str__(self):
        return f"리뷰어 수:{self.tot_reviews}"
