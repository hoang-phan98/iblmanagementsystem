from eligibility.api import views as eligibility_views
from rest_framework import routers

router = routers.DefaultRouter()

router.register('wam', eligibility_views.WamCheck, basename='Wam')
