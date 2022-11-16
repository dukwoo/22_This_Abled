from django.shortcuts import render

# Create your views here.

def landing(request):

    return render(
        request,
        'firstapp/landing.html',
    )

def community_list(request):
    return render(
        request,
        'firstapp/community_list.html'
    )