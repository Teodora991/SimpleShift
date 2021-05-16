from shifts.forms import ShiftForm
from shifts.models import Employee, Shift, ShiftEmployee, Job
from shifts.mixins import AdminRequiredMixin
from django.views import generic
from django.shortcuts import get_object_or_404, redirect, reverse
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.decorators import user_passes_test, login_required
from notifications.signals import notify


class ShiftCreateView(LoginRequiredMixin, AdminRequiredMixin, SuccessMessageMixin, generic.CreateView):
    template_name = 'shifts/shift_create.html'
    form_class = ShiftForm
    success_message = 'You have successfully created a new shift.'

    def get_success_url(self):
        shift = self.object
        return reverse("shifts:shift_detail", kwargs={'pk': shift.pk})

    def get(self, request, *args, **kwargs):
        if not Job.objects.all():
            messages.warning(
                request,
                "You haven't created jobs yet. Create jobs <a href='/jobs/create/'>here</a>.")
            return redirect('shifts:shift_list')
        self.object = None
        return super().get(request, *args, **kwargs)


class ShiftListView(LoginRequiredMixin, generic.ListView):
    template_name = 'shifts/shift_list.html'

    def get_queryset(self):
        user = self.request.user
        queryset = Shift.objects.order_by('job_type__title', 'start_time')
        if self.request.user.is_employee:
            queryset = queryset.filter(job_type__in=self.request.user.job.all())
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ShiftListView, self).get_context_data(**kwargs)
        user = self.request.user
        queryset = ShiftEmployee.objects.filter(employee_id=user.id).order_by('shift__start_time')
        assigned = [shiftemployee.shift for shiftemployee in ShiftEmployee.objects.filter(employee_id=user.id)]
        context.update({
            'assigned_shifts': queryset,
            # list of assigned_shifts
            'assigned': assigned,
        })
        return context


class ShiftDetailView(LoginRequiredMixin, generic.DetailView):
    template_name = 'shifts/shift_detail.html'
    queryset = Shift.objects.all()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ShiftDetailView, self).get_context_data(**kwargs)
        employees = Employee.objects.all()
        employees_list = [obj.employee for obj in context['shift'].assigned.all()]

        context.update({
            "employees": employees,
            # list of assigned employees
            'employees_list': employees_list,
        })
        return context


class ShiftUpdateView(LoginRequiredMixin, AdminRequiredMixin, SuccessMessageMixin, generic.UpdateView):
    template_name = 'shifts/shift_update.html'
    queryset = Shift.objects.all()
    form_class = ShiftForm
    success_message = 'You have successfully updated the shift.'

    def get_success_url(self):
        return reverse("shifts:shift_detail", kwargs={'pk': self.object.pk})


class ShiftDeleteView(LoginRequiredMixin, AdminRequiredMixin, SuccessMessageMixin, generic.DeleteView):
    template_name = 'shifts/shift_delete.html'
    queryset = Shift.objects.all()
    success_message = 'You have successfully deleted the shift.'

    def get_success_url(self):
        return reverse("shifts:shift_list")


@login_required
def apply_for_shift(request, pk):
    shift = get_object_or_404(Shift, pk=pk)
    overlap = any([shift.overlap(assigned_shift) for assigned_shift in request.user.assigned.all()])

    if overlap:
        messages.warning(
            request,
            "You can't apply for this shift because it overlaps with another shift that has already been assigned to you")
        return redirect('shifts:shift_list')
    else:
        if not ShiftEmployee.objects.filter(shift_id=shift.id).filter(employee_id=request.user.id):
            shift.apply(request.user)
            receiver = [request.user] + [obj for obj in Employee.objects.filter(is_admin=True) if obj != request.user]
            notify.send(
                sender=request.user,
                recipient=receiver,
                verb='Shift application',
                description=f'{request.user} applied for a shift.')
            return redirect('shifts:shift_detail', pk=pk)
    return redirect('shifts:shift_list')


@login_required
@user_passes_test(lambda u: u.is_admin, login_url='home')
def assign_to_shift(request, pk, employee_pk):
    shift = get_object_or_404(Shift, pk=pk)
    employee = get_object_or_404(Employee, pk=employee_pk)
    overlap = any([shift.overlap(assigned_shift) for assigned_shift in employee.assigned.all()])

    if overlap:
        messages.warning(request, "This shift overlaps with another shift already assigned to the worker")
        return redirect('shifts:shift_detail', pk=pk)
    else:
        if not ShiftEmployee.objects.filter(shift_id=shift.id).filter(employee_id=employee.id):
            shift.apply(employee)
            notify.send(
                sender=request.user,
                recipient=employee,
                verb='Assignment',
                description=f'A new shift has been assigned to you.')
            return redirect('shifts:shift_detail', pk=pk)

    return redirect('shifts:shift_detail', pk=pk)