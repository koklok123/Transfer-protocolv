from rest_framework import serializers
from apps.linux.models import User

class CoinTransferSerializer(serializers.Serializer):
    from_user = serializers.CharField(max_length=150)
    to_user = serializers.CharField(max_length=150)
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)

    def validate(self, data):
        from_user = data.get('from_user')
        to_user = data.get('to_user')
        amount = data.get('amount')

        if not User.objects.filter(username=from_user).exists():
            raise serializers.ValidationError(f"Пользователь {from_user} не найден.")
        if not User.objects.filter(username=to_user).exists():
            raise serializers.ValidationError(f"Пользователь {to_user} не найден.")
        if from_user == to_user:
            raise serializers.ValidationError("Нельзя перевести средства самому себе.")
        if amount <= 0:
            raise serializers.ValidationError("Сумма перевода должна быть больше нуля.")

        return data
