from netbox.filtersets import NetBoxModelFilterSet
from .models import CiscoDeviceSupport, CiscoDeviceTypeSupport


"""
class CiscoDeviceSupportFilterSet(NetBoxModelFilterSet):

    class Meta:
        model = CiscoDeviceSupport
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
