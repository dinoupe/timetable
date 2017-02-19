from django.forms import ModelForm, Form
from timetable.models import *
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django import forms
import csv

class CourseForm (ModelForm):
    class Meta:
        model = Course
        fields = '__all__'
        

class UploadedFileForm(Form):
    file = forms.FileField()
    
# def handle_uploaded_file(f):
    # with open('temp_room.csv', 'wb+') as fout:
        # for bit in f.chunks():
            # fout.write(bit)
    # fout.close()
    
    # with open('temp_room.csv', 'r') as fin:
        # reader = csv.reader(fin)
        # roomlist = list(reader)
    # for row in roomlist:
        # room = Room(room_name = row[0], room_capacity = row[1], room_equipment = row[2])
        # room.save()
            
    # fin.close()
    
def handle_uploaded_file(f):
    with open ('temp_group.csv', 'wb+') as fout:
        for bit in f.chunks():
            fout.write(bit)
    fout.close()
    
    with open('temp_group.csv', 'r') as fin:
        reader = csv.reader(fin)
        grouplist = list(reader)
    for row in grouplist:
        group = Group(group_name = row[0], group_size = row[1], group_parent=row[2], group_siblings=row[3])
        group.save()

    fin.close()