from rest_framework import serializers

from netbox.api.serializers import NetBoxModelSerializer, WritableNestedSerializer
from dcim.api.serializers import NestedDeviceTypeSerializer, NestedDeviceSerializer
from ..models import CiscoDeviceTypeSupport, CiscoSupport


#### Regular Serializers #####################################################################################


class CiscoDeviceTypeSupportSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="plugins-api:netbox_cisco_support_plugin-api:ciscodevicetypesupport-detail"
    )

    device_type = NestedDeviceTypeSerializer()

    class Meta:
        model = CiscoDeviceTypeSupport
        # fmt: off
        fields = [
            "id", "url", "display", "device_type", "eox_has_error", "eox_error", "eox_announcement_date",
            "end_of_sale_date", "end_of_sw_maintenance_releases", "end_of_security_vul_support_date",
            "end_of_routine_failure_analysis_date", "end_of_service_contract_renewal","last_date_of_support",
            "end_of_svc_attach_date", "tags", "custom_fields", "created", "last_updated",
        ]
        # fmt: on


class CiscoSupportSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="plugins-api:netbox_cisco_support_plugin-api:ciscosupport-detail"
    )

    device = NestedDeviceSerializer()
    device_type = NestedDeviceTypeSerializer()

    class Meta:
        model = CiscoSupport
        # fmt: off
        fields = [
            "id", "url", "display", "device", "device_type", "api_status", "sr_no_owner", "is_covered",
            "coverage_end_date", "contract_supplier", "service_line_descr", "service_contract_number",
            "warranty_end_date", "warranty_type", "recommended_release", "desired_release",
            "current_release", "desired_release_status", "current_release_status", "tags", "custom_fields",
            "created", "last_updated",
        ]
        # fmt: on
