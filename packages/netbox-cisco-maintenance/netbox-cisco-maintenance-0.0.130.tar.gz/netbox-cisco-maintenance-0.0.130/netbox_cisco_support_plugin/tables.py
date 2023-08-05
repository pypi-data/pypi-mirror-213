import django_tables2 as tables
from django.utils.safestring import mark_safe

from netbox.tables import BaseTable, NetBoxTable
from netbox.tables import columns
from .models import CiscoSupport, CiscoDeviceTypeSupport


class CiscoSupportTable(NetBoxTable):
    device = tables.Column(linkify=True)

    class Meta(NetBoxTable.Meta):
        model = CiscoSupport
        # fmt: off
        fields = (
           "pk", "id", "device", "recommended_release", "desired_release", "current_release",
            "desired_release_status", "current_release_status", "api_status", "sr_no_owner", "is_covered",
            "contract_supplier", "coverage_end_date", "service_line_descr", "service_contract_number",
            "warranty_end_date", "warranty_type",
        )
        default_columns = (
            "device", "recommended_release", "desired_release", "current_release", "sr_no_owner",
            "is_covered", "contract_supplier", "coverage_end_date", "service_line_descr",
        )
        # fmt: on
