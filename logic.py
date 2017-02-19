from django.db import models
from django.core.exceptions import ObjectDoesNotExist

from .models import *


def set_course_time(c, invalid_times):
    if c.course_time != None :
        return c.course_time

    for ts in c.course_prof.prof_time_preferences.all():
        valid = True
        if ts in invalid_times:
            continue
        if c.course_prof.course_set.filter(course_time=ts):
            print('Frist point of failure')
            print(str(ts))
            continue
        for g in c.course_groups.all():
            if g.course_set.filter(course_time=ts):
                valid = False
                print('second point of failure')
                print(str(ts))
        if valid:
            c.course_time = ts
            c.save()
            return ts

    for ts in TimeSlot.objects.all():
        if ts in c.course_prof.prof_time_restrictions.all() or c.course_prof.course_set.filter(course_time=ts):
            print('third point of failure')
            print(str(ts))
            continue
        if ts in invalid_times:
            continue
        valid = True
        for g in c.course_groups.all():
            if g.course_set.filter(course_time=ts):
                valid = False
                print('Forth point of failure')
                print(str(ts))
        if valid:
            c.course_time = ts
            c.save()
            return ts

    return False


def set_course_room(c):
    if c.course_room is None:
        return c.course_room

    for room in c.course_prof.prof_room_preferences.all():
        valid = True
        if room.room_capacity >= c.get_course_size():
            if not Course.objects.filter(course_room=room,course_time=c.course_time):
                c.course_room = room
                c.save()
                return room

    for room in Room.objects.all():
        if room in c.course_prof.prof_room_restrictions.all() or room.room_capacity <= c.get_course_size():
            print('Fifth point of failure')
            print(str(room))
            continue
        elif not Course.objects.filter(course_room=room,course_time=c.course_time):
                c.course_room = room
                c.save()
                return room

    return False


def create_timetable():
    valid = True
    for c in Course.objects.all():
        print(str(c))
        invalid_times = []
        ct = set_course_time(c, invalid_times)
        cr = set_course_room(c)
        if ct == False:
            continue
        while len(invalid_times) < 30 and ct != False and cr == False:
            invalid_times.append(c.course_time)
            c.course_time = None
            c.save()
            ct = set_course_time(c, invalid_times)
            cr = set_course_room(c)
            print(str(ct))
        if ct == False or cr == False:
            valid = False

    return valid


__author__ = 'dinu'
