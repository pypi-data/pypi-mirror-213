from django.urls import path

from netbox.views.generic import ObjectChangeLogView

from .models import PDUConfig

from .views import (
    PDUConfigView,
    PDUConfigDeleteView,
    PDUConfigBulkDeleteView,
    PDUConfigCreateView,
    PDUConfigEditView,
    PDUConfigListView,
)

urlpatterns = [
    path("pdu-config/", PDUConfigListView.as_view(), name="pduconfig_list"),
    path("pdu-config/add/", PDUConfigCreateView.as_view(), name="pduconfig_add"),
    path("pdu-config/delete/", PDUConfigBulkDeleteView.as_view(), name="pduconfig_bulk_delete"),
    path("pdu-config/<int:pk>/", PDUConfigView.as_view(), name="pduconfig_view"),
    path("pdu-config/<int:pk>/delete/", PDUConfigDeleteView.as_view(), name="pduconfig_delete"),
    path("pdu-config/<int:pk>/edit/", PDUConfigEditView.as_view(), name="pduconfig_edit"),
    path("pdu-config/<int:pk>/changelog/", ObjectChangeLogView.as_view(), name="pduconfig_changelog", kwargs={
        'model': PDUConfig
    }),
]
