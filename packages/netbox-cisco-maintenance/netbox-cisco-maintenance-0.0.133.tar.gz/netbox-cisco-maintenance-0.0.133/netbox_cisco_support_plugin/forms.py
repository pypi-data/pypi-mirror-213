from netbox.forms import NetBoxModelForm
from .models import CiscoSupport, CiscoDeviceTypeSupport
from utilities.forms.fields import CommentField


class CiscoSupportForm(NetBoxModelForm):
    comments = CommentField()

    class Meta:
        model = CiscoSupport
        # fmt: off
        fields = ("recommended_release", "desired_release", "current_release",
            "desired_release_status", "current_release_status", "api_status", "sr_no_owner", "is_covered",
            "contract_supplier", "coverage_end_date", "service_line_descr", "service_contract_number",
            "warranty_end_date", "warranty_type", "tags",
        )
        # fmt: on
