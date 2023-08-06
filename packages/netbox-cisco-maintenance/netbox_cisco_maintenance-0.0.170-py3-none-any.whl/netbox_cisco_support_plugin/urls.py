from django.urls import path
from netbox.views.generic import ObjectChangeLogView
from . import models, views


urlpatterns = (
    # Cisco Device Support
    path("cisco-support/", views.CiscoDeviceSupportListView.as_view(), name="ciscodevicesupport_list"),
    # Cisco Device Type Support
)

"""
urlpatterns = (
    # Cisco Device Support
    path("cisco-support/", views.CiscoDeviceSupportListView.as_view(), name="ciscodevicesupport_list"),
    path("cisco-support/add/", views.CiscoDeviceSupportEditView.as_view(), name="ciscodevicesupport_add"),
    path("cisco-support/<int:pk>/edit/", views.CiscoDeviceSupportEditView.as_view(), name="ciscodevicesupport_edit"),
    path("cisco-support/<int:pk>/delete/", views.CiscoDeviceSupportDeleteView.as_view(), name="ciscodevicesupport_delete"),
    path(
        "cisco-support/<int:pk>/changelog/",
        ObjectChangeLogView.as_view(),
        name="CiscoDeviceSupport_changelog",
        kwargs={"model": models.CiscoDeviceSupport},
    ),
    # Cisco Device Type Support
)
"""
