from shifts.forms import AbsenceReportForm
from shifts.models import Employee, ShiftEmployee
from django.utils import timezone
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test, login_required
from notifications.signals import notify


@login_required
def replace_request(request, pk):
    user = request.user
    shift = get_object_or_404(ShiftEmployee, shift_id=pk, employee_id=user.id)
    shift.status_replace()
    notify.send(sender=request.user,
                recipient=Employee.objects.all(),
                verb='Replacement',
                description=f'{user} is looking for a replacement for a shift.')
    return redirect('shifts:shift_list')


@login_required
def make_replacement(request, pk, to_replace_pk):
    shiftemployee = get_object_or_404(ShiftEmployee, shift_id=pk, employee_id=to_replace_pk)
    replaced_employee = shiftemployee.employee
    user = request.user
    # Returns True if shift overlaps with any other shift already assigned to the user
    overlap = any([shiftemployee.shift.overlap(assign_shift) for assign_shift in user.assigned.all()])
    if overlap:
        messages.warning(request,
                       "You can't apply for this shift because it overlaps with another shift that has already been assigned to you")
        return redirect('shifts:shift_list')

    elif shiftemployee.shift.job_type in user.job.all():
        shiftemployee.make_replacement(user)
        messages.success(request, f'You have successfully swapped places with {replaced_employee.first_name}')
        notify.send(
            sender=request.user,
            recipient=[user, replaced_employee],
            verb='Replacement',
            description=f'{user} applied for the shift for which {replaced_employee} asked for a replacement.')
    return redirect('shifts:shift_list')


@login_required
def absence_report(request, pk):
    form = AbsenceReportForm()
    user = request.user
    shift = get_object_or_404(ShiftEmployee, shift_id=pk, employee_id=user.id)
    if request.method == 'POST':
        form = AbsenceReportForm(request.POST)
        if form.is_valid():
            shift.status_absence()
            shift.absence_reason = form.cleaned_data['absence_reason']
            shift.absence_report_time = timezone.localtime()
            shift.save()
            messages.success(request, "You have successfully reported absence from work")
            receiver = [request.user] + [obj for obj in Employee.objects.filter(is_admin=True) if obj != request.user]
            print(receiver)
            notify.send(
                sender=request.user,
                recipient=receiver,
                verb='Absence Report',
                description=f'{request.user} will not do the shift.')
            return redirect('shifts:shift_list')
    context = {
        'form': form
    }
    return render(request, 'shifts/evaluation_absence_report.html', context=context)


@login_required
@user_passes_test(lambda u: u.is_admin, login_url='home')
def remove_shift_employee(request, pk, employee_pk):
    shift = get_object_or_404(ShiftEmployee, shift_id=pk, employee_id=employee_pk)
    shift.delete_shift_employee()
    return redirect('shifts:shift_detail', pk=pk)