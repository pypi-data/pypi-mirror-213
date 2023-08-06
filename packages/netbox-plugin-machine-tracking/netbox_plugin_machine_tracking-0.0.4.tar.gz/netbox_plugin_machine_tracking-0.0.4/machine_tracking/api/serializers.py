from rest_framework import serializers
from netbox.api.serializers import NetBoxModelSerializer
from machine_tracking.models import Event, Replacement

class EventSerializer(NetBoxModelSerializer):
    class Meta:
        model = Event
        fields = (
            'id',
            'time',
            'ticket_no',
            'machine',
            'new_state',
            'event_details',
        )

class ReplacementSerializer(NetBoxModelSerializer):
    class Meta:
        model = Replacement
        fields = (
            'id',
            'machine',
            'part_type',
            'new_serial',
            'part_model',
            'event')