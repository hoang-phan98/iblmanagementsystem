from rest_framework import viewsets, mixins
from rest_framework.response import Response
from .serializers import *
from django.http import HttpResponse, HttpResponseServerError
from ..models import *
import json
from rest_framework.permissions import BasePermission, IsAuthenticated
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from authentication.api.permissions import HasGroupPermission

class StudentViewSet(viewsets.GenericViewSet,
                   mixins.ListModelMixin,
                   mixins.RetrieveModelMixin):


    permission_classes = [HasGroupPermission]
    queryset = Student.objects.all()
    serializer_class = RetrieveStudentSerializer
    required_groups = {
         'GET': ['student'],
         'POST': ['student'],
         'PUT': ['student'],
     }

    def get_paginated_response(self, data):
        return Response(data)

class CourseViewSet(viewsets.GenericViewSet,
                   mixins.ListModelMixin,
                   mixins.RetrieveModelMixin):

    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Course.objects.all()
    serializer_class = RetrieveCourseSerializer

    def get_paginated_response(self, data):
        return Response(data)

class SupervisorViewSet(viewsets.GenericViewSet,
                   mixins.ListModelMixin,
                   mixins.RetrieveModelMixin):

    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Supervisor.objects.all()
    serializer_class = RetrieveSupervisorSerializer

    def get_paginated_response(self, data):
        return Response(data)

class CompanyViewSet(viewsets.GenericViewSet,
                   mixins.ListModelMixin,
                   mixins.RetrieveModelMixin):

    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Company.objects.all()
    serializer_class = RetrieveCompanySerializer

    def get_paginated_response(self, data):
        return Response(data)

class PlacementViewSet(viewsets.GenericViewSet,
                   mixins.ListModelMixin,
                   mixins.RetrieveModelMixin):

    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Placement.objects.all()
    serializer_class = RetrievePlacementSerializer

    def get_paginated_response(self, data):
        return Response(data)

class UnitViewSet(viewsets.GenericViewSet,
                   mixins.ListModelMixin,
                   mixins.RetrieveModelMixin):

    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Unit.objects.all()
    serializer_class = RetrieveUnitSerializer

    def get_paginated_response(self, data):
        return Response(data)

class ApplicationViewSet(viewsets.GenericViewSet,
                   mixins.ListModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.CreateModelMixin,
                   mixins.UpdateModelMixin):

    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Application.objects.all()
    serializer_class = RetrieveApplicationSerializer

    def get_paginated_response(self, data):
        return Response(data)

class InterviewViewSet(viewsets.GenericViewSet,
                   mixins.ListModelMixin,
                   mixins.RetrieveModelMixin):

    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Interview.objects.all()
    serializer_class = RetrieveInterviewSerializer

    def get_paginated_response(self, data):
        return Response(data)

class UnitCourseViewSet(viewsets.GenericViewSet,
                   mixins.ListModelMixin,
                   mixins.RetrieveModelMixin):

    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = UnitCourse.objects.all()
    serializer_class = RetrieveUnitCourseSerializer

    def get_paginated_response(self, data):
        return Response(data)

class EligibilityRulesViewSet(viewsets.GenericViewSet,
                   mixins.ListModelMixin,
                   mixins.RetrieveModelMixin):

    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = EligibilityRules.objects.all()
    serializer_class = RetrieveEligibilityRulesSerializer

    def get_paginated_response(self, data):
        return Response(data)

class ActivityViewSet(viewsets.GenericViewSet,
                   mixins.ListModelMixin,
                   mixins.RetrieveModelMixin):

    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Activity.objects.all()
    serializer_class = RetrieveActivitySerializer

    def get_paginated_response(self, data):
        return Response(data)

