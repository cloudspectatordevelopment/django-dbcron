import importlib
import json
from crontab import CronTab
from django.db import models
from django.utils.translation import ugettext_lazy as _


class Job(models.Model):
    name = models.CharField(max_length=200, verbose_name=_("name"))
    description = models.TextField(max_length=2000, verbose_name=_("description"), blank=True)
    func = models.CharField(max_length=250, verbose_name=_("function"))
    opts = models.TextField(max_length=2000, default='{}', verbose_name=_("options"))

    is_active = models.BooleanField(default=False, verbose_name=_("is active"))

    sec = models.CharField(max_length=50, default='0', verbose_name=_("second(s)"))
    min = models.CharField(max_length=50, verbose_name=_("minute(s)"))
    hou = models.CharField(max_length=50, verbose_name=_("hour(s)"))
    dom = models.CharField(max_length=50, verbose_name=_("day(s) of month"))
    mon = models.CharField(max_length=50, verbose_name=_("month"))
    dow = models.CharField(max_length=50, verbose_name=_("day(s) of week"))
    yea = models.CharField(max_length=50, default='*', verbose_name=_("year(s)"))

    class Meta:
        verbose_name = _("job")
        verbose_name_plural = _("jobs")

    @property
    def raw_entry(self):
        return ' '.join([self.min, self.hou, self.dom, self.mon,
                         self.dow])
        return ' '.join([self.sec, self.min, self.hou, self.dom, self.mon,
                         self.dow, self.yea])

    def __str__(self):
        return "%s (%s)" % (self.name, self.raw_entry)

    @property
    def entry(self):
        return CronTab(self.raw_entry.strip())

    def _get_func(self):
        module_path = '.'.join(self.func.split('.')[:-1])
        func_name = self.func.split('.')[-1]
        module = importlib.import_module(module_path)
        func = getattr(module, func_name)
        return func

    def run(self):
        func = self._get_func()
        opts = json.loads(self.opts)
        result = func(**opts)
        return result

    @property
    def next_time(self):
        return int(self.entry.next())