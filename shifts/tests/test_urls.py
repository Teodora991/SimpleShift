from django.test import SimpleTestCase
from django.urls import reverse, resolve
from shifts.views import (ShiftCreateView,
                          ShiftListView,
                          ShiftDetailView,
                          ShiftDeleteView,
                          ShiftUpdateView,
                          LiveShiftListView,
                          create_shift_evaluation,
                          ShiftEvaluationDetailView,
                          ShiftEvaluationUpdateView,
                          ShiftEvaluationDeleteView,
                          NotificationListView,
                          apply_for_shift,
                          assign_to_shift,
                          absence_report,
                          remove_shift_employee,
                          replace_request,
                          make_replacement,
                          SignupView,
                          ActivateAccount,
                          EmployeeCreateView,
                          EmployeeListView,
                          EmployeeDetailView,
                          EmployeeUpdateView,
                          EmployeeDeleteView,
                          activate_admin,
                          activate_employee,
                          JobListView,
                          JobDeleteView,
                          JobUpdateView,
                          JobCreateView,
                          JobDetailView,
                          )

from simpleshift.views import HomePageView

from django.contrib.auth.views import (LoginView,
                                       LogoutView,
                                       PasswordResetView,
                                       PasswordResetDoneView,
                                       PasswordResetConfirmView,
                                       PasswordResetCompleteView)


