# import login required mixin
# from django.contrib.auth.mixins import LoginRequiredMixin
# import redirect
from django.shortcuts import redirect
# make a mixin form medico


#
class MedicoMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('/login')
        if not request.user.groups.filter(name='medico').exists():
            return redirect('/login')
        return super(MedicoMixin, self).dispatch(request, *args, **kwargs)
