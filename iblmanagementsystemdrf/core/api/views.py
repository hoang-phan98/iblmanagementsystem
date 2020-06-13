from rest_framework import viewsets, mixins
from rest_framework.response import Response
from .serializers import *
from ..models import *

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
                   mixins.RetrieveModelMixin):

    queryset = Application.objects.all()
    serializer_class = RetrieveUnitSerializer

    def get_paginated_response(self, data):
        return Response(data)

class InterviewViewSet(viewsets.GenericViewSet,
                   mixins.ListModelMixin,
                   mixins.RetrieveModelMixin):

    queryset = Interview.objects.all()
    serializer_class = RetrieveInterviewSerializer

    def get_paginated_response(self, data):
        return Response(data)
