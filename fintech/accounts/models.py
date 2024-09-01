from django.db import models


class Account(models.Model):
    number = models.CharField(max_length=50, unique=True)
    balance = models.DecimalField(max_digits=10, blank=True, decimal_places=2, default=0.00)
    currency = models.CharField(max_length=5)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class AccountTransaction(models.Model):
    class Type(models.TextChoices):
        WITHDRAW = 'withdraw'
        TOP_UP = 'top_up'
    data = models.DateTimeField(auto_now_add=True)
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='account_transaction')
    type = models.CharField(max_length=150, choices=Type.choices)
    amount = models.DecimalField(max_digits=10, decimal_places=2)


