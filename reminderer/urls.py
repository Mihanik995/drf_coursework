from rest_framework import routers

from reminderer.apps import RemindererConfig
from reminderer.views import HabitViewSet

app_name = RemindererConfig.name

router = routers.DefaultRouter()
router.register(r'habits', HabitViewSet)

urlpatterns = router.urls
