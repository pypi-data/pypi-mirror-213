import django_tables2 as tables

from netbox.tables import BaseTable
from .models import CiscoDeviceSupport, CiscoDeviceTypeSupport


class CiscoDeviceSupportTable(BaseTable):
    device = tables.Column(linkify=True)

    class Meta(BaseTable.Meta):
        model = CiscoDeviceSupport
        # fmt: off
        fields = (
            "device", "serial", "recommended_release", "desired_release", "current_release",
            "desired_release_status", "current_release_status", "api_status", "sr_no_owner", "is_covered",
            "contract_supplier", "coverage_end_date", "service_line_descr", "service_contract_number",
            "warranty_end_date", "warranty_type", "eox_has_error", "eox_error", "eox_announcement_date",
            "end_of_sale_date", "end_of_sw_maintenance_releases", "end_of_security_vul_support_date",
            "end_of_routine_failure_analysis_date", "end_of_service_contract_renewal",
            "last_date_of_support", "end_of_svc_attach_date",
        )
        default_columns = (
            "device", "recommended_release", "desired_release_status", "desired_release",
            "current_release_status", "current_release", "sr_no_owner", "is_covered", "contract_supplier",
            "coverage_end_date", "service_line_descr", "eox_error", "eox_announcement_date",
        )
        # fmt: on


class CiscoDeviceTypeSupportTable(BaseTable):
    device_type = tables.Column(linkify=True)

    class Meta(BaseTable.Meta):
        model = CiscoDeviceTypeSupport
        # fmt: off
        fields = (
            "device_type", "eox_has_error", "eox_error", "eox_announcement_date", "end_of_sale_date",
            "end_of_sw_maintenance_releases", "end_of_security_vul_support_date",
            "end_of_routine_failure_analysis_date", "end_of_service_contract_renewal",
            "last_date_of_support", "end_of_svc_attach_date",
        )
        default_columns = (
            "device_type", "eox_has_error", "eox_error", "eox_announcement_date", "end_of_sale_date",
            "end_of_sw_maintenance_releases", "end_of_security_vul_support_date",
            "end_of_routine_failure_analysis_date", "end_of_service_contract_renewal",
            "last_date_of_support", "end_of_svc_attach_date",
        )
        # fmt: on
