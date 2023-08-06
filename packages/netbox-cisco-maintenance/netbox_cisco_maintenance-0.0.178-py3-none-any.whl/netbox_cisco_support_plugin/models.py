from django.db import models
from django.urls import reverse
from netbox.models import ChangeLoggedModel
from utilities.querysets import RestrictedQuerySet


class CiscoDeviceTypeSupport(ChangeLoggedModel):
    objects = RestrictedQuerySet.as_manager()

    device_type = models.OneToOneField(to="dcim.DeviceType", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.device_type}"

    def get_absolute_url(self):
        return reverse("plugins:netbox_cisco_support_plugin:ciscodevicetypesupport", args=[self.pk])

    eox_has_error = models.BooleanField(default=False)

    eox_error = models.CharField(max_length=100, blank=True, null=True)

    eox_announcement_date = models.DateField(blank=True, null=True)

    end_of_sale_date = models.DateField(blank=True, null=True)

    end_of_sw_maintenance_releases = models.DateField(blank=True, null=True)

    end_of_security_vul_support_date = models.DateField(blank=True, null=True)

    end_of_routine_failure_analysis_date = models.DateField(blank=True, null=True)

    end_of_service_contract_renewal = models.DateField(blank=True, null=True)

    last_date_of_support = models.DateField(blank=True, null=True)

    end_of_svc_attach_date = models.DateField(blank=True, null=True)


class CiscoDeviceSupport(ChangeLoggedModel):
    objects = RestrictedQuerySet.as_manager()

    device = models.OneToOneField(to="dcim.Device", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.device}"

    def get_absolute_url(self):
        return reverse("plugins:netbox_cisco_support_plugin:ciscodevicesupport", args=[self.pk])

    #### Fileds for CiscoDeviceSupport #######################################################################

    serial = models.CharField(max_length=100, blank=True, null=True)

    model = models.CharField(max_length=100, blank=True, null=True)

    coverage_end_date = models.DateField(blank=True, null=True)

    service_contract_number = models.CharField(max_length=100, blank=True, null=True)

    service_line_descr = models.CharField(max_length=100, blank=True, null=True)

    warranty_type = models.CharField(max_length=100, blank=True, null=True)

    warranty_end_date = models.DateField(blank=True, null=True)

    is_covered = models.BooleanField(default=False)

    sr_no_owner = models.BooleanField(default=False)

    contract_supplier = models.CharField(max_length=100, blank=True, null=True)

    api_status = models.CharField(max_length=100, blank=True, null=True)

    recommended_release = models.CharField(max_length=100, blank=True, null=True)

    desired_release = models.CharField(max_length=100, blank=True, null=True)

    current_release = models.CharField(max_length=100, blank=True, null=True)

    desired_release_status = models.BooleanField(default=False)

    current_release_status = models.BooleanField(default=False)

    #### Fileds same as CiscoDeviceTypeSupport ###############################################################
    # Create these fields again because referencing them from the CiscoDeviceTypeSupport model was not working

    eox_has_error = models.BooleanField(default=False)

    eox_error = models.CharField(max_length=100, blank=True, null=True)

    eox_announcement_date = models.DateField(blank=True, null=True)

    end_of_sale_date = models.DateField(blank=True, null=True)

    end_of_sw_maintenance_releases = models.DateField(blank=True, null=True)

    end_of_security_vul_support_date = models.DateField(blank=True, null=True)

    end_of_routine_failure_analysis_date = models.DateField(blank=True, null=True)

    end_of_service_contract_renewal = models.DateField(blank=True, null=True)

    last_date_of_support = models.DateField(blank=True, null=True)

    end_of_svc_attach_date = models.DateField(blank=True, null=True)
