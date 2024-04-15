from django.http import HttpResponse

def index(request):
    return HttpResponse("Pop Category Chart, in here")