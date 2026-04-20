from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home_redirect, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.custom_login_view, name='login'),
    path('logout/', views.custom_logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('ats-checker/', views.ats_checker_view, name='ats_checker'),
    path('jd-matcher/', views.jd_matcher_view, name='jd_matcher'),
    path('apply/<int:job_id>/', views.apply_job_view, name='apply_job'),
]
