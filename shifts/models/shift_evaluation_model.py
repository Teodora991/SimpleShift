from django.db import models
from datetime import timezone
from .shift_employee_model import ShiftEmployee


class ShiftEvaluation(models.Model):
    shiftemployee = models.OneToOneField(ShiftEmployee,
                                         on_delete=models.CASCADE,
                                         related_name='evaluation',
                                         blank=True,
                                         null=True)
    author = models.CharField(max_length=50)
    date_created = models.DateTimeField(blank=True, null=True)
    employee_started = models.DateTimeField(blank=True, null=True)
    employee_ended = models.DateTimeField(blank=True, null=True)
    employee_has_come = models.BooleanField(default=True, blank=True)
    reason_employee_has_not_come = models.CharField(max_length=255, null=True, blank=True)
    shift_fee = models.DecimalField("Shift Fee EUR", decimal_places=2, max_digits=10, blank=True, default=0)

    def get_employee_started(self):
        return self.employee_started.replace(tzinfo=timezone.utc).astimezone(tz=None)

    def get_employee_ended(self):
        return self.employee_ended.replace(tzinfo=timezone.utc).astimezone(tz=None)

    def __str__(self):
        return f"Evaluation({self.shiftemployee.shift.start_time.date}, {self.shiftemployee})"

    def calculate_fee(self):
        if not self.employee_started or not self.employee_ended:
            self.shift_fee = 0
        else:
            fee_per_minute = self.shiftemployee.shift.job_type.hourly_fee / 60
            td = self.employee_ended - self.employee_started
            td_minutes = td.total_seconds() / 60
            self.shift_fee = round(float(td_minutes) * float(fee_per_minute), 2)
