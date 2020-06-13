from rest_framework import routers
from ..api import views as core_views

router = routers.DefaultRouter()
router.register('student', core_views.StudentViewSet, basename='Student')
router.register('supervisor', core_views.SupervisorViewSet, basename='Supervisor')
router.register('course', core_views.CourseViewSet, basename='Course')
router.register('placement', core_views.CourseViewSet, basename='Placement')
router.register('company', core_views.CourseViewSet, basename='Company')
