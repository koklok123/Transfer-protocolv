from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.contrib.auth import authenticate
from apps.linux.models import User

from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from apps.linux.models import User
from apps.linux.serializers import UsersSerializers, UserRegisterSerializer


# ViewSet для работы с пользователями
class UsersApi(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UsersSerializers
    permission_classes = [IsAuthenticated]


# Представление для регистрации нового пользователя
class UserCreateAPIView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Проверка пароля
        if serializer.validated_data['password'] != serializer.validated_data['confirm_password']:
            return Response({'confirm_password': "Пароли не совпадают"}, status=status.HTTP_400_BAD_REQUEST)
        if len(serializer.validated_data['password']) < 8:
            return Response({'password': "Минимум 8 символов"}, status=status.HTTP_400_BAD_REQUEST)

        # Создание пользователя
        user = User.objects.create(
            username=serializer.validated_data['username'],
            email=serializer.validated_data['email'],
            phone_number=serializer.validated_data['phone_number'],
            address=serializer.validated_data['address']
        )
        user.set_password(serializer.validated_data['password'])
        user.save()

        # Возврат данных нового пользователя
        response_serializer = self.get_serializer(user)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)

class UserLoginAPIView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)
        if user is not None:
            # Если пользователь найден, создаем или получаем токен
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key,  # Отправляем токен клиенту
                'balance': user.balance,  # Отправляем баланс
            }, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Неверные данные для входа'}, status=status.HTTP_400_BAD_REQUEST)
