from django_filters import DateTimeFromToRangeFilter
from django import forms
from dcim.models import Device
from netbox.forms import NetBoxModelForm, NetBoxModelFilterSetForm
from utilities.forms.fields import CommentField, DynamicModelChoiceField
from machine_tracking.models import Event, Replacement


class EventForm(NetBoxModelForm):
    class Meta:
        model = Event
        fields = ['ticket_no', 'machine', 'new_state', 'part_type', 'event_details']

class ReplacementForm(NetBoxModelForm):
    class Meta:
        model = Replacement
        fields = ['machine', 'part_type', 'new_serial', 'part_model', 'event']

class EventFilterForm(NetBoxModelFilterSetForm):
    model = Event
    time = DateTimeFromToRangeFilter(
        required=False
    )
    machine = DynamicModelChoiceField(
        queryset=Device.objects.all(),
        required=False
    )
    new_state = forms.CharField(
        required=False
    )
    part_type = forms.CharField(
        required=False
    )

class ReplacementFilterForm(NetBoxModelFilterSetForm):
    model = Replacement
    machine = DynamicModelChoiceField(
        queryset=Device.objects.all(),
        required=False,
    )
    new_type = forms.CharField(
        required=False,
    )
    part_model = forms.CharField(
        required=False,
    )