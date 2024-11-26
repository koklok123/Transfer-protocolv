from rest_framework.routers import DefaultRouter
from .views import CoinTransferAPIView

router = DefaultRouter()
router.register('coin/transfer', CoinTransferAPIView, basename='coin-transfer')

urlpatterns = router.urls


