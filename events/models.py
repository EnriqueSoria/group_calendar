from django.db import models
from django.urls import reverse

from events.querysets import EventQuerySet


class Member(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Event(models.Model):
    name = models.CharField(max_length=100)
    link = models.URLField(blank=True)

    start_date = models.DateField()
    end_date = models.DateField()

    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    attendees = models.ManyToManyField(
        "Member", related_name="attendees", through="Attendance"
    )

    objects = EventQuerySet.as_manager()

    def __str__(self):
        return f"{self.start_date} - {self.name}"

    class Meta:
        ordering = ["start_date"]

    def get_absolute_url(self) -> str:
        return reverse(
            "event-detail",
            kwargs={
                "calendar_pk": self.calendar_set.values_list("pk", flat=True).first(),
                "event_pk": self.pk,
            },
        )

    def get_attending_members_that_are_going(self):
        return self.attendance_set.filter(
            type=Attendance.AttendanceType.ATTENDING
        ).values_list("member__name", flat=True)

    def get_attending_members_that_are_interested(self):
        return self.attendance_set.filter(
            type=Attendance.AttendanceType.INTERESTED
        ).values_list("member__name", flat=True)


class Attendance(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    class AttendanceType(models.TextChoices):
        ATTENDING = "attending"
        INTERESTED = "interested"

    type = models.CharField(choices=AttendanceType, max_length=50)


class Calendar(models.Model):
    name = models.CharField(max_length=100)

    events = models.ManyToManyField(Event, blank=True)
    members = models.ManyToManyField(Member, blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self) -> str:
        return reverse("calendar-detail", kwargs={"pk": self.pk})
