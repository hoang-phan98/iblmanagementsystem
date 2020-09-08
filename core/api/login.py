from django.http import HttpResponse, HttpRequest, HttpResponseServerError
import json
from core.models import Student, Supervisor
from core.api.serializers import RetrieveStudentSerializer, RetrieveSupervisorSerializer


def login(req: HttpRequest, email: str):
    """
    Checks for a Student or Supervisor based on input email, if exists (send 500 if not exist). Will also return their
    data.
    :param req: Not used
    :param email: Full email to check for
    :return: Dict with two keys. 'type' is either 'student' or 'supervisor', and 'info' is the Student/Supervisor
    QuerySet as an object. If the Student or Supervisor is not found, a 500 Response is sent.
    """
    is_student = True
    obj = Student.objects.filter(email__exact=str(email)).first()
    if not obj:
        is_student = False
        obj = Supervisor.objects.filter(email__exact=str(email)).first()
    if not obj:
        return HttpResponseServerError()
    if is_student:
        s = RetrieveStudentSerializer(obj)
    else:
        s = RetrieveSupervisorSerializer(obj)
    res = {
        'type': 'student' if is_student else 'supervisor',
        'info': s.data
    }
    return HttpResponse(json.dumps(res), content_type='application/json')