class QuestionnaireTemplateViewSet(viewsets.GenericViewSet,
                            mixins.ListModelMixin,
                            mixins.DestroyModelMixin,
                            mixins.RetrieveModelMixin,
                            mixins.UpdateModelMixin,
                            mixins.CreateModelMixin):

    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = QuestionnaireTemplate.objects.all()
    serializer_class = RetrieveQuestionnaireTemplateSerializer

    def list(self, request, *args, **kwargs):
        active_query = request.query_params.get('active', None)
        #If no parameter is given then just use the ListModelMixin to list all the tasks.
        if active_query is None:
            return super().list(request, *args, **kwargs)

        # Attempt to retrieve instance
        try:
            if active_query.lower() == "true":
                active_query = True
            instances = QuestionnaireTemplate.objects.filter(active=active_query)
        except:
            return Response({})

        serializer = RetrieveQuestionnaireTemplateSerializer(instances, many=True)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        response_query = request.POST.get("questions")

        validateJson = self.validateTemplateJson(response_query)
        if response_query is None or validateJson != "":
            return Response(validateJson)

        return super().update(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        response_query = request.POST.get("questions") #Query_params didn't work, but POST.get did?
       # response_query = request.query_params.get("response",None)

        validateJson = self.validateTemplateJson(response_query)
        if response_query is None or validateJson != "":
            return Response(validateJson)

        return super().create(request, *args, **kwargs)


    """
        The validateTemplateJson function for the student response class ensures that a string given can be converted to
        JSON. Valid JSON formats conform to following:
            questions: [{"question": "question here", "format": "A format to display the question on the frontend"}]
            To further elaborate format, this field can be used to specify how the question should be presented.
            For example if the question was a radio button selection the format may be: radio buttons

        Parameters:
            json_object - a string to validate
        Returns:
            A boolean of if the string meets the above requirements.
    """
    def validateTemplateJson(self, json_object):
        try:
            json_data = json.loads(json_object) #This won't be needed if we use JSONField

            #Checking that there aren't any fields other than the response and the only key is response
            if len(json_data) > 1:
                return "There are too many keys in the JSON object. Only 'questions' should be present."

            #If accessing response doesn't work then there's a key error and this will return false
            response_array = json_data['questions']

            #Checking that all the fields are the specified format.
            if len(response_array) == 0:
                return "questions is empty."

            for i in range(len(response_array)):
                keys = list(response_array[i].keys())
                if keys[0].lower() != 'question' or keys[1].lower() != 'format' or len(keys) != 2:
                    return "Invalid key in response array."

            return ""
        except:
            return "Invalid JSON object or no 'questions' key present in object."

    def get_paginated_response(self,data):
        return Response(data)

class StudentResponse(viewsets.GenericViewSet,
                   mixins.ListModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.CreateModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.DestroyModelMixin):

    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = StudentResponse.objects.all()
    serializer_class = RetrieveStudentResponseSerializer


    def update(self, request, *args, **kwargs):
        response_query = request.POST.get("response")
        validateJson = self.validateResponseJson(response_query)
        if response_query is None or validateJson != "":
            return Response(validateJson)

        return super().update(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        response_query = request.POST.get("response") #Query_params didn't work, but POST.get did?
       # response_query = request.query_params.get("response",None)
        validateJson = self.validateResponseJson(response_query)
        if response_query is None or validateJson != "":
            return Response(validateJson)

        return super().create(request, *args, **kwargs)


    """
        The validateResponseJson function for the student response class ensures that a string given can be converted to
        JSON and it contains only the specified keys of 'question' and 'answer'
        Parameters:
            json_object - a string to validate
        Returns:
            A boolean of if the string meets the above requirements.
    """
    def validateResponseJson(self, json_object):
        try:
            json_data = json.loads(json_object) #This won't be needed if we use JSONField

            #Checking that there aren't any fields other than the response and the only key is response
            if len(json_data) > 1:
                return "There are too many keys in the JSON object. Only 'response' should be present."

            #If accessing response doesn't work then there's a key error and this will return false
            response_array = json_data['response']

            #Checking that all the fields are the specified format.
            if len(response_array) == 0:
                return "Response is empty."

            for i in range(len(response_array)):
                keys = list(response_array[i].keys())
                if keys[0].lower() != 'question' or keys[1].lower() != 'answer' or len(keys) != 2:
                    return "Invalid key in response array."

            return ""
        except:
            return "Invalid JSON object or no 'response' key present in object."


    def get_paginated_response(self, data):
        return Response(data)

class UserResponse(viewsets.GenericViewSet):
    """
    Checks for a Student or Supervisor based on input email, if exists (send 500 if not exist). Will also return their
    data. Return dict with two keys. 'type' is either 'student' or 'supervisor', and 'info' is the Student/Supervisor
    QuerySet as an object. If the Student or Supervisor is not found, a 500 Response is sent.
    """
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    lookup_value_regex = '[^/]+'

    def retrieve(self, request, pk=None):
        if pk is None:
            return HttpResponseServerError()
        obj = Student.objects.filter(email__exact=str(pk)).first()
        is_student = obj is not None
        obj = obj if obj else Supervisor.objects.filter(email__exact=str(pk)).first()
        if not obj:
            return HttpResponseServerError()
        if is_student:
            s = RetrieveStudentSerializer(obj)
        else:
            s = RetrieveSupervisorSerializer(obj)
        res = {
            'type': 'student' if is_student else 'supervisor',
            'info': s.data
        }
        return HttpResponse(json.dumps(res), content_type='application/json')

# class PrereqConjunctionViewSet(viewsets.GenericViewSet,
#                    mixins.ListModelMixin,
#                    mixins.RetrieveModelMixin):
#
#     queryset = PrereqConjunction.objects.all()
#     serializer_class = RetrievePrereqConjunction
#
#     def get_paginated_response(self, data):
#         return Response(data)
