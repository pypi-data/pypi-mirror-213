from django.contrib.postgres.fields import ArrayField
from django.db import models
from netbox.models import NetBoxModel
from django.urls import reverse
from utilities.choices import ChoiceSet
from dcim.models import Device
from django.core.validators import MinValueValidator


class Event(NetBoxModel):
    time = models.DateTimeField(
        auto_now=True,
    )
    ticket_no = models.CharField(
        max_length=100,
        null=True,
    )
    machine = models.ForeignKey(
        to="dcim.Device",
        on_delete=models.CASCADE,
        related_name='event',
    )
    new_state = models.CharField(
        max_length=20,
        null=True,
    )
    part_type = models.CharField(
        max_length=20,
        null=True,
    )
    event_details = models.CharField(
        max_length=1000,
        null=True,
    )

    def __str__(self):
        try:
            machine_name = self.machine
        except Device.DoesNotExist:
            machine_name = "N/A"
        return f'{self.time.strftime("%Y-%m-%d, %H:%M:%S")}: {machine_name}'
    def get_absolute_url(self):
        return reverse('plugins:machine_tracking:event', args=[self.pk])


class Replacement(NetBoxModel):
    machine = models.ForeignKey(
        to="dcim.Device",
        on_delete=models.CASCADE,
        related_name='replacements',
    )
    part_type = models.CharField(
        max_length=20,
    )
    new_serial = models.CharField(
        max_length=100,
    )
    part_model = models.CharField(
        max_length=100,
    )
    event = models.OneToOneField(
        to=Event,
        on_delete=models.CASCADE,
        related_name='replacement',
        null=True,
    )

    def __str__(self):
        return f'{self.event}'
    def get_absolute_url(self):
        return reverse('plugins:machine_tracking:replacement', args=[self.pk])