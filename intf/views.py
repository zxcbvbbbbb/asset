from django.shortcuts import render,HttpResponse

# Create your views here.

def asset(request):
    print(request.GET)
    print(request.POST)
    return HttpResponse('美国队vs塞尔维亚队')