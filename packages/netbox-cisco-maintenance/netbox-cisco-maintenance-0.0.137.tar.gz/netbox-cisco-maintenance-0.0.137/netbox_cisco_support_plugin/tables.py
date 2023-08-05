from dataclasses import dataclass
from typing import Optional
from urllib.parse import quote

import django_tables2 as tables
from django.contrib.auth.models import AnonymousUser
from django.urls import reverse
from django.urls.exceptions import NoReverseMatch
from django.utils.safestring import mark_safe
from django.template import Context, Template

from netbox.tables import BaseTable, NetBoxTable, columns
from .models import CiscoSupport, CiscoDeviceTypeSupport
from utilities.utils import get_viewname


@dataclass
class ActionsItem:
    title: str
    icon: str
    permission: Optional[str] = None
    css_class: Optional[str] = 'secondary'


class ActionsColumn(tables.Column):
    """
    A dropdown menu which provides edit, delete, and changelog links for an object. Can optionally include
    additional buttons rendered from a template string.

    :param actions: The ordered list of dropdown menu items to include
    :param extra_buttons: A Django template string which renders additional buttons preceding the actions dropdown
    :param split_actions: When True, converts the actions dropdown menu into a split button with first action as the
        direct button link and icon (default: True)
    """
    attrs = {'td': {'class': 'text-end text-nowrap noprint'}}
    empty_values = ()
    actions = {
        'delete': ActionsItem('Delete', 'trash-can-outline', 'delete', 'danger'),
    }

    def __init__(self, *args, actions=('edit', 'delete', 'changelog'), extra_buttons='', split_actions=True, **kwargs):
        super().__init__(*args, **kwargs)

        self.extra_buttons = extra_buttons
        self.split_actions = split_actions

        # Determine which actions to enable
        self.actions = {
            name: self.actions[name] for name in actions
        }

    def header(self):
        return ''

    def render(self, record, table, **kwargs):
        # Skip dummy records (e.g. available VLANs) or those with no actions
        if not getattr(record, 'pk', None) or not self.actions:
            return ''

        model = table.Meta.model
        if request := getattr(table, 'context', {}).get('request'):
            return_url = request.GET.get('return_url', request.get_full_path())
            url_appendix = f'?return_url={quote(return_url)}'
        else:
            url_appendix = ''

        html = ''

        # Compile actions menu
        button = None
        dropdown_class = 'secondary'
        dropdown_links = []
        user = getattr(request, 'user', AnonymousUser())
        for idx, (action, attrs) in enumerate(self.actions.items()):
            permission = f'{model._meta.app_label}.{attrs.permission}_{model._meta.model_name}'
            if attrs.permission is None or user.has_perm(permission):
                url = reverse(get_viewname(model, action), kwargs={'pk': record.pk})

                # Render a separate button if a) only one action exists, or b) if split_actions is True
                if len(self.actions) == 1 or (self.split_actions and idx == 0):
                    dropdown_class = attrs.css_class
                    button = (
                        f'<a class="btn btn-sm btn-{attrs.css_class}" href="{url}{url_appendix}" type="button">'
                        f'<i class="mdi mdi-{attrs.icon}"></i></a>'
                    )

                # Add dropdown menu items
                else:
                    dropdown_links.append(
                        f'<li><a class="dropdown-item" href="{url}{url_appendix}">'
                        f'<i class="mdi mdi-{attrs.icon}"></i> {attrs.title}</a></li>'
                    )

        # Create the actions dropdown menu
        if button and dropdown_links:
            html += (
                f'<span class="btn-group dropdown">'
                f'  {button}'
                f'  <a class="btn btn-sm btn-{dropdown_class} dropdown-toggle" type="button" data-bs-toggle="dropdown" style="padding-left: 2px">'
                f'  <span class="visually-hidden">Toggle Dropdown</span></a>'
                f'  <ul class="dropdown-menu">{"".join(dropdown_links)}</ul>'
                f'</span>'
            )
        elif button:
            html += button
        elif dropdown_links:
            html += (
                f'<span class="btn-group dropdown">'
                f'  <a class="btn btn-sm btn-secondary dropdown-toggle" type="button" data-bs-toggle="dropdown">'
                f'  <span class="visually-hidden">Toggle Dropdown</span></a>'
                f'  <ul class="dropdown-menu">{"".join(dropdown_links)}</ul>'
                f'</span>'
            )

        # Render any extra buttons from template code
        if self.extra_buttons:
            template = Template(self.extra_buttons)
            context = getattr(table, "context", Context())
            context.update({'record': record})
            html = template.render(context) + html

        return mark_safe(html)


class CiscoSupportTable(BaseTable):
    pk = columns.ToggleColumn(
        visible=False
    )
    id = tables.Column(
        linkify=True,
        verbose_name='ID'
    )
    actions = ActionsColumn()

    exempt_columns = ('pk', 'actions')

    device = tables.Column(linkify=True)

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
            "device", "recommended_release", "desired_release", "current_release", "sr_no_owner",
            "is_covered", "contract_supplier", "coverage_end_date", "service_line_descr",
        )
        # fmt: on

    @property
    def htmx_url(self):
        """
        Return the base HTML request URL for embedded tables.
        """
        if getattr(self, "embedded", False):
            viewname = get_viewname(self._meta.model, action="list")
            try:
                return reverse(viewname)
            except NoReverseMatch:
                pass
        return ""
