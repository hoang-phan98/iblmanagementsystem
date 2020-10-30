from rest_framework import viewsets, mixins
from rest_framework.response import Response
from .serializers import *
from django.http import HttpResponse, HttpResponseServerError
from ..models import *
import json
from rest_framework.permissions import BasePermission, IsAuthenticated
from authentication.api.permissions import HasGroupPermission
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
import datetime

class StudentViewSet(viewsets.GenericViewSet,
                   mixins.ListModelMixin,
                   mixins.RetrieveModelMixin):

    queryset = Student.objects.all()
    serializer_class = RetrieveStudentSerializer
    permission_classes = [HasGroupPermission]
    required_groups = {
         'GET': ['student', 'staff'],
         'POST': ['student', 'staff'],
         'PUT': ['student', 'staff'],
     }

    def get_paginated_response(self, data):
        return Response(data)

class CourseViewSet(viewsets.GenericViewSet,
                   mixins.ListModelMixin,
                   mixins.RetrieveModelMixin):

    queryset = Course.objects.all()
    serializer_class = RetrieveCourseSerializer
    permission_classes = [HasGroupPermission]
    required_groups = {
         'GET': ['student', 'staff'],
         'POST': ['student', 'staff'],
         'PUT': ['student', 'staff'],
     }

    def get_paginated_response(self, data):
        return Response(data)

class SupervisorViewSet(viewsets.GenericViewSet,
                   mixins.ListModelMixin,
                   mixins.RetrieveModelMixin):

    queryset = Supervisor.objects.all()
    serializer_class = RetrieveSupervisorSerializer
    permission_classes = [HasGroupPermission]
    required_groups = {
         'GET': ['student', 'staff'],
         'POST': ['student', 'staff'],
         'PUT': ['student', 'staff'],
     }

    def get_paginated_response(self, data):
        return Response(data)

class CompanyViewSet(viewsets.GenericViewSet,
                   mixins.ListModelMixin,
                   mixins.RetrieveModelMixin):

    queryset = Company.objects.all()
    serializer_class = RetrieveCompanySerializer
    permission_classes = [HasGroupPermission]
    required_groups = {
         'GET': ['student', 'staff'],
         'POST': ['student', 'staff'],
         'PUT': ['student', 'staff'],
     }

    def get_paginated_response(self, data):
        return Response(data)

class PlacementViewSet(viewsets.GenericViewSet,
                   mixins.ListModelMixin,
                   mixins.RetrieveModelMixin):

    queryset = Placement.objects.all()
    serializer_class = RetrievePlacementSerializer
    permission_classes = [HasGroupPermission]
    required_groups = {
         'GET': ['student', 'staff'],
         'POST': ['student', 'staff'],
         'PUT': ['student', 'staff'],
     }

    def get_paginated_response(self, data):
        return Response(data)

class UnitViewSet(viewsets.GenericViewSet,
                   mixins.ListModelMixin,
                   mixins.RetrieveModelMixin):

    queryset = Unit.objects.all()
    serializer_class = RetrieveUnitSerializer
    permission_classes = [HasGroupPermission]
    required_groups = {
         'GET': ['student', 'staff'],
         'POST': ['student', 'staff'],
         'PUT': ['student', 'staff'],
     }

    def get_paginated_response(self, data):
        return Response(data)

class ApplicationViewSet(viewsets.GenericViewSet,
                   mixins.ListModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.CreateModelMixin,
                   mixins.UpdateModelMixin):

    queryset = Application.objects.all()
    serializer_class = RetrieveApplicationSerializer
    permission_classes = [HasGroupPermission]
    required_groups = {
         'GET': ['student', 'staff'],
         'POST': ['student', 'staff'],
         'PUT': ['student', 'staff'],
     }

    def get_paginated_response(self, data):
        return Response(data)

    def list(self, request, *args, **kwargs):

        # Get current user
        user = self.request.user

        # If user is staff, show all applications
        if self.is_member(user, "Staff"):
            query_set = Application.objects.all()

        # If user is student, show relevant application
        elif self.is_member(user, "Student"):
            query_set = Application.objects.filter(student__email__contains=user.email)

        else:
            query_set = None

        serializer = RetrieveApplicationSerializer(query_set, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):

        # Get current user
        user = self.request.user

        # If user is staff, show application
        if self.is_member(user, "Staff"):
            query_set = Application.objects.all()
            application = get_object_or_404(query_set, pk=pk)

        # If user is student, only show application if relevant
        elif self.is_member(user, "Student"):
            query_set = Application.objects.filter(student__email__contains=user.email)
            application = get_object_or_404(query_set, pk=pk)
        else:
            application = None

        serializer = RetrieveApplicationSerializer(application)
        return Response(serializer.data)

    def is_member(self, user, group):
        return user.groups.filter(name=group).exists()

class InterviewSlotViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.RetrieveModelMixin,
                            mixins.CreateModelMixin, mixins.DestroyModelMixin):
   
    queryset = InterviewSlot.objects.all()
    serializer_class = RetrieveInterviewSlotSerializer
    permission_classes = [HasGroupPermission]
    required_groups = {
         'GET': ['student', 'staff'],
         'POST': ['student', 'staff'],
         'PUT': ['student', 'staff'],
     }


    """
        The list function overrides the ListModelMixin list function to also provide the functionality
        of providing a start and end date to filter the time slots returned when considering the day (not time)
        If none is provided then the origin ListModelMixin list function is utilised.
        Add /?start=year,month,day&end=year,month,day to the end of the url to filter
    """
    def list(self, request, *args, **kwargs):
        start = request.query_params.get('start', None)
        end = request.query_params.get('end', None)

        if start is None or end is None:
            return super().list(request, args, kwargs)
        
        try:
           start = list(map(int, start.split(",")))
           end = list(map(int, end.split(",")))
           start = datetime.datetime(start[0], start[1], start[2])
           end = datetime.datetime(end[0], end[1], end[2])
           slots = InterviewSlot.objects.filter(date__range=[start,end])
           serializer = RetrieveInterviewSlotSerializer(slots, many=True)
           return Response({"data": serializer.data, "error": ""})
        except:
           return Response({"data":"", "error": "Error when filtering the range of dates"})



    """
        The createbatch method provides a way to create a batch of interview times in a single
        request rather than having to make multiple requests for each. Note that it is possible
        for there to be multiples of the same time as there may be more than one interviewer. 
        Parameters:
            request - Request should be a JSON/dict object that includes the key time_slots. time_slots
                requires to be a list of lists. Each inner list should contain the following integers:
                [year, month, day, hour (24 hour time), minute]

    """
    @action(detail=False, methods=['post'])
    def createbatch(self, request, *args, **kwargs):
        if "time_slots" not in request.data.keys():
            return Response({"data": "", "error": "Missing 'time_slots' key in the request"})

        if type(request.data["time_slots"]) != list:
            return Response({"data":"", "error": "time_slots key data is not a list"})

        created_slots = []

        for i, timeslot in enumerate(request.data["time_slots"]):
            try:
                new_date_time = datetime.datetime(timeslot[0],timeslot[1],timeslot[2], hour=timeslot[3], minute=timeslot[4])
                created_model = InterviewSlot.objects.create(date=new_date_time)
                created_slots.append(created_model.id)
            except:
                return Response({"data": created_slots,
                                "error": "Error when processing a date. Index of date that failed was: " + str(i)})

        return Response({"data":created_slots,"error":""})
        #super().create

    def get_paginated_response(self, data):
        return Response(data)





class InterviewViewSet(viewsets.GenericViewSet,
                   mixins.ListModelMixin,
                   mixins.RetrieveModelMixin):

    queryset = Interview.objects.all()
    serializer_class = RetrieveInterviewSerializer
    permission_classes = [HasGroupPermission]
    required_groups = {
         'GET': ['student', 'staff'],
         'POST': ['student', 'staff'],
         'PUT': ['student', 'staff'],
     }

    def get_paginated_response(self, data):
        return Response(data)

class UnitCourseViewSet(viewsets.GenericViewSet,
                   mixins.ListModelMixin,
                   mixins.RetrieveModelMixin):

    queryset = UnitCourse.objects.all()
    serializer_class = RetrieveUnitCourseSerializer
    permission_classes = [HasGroupPermission]
    required_groups = {
         'GET': ['student', 'staff'],
         'POST': ['student', 'staff'],
         'PUT': ['student', 'staff'],
     }

    def get_paginated_response(self, data):
        return Response(data)

class EligibilityRulesViewSet(viewsets.GenericViewSet,
                   mixins.ListModelMixin,
                   mixins.RetrieveModelMixin):

    queryset = EligibilityRules.objects.all()
    serializer_class = RetrieveEligibilityRulesSerializer
    permission_classes = [HasGroupPermission]
    required_groups = {
         'GET': ['student', 'staff'],
         'POST': ['student', 'staff'],
         'PUT': ['student', 'staff'],
     }

    def get_paginated_response(self, data):
        return Response(data)

