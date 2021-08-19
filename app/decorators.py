from django.shortcuts import redirect

def only_admin_can_access(view_func):
    def wrapper_func(request, *args, **kwargs):
        
        if request.user.groups.exists():
            for i in request.user.groups.all():
                if i.name == "admin":
                    return view_func(request, *args,**kwargs)

        return redirect('tmc:home')
    
    return wrapper_func

