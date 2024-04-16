from django.http import HttpResponse
from django.shortcuts import render
from chart.models import *

def index(request):
    topsellers_list = TopSellers.objects.all()
    category_list = GameCategory.objects.all()
    
    context = {'topsellers': topsellers_list, 'categories': category_list}
    return render(request,'category/index.html',context)