class ActivityViewSet(viewsets.GenericViewSet,
                   mixins.ListModelMixin,
                   mixins.RetrieveModelMixin):

    queryset = Activity.objects.all()
    serializer_class = RetrieveActivitySerializer
    permission_classes = [HasGroupPermission]
    required_groups = {
         'GET': ['student', 'staff'],
         'POST': ['student', 'staff'],
         'PUT': ['student', 'staff'],
     }

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
    permission_classes = [HasGroupPermission]
    required_groups = {
         'GET': ['student', 'staff'],
         'POST': ['student', 'staff'],
         'PUT': ['student', 'staff'],
     }

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
        validateJson = self.validateTemplateJson(request.data)
        if response_query is None or validateJson != "":
            return Response(validateJson)

        return super().update(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        validateJson = self.validateTemplateJson(request.data)
        if validateJson != "":
            return Response(validateJson)

        return super().create(request, *args, **kwargs)


    """
        The validateTemplateJson function for the student response class ensures that a string given can be converted to
        JSON. Valid JSON formats conform to following:
            questions: [{"question": "question here", "format": "A format to display the question on the frontend"}]
            To further elaborate format, this field can be used to specify how the question should be presented.
            For example if the question was a radio button selection the format may be: radio buttons

        Parameters:
            request_data: The data from the request
        Returns:
            A boolean of if the string meets the above requirements.
    """
    def validateTemplateJson(self, request_data):
        try:
            questions = json.loads(request_data["questions"]) 

            #Checking that all the fields are the specified format.
            if len(questions) == 0:
                return "questions is empty."

            for i in range(len(questions)):
                keys = list(questions[i].keys())
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

    queryset = StudentResponse.objects.all()
    serializer_class = RetrieveStudentResponseSerializer
    permission_classes = [HasGroupPermission]
    required_groups = {
         'GET': ['student', 'staff'],
         'POST': ['student', 'staff'],
         'PUT': ['student', 'staff'],
     }

    def update(self, request, *args, **kwargs):
        validateJson = self.validateResponseJson(request.data)
        if validateJson != "":
            return Response(validateJson)

        return super().update(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        validateJson = self.validateResponseJson(request.data)
        if validateJson != "":
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
    def validateResponseJson(self, request_data):
        try:

            responses = json.loads(request_data["response"]) 

            #Checking that all the fields are the specified format.
            if len(responses) == 0:
                return "There are no question and answers present."

            for i in range(len(responses)):
                keys = list(responses[i].keys())
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

    lookup_value_regex = '[^/]+'
    permission_classes = [HasGroupPermission]
    required_groups = {
         'GET': ['student', 'staff'],
         'POST': ['student', 'staff'],
         'PUT': ['student', 'staff'],
     }

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

class StudentUnitViewset(viewsets.GenericViewSet,
                   mixins.ListModelMixin,
                   mixins.RetrieveModelMixin):
    queryset = StudentUnit.objects.all()
    serializer_class = RetrieveStudentUnitSerializer
    def get_paginated_response(self, data):
        return Response(data)
        
        
class CourseMapSnapshotViewset(viewsets.GenericViewSet,
                   mixins.ListModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.CreateModelMixin):
    queryset = CourseMapSnapshot.objects.all()
    serializer_class = RerieveCourseMapSnapshotSerializer
    def get_paginated_response(self, data):
        return Response(data)


    def create(self, request, *args, **kwargs):
        snapshot_query = request.POST.get("snapshot") 
        validateSnapshotJson = self.validateSnapshotJson(snapshot_query)
        if snapshot_query is None or validateSnapshotJson != "":
            return Response(validateSnapshotJson)

        return super().create(request, *args, **kwargs)

    def validateSnapshotJson(self, json_object):
        try:
            json_data = json.loads(json_object) #This won't be needed if we use JSONField

            #Checking that there aren't any fields other than the snapshot and the only key is snapshot
            if len(json_data) > 1:
                return "There are too many keys in the JSON object. Only 'snapshot' should be present."

            #If accessing snapshot doesn't work then there's a key error and this will return false
            snapshot_array = json_data['snapshot']

            #Checking that all the fields are the specified format.
            if len(snapshot_array) == 0:
                return "snapshot is empty."

            for i in range(len(snapshot_array)):
                keys = list(snapshot_array[i].keys())
                if keys[0].lower() != 'unitname' or keys[1].lower() != 'year'or keys[2].lower() != 'semester'or keys[3].lower() != 'creditpoint' or keys[4].lower() != 'status'or len(keys) != 5:
                    return "Invalid key in snapshot array."

            return ""
        except:
            return "Invalid JSON object or no 'snapshot' key present in object."


        
# class PrereqConjunctionViewSet(viewsets.GenericViewSet,
#                    mixins.ListModelMixin,
#                    mixins.RetrieveModelMixin):
#
#     queryset = PrereqConjunction.objects.all()
#     serializer_class = RetrievePrereqConjunction
#
#     def get_paginated_response(self, data):
#         return Response(data)
