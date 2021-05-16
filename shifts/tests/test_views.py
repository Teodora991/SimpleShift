from django.test import TestCase, Client
from django.urls import reverse
from shifts.models import Employee, ShiftEmployee, Shift, ShiftEvaluation, Job
import json
from shifts.views import EmployeeCreateView


class TestViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.home = reverse('home')
        self.employee_list = reverse('employee_list')
        self.employee_detail = reverse('employee_detail', args=[1])
        self.employee_create = reverse('employee_create')
        self.username = 'testuser'
        self.email = 'test@test.com'
        self.password = '12345'
        self.user = Employee(username=self.username, email=self.email)
        self.user.set_password(self.password)
        self.user.save()
        login = self.client.login(username=self.username, password=self.password)
        self.assertEqual(login, True)

    def test_home_GET(self):
        response = self.client.get(self.home)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "index.html")

    def test_employee_list_GET(self):
        response = self.client.get(self.employee_list)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'shifts/employee_list.html')

    def test_employee_detail_GET(self):
        response = self.client.get(self.employee_detail)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'shifts/employee_detail.html')

    def test_employee_create_POST_valid_input(self):
        response = self.client.post(self.employee_create, data={'username': 'marija100',
                                                'first_name': 'Marija',
                                                'last_name': 'Milic',
                                                'email': 'marija@gmail.com',
                                                'is_employee': True})

        self.assertEqual(response.status_code, 302)
        marija = Employee.objects.last()
        self.assertEqual(marija.username, 'marija100')
        self.assertRedirects(response, reverse('employee_detail', args=[marija.pk]))

    def test_employee_create_POST_no_data(self):
        response = self.client.post(self.employee_create, data={})
        self.assertEqual(Employee.objects.all().count(), 1)








