from django.urls import path
from . import views

urlpatterns = [
    path('',views.landing),
    path('community_list/', views.community_list),
    path('job_community/', views.job_community),
    path('hobby_community/', views.hobby_community),
    path('notice_community/', views.notice_community),
    path('qna_community/', views.qna_community),
    path('admin_community/', views.admin_community),
]