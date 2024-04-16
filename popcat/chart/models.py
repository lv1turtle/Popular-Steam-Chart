from django.db import models
from datetime import datetime

class TopSellers(models.Model):
    game_name = models.CharField(max_length=255) # 게임 이름
    created_at = models.DateTimeField(auto_now_add=True) # DB에 생성된 날짜

    def __str__(self):
        return f"게임 이름:{self.game_name}"

# fk 수정
class GameCategory(models.Model):
    topsellers_id = models.ForeignKey(TopSellers, related_name="gamecategories", on_delete=models.CASCADE)
    game_name = models.CharField(max_length=255) # 게임 이름
    reviews = models.IntegerField(default=0) # 리뷰어 수 ( 이용자 수와 비례 )
    category = models.CharField(max_length=255) # 특정 게임에 포함된 여러 카테고리 중 하나
    created_at = models.DateTimeField(auto_now_add=True) # DB에 생성된 날짜

    def __str__(self):
        return f"{self.game_name}"
