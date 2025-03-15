from functools import wraps


def clear_toast_messages(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        response = view_func(request, *args, **kwargs)  # Exécuter la vue
        if request.session.get('toast') and request.session.get('toast').get('redirect') == False:
            request.session.pop('toast')
        if request.session.get('toast'):
            request.session['toast']['redirect'] = False
        return response
    return wrapper