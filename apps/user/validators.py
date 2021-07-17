from rest_framework.exceptions import ValidationError


def validate_hour_minute_format(time_str):
    """
    check if time_str matches following format:
    "hh:mm"
    if not matches, then raise ValidationError
    """
    error_message = 'Please input correct hour/minute. For example: 10:00'
    try:
        hour, minute = map(int, time_str.split(':'))
        if hour < 0 or hour > 23 or minute < 0 or minute > 59:
            raise ValidationError(error_message)
    except ValueError:
        raise ValidationError(error_message)