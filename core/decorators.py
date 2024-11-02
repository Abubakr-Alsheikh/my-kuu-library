from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

def admin_required(function):
    """Decorator for views that checks that the user is logged in and is an admin.
    """
    @login_required
    def wrapper(request, *args, **kwargs):
        if request.user.is_staff:
            return function(request, *args, **kwargs)
        else:
            return redirect('core:home')  # Redirect to your app's home page
    return wrapper