from netbox.views import generic
from machine_tracking import models, tables, forms, filtersets


# Event
class EventView(generic.ObjectView):
    queryset = models.Event.objects.all()

class EventListView(generic.ObjectListView):
    queryset = models.Event.objects.all()
    table = tables.EventTable
    filterset = filtersets.EventFilterSet
    filterset_form = forms.EventFilterForm

class EventEditView(generic.ObjectEditView):
    queryset = models.Event.objects.all()
    form = forms.EventForm

class EventDeleteView(generic.ObjectDeleteView):
    queryset = models.Event.objects.all()


#Replacement
class ReplacementView(generic.ObjectView):
    queryset = models.Replacement.objects.all()

class ReplacementListView(generic.ObjectListView):
    queryset = models.Replacement.objects.all()
    table = tables.ReplacementTable
    filterset = filtersets.ReplacementFilterSet
    filterset_form = forms.ReplacementFilterForm

class ReplacementEditView(generic.ObjectEditView):
    queryset = models.Replacement.objects.all()
    form = forms.ReplacementForm

class ReplacementDeleteView(generic.ObjectDeleteView):
    queryset = models.Replacement.objects.all()