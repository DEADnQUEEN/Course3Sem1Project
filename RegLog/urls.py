from django.urls import path
from . import views

urlpatterns = [
    path('', views.main),
    path('login/', views.login),
    path('register/', views.register),
    path('logout/', views.logout),
    path('not-allowed/', views.not_allowed),
]
