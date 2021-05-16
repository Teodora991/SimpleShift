from notifications.signals import notify
from django.db.models.signals import pre_delete, pre_save, post_save
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver
from .models import Employee, Shift, ShiftEvaluation


@receiver(pre_delete, sender=Shift)
def pre_shift_deleted_signal(sender, instance, **kwargs):
    recipient = [obj.employee for obj in instance.assigned.all()]
    notify.send(sender=instance,
                recipient=recipient,
                verb='was deleted',
                description='The shift assigned to you has been deleted.')


@receiver(pre_save, sender=ShiftEvaluation)
def pre_evaluation_save_signal(sender, instance, **kwargs):
    instance.calculate_fee()


@receiver(user_logged_in, sender=Employee)
def login_handler(sender, user, request, **kwargs):
    user.is_logged = True
    user.save()


@receiver(user_logged_out, sender=Employee)
def logout_handler(sender, user, request, **kwargs):
    user.is_logged = False
    user.save()


@receiver(post_save, sender=Employee)
def post_user_create_signal(sender, instance, created, *args, **kwargs):
    if created and Employee.objects.all().count() == 1:
        instance.is_admin = True
        instance.is_staff = True
        instance.is_superuser = True
        instance.is_active = True
        instance.save()


@receiver(post_save, sender=Shift)
def post_shift_update_signal(sender, instance, created, *args, **kwargs):
    if not created:
        for obj in instance.assigned.all():
            if instance.job_type not in obj.employee.job.all():
                obj.delete_shift_employee()


@receiver(post_save, sender=Employee)
def post_employee_update_signal(sender, instance, created, *args, **kwargs):
    if not created:
        for obj in instance.assigned.all():
            if obj.shift.job_type not in instance.job.all():
                obj.delete_shift_employee()






