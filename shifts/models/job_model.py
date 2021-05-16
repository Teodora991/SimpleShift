from django.db import models


class Job(models.Model):
    title = models.CharField(max_length=100)
    hourly_fee = models.DecimalField('Hourly fee EUR', max_digits=10, decimal_places=2)
    description = models.TextField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.title

    def get_description(self):
        return self.description or '/'