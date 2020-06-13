import uuid
from django.db import models

class Course(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    course_code = models.CharField(max_length=7)
    course_name = models.CharField(max_length=255)

class Supervisor(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    given_name = models.CharField(max_length=256)
    family_name = models.CharField(max_length=256)

class Placement(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    semester = models.IntegerField()
    year = models.IntegerField()
    role = models.CharField(max_length=256)
    department = models.CharField(max_length=256)
    student_id = models.IntegerField()
    company_id = models.IntegerField()

class Student(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    supervisor = models.ForeignKey(Supervisor, on_delete=models.CASCADE)
    placement = models.ForeignKey(Placement, on_delete=models.CASCADE)
    given_name = models.CharField(max_length=256)
    family_name = models.CharField(max_length=256)

class Company(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company_name = models.CharField(max_length=256)
    placement = models.ForeignKey(Placement, on_delete=models.CASCADE)

class Unit(models.Model):
    code = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=256)
    year = models.IntegerField()
    semester = models.IntegerField()
    is_ibl_unit = models.BooleanField()

class UnitCourse(models.Model):
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
    course = models.ForeignKey(Placement, on_delete=models.CASCADE)

class Application(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    status = models.CharField(max_length=256)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)