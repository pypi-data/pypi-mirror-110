from django.http import HttpResponseForbidden

def super_user_active_only(funct):
    def wrap(request, *args, **kwargs):
        if request.user.is_superuser:
            return funct(request, *args, **kwargs)
        else:
            return HttpResponseForbidden()
    return wrap
