from shifts.forms import JobForm
from shifts.models import Job
from shifts.mixins import AdminRequiredMixin
from django.views import generic
from django.shortcuts import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin


class JobCreateView(LoginRequiredMixin, AdminRequiredMixin, SuccessMessageMixin, generic.CreateView):
    template_name = 'shifts/job_create.html'
    form_class = JobForm
    success_message = 'You have successfully created a new job.'

    def get_success_url(self):
        job = self.object
        return reverse("job_detail", kwargs={'pk': job.pk})


class JobListView(LoginRequiredMixin, AdminRequiredMixin, generic.ListView):
    template_name = 'shifts/job_list.html'
    queryset = Job.objects.all().order_by('title')


class JobDetailView(LoginRequiredMixin, AdminRequiredMixin, generic.DetailView):
    template_name = 'shifts/job_detail.html'
    queryset = Job.objects.all()


class JobUpdateView(LoginRequiredMixin, AdminRequiredMixin, SuccessMessageMixin, generic.UpdateView):
    template_name = 'shifts/job_update.html'
    queryset = Job.objects.all()
    form_class = JobForm
    success_message = 'You have successfully updated the job.'

    def get_success_url(self):
        job = self.object
        return reverse("job_detail", kwargs={'pk': job.pk})


class JobDeleteView(LoginRequiredMixin, AdminRequiredMixin, generic.DeleteView):
    template_name = 'shifts/job_delete.html'
    queryset = Job.objects.all()

    def get_success_url(self):
        return reverse("job_list")

