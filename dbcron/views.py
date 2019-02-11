from django.shortcuts import render
from django.utils.timezone import now
from django.utils.html import mark_safe
from dbcron import calendar


class JobCalendarMixin:
    calendar_class = calendar.JobCalendar

    def get_calendar_class(self):
        return self.calendar_class

    def get_calendar_kwargs(self):
        return {
            'jobs': self.object_list,
        }

    def get_calendar(self, calendar_class=None):
        klass = calendar_class or self.get_calendar_class()
        calendar_kwargs = self.get_calendar_kwargs()
        return klass(**calendar_kwargs)

    def get_context_data(self, *args, **kwargs):
        data = super().get_context_data(*args, **kwargs)
        calendar = self.get_calendar()
        month_calendar = calendar.formatmonth(now().year, now().month)
        data.update({
            'calendar': calendar,
        })
        return data


class JobMonthCalendarMixin(JobCalendarMixin):
    def get_context_data(self, *args, **kwargs):
        data = super().get_context_data(*args, **kwargs)
        calendar = data['calendar']
        month_calendar = calendar.formatmonth(now().year, now().month)
        data.update({
            'month_calendar': mark_safe(month_calendar),
        })
        return data


class JobWeekCalendarMixin(JobCalendarMixin):
    def get_context_data(self, *args, **kwargs):
        data = super().get_context_data(*args, **kwargs)
        now_ = now()
        current_week = now_.date().isocalendar()[1]
        week = kwargs.get('week', current_week)
        year = kwargs.get('year', now_.year)
        calendar = data['calendar']
        week_calendar = calendar.formatweekofmonth(year, week)
        data.update({
            'week_calendar': mark_safe(week_calendar),
            'current_week': current_week,
        })
        return data
