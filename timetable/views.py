from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404

from timetable.models import TimeTable
from .forms import *
from django.http import JsonResponse
from main.utils import *
from datetime import datetime
# Create your views here.
# view current day time tables for all classes
@login_required
def time_tables(request, school_id):
    if is_approved_account(request)==False: return redirect('main:un_approved') 
    institution=get_institution(request, school_id)
    classes=ClassRoom.objects.filter(school=institution)
    time_table_data=TimeTable.objects.filter(school=institution)
    form=TimeTableForm()
    day_of_week=datetime.today().weekday()
    days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
    day = days[day_of_week]

    if request.method=='POST':
        form=TimeTableForm(request.POST)
        clses=request.POST.getlist('classes', '')
        if form.is_valid():
            d=form.save(commit=False)
            d.school=institution
            d.save()
            for cls_id in clses:
                cls=ClassRoom.objects.filter(id=cls_id)
                for cl in cls:
                    for t in time_table_data:
                        if cl in t.classes.all():pass
                        else:
                            d.classes.add(cl)
                            d.save()
        else:
            print(form.errors)
    cont={
        'data':time_table_data,
        'form':form,
        'classes':classes,
        'day':day,
        'school_id':school_id,
        'institution':institution
    }
    return render(request, 'templates/timetable/time_tables.html', cont)

@login_required
def inclass_time_table(request, table_id, school_id):
    if is_approved_account(request)==False: return redirect('main:un_approved') 
    institution=get_institution(request, school_id)
    
    time_table=TimeTable.objects.get(id=table_id)
    class_rooms=time_table.classes.all()
    print(class_rooms, 'kkkkkkkkkkkkkkkkkkk')
    form=TimeTableForm()
    day_of_week=datetime.today().weekday()
    days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
    day = days[day_of_week]
    # if request.method=='POST':
    #     form=TimeTableForm(request.POST)
    #     if form.is_valid():
    #         d=form.save(commit=False)
    #         d.school=institution
    #         try:
    #             TimeTable.objects.get(classi=d.classi)
    #         except:
    #             d.save()
    #     else:
    #         print(form.errors)
    cont={
        'time_table':time_table,
        'form':form,
        'class_rooms':class_rooms,
        'day':day,
        'school_id':school_id,
        'institution':institution
    }
    return render(request, 'templates/timetable/in_class_timetable.html', cont)


# full single time table view
@login_required
def time_table(request, table_id, school_id):
    if is_approved_account(request)==False: return redirect('main:un_approved') 
    institution=get_institution(request, school_id)
    time_table=TimeTable.objects.get(id=table_id, school=institution)
    form=TimeTableSubjectForm()
    day_of_week=datetime.today().weekday()
    days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
    day = days[day_of_week]

    # year=sdate[0]
    # month=sdate[1]
    # day=sdate[2]
    print(day_of_week, day, 'mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm')
    if request.method=='POST':
        form=TimeTableSubjectForm(request.POST)
        if form.is_valid():
            d=form.save(commit=False)
            d.timetable=time_table
            d.save()
        else:
            print(form.errors)
    cont={
        'data':time_table,
        'form':form,
        'today':day,
        'school_id':school_id,
        'institution':institution
    }
    return render(request, 'templates/timetable/time_table.html', cont)
