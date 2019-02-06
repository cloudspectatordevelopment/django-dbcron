from django.utils.translation import ugettext_lazy as _

import django_tables2 as tables
from django_tables2 import columns

from dbcron import models
from dbcron import utils


class JobTable(tables.Table):
    next_time = columns.Column(
        orderable=False, verbose_name=_("Next run"))

    class Meta:
        model = models.Job
        fields = sequence = ['name', 'func', 'is_active', 'next_time', 'sec',
                             'min', 'hou', 'dom', 'mon', 'dow', 'yea']

    def render_next_time(self, value, record):
        return utils.get_next_time(record)
