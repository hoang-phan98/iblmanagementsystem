from django.http import HttpResponse, HttpResponseServerError
from rest_framework import viewsets
from eligibility.config import MINIMUM_ROUNDED_WAM
import json
from core.models import Student


class WamCheck(viewsets.GenericViewSet):
    """
    Pass in Student ID as pk, e.g. /wam/12345678
    If student found, return JSON with student_id and a 'success' Boolean field in 200 Ok
    Else return student_id in 500 Internal Server Error
    """
    def retrieve(self, request, pk=None):
        if pk is None:
            return HttpResponseServerError()
        student_obj = Student.objects.filter(id__exact=str(pk)).first()
        res = {
            'student_id': pk
        }
        if student_obj:
            result = round(student_obj.WAM) > MINIMUM_ROUNDED_WAM
            res['success'] = result
            return HttpResponse(json.dumps(res), content_type='application/json')
        else:
            return HttpResponseServerError(json.dumps(res), content_type='application/json')
