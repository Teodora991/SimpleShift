from django.db import models
from datetime import timezone
from .shift_employee_model import ShiftEmployee


class Shift(models.Model):
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    job_type = models.ForeignKey('Job', on_delete=models.CASCADE, related_name='shifts')
    required_employees = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{ self.get_start_time().strftime('%I:%M %p') } - { self.get_end_time().strftime('%I:%M %p') }".lower()

    def get_start_time(self):
        return self.start_time.replace(tzinfo=timezone.utc).astimezone(tz=None)

    def get_end_time(self):
        return self.end_time.replace(tzinfo=timezone.utc).astimezone(tz=None)

    def apply(self, user):
        """if there is still place to fill in the shift, creates new instance of the class ShiftEmployee"""
        if self.count_difference() and self.job_type in user.job.all():
            shift_employee = ShiftEmployee(shift=self, employee=user)
            shift_employee.save()

    def count_difference(self):
        return self.required_employees - self.assigned.filter(shift_id=self.id).count()

    def replacement_requested(self):
        return ShiftEmployee.objects.filter(shift_id=self.pk).filter(status='replace')

    def overlap(self, assigned_shift):
        """Takes instance of the class Shift and instance of the class ShiftEmployee and returns True
        if shift durations overlap."""
        if not assigned_shift:
            return False
        if self.start_time < assigned_shift.shift.end_time and assigned_shift.shift.start_time < self.end_time or \
             self.start_time == assigned_shift.shift.start_time and assigned_shift.shift.end_time == self.end_time:
            return True
        return False
