from datetime import timedelta
from shifts.models import Employee, ShiftEmployee
from django.views import generic
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin


class LiveShiftListView(LoginRequiredMixin, generic.ListView):
    template_name = 'shifts/live_shift_list.html'

    def get_queryset(self):
        queryset = ShiftEmployee.objects.all()
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(LiveShiftListView, self).get_context_data(**kwargs)
        # actual_shifts = current_shifts + 1h overtime
        actual_shifts = context['object_list'].filter(shift__start_time__lte=timezone.now()).filter(shift__end_time__gte=timezone.now()-timedelta(hours=1))
        current_shifts = actual_shifts.filter(shift__end_time__gte=timezone.now())

        time_threshold = timezone.now() + timedelta(hours=2)
        next_2h = context['object_list'].filter(shift__start_time__gt=timezone.now()).filter(shift__start_time__lte=time_threshold)

        actual_employees_id_lst = [obj.employee.id for obj in actual_shifts]
        logged_employees = Employee.objects.filter(is_logged=True).exclude(id__in=actual_employees_id_lst)

        context.update({
           'actual_shifts': actual_shifts,
            'next_2h': next_2h,
            'logged_employees': logged_employees,
            'current_shifts': current_shifts,
        })

        return context
