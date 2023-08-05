import django_tables2 as tables

from netbox.tables import NetBoxTable, ChoiceFieldColumn
from .models import CiscoSupport, CiscoDeviceTypeSupport


class CiscoSupportTable(NetBoxTable):
    class Meta(NetBoxTable.Meta):
        model = CiscoSupport
        # fmt: off
        fields = (
           "pk", "id", "recommended_release", "desired_release", "current_release",
            "desired_release_status", "current_release_status", "api_status", "sr_no_owner", "is_covered",
            "contract_supplier", "coverage_end_date", "service_line_descr", "service_contract_number",
            "warranty_end_date", "warranty_type",
        )
        default_columns = (
            "recommended_release", "desired_release", "current_release", "api_status", "sr_no_owner",
            "is_covered", "contract_supplier", "coverage_end_date", "service_line_descr",
            "service_contract_number",
        )
        # fmt: on
