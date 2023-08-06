from netbox.api.routers import NetBoxRouter
from machine_tracking.api import views

router = NetBoxRouter()
router.register('events', views.EventViewSet)
router.register('replacements', views.ReplacementViewSet)

urlpatterns = router.urls