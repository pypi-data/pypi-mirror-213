from netbox.views import generic
from . import forms, models, tables


class CiscoSupportListView(generic.ObjectListView):
    queryset = models.CiscoSupport.objects.all()
    table = tables.CiscoSupportTable


class CiscoSupportView(generic.ObjectView):
    queryset = models.CiscoSupport.objects.all()


class CiscoSupportEditView(generic.ObjectEditView):
    queryset = models.CiscoSupport.objects.all()
    form = forms.CiscoSupportForm


class CiscoSupportDeleteView(generic.ObjectDeleteView):
    queryset = models.CiscoSupport.objects.all()