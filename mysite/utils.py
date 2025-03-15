



def define_toast_message(request, message, error=False, redirect=False):
    request.session["toast"] = {'message': message, 'error': error, 'redirect': redirect}