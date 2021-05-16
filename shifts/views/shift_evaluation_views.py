from shifts.forms import ShiftEvaluationForm
from shifts.models import ShiftEmployee, ShiftEvaluation
from shifts.mixins import AdminRequiredMixin
from django.views import generic
from django.utils import timezone
from django.shortcuts import redirect, render, reverse
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.decorators import user_passes_test, login_required


@login_required
@user_passes_test(lambda u: u.is_admin, login_url='home')
def create_shift_evaluation(request, pk):
    form = ShiftEvaluationForm()
    if request.method == 'POST':
        form = ShiftEvaluationForm(request.POST)
        if form.is_valid():
            evaluation = form.save(commit=False)
            evaluation.shiftemployee = ShiftEmployee.objects.filter(id=pk).get()
            evaluation.author = request.user.username
            evaluation.date_created = timezone.localtime()
            evaluation.save()
            messages.success(request, 'You have successfully created the shift evaluation.')
            current_shift = evaluation.shiftemployee.shift
            return redirect('shifts:shift_detail', pk=current_shift.pk)
    context = {
        'form': form,
        'assigned_shift': ShiftEmployee.objects.filter(id=pk).get()
    }
    return render(request, 'shifts/evaluation_create.html', context=context)


class ShiftEvaluationDetailView(LoginRequiredMixin, generic.DetailView):
    template_name = 'shifts/evaluation_detail.html'
    queryset = ShiftEvaluation.objects.all()
    context_object_name = 'evaluation'


class ShiftEvaluationUpdateView(LoginRequiredMixin, AdminRequiredMixin, SuccessMessageMixin, generic.UpdateView):
    template_name = 'shifts/evaluation_update.html'
    queryset = ShiftEvaluation.objects.all()
    form_class = ShiftEvaluationForm
    context_object_name = 'evaluation'
    success_message = "You have successfully updated the shift evaluation."

    def get_success_url(self):
        shift = self.object.shiftemployee.shift
        return reverse('shifts:shift_detail', kwargs={'pk': shift.pk})

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ShiftEvaluationUpdateView, self).get_context_data(**kwargs)
        assigned_shift = self.object.shiftemployee
        context.update({
            'assigned_shift': assigned_shift,
        })
        return context


class ShiftEvaluationDeleteView(LoginRequiredMixin, AdminRequiredMixin, SuccessMessageMixin, generic.DeleteView):
    template_name = 'shifts/evaluation_delete.html'
    queryset = ShiftEvaluation.objects.all()
    context_object_name = 'evaluation'
    success_message = "You have successfully deleted the shift evaluation."

    def get_success_url(self):
        shift = self.object.shiftemployee.shift
        return reverse('shifts:shift_detail', kwargs={'pk': shift.pk})
