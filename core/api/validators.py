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


