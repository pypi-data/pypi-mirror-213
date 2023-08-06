from django.db import models
from django.urls import reverse
from .choices import PDUUnitChoices
from netbox.models import NetBoxModel


class PDUConfig(NetBoxModel):
    """PDU Configuration is contained within this model."""

    device_type = models.OneToOneField(to="dcim.DeviceType", on_delete=models.CASCADE, blank=True, null=True)

    power_usage_oid = models.CharField(
        max_length=255, help_text="OID string to collect power usage", blank=True, null=True
    )

    power_usage_unit = models.CharField(
        max_length=255, choices=PDUUnitChoices, help_text="The unit of power to be collected"
    )

    csv_headers = ["device_type", "power_usage_oid", "power_usage_unit"]

    def __str__(self):
        """String representation of an PDUConfig."""
        return f"{self.device_type}"

    def get_absolute_url(self):
        return reverse('dcim:devicetype', args=[self.device_type.id])


class PDUStatus(NetBoxModel):
    """PDU Status is contained within this model."""

    device = models.OneToOneField(to="dcim.Device", on_delete=models.CASCADE, blank=True, null=True)

    power_usage = models.PositiveSmallIntegerField(blank=True, null=True, help_text="Current PDU Power Usage")

    updated_at = models.DateTimeField(auto_now=True)

    def get_power_usage(self):
        return f"{self.power_usage} {PDUUnitChoices.UNIT_WATTS.capitalize()}"

    def get_power_usage_watts(self):
        return self.power_usage
