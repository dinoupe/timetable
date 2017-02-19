from django.views import generic
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.forms import modelformset_factory

from .models import *
from .logic import *
from .forms import *

def index_view(request):
    valid = create_timetable()
    return HttpResponse("Is Timetable validation result is %s" % valid)

def prof_view(request, prof_id):
    p = get_object_or_404(Prof, pk=prof_id)
    context = {'days': TimeSlotManager.days, 'start_times': TimeSlotManager.start_times, 'timeslots': TimeSlot.objects.all(), 'prof': p}
    return render(request, 'timetable/prof.html', context)

def group_view(request, group_id):
    g = get_object_or_404(Group, pk=group_id)
    context = {'days': TimeSlotManager.days, 'start_times': TimeSlotManager.start_times, 'timeslots': TimeSlot.objects.all(), 'group': g}
    return render(request, 'timetable/group.html', context)

def timeslots_view(request):
    context = {'days': TimeSlotManager.days, 'start_times': TimeSlotManager.start_times, 'timeslots': TimeSlot.objects.all()}
    return render(request, 'timetable/timeslots.html', context)
    
def manage_courses(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
    
    else:
        form = CourseForm()
    return render(request, 'timetable/manage_courses.html', {'form':form})
    
def list_upload(request):
    if request.method == 'POST' and request.FILES['file']:
        form = UploadedFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES['file'])
            return HttpResponse('succcess')
    else:
        form = UploadedFileForm()
    return render(request, 'timetable/upload_list.html', {'form': form})
