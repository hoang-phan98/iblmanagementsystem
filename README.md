IBL Management System - Django Rest Framework
---

This is the django rest framework backend for the IBL Management System.

# Project Creation

Create the virtual environment in the root directory
```
$ python3 -m venv ./IBLManagementSystemDRFVenv
```

Activate the virtual environment
```
./IBLManagementSystemDRFVenv/Scripts/activate
```

Install the dependencies
```
$ pip install django
$ pip install djangorestframework
```

Start an empty Django project
```
$ django-admin startproject IBLManagementSystemDRF .
```

Create the app that encapsulates all the models:
- Apps create logical separation between similar models in the system
- Models in different apps can still have connections between them
- Main purpose is for maintainability and separation of concerns
```
$ django-admin startapp core
```

Ensure that the app is registered in `/IBLManagementSystemDRF/settings.py`
```
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'IBLManagementSystemDRF',
    'core',
]
```

A folder is created within the app (/app/api) to contain all DRF information
```
$ mkdir core/api
```

Create the following files in the app:
- `__init__.py`
    - An empty file that python uses to flag that this folder is a package
- `serializers.py`
    - Defines all the serializers for this app
    - A serializer defines how to form the django model (object in the database) to a JSON object
    - Useful for when you want to filter fields in the JSON response, or when you want to have multiple API's for a single object, etc...
    - Acts like a DTO (Data Transfer Object)
- `views.py`
    - Defines ViewSets which dictate the GET/SET/UPDATE rules of the API
    - Utilises the serializers to define that is shown
    - Can perform validation and data processing here
    - Works on the API level
- `urls.py`
    - Defines the api routing and which ViewSet will be used for the specified URL path
    - Links the app's routing to the main router

## Creating an End Point
Below are the steps to create an endpoint from start to finish

### Creating a Model
First you will need to create a model (database object) in the `models.py` file at the app level
```
class Course(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    course_code = models.CharField(max_length=7)
    course_name = models.CharField(max_length=255)

class SuperVisor(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    given_name = models.CharField(max_length=256)
    family_name = models.CharField(max_length=256)
    email = models.CharField(max_length=256)

class Student(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    supervisor = models.ForeinKey(SuperVisor, on_delete=models.CASCADE)
    given_name = models.CharField(max_length=256)
    family_name = models.CharField(max_length=256)
    email = models.CharField(max_length=256)
```

- A full list of fields can be found at:
    - https://docs.djangoproject.com/en/3.0/ref/models/fields/
- Note that you have to define the foreign objects before using them as foreign keys (Course is defined before Student)
- `Foreign Keys Fields` are used for one-to-many relationships, `One-to-One Fields` are used for one-to-one relationships
- More detailed examples of relationships can be found at:
    - https://docs.djangoproject.com/en/3.0/topics/db/examples/one_to_one/
    - https://docs.djangoproject.com/en/3.0/topics/db/examples/many_to_one/

### Creating a serializer
A serializer will define how the django model will be presented. Which fields to will be shown in the API.

```
from core.models import Course, Supervisor, Student
from rest_framework import serializers

class RetrieveStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ["given_name", "family_name", "course", "supervisor", "email"]

class RetrieveCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ["course_code", "course_name", "student_set"]


class RetrieveSupervisorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supervisor
        fields = ["given_name", "family_name", "student_set", "email"]

```

- The fields correspond the what fields will be presented and the order in which they will appear
- In a one-to-many relationship, the `many` side (student) will have direct access to the `one` side (course and supervisor) by the field name
- In a one-to-many relationship, the `one` side (course and supervisor) will have access to the set of the `many` side (student) by the field name appended by `_set` (student_set)

### Creating a viewset
The viewset will now define the API logic utilising the objects we have just created.

```
from rest_framework import viewsets, mixins
from rest_framework.response import Response
from core.api.serializers import RetrieveCourseSerializer, RetrieveStudentSerializer, RetrieveSupervisorSerializer
from core.models import Student, Course, Supervisor

class StudentViewSet(viewsets.GenericViewSet,
                   mixins.ListModelMixin,
                   mixins.RetrieveModelMixin):

    queryset = Student.objects.all()
    serializer_class = RetrieveStudentSerializer
    lookup_field = email

    def get_paginated_response(self, data):
        return Response(data)
```

- First we inherit from `GenericViewSet` which defines basic properties of the viewset
- Then we inherit from the `mixins` of the functionality we want the API to have
    - Inheriting from `mixins.ListModelMixin` creates an API which gets a list of all students
    - Inheriting from `mixins.RetreiveModelMixin` creates an API which gets a single student
- The API's are created with barebones basic functionality based of logic in the serializer
    - If more fine tuned logic needs to be implemented, override the functions of the `mixin`
    - https://github.com/encode/django-rest-framework/blob/master/rest_framework/mixins.py

### Registering the API (Routing)
After defining the API logic, it will need to be linked to the django system using routing.
```
from rest_framework import routers
from core.api import views as core_views

router = routers.DefaultRouter()
router.register('student', core_views.StudentViewSet, basename='Student')
```

- A router is created for the current app
- The viewset is then registered to the router at path `/student`

The app's router will now need to be registered to the main router.
```
from core.api.urls import router as core_router

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/core/', include(core_router.urls)),
]
```

- The app's router is imported to the main router found in `/IBLManagementSystemDRF/urls.py`
- The router's URL is then included in the `urlpatterns` array

## Running the Server
Create the virtual environment in the root directory (only needs to be done once)
```
$ python3 -m venv ./IBLManagementSystemDRFVenv
```

Activate the virtual environment
```
./IBLManagementSystemDRFVenv/Scripts/activate
```

Install the dependencies (only needs to be done once)
```
$ pip install -r requirements.txt
```

If changes were made to the database you need to `makemigrations` which creates a file that defines how the database changed from the last version
```
$ python manage.py makemigrations
```

Ensure that your version of the database (tables and relationships) is up to date
```
$ python manage.py migrate
```

Run the django server
```
$ python manage.py runserver
```
