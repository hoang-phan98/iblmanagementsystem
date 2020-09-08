from eligibility.api.views import wam
from django.urls import path


url_patterns = [
	path('wam', wam)
]
