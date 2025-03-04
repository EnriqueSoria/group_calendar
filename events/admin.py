from typing import Any
from typing import Callable

from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe

from events.models import Calendar
from events.models import Event

from events.models import Member

from events.models import Attendance


def admin_url(obj, view_suffix: str):
    # Stolen from:
    # https://hakibenita.com/things-you-must-know-about-django-admin-as-your-app-gets-bigger
    app_label = obj._meta.app_label
    model_name = obj._meta.model.__name__.lower()
    return reverse(f"admin:{app_label}_{model_name}_{view_suffix}", args=(obj.pk,))


def admin_change_url(obj):
    return admin_url(obj, "change")


def admin_change_link(
    obj: Any,
    accessor: Callable[[Any], str] = str,
    empty_description: str = "-",
) -> str:
    """Build a (safe) HTML admin change link given an instance object"""
    admin_url = admin_change_url(obj)
    object_item = accessor(obj)
    link_text = object_item if object_item is not None else empty_description
    return mark_safe(f'<a href="{admin_url}">{link_text}</a>')


class AttendanceInline(admin.TabularInline):
    model = Attendance


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    search_fields = ("name",)
    inlines = (AttendanceInline,)


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    search_fields = ("name",)


@admin.register(Calendar)
class CalendarAdmin(admin.ModelAdmin):
    search_fields = ("name",)

    fields = (
        "name",
        "get_events",
        "events",
        "members",
    )
    readonly_fields = ("get_events",)
    autocomplete_fields = ("events", "members")

    @admin.display(description="Events")
    def get_events(self, obj):
        return mark_safe(
            "\n".join(
                [
                    admin_change_link(event)
                    for event in obj.events.order_by("-start_date")
                ]
            )
        )


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    pass
