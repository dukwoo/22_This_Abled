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

def start_job_test(request):
    return render(
        request,
        'firstapp/start_job_test.html'
    )
def job_community(request):
    return render(
        request,
        'firstapp/job_community.html'
    )
    
def hobby_community(request):
    return render(
        request,
        'firstapp/hobby_community.html'
    )

def notice_community(request):
    return render(
        request,
        'firstapp/notice_community.html'
    )

def qna_community(request):
    return render(
        request,
        'firstapp/qna_community.html'
    )

def admin_community(request):
    return render(
        request,
        'firstapp/admin_community.html'
    )