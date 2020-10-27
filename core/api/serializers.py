from ..models import *
from rest_framework import serializers

class RetrieveStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ["id", "given_name", "family_name", "course", "supervisor", "WAM", "credit_points", "email",
                  "interview_set", "placement_set", "application_set"]

class RetrieveCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ["code", "course_name", "student_set"]

class RetrieveSupervisorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supervisor
        fields = ["id", "given_name", "family_name", "student_set", "interview_set", "email"]

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
        fields = ["code", "name", "is_ibl_unit", "credit_points", "duration"]

class RetrieveUnitCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnitCourse
        fields = ["unit", "course", "year", "semester"]

class RetrieveApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = ["status", "student", "date_started", "date_completed", "year_preference","semester_preference"]

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

class RetrieveQuestionnaireTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionnaireTemplate
        fields = ["questions", "active"]

class RetrieveStudentResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentResponse
        fields = ["id", "response"]

class RetrieveStudentUnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentUnit
        fields = ["id", "student", "unit", "year", "semester", "Pass"]

class RerieveCourseMapSnapshotSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseMapSnapshot
        fields = ["id", "Snapshot", "application", "approval"]

# class RetrievePrereqConjunction(serializers.ModelSerializer):
#     class Meta:
#         model = PrereqConjunction
#         fields = ["unit_code"]

