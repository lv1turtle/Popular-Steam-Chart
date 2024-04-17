from django.db import models
from datetime import datetime

class Game(models.Model):
    game_name = models.CharField(max_length=255) # 게임 이름

    def __str__(self):
        return f"게임 이름:{self.game_name}"

class TopSellers(models.Model):
    game = models.ForeignKey(Game, related_name="topsellers", on_delete=models.CASCADE) # 게임 id
    created_at = models.DateTimeField(auto_now_add=True) # TopSellers에 올라와있던 해당 날짜

    def __str__(self):
        return f"생성 날짜:{self.created_at}"

class GameCategory(models.Model):
    game = models.ForeignKey(Game, related_name="gamecategories", on_delete=models.CASCADE) # 게임 id
    category = models.CharField(max_length=255) # 특정 게임에 포함된 여러 카테고리 중 하나

    def __str__(self):
        return f"카테고리명:{self.category}"

class GameReviewers(models.Model):
    game = models.ForeignKey(Game, related_name="gamereviewers", on_delete=models.CASCADE) # 게임 id
    reviewers = models.IntegerField(default=0) # 리뷰어 수
    
    def __str__(self):
        return f"리뷰어 수:{self.reviewers}"