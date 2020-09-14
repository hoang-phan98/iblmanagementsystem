from rest_framework import viewsets, mixins
from rest_framework.response import Response
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from rest_auth.registration.views import SocialLoginView
from django.http import HttpResponse, HttpResponseServerError
from rest_auth.views import LoginView
from rest_auth.registration.serializers import SocialLoginSerializer
from allauth.account.adapter import get_adapter
from django.contrib.auth.models import Group

class IBLLoginView(LoginView):

   def login(self):
        self.user = self.serializer.validated_data['user']
        email = self.user.__dict__['email']

        if email[-19:] == "@student.monash.edu":
            print("\n\nstudent detected\n\n")
            student_group = Group.objects.get(name='student')
            student_group.user_set.add(self.user)

        elif email[-11:] == "@monash.edu":
            print("\n\nstaff detected\n\n")
            staff_group = Group.objects.get(name='student')
            staff_group.user_set.add(self.user)

        super().login()


class IBLSocialLoginView(IBLLoginView):
    serializer_class = SocialLoginSerializer

    def process_login(self):
        get_adapter(self.request).login(self.request, self.user)


class GoogleLogin(IBLSocialLoginView):
    adapter_class = GoogleOAuth2Adapter
