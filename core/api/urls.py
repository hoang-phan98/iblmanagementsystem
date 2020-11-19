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
router.register('unit_course', core_views.UnitCourseViewSet, basename='Unit Course')
router.register('eligibility_rules', core_views.EligibilityRulesViewSet, basename='Eligibility Rule')
router.register('questionnaire_template', core_views.QuestionnaireTemplateViewSet, basename='Questionnaire Template')
router.register('student_response', core_views.StudentResponse, basename='Student Response')
router.register('user', core_views.UserResponse, basename='User Response')
router.register('coursemap_snapshot',core_views.CourseMapSnapshotViewset, basename="Course map snapshot")