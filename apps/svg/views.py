from django.db import transaction
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework import status, mixins
from apps.svg.models import Transactions_coin
from apps.svg.serializers import CoinTransferSerializer
from apps.linux.models import User

class CoinTransferAPIView(GenericViewSet, mixins.CreateModelMixin):
    queryset = Transactions_coin.objects.all()
    serializer_class = CoinTransferSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        from_user_name = serializer.validated_data['from_user']
        to_user_name = serializer.validated_data['to_user']
        amount = serializer.validated_data['amount']

        try:
            # Начинаем транзакцию с использованием блокировки строк
            with transaction.atomic():  
                from_user = User.objects.select_for_update().get(username=from_user_name)
                to_user = User.objects.select_for_update().get(username=to_user_name)

                if from_user.balance < amount:
                    return Response(
                        {'error': 'Недостаточно средств для перевода.'},
                        status=status.HTTP_400_BAD_REQUEST
                    )

                from_user.balance -= amount
                to_user.wallet += amount

                from_user.save()
                to_user.save()

                # Создаём транзакцию
                Transactions_coin.objects.create(
                    from_user=from_user,
                    to_user=to_user,
                    amount=amount
                )

        except User.DoesNotExist as e:
            return Response(
                {'error': f"Ошибка: {str(e)}"},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            # Ловим другие исключения, которые могут возникнуть
            return Response(
                {'error': f"Ошибка при выполнении транзакции: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        return Response(
            {
                'message': f"Перевод {amount} коинов успешно завершён."
            },
            status=status.HTTP_201_CREATED
        )
