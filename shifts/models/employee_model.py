from django.db import models
from django.contrib.auth.models import AbstractUser
from simple_email_confirmation.models import SimpleEmailConfirmationUserMixin


class Employee(SimpleEmailConfirmationUserMixin, AbstractUser):
    job = models.ManyToManyField('Job', blank=True, related_name='employees')
    is_admin = models.BooleanField(default=False)
    is_employee = models.BooleanField(default=False)
    is_logged = models.BooleanField(default=False)

    def __str__(self):
        if self.first_name:
            return f"{self.first_name} {self.last_name}"
        else:
            return f"{self.username}"

    def account_status(self):
        if self.is_employee:
            return 'Employee'
        elif self.is_admin:
            return 'Admin'
        elif not self.is_active:
            return 'Not assigned'

    def activate_employee_acc(self):
        self.is_employee = True
        self.is_active = True
        self.save()

    def activate_admin_acc(self):
        self.is_admin = True
        self.is_active = True
        self.save()
