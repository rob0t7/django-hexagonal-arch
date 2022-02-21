from rest_framework import routers

from .views import CartItemViewSet, CartViewSet, ProductViewSet

router = routers.DefaultRouter()
router.register(r"products", ProductViewSet)
router.register(r"cart", CartViewSet)
router.register(r"cart/<uuid:cart_id>/items", CartItemViewSet)

urlpatterns = router.urls
