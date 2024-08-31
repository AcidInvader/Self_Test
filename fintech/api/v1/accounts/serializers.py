from rest_framework import serializers
from accounts.models import Account, AccountTransaction


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['id', 'number', 'balance', 'currency', ]


# class AccountTransactionSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = AccountTransaction
#         fields = '__all__'

class TopUpBalanceSerializer(serializers.Serializer):
    class Meta:
        model = Account
        fields = '__all__'


    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Top-up amount must be greater than zero.")
        return value
