from netbox.api.viewsets import NetBoxModelViewSet
from machine_tracking import filtersets, models
from machine_tracking.api.serializers import EventSerializer, ReplacementSerializer


class EventViewSet(NetBoxModelViewSet):
    queryset = models.Event.objects.all()
    serializer_class = EventSerializer
    filterset_class = filtersets.EventFilterSet

class ReplacementViewSet(NetBoxModelViewSet):
    queryset = models.Replacement.objects.all()
    serializer_class = ReplacementSerializer
    filterset_class = filtersets.ReplacementFilterSet