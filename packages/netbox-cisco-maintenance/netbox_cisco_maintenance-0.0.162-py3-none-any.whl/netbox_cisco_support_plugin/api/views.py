from netbox.api.viewsets import NetBoxModelViewSet

from .. import filtersets, models
from .serializers import CiscoDeviceSupportSerializer, CiscoDeviceTypeSupportSerializer


class CiscoDeviceSupportViewSet(NetBoxModelViewSet):
    queryset = models.CiscoDeviceSupport.objects.prefetch_related("device")
    queryset = (
        models.CiscoDeviceSupport.objects.all()
        .prefetch_related("device")
        .prefetch_related("device_type", "serial")
    )
    serializer_class = CiscoDeviceSupportSerializer
    # filterset_class = filtersets.CiscoDeviceSupportFilterSet


class CiscoDeviceTypeSupportViewSet(NetBoxModelViewSet):
    queryset = models.CiscoDeviceTypeSupport.objects.prefetch_related("device_type")
    serializer_class = CiscoDeviceTypeSupportSerializer
    # filterset_class = filtersets.CiscoDeviceTypeSupportFilterSet
