from collections import defaultdict
from django.utils.translation import gettext_lazy
from netbox.views import generic
from . import models, tables


class CiscoDeviceSupportListView(generic.ObjectListView):
    actions = ("export", "bulk_delete")
    action_perms = defaultdict(set, **{"bulk_delete": {"delete"}})
    queryset = models.CiscoDeviceSupport.objects.all()
    table = tables.CiscoDeviceSupportTable


class CiscoDeviceTypeSupportListView(generic.ObjectListView):
    actions = ("export", "bulk_delete")
    action_perms = defaultdict(set, **{"bulk_delete": {"delete"}})
    queryset = models.CiscoDeviceTypeSupport.objects.all()
    table = tables.CiscoDeviceTypeSupportTable
