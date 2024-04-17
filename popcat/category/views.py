from django.http import HttpResponse
from django.shortcuts import render
from chart.models import *

def index(request):
    game_list = Game.objects.all()
    topsellers_list = TopSellers.objects.all()
    category_list = GameCategory.objects.all()
    reviewers_list = GameReviewers.objects.all()
    
    context = {
        'games': game_list,
        'topsellers': topsellers_list,
        'categories': category_list,
        'reviewers': reviewers_list
    }
    return render(request,'category/index.html',context)