from rest_framework import routers

from .views import CartViewSet, ProductViewSet

router = routers.DefaultRouter()
router.register(r"products", ProductViewSet)
router.register(r"cart", CartViewSet)

urlpatterns = router.urls
