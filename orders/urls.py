from rest_framework.routers import SimpleRouter
from . import views

router = SimpleRouter()
router.register(r"orders", views.OrderViewSet)
urlpatterns = router.urls
