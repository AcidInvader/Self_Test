from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('top-up/', views.TopUpView.as_view(), name='top-up-account'),
]
