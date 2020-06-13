from rest_framework import routers
from ..api import views as core_views

router = routers.DefaultRouter()
router.register('student', core_views.StudentViewSet, basename='Student')
router.register('supervisor', core_views.SupervisorViewSet, basename='Supervisor')
router.register('course', core_views.CourseViewSet, basename='Course')
router.register('placement', core_views.PlacementViewSet, basename='Placement')
router.register('company', core_views.CompanyViewSet, basename='Company')
router.register('unit', core_views.UnitViewSet, basename='Unit')
router.register('application', core_views.ApplicationViewSet, basename='Application')
router.register('interview', core_views.InterviewViewSet, basename='Interview')