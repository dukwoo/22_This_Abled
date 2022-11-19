from django.urls import path
from . import views

urlpatterns = [
    path('',views.landing),
    path('community_list/', views.community_list),
    path('start_job_test/', views.start_job_test),
]