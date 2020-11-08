import uuid
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from .api.validators import *


class Course(models.Model):
    code = models.CharField(primary_key=True, max_length=5, editable=True, validators=[validate_course_code])
    course_name = models.CharField(max_length=255)

class Unit(models.Model):
    code = models.CharField(primary_key=True, max_length=7, editable=True, validators=[validate_unit_code])
    name = models.CharField(max_length=256)
    is_ibl_unit = models.BooleanField()
    credit_points = models.PositiveIntegerField()
    duration = models.PositiveIntegerField()

class UnitCourse(models.Model):
    class Meta:
        unique_together = ('unit', 'course')

    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    year = models.PositiveIntegerField(validators=[validate_unitcourse_year])
    semester = models.PositiveIntegerField()

class Supervisor(models.Model):
    id = models.CharField(primary_key=True, max_length=10, editable=True)
    given_name = models.CharField(max_length=256)
    family_name = models.CharField(max_length=256)
    email = models.EmailField(max_length=256)

class Student(models.Model):
    id = models.CharField(primary_key=True, max_length=8, editable=True, validators=[validate_student_id])
    given_name = models.CharField(max_length=256)
    family_name = models.CharField(max_length=256)
    WAM = models.DecimalField(max_digits=5, decimal_places=2, validators=[validate_student_wam])
    credit_points = models.PositiveIntegerField(validators=[validate_credit_points])
    supervisor = models.ForeignKey(Supervisor, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    email = models.EmailField(max_length=256, validators=[validate_school_email])

class Company(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company_name = models.CharField(max_length=256)

class Placement(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    semester = models.PositiveIntegerField()
    year = models.PositiveIntegerField(validators=[validate_year])
    role = models.CharField(max_length=256)
    department = models.CharField(max_length=256)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

# class PrereqConjunction(models.Model):
#     class Meta:
#         unique_together = (('unit_code', 'prereq_unit_code'),)

#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     unit_code = models.ForeignKey(Unit, on_delete=models.CASCADE)
#     prereq_unit_code = models.ForeignKey(Unit, on_delete=models.CASCADE)

class EligibilityRules(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)

class Application(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    status = models.CharField(max_length=1, default=("I", "Incomplete"), choices=[("I", "Incomplete"),
                                                                                  ("C", "Completed")])
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date_started = models.DateField(auto_now_add=True)
    date_completed = models.DateField(default=None, blank=True, null=True)
    year_preference = models.PositiveIntegerField(validators=[validate_year])
    semester_preference = models.CharField(max_length=1, choices=[("1", "1"), ("2", "2")])

class Activity(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

class Interview(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True)
    supervisor = models.ForeignKey(Supervisor, on_delete=models.CASCADE)
    title = models.TextField()
    notes = models.TextField(blank=True)
    # ----------
    application = models.ForeignKey(Application, on_delete=models.CASCADE, null=True)
    location = models.CharField(max_length=256, blank=True)
    outcome_details = models.CharField(max_length=1, blank=True, choices=[("S", "Successful"), ("U", "Unsuccessful")])
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True)

class QuestionnaireTemplate(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    #Currently just a TetField to store the JSON. JSONField can be used in Postgres.
    #Otherwise could also use https://github.com/rpkilby/jsonfield
    questions = models.TextField() 
    active = models.BooleanField()

class StudentResponse(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    response = models.TextField()

class StudentUnit(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
    year = models.PositiveIntegerField(validators=[validate_year])
    semester = models.PositiveIntegerField()
    Pass = models.BooleanField()
    


class CourseMapSnapshot(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    application = models.ForeignKey(Application, on_delete=models.CASCADE)
    Snapshot = models.TextField() 
    approval = models.BooleanField()
