from django.db import models
from django.urls import reverse
from netbox.models import ChangeLoggedModel
from utilities.querysets import RestrictedQuerySet


class CiscoDeviceTypeSupport(ChangeLoggedModel):
    objects = RestrictedQuerySet.as_manager()

    device_type = models.OneToOneField(to="dcim.DeviceType", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.device_type}"

    eox_has_error = models.BooleanField(default=False)

    eox_error = models.TextField(blank=True, null=True)

    eox_announcement_date = models.DateField(blank=True, null=True)

    end_of_sale_date = models.DateField(blank=True, null=True)

    end_of_sw_maintenance_releases = models.DateField(blank=True, null=True)

    end_of_security_vul_support_date = models.DateField(blank=True, null=True)

    end_of_routine_failure_analysis_date = models.DateField(blank=True, null=True)

    end_of_service_contract_renewal = models.DateField(blank=True, null=True)

    last_date_of_support = models.DateField(blank=True, null=True)

    end_of_svc_attach_date = models.DateField(blank=True, null=True)


class CiscoSupport(ChangeLoggedModel):
    objects = RestrictedQuerySet.as_manager()

    device = models.OneToOneField(to="dcim.Device", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.device}"

    def get_absolute_url(self):
        return reverse("plugins:netbox_cisco_support_plugin:ciscosupport", args=[self.pk])

    # models.CharField(max_length=100, blank=True, null=True)

    coverage_end_date = models.DateField(blank=True, null=True)

    service_contract_number = models.TextField(blank=True, null=True)

    service_line_descr = models.TextField(blank=True, null=True)

    warranty_type = models.TextField(blank=True, null=True)

    warranty_end_date = models.DateField(blank=True, null=True)

    is_covered = models.BooleanField(default=False)

    sr_no_owner = models.BooleanField(default=False)

    contract_supplier = models.TextField(blank=True, null=True)

    api_status = models.TextField(blank=True, null=True)

    recommended_release = models.TextField(blank=True, null=True)

    desired_release = models.TextField(blank=True, null=True)

    current_release = models.TextField(blank=True, null=True)

    desired_release_status = models.BooleanField(default=False)

    current_release_status = models.BooleanField(default=False)
