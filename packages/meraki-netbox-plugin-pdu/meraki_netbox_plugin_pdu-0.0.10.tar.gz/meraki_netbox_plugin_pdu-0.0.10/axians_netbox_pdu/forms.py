from django import forms

from dcim.models import DeviceType, Manufacturer
from utilities.forms import BootstrapMixin

from netbox.forms import NetBoxModelForm

from .choices import PDUUnitChoices
from .models import PDUConfig

BLANK_CHOICE = (("", "---------"),)


class PDUConfigForm(NetBoxModelForm):
    """Form for creating a new PDUConfig"""

    device_type = forms.ModelChoiceField(
        queryset=DeviceType.objects.filter(poweroutlettemplates__isnull=False).distinct(),
        required=True,
        to_field_name="slug",
        label="Device Type",
    )

    power_usage_oid = forms.CharField(
        required=True, label="Power Usage OID", help_text="OID string to collect power usage"
    )

    power_usage_unit = forms.ChoiceField(
        choices=BLANK_CHOICE + PDUUnitChoices.CHOICES, required=True, label="Power Usage Unit"
    )

    class Meta:
        model = PDUConfig
        fields = ["device_type", "power_usage_oid", "power_usage_unit"]
        obj_type = "test"


class PDUConfigFilterForm(NetBoxModelForm):
    """Form for siltering PDUConfig instances."""

    device_type = forms.ModelChoiceField(
        queryset=DeviceType.objects.filter(poweroutlettemplates__isnull=False).distinct(),
        required=False,
        to_field_name="slug",
    )

    manufacturer = forms.ModelChoiceField(
        queryset=Manufacturer.objects.filter(device_types__poweroutlettemplates__isnull=False).distinct(),
        required=False,
        to_field_name="slug",
    )

    q = forms.CharField(required=False, label="Search")

    class Meta:
        model = PDUConfig
        fields = ["q", "device_type", "manufacturer"]
