from django.contrib import admin
from .models.employee_model import Employee
from .models.job_model import Job
from .models.shift_model import Shift
from .models.shift_employee_model import ShiftEmployee
from .models.shift_evaluation_model import ShiftEvaluation

admin.site.register(Employee)
admin.site.register(Job)
admin.site.register(Shift)
admin.site.register(ShiftEmployee)
admin.site.register(ShiftEvaluation)


