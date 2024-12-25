from django.urls import include, path

urlpatterns = [
    path('', include('RegLog.urls')),
    path('payments/', include('payment.urls'))
]
