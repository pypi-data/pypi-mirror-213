from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import get_object_or_404, render
from django.views.generic import View

from netbox.views.generic import BulkDeleteView, BulkImportView, ObjectEditView, ObjectListView, ObjectView, ObjectDeleteView

from .filters import PDUConfigFilter
from .forms import PDUConfigFilterForm, PDUConfigForm
from .models import PDUConfig
from .tables import PDUConfigBulkTable, PDUConfigTable

class PDUConfigView(PermissionRequiredMixin, ObjectView):

    permission_required = "axians_netbox_pdu.view_pduconfig"
    queryset = PDUConfig.objects.all()
    template_name = 'axians_netbox_pdu/pduconfig.html'


class PDUConfigListView(PermissionRequiredMixin, ObjectListView):
    """View for listing all PDUConfig items"""

    permission_required = "axians_netbox_pdu.view_pduconfig"
    queryset = PDUConfig.objects.all()
    filterset = PDUConfigFilter
    filterset_form = PDUConfigFilterForm
    table = PDUConfigTable
    template_name = "axians_netbox_pdu/pduconfig_list.html"


class PDUConfigCreateView(PermissionRequiredMixin, ObjectEditView):
    """View for creating a new PDUConfig"""

    permission_required = "axians_netbox_pdu.add_pduconfig"
    model = PDUConfig
    queryset = PDUConfig.objects.all()
    form = PDUConfigForm
    template_name = "axians_netbox_pdu/pduconfig_edit.html"
    default_return_url = "plugins:axians_netbox_pdu:pduconfig_list"


class PDUConfigDeleteView(PermissionRequiredMixin, ObjectDeleteView):
    """View for deleting one PDUConfig."""

    permission_required = "axians_netbox_pdu.delete_pduconfig"
    queryset = PDUConfig.objects.filter()
    default_return_url = "plugins:axians_netbox_pdu:pduconfig_list"


class PDUConfigBulkDeleteView(PermissionRequiredMixin, BulkDeleteView):
    """View for deleting one or more PDUConfigs."""

    permission_required = "axians_netbox_pdu.delete_pduconfig"
    queryset = PDUConfig.objects.filter()
    table = PDUConfigTable
    default_return_url = "plugins:axians_netbox_pdu:pduconfig_list"


class PDUConfigEditView(PDUConfigCreateView):
    permission_required = "axians_netbox_pdu.change_pduconfig"
