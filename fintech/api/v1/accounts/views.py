from rest_framework.views import APIView
from accounts.models import Account, AccountTransaction
from rest_framework.permissions import AllowAny
from .serializers import AccountSerializer, TopUpAccountSerializer, WithdrawAccountSerializer, \
    AccountTransactionSerializer
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes


class CreateAccountView(APIView):
    permission_classes = (AllowAny,)

    @extend_schema(
        request=AccountSerializer,
        responses={200: 'Success'}
    )
    def post(self, request):
        serializer = AccountSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            account_number = serializer.validated_data['number']
            currency = serializer.validated_data['currency']
            amount = float(serializer.validated_data['amount'])
            account = Account()
            account.number = account_number
            account.currency = currency
            account.balance += amount
            account.save()

            return Response(
                {'account_number': account.number, 'account_balance': account.balance, 'currency': account.currency},
                status=status.HTTP_200_OK
            )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TopUpView(APIView):
    permission_classes = (AllowAny,)

    @extend_schema(
        request=TopUpAccountSerializer,
        responses={200: 'Success'},
    )
    def post(self, request):
        serializer = TopUpAccountSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            account_number = serializer.validated_data['account_number']
            amount = serializer.validated_data['amount']
            account = get_object_or_404(Account, number=account_number)
            print(f'{amount=}')

            account.balance += amount
            account.save()

            AccountTransaction.objects.create(
                account=account,
                type=AccountTransaction.Type.TOP_UP,
                amount=amount,
            )

            return Response({'account_number': account.number,
                             'account_balance': account.balance,
                             'currency': account.currency},
                            status=status.HTTP_200_OK
                            )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WithdrawAccountView(APIView):
    permission_classes = (AllowAny,)

    @extend_schema(
        request=WithdrawAccountSerializer,
        responses={200, 'success'}
    )
    def post(self, request):
        serializer = WithdrawAccountSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            print(f'we are in if')
            account_number = serializer.validated_data['account_number']
            amount = serializer.validated_data['amount']
            print(f'{amount=}')
            account = get_object_or_404(Account, number=account_number)
            print(f'{account=}')
            if account.balance >= amount:
                account.balance -= amount
                account.save()

                AccountTransaction.objects.create(
                    account=account,
                    type=AccountTransaction.Type.WITHDRAW,
                    amount=amount,
                )

                return Response({'account_number': account.number,
                                 'account_balance': account.balance,
                                 'currency': account.currency},
                                status=status.HTTP_200_OK)
            else:
                return Response({'detail': 'The account balance less then amount of withdraw'},
                                status=status.HTTP_406_NOT_ACCEPTABLE)


class AccountTransactionView(APIView):
    permission_classes = (AllowAny,)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='account-number',
                type=OpenApiTypes.STR,
                location=OpenApiParameter.HEADER,
                description='Account number to retrieve transactions for it',
                required=True,
            ),
        ],
        responses={200: AccountTransactionSerializer(many=True)}
    )
    def get(self, request):
        try:
            print(f'{request=}')
            account_number = request.headers.get('account_number')
            if not account_number:
                return Response({"error": "Account Number is required"}, status=status.HTTP_400_BAD_REQUEST)

            account = get_object_or_404(Account, number=account_number)
            transactions = AccountTransaction.objects.filter(account=account)

            serializer = AccountTransactionSerializer(transactions, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as ex:
            return ex




