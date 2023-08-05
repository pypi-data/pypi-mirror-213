import django_tables2 as tables
from django.utils.safestring import mark_safe

from netbox.tables import BaseTable, NetBoxTable
from .models import CiscoSupport, CiscoDeviceTypeSupport


class CiscoSupportTable(BaseTable):
    device = tables.Column(linkify=True)

    class BooleanColumn(tables.Column):
        """
        Custom implementation of BooleanColumn to render a nicely-formatted checkmark or X icon instead of a Unicode
        character.
        """
        def render(self, value):
            if value:
                rendered = '<span class="text-success"><i class="mdi mdi-check-bold text-success"></i></span>'
            elif value is None:
                rendered = '<span class="text-muted">&mdash;</span>'
            else:
                rendered = '<span class="text-danger"><i class="mdi mdi-close-thick text-danger"></i></span>'
            return mark_safe(rendered)

        def value(self, value):
            return str(value)

    class Meta(BaseTable.Meta):
        model = CiscoSupport
        # fmt: off
        fields = (
           "pk", "id", "device", "recommended_release", "desired_release", "current_release",
            "desired_release_status", "current_release_status", "api_status", "sr_no_owner", "is_covered",
            "contract_supplier", "coverage_end_date", "service_line_descr", "service_contract_number",
            "warranty_end_date", "warranty_type",
        )
        default_columns = (
            "device", "recommended_release", "desired_release", "current_release", "api_status", "sr_no_owner",
            "is_covered", "contract_supplier", "coverage_end_date", "service_line_descr",
            "service_contract_number",
        )
        # fmt: on
