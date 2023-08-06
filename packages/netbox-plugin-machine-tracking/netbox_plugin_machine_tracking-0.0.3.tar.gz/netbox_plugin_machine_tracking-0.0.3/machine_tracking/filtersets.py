from netbox.filtersets import NetBoxModelFilterSet
from machine_tracking.models import Event, Replacement
from django.db.models import Q


class EventFilterSet(NetBoxModelFilterSet):
    class Meta:
        model = Event
        fields = (
            'id',
            'time',
            'machine',
            'new_state',
            'part_type',
        )

    def search(self, queryset, name, value):
        if value is not None:
            return queryset.filter(
                Q(new_state__icontains=value) |
                Q(part_type__icontains=value)
            )
        return queryset


class ReplacementFilterSet(NetBoxModelFilterSet):
    class Meta:
        model = Replacement
        fields = (
            'id',
            'machine',
            'part_type',
            'part_model',
        )

    def search(self, queryset, name, value):
        if value is not None:
            return queryset.filter(
                Q(part_model__icontains=value) |
                Q(part_type__icontains=value)
            )
        return queryset