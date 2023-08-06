from netbox.api.viewsets import NetBoxModelViewSet

from .. import filtersets, models
from .serializers import CiscoSupportSerializer, CiscoDeviceTypeSupportSerializer


class CiscoSupportViewSet(NetBoxModelViewSet):
    queryset = models.CiscoSupport.objects.prefetch_related("device")
    serializer_class = CiscoSupportSerializer
    # filterset_class = filtersets.CiscoSupportFilterSet


class CiscoDeviceTypeSupportViewSet(NetBoxModelViewSet):
    queryset = models.CiscoDeviceTypeSupport.objects.prefetch_related("device_type")
    serializer_class = CiscoDeviceTypeSupportSerializer
    # filterset_class = filtersets.CiscoDeviceTypeSupportFilterSet
