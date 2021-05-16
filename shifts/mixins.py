from django.contrib.auth.mixins import AccessMixin
from django.shortcuts import redirect


class AdminRequiredMixin(AccessMixin):
    """Verify that the current user is an admin."""
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_employee:
            return redirect("shifts:shift_list")
        return super().dispatch(request, *args, **kwargs)

