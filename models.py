from django.db import models
from django.core.exceptions import ValidationError, ObjectDoesNotExist


class Group(models.Model):
    group_name = models.CharField(max_length=20)
    group_size = models.PositiveIntegerField()
    group_parent = models.CharField(max_length=20,blank=True)
    group_siblings = models.CharField(max_length=40,blank=True)

    def __str__(self):
        return self.group_name

class TimeSlotManager(models.Manager):
    days = ['MO', 'TU', 'WE', 'TH', 'FR']
    start_times = [8, 10, 12, 14, 16, 18]
    end_times = [8, 10, 12, 14, 16, 18]

    def create_timeslot(self, day, start):
        try:
            t = TimeSlot.objects.get(day_of_week=day, t_start=start)
        except ObjectDoesNotExist:
            t = TimeSlot(day_of_week=day, t_start=start, t_end=start+2)

        try:
            t.clean_fields()
        except ValidationError:
            print ("The values you have provided for TimeSlot are not valid")
        else:
            return t


def validate_t_start(val):
    if val not in TimeSlotManager.start_times:
        raise ValidationError('%s is not a valid starting time for classes' % val)


def validate_t_end(val):
    if val not in TimeSlotManager.end_times:
        raise ValidationError('%s is not a valid ending time for classes' % val)


class TimeSlot(models.Model):
    t_start = models.PositiveSmallIntegerField(validators=[validate_t_start])
    t_end = models.PositiveSmallIntegerField(validators=[validate_t_end])
    DAY_IN_WEEK_CHOICES = (
        ('MO', 'Monday'),
        ('TU', 'Tuesday'),
        ('WE', 'Wednesday'),
        ('TH', 'Thursday'),
        ('FR', 'Friday'),
    )
    day_of_week = models.CharField(max_length=10, choices=DAY_IN_WEEK_CHOICES)
    objects = TimeSlotManager()

    def __str__(self):
        return self.day_of_week + ': ' + str(self.t_start) + ' - ' + str(self.t_end)

    @staticmethod
    def create_all():
        for day in TimeSlotManager.days:
            for start in TimeSlotManager.start_times:
                t = TimeSlot.objects.create_timeslot(day, start)
                t.save()


class Room(models.Model):
    room_name = models.CharField(max_length=20)
    room_capacity = models.PositiveSmallIntegerField()
    room_equipment = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.room_name


class Prof(models.Model):
    prof_name = models.CharField(max_length=100)
    prof_time_preferences = models.ManyToManyField(TimeSlot, related_name='t_pref', blank=True)
    prof_time_restrictions = models.ManyToManyField(TimeSlot, related_name='t_rest', blank=True)
    prof_room_preferences = models.ManyToManyField(Room, related_name='r_pref', blank=True)
    prof_room_restrictions = models.ManyToManyField(Room, related_name='r_rest', blank=True)

    def __str__(self):
        return self.prof_name
        




class Course(models.Model):
    course_name = models.CharField(max_length=100)
    course_type = models.CharField(max_length=3)
    course_prof = models.ForeignKey(Prof)
    course_groups = models.ManyToManyField(Group)
    course_room = models.ForeignKey(Room, null=True, blank=True, default= None)
    course_time = models.ForeignKey(TimeSlot, null=True, blank=True, default= None)
    course_equipment_required = models.CharField(max_length=20, blank=True)
    
    class Meta:
        unique_together=(('course_prof','course_time'),('course_room','course_time'))

    def __str__(self):
        return self.course_name
		
    def get_group_names(self):
        names = ''
        for g in self.course_groups.all():
            if (g != self.course_groups.all()[0]):
                names = names + ' & ' + str(g)
            else:
                names = str(g)
        return names

    def get_course_size(self):
        sz = 0
        for g in self.course_groups.all():
            sz += g.group_size
        return sz
