from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins, status
from rest_framework.response import Response
from django.shortcuts import render
from apps.linux.models import User
from apps.main.serializers import CoinInfoSerializer

class CoinInfoAPIView(GenericViewSet, mixins.ListModelMixin):
    serializer_class = CoinInfoSerializer

    def list(self, request, *args, **kwargs):   
        username = request.GET.get('username', None)  # Получаем параметр из GET-запроса
        if username:
            # Ищем пользователя по имени
            user = User.objects.filter(username=username).first()
            if user:
                # Если пользователь найден, сериализуем его данные
                serializer = self.get_serializer(user)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({"error": f"Пользователь с именем '{username}' не найден"}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"error": """пользователь на нешлся напишите в пути перед хостом: /coin/info/?username=<имя_пользователя>"""}, status=status.HTTP_400_BAD_REQUEST)

# В views.py добавьте обработку отображения страницы
def search_coin_info(request):
    if request.GET.get('username'):
        username = request.GET.get('username')
        user = User.objects.filter(username=username).first()
        coin_info = user if user else None
        return render(request, 'coin/search_form.html', {'coin_info': coin_info})
    return render(request, 'coin/search_form.html')
