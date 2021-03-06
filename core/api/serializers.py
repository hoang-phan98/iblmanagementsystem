from ..models import *
from rest_framework import serializers

class RetrieveStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ["id", "given_name", "family_name", "course", "supervisor", "WAM", "credit_points",
                  "interview_set", "placement_set", "application_set"]

class RetrieveCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ["code", "course_name", "student_set"]

class RetrieveSupervisorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supervisor
        fields = ["id", "given_name", "family_name", "student_set", "interview_set"]

class RetrievePlacementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Placement
        fields = ["semester", "year", "role", "department", "student", "company"]

class RetrieveCompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ["company_name"]

class RetrieveUnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unit
        fields = ["code", "name", "year", "semester", "is_ibl_unit"]

class RetrieveUnitCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnitCourse
        fields = ["unit", "course"]

class RetrieveApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = ["status", "student", "unit"]

class RetrieveInterviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interview
        fields = ["time", "location", "outcome_details", "student", "application", "company", "staff"]

class RetrieveEligibilityRulesSerializer(serializers.ModelSerializer):
    class Meta:
        model = EligibilityRules
        fields = ["unit"]

class RetrieveActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = ["id"]

# class RetrievePrereqConjunction(serializers.ModelSerializer):
#     class Meta:
#         model = PrereqConjunction
#         fields = ["unit_code"]

