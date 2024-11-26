from rest_framework.routers import DefaultRouter
from .views import CoinInfoAPIView

router = DefaultRouter()
router.register('info', CoinInfoAPIView, basename='coin-info')

urlpatterns = router.urls
