from django.db import models
from datetime import timedelta, timezone
from django.utils import timezone as tz


class ShiftEmployee(models.Model):
    shift = models.ForeignKey('Shift', on_delete=models.CASCADE, related_name='assigned')
    employee = models.ForeignKey('Employee', on_delete=models.CASCADE, null=True, related_name='assigned')
    status = models.CharField(max_length=20, null=True, blank=True)
    absence_reason = models.CharField(max_length=255, null=True, blank=True)
    absence_report_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.shift} {self.employee}"

    def get_report_time(self):
        return self.absence_report_time.replace(tzinfo=timezone.utc).astimezone(tz=None)

    def status_replace(self):
        self.status = 'replace'
        self.save()

    def status_absence(self):
        self.status = 'absence'
        self.save()

    def make_replacement(self, user):
        if self.status == 'replace':
            self.status = ''
            self.employee = user
            self.save()

    def delete_shift_employee(self):
        self.delete()

    def check_how_late(self):
        if not self.employee.is_logged:
            time_elapsed = tz.now() - self.shift.start_time

            if time_elapsed > timedelta(minutes=5):
                hours, remainder = divmod(time_elapsed.seconds, 3600)
                minutes, _ = divmod(remainder, 60)
                return f'{ hours } hours and { minutes } minutes late'
