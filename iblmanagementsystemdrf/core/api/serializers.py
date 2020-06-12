from core.models import Course, Supervisor, Student
from rest_framework import serializers

class RetrieveStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ["given_name", "family_name", "course", "supervisor"]

class RetrieveCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ["course_code", "course_name", "student_set"]


class RetrieveSupervisorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supervisor
        fields = ["given_name", "family_name", "student_set"]
