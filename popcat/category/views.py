from django.http import HttpResponse
from django.shortcuts import render
from chart.models import *

# 테스트 용, 마음대로 수정해주세요.
def index(request):
    game_list = Game.objects.all()
    topsellers_list = TopSellers.objects.all()
    reviewers_list = GameReviewers.objects.all()
    
    context = {
        'games': game_list,
        'topsellers': topsellers_list,
        'reviewers': reviewers_list
    }
    
    return render(request,'category/index.html',context)