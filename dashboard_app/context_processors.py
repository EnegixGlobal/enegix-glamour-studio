def user_context(request):

    return {
        'session_user_name': request.session.get('full_name', ''),
        'session_user_role': request.session.get('role', ''),
        'session_user_email': request.session.get('email', ''),
        'session_user_type': request.session.get('user_type', ''),
        'is_logged_in': 'user_id' in request.session,
    }