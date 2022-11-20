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
    path('start_job_test/', views.start_job_test),
    path('job_test_1/', views.job_test_1),
    path('job_making/', views.job_making),
    path('hobby_exercise/', views.hobby_exercise),
    path('job_making_post1/', views.job_making_post1),
    path('hobby_exercise_post1/', views.hobby_exercise_post1),
]