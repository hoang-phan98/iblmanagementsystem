from rest_framework import viewsets, mixins
from rest_framework.response import Response
from .serializers import *
from core.models import *
from django.http import HttpResponse, HttpResponseServerError
import json


class StudentViewSet(viewsets.GenericViewSet,
                   mixins.ListModelMixin,
                   mixins.RetrieveModelMixin):

    queryset = Student.objects.all()
    serializer_class = RetrieveStudentSerializer

    def get_paginated_response(self, data):
        return Response(data)

class CourseViewSet(viewsets.GenericViewSet,
                   mixins.ListModelMixin,
                   mixins.RetrieveModelMixin):

    queryset = Course.objects.all()
    serializer_class = RetrieveCourseSerializer

    def get_paginated_response(self, data):
        return Response(data)

class SupervisorViewSet(viewsets.GenericViewSet,
                   mixins.ListModelMixin,
                   mixins.RetrieveModelMixin):

    queryset = Supervisor.objects.all()
    serializer_class = RetrieveSupervisorSerializer

    def get_paginated_response(self, data):
        return Response(data)

class CompanyViewSet(viewsets.GenericViewSet,
                   mixins.ListModelMixin,
                   mixins.RetrieveModelMixin):

    queryset = Company.objects.all()
    serializer_class = RetrieveCompanySerializer

    def get_paginated_response(self, data):
        return Response(data)

class PlacementViewSet(viewsets.GenericViewSet,
                   mixins.ListModelMixin,
                   mixins.RetrieveModelMixin):

    queryset = Placement.objects.all()
    serializer_class = RetrievePlacementSerializer

    def get_paginated_response(self, data):
        return Response(data)

class UnitViewSet(viewsets.GenericViewSet,
                   mixins.ListModelMixin,
                   mixins.RetrieveModelMixin):

    queryset = Unit.objects.all()
    serializer_class = RetrieveUnitSerializer

    def get_paginated_response(self, data):
        return Response(data)

class ApplicationViewSet(viewsets.GenericViewSet,
                   mixins.ListModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.CreateModelMixin,
                   mixins.UpdateModelMixin):

    queryset = Application.objects.all()
    serializer_class = RetrieveApplicationSerializer

    def get_paginated_response(self, data):
        return Response(data)

class InterviewViewSet(viewsets.GenericViewSet,
                   mixins.ListModelMixin,
                   mixins.RetrieveModelMixin):

    queryset = Interview.objects.all()
    serializer_class = RetrieveInterviewSerializer

    def get_paginated_response(self, data):
        return Response(data)

class UnitCourseViewSet(viewsets.GenericViewSet,
                   mixins.ListModelMixin,
                   mixins.RetrieveModelMixin):

    queryset = UnitCourse.objects.all()
    serializer_class = RetrieveUnitCourseSerializer

    def get_paginated_response(self, data):
        return Response(data)

class EligibilityRulesViewSet(viewsets.GenericViewSet,
                   mixins.ListModelMixin,
                   mixins.RetrieveModelMixin):

    queryset = EligibilityRules.objects.all()
    serializer_class = RetrieveEligibilityRulesSerializer

    def get_paginated_response(self, data):
        return Response(data)

class ActivityViewSet(viewsets.GenericViewSet,
                   mixins.ListModelMixin,
                   mixins.RetrieveModelMixin):

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


    def get_paginated_response(self,data):
        return Response(data)

class StudentResponse(viewsets.GenericViewSet,
                   mixins.ListModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.CreateModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.DestroyModelMixin):
    queryset = StudentResponse.objects.all()
    serializer_class = RetrieveStudentResponseSerializer

    def get_paginated_response(self, data):
        return Response(data)

class UserResponse(viewsets.GenericViewSet):
    """
    Checks for a Student or Supervisor based on input email, if exists (send 500 if not exist). Will also return their
    data. Return dict with two keys. 'type' is either 'student' or 'supervisor', and 'info' is the Student/Supervisor
    QuerySet as an object. If the Student or Supervisor is not found, a 500 Response is sent.
    """

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
