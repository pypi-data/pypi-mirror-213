import django_tables2 as tables

from netbox.tables import NetBoxTable, ToggleColumn

from .models import PDUConfig


class PDUConfigTable(NetBoxTable):
    """Table for displaying PDUConfig information"""

    pk = ToggleColumn()
    device_type = tables.LinkColumn()

    class Meta(NetBoxTable.Meta):
        model = PDUConfig
        fields = (
            "pk",
            "device_type",
            "power_usage_oid",
            "power_usage_unit",
        )


class PDUConfigBulkTable(NetBoxTable):

    device_type = tables.LinkColumn()

    class Meta(NetBoxTable.Meta):
        model = PDUConfig
        fields = (
            "pk",
            "device_type",
            "power_usage_oid",
            "power_usage_unit",
        )
