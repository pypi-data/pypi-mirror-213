from django.urls import path
from netbox.views.generic import ObjectChangeLogView
from . import models, views


urlpatterns = (
    # Cisco Device Support
    path("cisco-device-support/", views.CiscoSupportListView.as_view(), name="ciscodevicesupport_list"),
    path("cisco-device-support/<int:pk>/delete/", views.CiscoSupportDeleteView.as_view(), name="ciscodevicesupport_delete"),
    # Cisco Device Type Support
)
