from ..models import *
from rest_framework import serializers

class RetrieveStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ["given_name", "family_name", "course", "supervisor", "placement_set", "application_set"]

class RetrieveCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ["course_code", "course_name", "student_set"]

class RetrieveSupervisorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supervisor
        fields = ["given_name", "family_name", "student_set"]

class RetrievePlacementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Placement
        fields = ["semester", "year", "role", "department", "student", "company"]

class RetrieveCompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ["company_name", "placement_set"]

class RetrieveUnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unit
        fields = ["code", "name", "year", "semester", "is_ibl_unit"]

class RetrieveUnitCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnitCourse
        fields = ["unit_set", "course_set"]

class RetrieveApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = ["status", "student", "unit"]

class RetrieveInterviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interview
        fields = ["time", "location", "outcome", "student_set", "application_set", "supervisor_set", "company_set"]
