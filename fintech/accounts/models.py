from django.db import models


class Currency(models.Model):
    code = models.CharField(max_length=3, unique=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.code


class Account(models.Model):
    number = models.CharField(max_length=50, unique=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
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


