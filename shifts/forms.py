from django import forms
from .models.employee_model import Employee
from .models.job_model import Job
from .models.shift_model import Shift
from .models.shift_employee_model import ShiftEmployee
from .models.shift_evaluation_model import ShiftEvaluation
from django.contrib.auth.forms import UserCreationForm, UsernameField
from django.contrib.auth import get_user_model
from django.utils import timezone


User = get_user_model()


class EmployeeForm(forms.ModelForm):
    is_admin = forms.BooleanField(required=False, label='Status Admin')
    is_employee = forms.BooleanField(required=False, label='Status Employee')
    is_active = forms.BooleanField(widget=forms.HiddenInput(), initial=True, required=False)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    email = forms.EmailField(required=True)

    class Meta:
        model = Employee
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "job",
            'is_admin',
            'is_employee',
            'is_active',
        )

    def clean(self):
        if 'is_admin' in self.data and 'is_employee' in self.data:
            raise forms.ValidationError('Account user can not be both Admin and Employee. Please provide one answer.')
        elif 'is_admin' not in self.data and 'is_employee' not in self.data:
            raise forms.ValidationError('Please provide status for Account user.')


class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=20)
    last_name = forms.CharField(max_length=20)
    email = forms.EmailField(required=True, max_length=30)
    is_active = forms.BooleanField(widget=forms.HiddenInput(), initial=False, required=False)

    class Meta:
        model = User
        fields = ("username", 'email', 'first_name', 'last_name', 'is_active')
        field_classes = {'username': UsernameField}


class ShiftForm(forms.ModelForm):

    start_time = forms.SplitDateTimeField(required=True,
        widget=forms.SplitDateTimeWidget(date_attrs={'type': 'date'},
                                         time_attrs={'type': 'time'}),
    )
    end_time = forms.SplitDateTimeField(required=True,
        widget=forms.SplitDateTimeWidget(date_attrs={'type': 'date'},
                                         time_attrs={'type': 'time'}),
    )


    class Meta:
        model = Shift
        fields = ('start_time', 'end_time', 'job_type', 'required_employees')

    def clean(self):
        start_time = self.cleaned_data.get('start_time')
        end_time = self.cleaned_data.get('end_time')
        if start_time is None:
            raise forms.ValidationError('Start time is invalid.')
        elif start_time < timezone.now():
            raise forms.ValidationError('The shift can only be created for the future.')
        elif end_time is None:
            raise forms.ValidationError('End time is invalid.')
        elif end_time < start_time:
            raise forms.ValidationError('Check your input. Start and End time do not match')


class ShiftEvaluationForm(forms.ModelForm):

    employee_has_come = forms.BooleanField(
        label='Employee attended (leave blank if the employee did not come to work)',
        required=False)

    employee_started = forms.SplitDateTimeField(
        required=False,
        label='At what time did the employee take over the shift?',
        widget=forms.SplitDateTimeWidget(date_attrs={'type': 'date'},
                                         time_attrs={'type': 'time'}),
    )
    employee_ended = forms.SplitDateTimeField(
        required=False,
        label='At what time did the employee complete the shift?',
        widget=forms.SplitDateTimeWidget(date_attrs={'type': 'date'},
                                         time_attrs={'type': 'time'}),
    )

    reason_employee_has_not_come = forms.CharField(
        widget=forms.TextInput,
        label="Why didn't the worker come to work?",
        required=False)

    class Meta:
        model = ShiftEvaluation
        fields = (
            "employee_has_come",
            "employee_started",
            "employee_ended",
            "reason_employee_has_not_come",
        )

    def clean(self):
        employee_has_come = self.cleaned_data.get('employee_has_come')
        employee_started = self.cleaned_data.get('employee_started')
        employee_ended = self.cleaned_data.get('employee_ended')
        reason_employee_has_not_come = self.cleaned_data.get('reason_employee_has_not_come')
        if employee_has_come:
            if employee_started is None:
                raise forms.ValidationError('Please provide a valid time when the employee started work')
            elif employee_ended is None:
                raise forms.ValidationError('Please provide a valid time when the employee ended work')
            elif employee_ended < employee_started:
                raise forms.ValidationError('Check your input. Start and End time do not match')
            elif reason_employee_has_not_come:
                raise forms.ValidationError({"reason_employee_has_not_come": "Please leave this field blank if the employee did come to work"})

        elif not employee_has_come:
            if not reason_employee_has_not_come:
                raise forms.ValidationError({"reason_employee_has_not_come": "Please fill in this field if the employee did not come to work"})
            elif employee_started or employee_ended:
                raise forms.ValidationError("Please leave time fields blank if the employee did not come to work")


class AbsenceReportForm(forms.ModelForm):
    absence_reason = forms.CharField(
        label="Please state the reason for your absence.",
        widget=forms.Textarea)

    class Meta:
        model = ShiftEmployee
        fields = ('absence_reason',)


class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = '__all__'
