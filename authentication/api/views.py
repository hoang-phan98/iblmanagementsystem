from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from rest_auth.registration.views import SocialLoginView
from django.contrib.auth.models import Group

class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter

    def login(self):
        self.user = self.serializer.validated_data['user']
        email = self.user.__dict__['email']

        if email[-19:] == "@student.monash.edu":
            student_group = Group.objects.get(name='student')
            student_group.user_set.add(self.user)

        elif email[-11:] == "@monash.edu":
            staff_group = Group.objects.get(name='staff')
            staff_group.user_set.add(self.user)

        super().login()