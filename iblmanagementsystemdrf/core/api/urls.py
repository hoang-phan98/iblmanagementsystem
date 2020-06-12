from rest_framework import routers
from core.api import views as core_views

router = routers.DefaultRouter()
router.register('student', core_views.StudentViewSet, basename='Student')
