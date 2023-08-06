from django.urls import path
from netbox.views.generic import ObjectChangeLogView
from . import models, views


urlpatterns = (
    # Cisco Device Support
    path("device-support/", views.CiscoDeviceSupportListView.as_view(), name="ciscodevicesupport_list"),
    # Cisco Device Type Support
    path("device-type-support/", views.CiscoDeviceTypeSupportListView.as_view(), name="ciscodevicetypesupport_list"),
)
