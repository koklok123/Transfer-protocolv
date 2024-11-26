from rest_framework import serializers
from .models import User


class UsersSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'phone_number', 'address']


class UserRegisterSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'phone_number', 'address', 'password', 'confirm_password']
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError({'confirm_password': "Пароли не совпадают"})
        if len(attrs['password']) < 8:
            raise serializers.ValidationError({'password': "Минимум 8 символов"})
        return attrs

    def create(self, validated_data):
        validated_data.pop('confirm_password')  # Удаляем confirm_password перед сохранением
        user = User.objects.create(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user
