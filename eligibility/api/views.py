from django.http import HttpResponse, HttpRequest, HttpResponseBadRequest
from eligibility.config import MINIMUM_ROUNDED_WAM
import json
from core.models import Student


# pass in student ID as a query string, e.g. ?student_id=12345678
# returns a JSON with the student_id, and a 'success' Boolean field if student is found as 200
# if student not found, returns only student_id as 400 Bad Request
def wam(req: HttpRequest):
    student_id = req.GET["student_id"]
    student_obj = Student.objects.filter(id__exact=str(student_id)).first()
    res = {
        'student_id': student_id
    }
    if student_obj:
        result = round(student_obj.WAM) > MINIMUM_ROUNDED_WAM
        res['success'] = result
        return HttpResponse(json.dumps(res), content_type='application/json')
    else:
        return HttpResponseBadRequest(json.dumps(res), content_type='application/json')
