from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('create/', views.CreateAccountView.as_view(), name='create-account'),
    path('top-up/', views.TopUpView.as_view(), name='top-up-account'),
    path('withdraw/', views.WithdrawAccountView.as_view(), name='withdraw-account'),
    path('transactions/', views.AccountTransactionView.as_view(), name='account-transactions'),
]
