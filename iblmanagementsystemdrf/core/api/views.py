from rest_framework import viewsets, mixins
from rest_framework.response import Response
from core.api.serializers import RetrieveCourseSerializer, RetrieveStudentSerializer, RetrieveSupervisorSerializer
from core.models import Student, Course, Supervisor

class StudentViewSet(viewsets.GenericViewSet,
                   mixins.ListModelMixin,
                   mixins.RetrieveModelMixin):

    queryset = Student.objects.all()
    serializer_class = RetrieveStudentSerializer

    def get_paginated_response(self, data):
        return Response(data)
