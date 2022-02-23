from django.core.exceptions import PermissionDenied
from django.http import HttpResponseForbidden, HttpResponse
from django.shortcuts import redirect

from profiles.models import Profiles
from accounts.models import MyUser


def is_admin():
    def decorator(view_function):
        def wrap(request, *args, **kwargs):
            if request.user.is_authenticated:
                if request.user.is_admin:
                    return view_function(request, *args, **kwargs)
                else:
                    raise PermissionDenied
            else:
                return redirect('accounts:login')
        return wrap

    return decorator


def is_user():
    def decorator(view_function):
        def wrap(request, *args, **kwargs):
            if request.user.is_authenticated:
                if request.user.is_email_verified:
                    if not request.user.is_user_verified:
                        return HttpResponse('please contact your admin verify your account')
                    if Profiles.objects.filter(user__email=request.user).exists():
                        return view_function(request, *args, **kwargs)
                    else:
                        return redirect('user_dash:profile_create')
                else:
                    return redirect('accounts:verify_email')
            else:
                return redirect('accounts:login')

        return wrap

    return decorator
