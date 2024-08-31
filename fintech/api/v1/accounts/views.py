from rest_framework.views import APIView
from accounts.models import Account, AccountTransaction
from rest_framework.permissions import AllowAny
from .serializers import AccountSerializer, TopUpBalanceSerializer
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status


class TopUpView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = TopUpBalanceSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            account_number = serializer.validated_data['account_number']
            amount = serializer.validated_data['amount']
            account = get_object_or_404(Account, number=account_number)

            account.balance += amount
            account.save()

            AccountTransaction.objects.create(
                account=account,
                type=AccountTransaction.Type.TOP_UP,
                amount=amount,
            )

            return Response({'balance': account.balance}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

