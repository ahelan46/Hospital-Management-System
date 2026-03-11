def sidebar_context(request):
    if request.user.is_authenticated:
        return {
            'hasattr_doctor': hasattr(request.user, 'doctor') or (hasattr(request.user, 'role') and request.user.role and request.user.role.upper() == 'DOCTOR'),
            'hasattr_patient': hasattr(request.user, 'patient') or (hasattr(request.user, 'role') and request.user.role and request.user.role.upper() == 'PATIENT'),
        }
    return {}
