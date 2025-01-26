from django.views.generic import DetailView
from django.views.generic import ListView

from events.calendar import EventCalendar
from events.models import Calendar
from events.models import Event


class CalendarListView(ListView):
    model = Calendar
    template_name = "calendar_list.html"
    context_object_name = "calendars"


class CalendarDetailView(DetailView):
    model = Calendar
    template_name = "calendar_detail.html"

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        events_starting_from_this_month = (
            data["calendar"].events.annotate_year().annotate_month()
            # .filter(start_date__gte=timezone.now().replace(day=1))
        )
        print(set(events_starting_from_this_month.values_list("year", "month")))
        data["html_calendars"] = [
            EventCalendar(
                events_starting_from_this_month.filter(
                    start_date__year=year,
                    start_date__month=month,
                ),
            ).formatmonth(theyear=year, themonth=month)
            for year, month in sorted(
                set(events_starting_from_this_month.values_list("year", "month"))
            )
        ]
        return data


class EventDetailView(DetailView):
    model = Event
    pk_url_kwarg = "event_pk"
    template_name = "event_detail.html"

    def get_queryset(self):
        return Event.objects.filter(calendar=self.kwargs["calendar_pk"])
