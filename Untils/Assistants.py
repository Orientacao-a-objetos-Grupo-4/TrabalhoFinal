from datetime import timedelta

def uuid_from_maybe_string(value):
    import uuid
    if isinstance(value, uuid.UUID):
        return value
    try:
        return uuid.UUID(value)
    except (ValueError, TypeError):
        return None
    
def date_emp_plus_days(dt, days):
    return dt + timedelta(days=days)