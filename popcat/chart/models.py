from django.db import models


# Create your models here.
class TopSellers(models.Model):
    game_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"게임 이름:{self.game_name}"


class GameCategory(models.Model):
    game_name = models.ForeignKey(TopSellers, on_delete=models.CASCADE)
    reviews = models.IntegerField(default=0)
    category = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.game_name}"
