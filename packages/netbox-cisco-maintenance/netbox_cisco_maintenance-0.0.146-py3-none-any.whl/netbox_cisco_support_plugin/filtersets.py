from netbox.filtersets import NetBoxModelFilterSet
from .models import CiscoSupport, CiscoDeviceTypeSupport


"""
class CiscoSupportFilterSet(NetBoxModelFilterSet):

    class Meta:
        model = CiscoSupport
        fields = ["id", "sr_no_owner", "is_covered", "contract_supplier"]

    def search(self, queryset, name, value):
        return queryset.filter(description__icontains=value)


class CiscoDeviceTypeSupportFilterSet(NetBoxModelFilterSet):

    class Meta:
        model = CiscoDeviceTypeSupport
        fields = ["id", "eox_has_error"]

    def search(self, queryset, name, value):
        return queryset.filter(description__icontains=value)
"""
