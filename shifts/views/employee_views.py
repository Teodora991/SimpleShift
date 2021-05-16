import random
from shifts.forms import EmployeeForm, CustomUserCreationForm
from shifts.models import Employee
from shifts.mixins import AdminRequiredMixin
from django.views import generic, View
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect, render, reverse
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode,  urlsafe_base64_decode
from simple_email_confirmation.models import EmailAddress
from django.contrib.auth.decorators import user_passes_test, login_required


class ActivateAccount(View):

    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = Employee.objects.get(pk=uid)

        except (TypeError, ValueError, OverflowError, Employee.DoesNotExist):
            user = None

        if user is not None:
            try:
                user.confirm_email(token)
            except EmailAddress.DoesNotExist:
                messages.warning(request,
                                 ('The confirmation link was invalid.'))
                return redirect('login')
            else:
                user.save()
            if Employee.objects.all().count() == 1:
                messages.success(request, ('Your account has been confirmed.'))
            else:
                messages.success(request, ('Your account has been confirmed. Once the Administrator activates Your Account, You will be able to log in to the site.'))
            return redirect('login')


class SignupView(generic.CreateView):
    template_name = "registration/signup.html"
    form_class = CustomUserCreationForm

    def get_success_url(self):
        return reverse("login")

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save()

            current_site = get_current_site(request)
            subject = 'Verify your SimpleShift Account'
            message = render_to_string('registration/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': user.confirmation_key
            })
            send_mail(subject=subject,
                      message=message,
                      from_email='teodorovict00@gmail.com',
                      recipient_list=[user.email]
                      )
            messages.success(request, ('Sign in to your email to verify your account.'))
            return redirect('login')

        return render(request, self.template_name, {'form': form})


class EmployeeCreateView(LoginRequiredMixin, AdminRequiredMixin, SuccessMessageMixin, generic.CreateView):
    template_name = 'shifts/employee_create.html'
    form_class = EmployeeForm
    success_message = 'You have successfully created a new user.'

    def get_success_url(self):
        employee = self.object
        return reverse("employee_detail", kwargs={'pk': employee.pk})

    def form_valid(self, form):
        username = form.cleaned_data['username']
        if Employee.objects.filter(username=username):
            messages.warning(self.request, 'A user with that username already exists.')
            return redirect('employee_create')
        else:
            user = form.save()
            user.set_password(f"{random.randint(10_000, 100_000_000)}")
            # Email does not have to be validated if user is created by admin.
            user.confirm_email(user.confirmation_key)
            user.save()
            current_site = get_current_site(self.request)
            send_mail(subject="Welcome to SimpleShift",
                      message=f'Your SimpleShift account has been created (username: { user.username }). Click on the following link and then go to "Forgot password?" to reset your password: http://{ current_site.domain }',
                      from_email='teodorovict00@gmail.com',
                      recipient_list=[user.email]
                      )
        return super(EmployeeCreateView, self).form_valid(form)


class EmployeeListView(LoginRequiredMixin, AdminRequiredMixin, generic.ListView):
    template_name = 'shifts/employee_list.html'
    queryset = Employee.objects.all().order_by('is_active', 'username')


class EmployeeDetailView(LoginRequiredMixin, generic.DetailView):
    template_name = 'shifts/employee_detail.html'
    queryset = Employee.objects.all()


class EmployeeUpdateView(LoginRequiredMixin, AdminRequiredMixin, SuccessMessageMixin, generic.UpdateView):
    template_name = 'shifts/employee_update.html'
    queryset = Employee.objects.all()
    form_class = EmployeeForm
    success_message = 'You have successfully updated the user.'

    def get_success_url(self):
        employee = self.object
        return reverse("employee_detail", kwargs={'pk': employee.pk})


class EmployeeDeleteView(LoginRequiredMixin, AdminRequiredMixin, generic.DeleteView):
    template_name = 'shifts/employee_delete.html'
    queryset = Employee.objects.all()

    def get_success_url(self):
        return reverse("employee_list")


@login_required
@user_passes_test(lambda u: u.is_admin, login_url='home')
def activate_admin(request, pk):
    user = get_object_or_404(Employee, pk=pk)
    if user.is_confirmed:
        user.activate_admin_acc()
        send_mail(subject="Welcome",
                  message=f'Your account for SimpleShift has been activated. You can now login.',
                  from_email='teodorovict00@gmail.com',
                  recipient_list=[user.email]
                  )
        return redirect("employee_detail", pk=pk)

    else:
        messages.warning(request, 'The account cannot be activated until the user confirms the email address.')
        return redirect('employee_list')


@login_required
@user_passes_test(lambda u: u.is_admin, login_url='home')
def activate_employee(request, pk):
    user = get_object_or_404(Employee, pk=pk)
    if user.is_confirmed:
        user.activate_employee_acc()
        send_mail(subject="Welcome",
                  message=f'Your account for SimpleShift has been activated. You can now login.',
                  from_email='teodorovict00@gmail.com',
                  recipient_list=[user.email]
                  )
        return redirect("employee_detail", pk=pk)

    else:
        messages.warning(request, 'The account cannot be activated until the user confirms the email address.')
        return redirect('employee_list')