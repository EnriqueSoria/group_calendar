from django.db import models
from django.db.models.functions import ExtractMonth
from django.db.models.functions import ExtractYear


class EventQuerySet(models.QuerySet):
    def annotate_month(self, from_field="start_date", with_name="month"):
        """Extract month from field `from_field`"""
        return self.annotate(
            **{
                with_name: ExtractMonth(from_field),
            }
        )

    def annotate_year(self, from_field="start_date", with_name="year"):
        """Extract year from field `from_field`"""
        return self.annotate(
            **{
                with_name: ExtractYear(from_field),
            }
        )
