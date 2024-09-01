from rest_framework import serializers
from accounts.models import Account, AccountTransaction


class AccountSerializer(serializers.ModelSerializer):
    """ Сериализатор для создания счета. """
    amount = serializers.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    class Meta:
        model = Account
        fields = ['id', 'number', 'amount', 'currency']

    def validate_amount(self, value):
        print(f'{value=}')
        if value < 0:
            raise serializers.ValidationError("Amount must be positive.")
        return value


class TopUpAccountSerializer(serializers.Serializer):
    """ Сериализатор для пополнения баланса счета. """
    amount = serializers.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    account_number = serializers.CharField()

    def validate_amount(self, value):
        print(f'{value=}')
        if value < 0:
            raise serializers.ValidationError("Top-up amount must be greater than zero.")
        return value


class WithdrawAccountSerializer(TopUpAccountSerializer):
    """ Сериализатор для дебетования счета. """


class AccountTransactionSerializer(serializers.ModelSerializer):
    account_number = serializers.SerializerMethodField()

    class Meta:
        model = AccountTransaction
        fields = ['id', 'data', 'type', 'amount', 'account_number']

    def get_account_number(self, obj):
        return obj.account.number

