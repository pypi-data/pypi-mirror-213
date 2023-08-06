from collections import defaultdict
from django.utils.translation import gettext_lazy
from netbox.views import generic
from . import forms, models, tables


class CiscoDeviceSupportListView(generic.ObjectListView):
    actions = ("export", "bulk_delete")
    action_perms = defaultdict(set, **{"bulk_delete": {"delete"}})
    queryset = models.CiscoDeviceSupport.objects.all()
    table = tables.CiscoDeviceSupportTable


"""
class CiscoDeviceSupportView(generic.ObjectView):
    queryset = models.CiscoDeviceSupport.objects.all()
"""

"""
class CiscoDeviceSupportEditView(generic.ObjectEditView):
    queryset = models.CiscoDeviceSupport.objects.all()
    form = forms.CiscoDeviceSupportForm
"""

"""
class CiscoDeviceSupportDeleteView(generic.ObjectDeleteView):
    queryset = models.CiscoDeviceSupport.objects.all()
"""
