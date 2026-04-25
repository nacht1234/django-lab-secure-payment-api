from django.urls import path
from .views import create_payment, login_view, get_payment

urlpatterns = [
    path('pay/', create_payment),
    path('login/', login_view),
    path('payment/<int:pk>/', get_payment),
]