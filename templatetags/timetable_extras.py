from django import template
from django.db import models
from django.core.exceptions import ObjectDoesNotExist

from timetable.models import *


register = template.Library()

@register.simple_tag(takes_context=True)
def get_timeslot(context):
    return TimeSlot.objects.get(day_of_week=context['day'], t_start=context['time'])

@register.inclusion_tag('course_data_prof.html',takes_context=True)
def get_prof_course(context):
    ts = TimeSlot.objects.get(day_of_week=context['day'], t_start=context['time'])
    try:
        c = ts.course_set.get(course_prof=context['prof'])
    except ObjectDoesNotExist:
        return {'name': '-', 'room': '-', 'group': '-'}

    return {'name': c, 'room': c.course_room, 'group': c.get_group_names}

@register.inclusion_tag('course_data_group.html',takes_context=True)
def get_group_course(context):
	ts = TimeSlot.objects.get(day_of_week=context['day'], t_start=context['time'])
	group = context['group']
	try:
		c = group.course_set.get(course_time=ts)
	except ObjectDoesNotExist:
		return {'name': '-', 'room': '-', 'prof': '-'}

	return {'name': c, 'room': c.course_room, 'prof': c.course_prof}


__author__ = 'dinu'
