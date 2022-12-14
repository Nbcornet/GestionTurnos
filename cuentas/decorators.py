# from urllib import request
from django.http import HttpResponse
from django.shortcuts import redirect
# from django.core.exceptions import PermissionDenied

def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('/') # en caso de que el usuario esté autenticado, redirige a Home page
        else:
            # retorna Login Page
            return view_func(request, *args, **kwargs)

    return wrapper_func

def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request,*args,**kwargs):
            
            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
            
            if group in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse('No está autorizado a ver esta página')    
            
        return wrapper_func
    return decorator

