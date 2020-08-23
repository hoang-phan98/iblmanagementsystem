import uuid
from django.db import models

class Course(models.Model):
    code = models.CharField(primary_key=True, max_length=5, editable=True)
    course_name = models.CharField(max_length=255)

class Unit(models.Model):
    code = models.CharField(primary_key=True, max_length=7, editable=True)
    name = models.CharField(max_length=256)
    year = models.PositiveIntegerField()
    semester = models.PositiveIntegerField()
    is_ibl_unit = models.BooleanField()

class UnitCourse(models.Model):
    class Meta:
        unique_together = ('unit', 'course')

    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

class Supervisor(models.Model):
    id = models.CharField(primary_key=True, max_length=10, editable=True)
    given_name = models.CharField(max_length=256)
    family_name = models.CharField(max_length=256)
    email = models.CharField(max_length=256)


class Student(models.Model):
    id = models.CharField(primary_key=True, max_length=8, editable=True)
    given_name = models.CharField(max_length=256)
    family_name = models.CharField(max_length=256)
    WAM = models.FloatField()
    credit_points = models.PositiveIntegerField()
    supervisor = models.ForeignKey(Supervisor, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    email = models.CharField(max_length=256)

class Company(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company_name = models.CharField(max_length=256)

class Placement(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    semester = models.PositiveIntegerField()
    year = models.PositiveIntegerField()
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
    status = models.CharField(max_length=256)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)

class Activity(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

class Interview(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    time = models.DateTimeField()
    location = models.CharField(max_length=256)
    outcome_details = models.CharField(max_length=256)
    application = models.ForeignKey(Application, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    staff = models.ForeignKey(Supervisor, on_delete=models.CASCADE)
