from django.urls import path
from . import views

urlpatterns = [
    path('add/', views.add),
    path('add-for-company-<int:index>/', views.add_for_company),
    path('add-for-company-<int:index>/refresh-code/', views.refresh_company_code)
]