from django.contrib import admin

from events.models import Calendar
from events.models import Event

from events.models import Member

from events.models import Attendance


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    search_fields = ("name",)


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    search_fields = ("name",)


@admin.register(Calendar)
class CalendarAdmin(admin.ModelAdmin):
    search_fields = ("name",)
    fields = ("name", "events", "members")

    autocomplete_fields = ("events", "members")


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    pass
