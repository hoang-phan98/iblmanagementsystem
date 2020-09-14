from django.core.exceptions import ValidationError


def validate_student_id(student_id):
    """
    Validate that the student is an 8-digit integer
    """
    if len(student_id) != 8:
        try:
            int(student_id)
        except ValueError:
            raise ValidationError("Please enter a valid student ID")
    else:
        return student_id


def validate_course_code(course_code):
    """
    Validate the given course code - 5 characters long and first one is an alphabetic letter
    """
    if str.isalpha(course_code[0]):
        try:
            int(course_code[1:])
            return course_code
        except ValueError:
            raise ValidationError("Please enter a valid course code")
    raise ValidationError("Please enter a valid course code")


def validate_unit_code(unit_code):
    """
    Validate the given unit code - 7 characters long and first 3 are alphabetic
    """
    if str.isalpha(unit_code[:3]):
        try:
            int(unit_code[3:])
            return unit_code
        except ValueError:
            raise ValidationError("Please enter a valid unit code")
    raise ValidationError("Please enter a valid unit code")


def validate_school_email(email):
    """
    Validate that the given email is a Monash Uni email
    """
    if not ".monash.edu" in email:
        raise ValidationError("Please enter a valid Monash email address")
    else:
        return email


def validate_student_wam(wam):
    """
    Validate the given student WAM - between 0-100, 2 decimal places
    """
    if wam < 0 or wam > 100:
        raise ValidationError("Please enter a value between 0 and 100")
    return round(wam, 2)


def validate_credit_points(credit_points):
    """
    Validate the given credit points - must be a multiple of 6
    """
    if credit_points%6 != 0:
        raise ValidationError("Credit points must be a multiple of 6")
    return credit_points


def validate_year(year):
    """
    Validate a given year field - must have fixed length of 4
    """
    if len(str(year)) != 4:
        raise ValidationError("Please enter a valid year")
    return year
