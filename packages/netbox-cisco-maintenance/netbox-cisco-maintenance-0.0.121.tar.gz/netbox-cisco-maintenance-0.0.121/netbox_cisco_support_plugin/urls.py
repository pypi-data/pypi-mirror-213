from django.urls import path
from netbox.views.generic import ObjectChangeLogView
from . import models, views


urlpatterns = (
    # Cisco Device Support
    path("cisco-support/", views.CiscoSupportListView.as_view(), name="ciscosupport_list"),
    # path("cisco-support/add/", views.CiscoSupportEditView.as_view(), name="accesslist_add"),
    path("cisco-support/<int:pk>/", views.CiscoSupportView.as_view(), name="ciscosupport"),
    # path("access-lists/<int:pk>/edit/", views.CiscoSupportEditView.as_view(), name="accesslist_edit"),
    # path("access-lists/<int:pk>/delete/", views.CiscoSupportDeleteView.as_view(), name="accesslist_delete"),
    path(
        "cisco-support/<int:pk>/changelog/",
        ObjectChangeLogView.as_view(),
        name="ciscosupport_changelog",
        kwargs={"model": models.CiscoSupport},
    ),
    # Cisco Device Type Support
)
