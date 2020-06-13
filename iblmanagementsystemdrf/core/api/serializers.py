from ..models import Course, Supervisor, Student, Placement, Company
from rest_framework import serializers

class RetrieveStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ["given_name", "family_name", "course", "supervisor", "placement_set"]

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
        fields = ["semester", "year", "role", "department", "student_id", "company_id"]

class RetrieveCompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ["company_name", "placement_set"]
