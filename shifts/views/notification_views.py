from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from notifications.models import Notification


class NotificationListView(LoginRequiredMixin, generic.ListView):
    model = Notification
    context_object_name = 'notifications'
    paginate_by = 10
    template_name = 'shifts/notifications.html'

    def get_queryset(self):
        notifications = self.model.objects.filter(recipient=self.request.user)
        notifications.mark_all_as_read()
        return notifications