class TestUrls(SimpleTestCase):

    def test_shift_create_url_resolves(self):
        url = reverse('shifts:shift_create')
        self.assertEquals(resolve(url).func.view_class, ShiftCreateView)

    def test_shift_list_url_resolves(self):
        url = reverse('shifts:shift_list')
        self.assertEquals(resolve(url).func.view_class, ShiftListView)

    def test_shift_detail_url_resolves(self):
        url = reverse('shifts:shift_detail', args=[1])
        self.assertEquals(resolve(url).func.view_class, ShiftDetailView)

    def test_shift_delete_url_resolves(self):
        url = reverse('shifts:shift_delete', args=[1])
        self.assertEquals(resolve(url).func.view_class, ShiftDeleteView)

    def test_shift_update_url_resolves(self):
        url = reverse('shifts:shift_update', args=[1])
        self.assertEquals(resolve(url).func.view_class, ShiftUpdateView)

    def test_live_shifts_list_url_resolves(self):
        url = reverse('shifts:live_shifts')
        self.assertEquals(resolve(url).func.view_class, LiveShiftListView)

    def test_shift_evaluation_create_url_resolves(self):
        url = reverse('shifts:evaluation_create', args=[1])
        self.assertEquals(resolve(url).func, create_shift_evaluation)

    def test_shift_evaluation_detail_url_resolves(self):
        url = reverse('shifts:evaluation_detail', args=[1])
        self.assertEquals(resolve(url).func.view_class, ShiftEvaluationDetailView)

    def test_shift_evaluation_delete_url_resolves(self):
        url = reverse('shifts:evaluation_delete', args=[1])
        self.assertEquals(resolve(url).func.view_class, ShiftEvaluationDeleteView)

    def test_shift_evaluation_update_url_resolves(self):
        url = reverse('shifts:evaluation_update', args=[1])
        self.assertEquals(resolve(url).func.view_class, ShiftEvaluationUpdateView)

    def test_notification_list_url_resolves(self):
        url = reverse('shifts:notice')
        self.assertEquals(resolve(url).func.view_class, NotificationListView)

    def test_apply_url_resolves(self):
        url = reverse('shifts:apply', args=[1])
        self.assertEquals(resolve(url).func, apply_for_shift)

    def test_assign_url_resolves(self):
        url = reverse('shifts:assign', args=[1, 1])
        self.assertEquals(resolve(url).func, assign_to_shift)

    def test_remove_shiftemployee_url_resolves(self):
        url = reverse('shifts:remove_shift_employee', args=[1, 1])
        self.assertEquals(resolve(url).func, remove_shift_employee)

    def test_replace_request_url_resolves(self):
        url = reverse('shifts:replace_request', args=[1])
        self.assertEquals(resolve(url).func, replace_request)

    def test_make_replacement_resolves(self):
        url = reverse('shifts:make_replacement', args=[1, 1])
        self.assertEquals(resolve(url).func, make_replacement)

    def test_absence_report_url_resolves(self):
        url = reverse('shifts:absence_report', args=[1])
        self.assertEquals(resolve(url).func, absence_report)

    def test_home_url_resolves(self):
        url = reverse('home')
        self.assertEquals(resolve(url).func.view_class, HomePageView)

    def test_login_url_resolves(self):
        url = reverse('login')
        self.assertEquals(resolve(url).func.view_class, LoginView)

    def test_logout_url_resolves(self):
        url = reverse('logout')
        self.assertEquals(resolve(url).func.view_class, LogoutView)

    def test_signup_url_resolves(self):
        url = reverse('signup')
        self.assertEquals(resolve(url).func.view_class, SignupView)

    def test_activate_url_resolves(self):
        url = reverse('activate', args=[1, 1])
        self.assertEquals(resolve(url).func.view_class, ActivateAccount)

    def test_reset_password_url_resolves(self):
        url = reverse('reset_password')
        self.assertEquals(resolve(url).func.view_class, PasswordResetView)

    def test_password_reset_done_url_resolves(self):
        url = reverse('password_reset_done')
        self.assertEquals(resolve(url).func.view_class, PasswordResetDoneView)

    def test_password_reset_confirm_url_resolves(self):
        url = reverse('password_reset_confirm', args=[1, 1])
        self.assertEquals(resolve(url).func.view_class, PasswordResetConfirmView)

    def test_password_reset_complete_url_resolves(self):
        url = reverse('password_reset_complete')
        self.assertEquals(resolve(url).func.view_class, PasswordResetCompleteView)

    def test_employee_create_url_resolves(self):
        url = reverse('employee_create')
        self.assertEquals(resolve(url).func.view_class, EmployeeCreateView)

    def test_employee_list_url_resolves(self):
        url = reverse('employee_list')
        self.assertEquals(resolve(url).func.view_class, EmployeeListView)

    def test_employee_detail_url_resolves(self):
        url = reverse('employee_detail', args=[1])
        self.assertEquals(resolve(url).func.view_class, EmployeeDetailView)

    def test_employee_update_url_resolves(self):
        url = reverse('employee_update', args=[1])
        self.assertEquals(resolve(url).func.view_class, EmployeeUpdateView)

    def test_employee_delete_url_resolves(self):
        url = reverse('employee_delete', args=[1])
        self.assertEquals(resolve(url).func.view_class, EmployeeDeleteView)

    def test_job_create_url_resolves(self):
        url = reverse('job_create')
        self.assertEquals(resolve(url).func.view_class, JobCreateView)

    def test_job_list_url_resolves(self):
        url = reverse('job_list')
        self.assertEquals(resolve(url).func.view_class, JobListView)

    def test_job_detail_url_resolves(self):
        url = reverse('job_detail', args=[1])
        self.assertEquals(resolve(url).func.view_class, JobDetailView)

    def test_job_update_url_resolves(self):
        url = reverse('job_update', args=[1])
        self.assertEquals(resolve(url).func.view_class, JobUpdateView)

    def test_job_delete_url_resolves(self):
        url = reverse('job_delete', args=[1])
        self.assertEquals(resolve(url).func.view_class, JobDeleteView)

    def test_activate_admin_url_resolves(self):
        url = reverse('activate_admin', args=[1])
        self.assertEquals(resolve(url).func, activate_admin)

    def test_activate_employee_url_resolves(self):
        url = reverse('activate_employee', args=[1])
        self.assertEquals(resolve(url).func, activate_employee)










