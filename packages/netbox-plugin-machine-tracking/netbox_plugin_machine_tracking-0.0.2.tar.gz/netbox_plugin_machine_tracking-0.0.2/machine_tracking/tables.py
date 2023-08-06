import django_tables2 as tables
from netbox.tables import NetBoxTable, ChoiceFieldColumn, ToggleColumn
from machine_tracking.models import Event, Replacement


class EventTable(NetBoxTable):
    pk = ToggleColumn()
    machine = tables.Column(
        linkify=True,
    )
    time = tables.Column(
        linkify=True,
    )
    ticket_no = tables.TemplateColumn(
        template_code="""<a href="https://jira.ikarem.io/browse/{{ record.ticket_no }}">{{ record.ticket_no }}</a>""",
        verbose_name='Ticket No',
    )

    class Meta(NetBoxTable.Meta):
        model = Event
        fields = (
            'pk',
            'time',
            'ticket_no',
            'machine',
            'part_type',
            'new_state',
            'event_details',
        )
        default_columns = (
            'time',
            'ticket_no',
            'machine',
            'part_type',
            'new_state',
        )


class ReplacementTable(NetBoxTable):
    pk = ToggleColumn()
    part_type = tables.Column(
        linkify=True,
    )
    machine = tables.Column(
        linkify=True,
    )
    event = tables.Column(
        linkify=True,
    )

    class Meta(NetBoxTable.Meta):
        model = Replacement
        fields = (
            'pk',
            'machine',
            'part_type',
            'new_serial',
            'part_model',
            'event'
        )
        default_fields = (
            'machine',
            'part_type',
            'new_serial',
            'part_model',
            'event'
        )