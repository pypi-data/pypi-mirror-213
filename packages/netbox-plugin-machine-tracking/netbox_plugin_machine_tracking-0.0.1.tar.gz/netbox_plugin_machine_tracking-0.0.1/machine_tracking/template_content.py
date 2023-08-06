from django.utils import timezone
from datetime import timedelta

from extras.plugins import PluginTemplateExtension
from .models import Event


class DeviceEvents(PluginTemplateExtension):
    model = 'dcim.device'

    # Calculates average time between failures in last 60 days
    def _average_time(self, fail_count, fail_events):
        duration_sum = 0
        for i in range(fail_count - 1):
            duration_sum += (fail_events[i+1].time - fail_events[i].time).total_seconds()
        avg_fail = timedelta(seconds=(duration_sum / (fail_count - 1)))
        avg_days = avg_fail.days
        return str(avg_days) + " days"

    def right_page(self):
        device = self.context['object']
        sixty_days_ago = timezone.now() - timedelta(days=60)
        fail_events = Event.objects.filter(machine=device, new_state="failed", time__gte=sixty_days_ago)
        fail_count = fail_events.count()
        fail_time = "N/A" if fail_count <= 1 else self._average_time(fail_count, fail_events)

        return self.render('machine_tracking/device_panel.html', extra_context={
            'fail_count': fail_count,
            'fail_time': fail_time,
        })

template_extensions = [
    DeviceEvents,
]