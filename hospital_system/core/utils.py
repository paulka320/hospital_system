def is_reception(user):
    return user.groups.filter(name='Receptionist').exists()
def is_doctor(user):
    return user.groups.filter(name='Doctor').exists()
def is_lab(user):
    return user.groups.filter(name='LabAttendant').exists()