import calendar

from django import template

register = template.Library()


@register.simple_tag
def month_name_by_number(month_number: int) -> str:
    return calendar.month_name[month_number]
