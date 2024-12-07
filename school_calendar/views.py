from django.shortcuts import redirect, render

from main.utils import get_institution, is_approved_account
from school_calendar.models import AcademicYear, Term
from school_calendar.forms import AcademicYearForm, TermForm


# Create your views here.

def academic_calendar(request, school_id):
    if is_approved_account(request)==False: return redirect('main:un_approved', school_id) 
    institution=get_institution(request, school_id)
    academic_form = AcademicYearForm()
    if request.method == 'POST':
        last_calendar=AcademicYear.objects.filter(institution=institution).last()
        if 'close' in request.POST:
            calendar_id=request.POST.get('calendar_id', '')
            calendar=AcademicYear.objects.get(id=calendar_id)
            calendar.closed=True
            calendar.save()
            for term in calendar.terms.all():
                term.closed=True
                term.save()
            
        if last_calendar is not None:    
            if last_calendar.closed:
                academic_form = AcademicYearForm(request.POST)
                if academic_form.is_valid():
                    d=academic_form.save(commit=False)
                    d.institution=institution
                    d.save()
        else:
            academic_form = AcademicYearForm(request.POST)
            if academic_form.is_valid():
                d=academic_form.save(commit=False)
                d.institution=institution
                d.save()
        
    last_calendar=AcademicYear.objects.filter(institution=institution).last()
    showform=False
    if last_calendar is not None:
        if last_calendar.closed: showform=True 
    else: showform=True
    
    academic_years = AcademicYear.objects.filter(institution=institution).order_by('date')
    cont={
        'academic_form': academic_form,
        'academic_years':academic_years,
        'showform':showform,
        'school_id':school_id,
        'institution':institution
        }
    return render(request, 'templates/school_calendar/calendar.html', cont)


def calendar_detail(request, calendar_id, school_id):
    if is_approved_account(request)==False: return redirect('main:un_approved', school_id) 
    institution=get_institution(request, school_id)
    calendar = AcademicYear.objects.get(id=calendar_id)
    terms = Term.objects.filter(institution=institution, academic_year=calendar)
    form=TermForm()

    if request.method=='POST':
        last_term=Term.objects.filter(academic_year=calendar).last()
        if 'close' in request.POST:
            term_id=request.POST.get('term_id', '')
            term=Term.objects.get(id=term_id)
            term.closed=True
            term.save()
        if last_term is not None:
            form = TermForm(request.POST)
            if last_term.closed:
                if form.is_valid():
                    d=form.save(commit=False)
                    d.institution=institution
                    d.academic_year=calendar
                    d.save()
        else:
            form = TermForm(request.POST)
            if form.is_valid():
                d=form.save(commit=False)
                d.institution=institution
                d.academic_year=calendar
                d.save()
    last_term=Term.objects.filter(academic_year=calendar).last()
    showform=False
    if last_term is not None:
        if last_term.closed: showform=True
    else: showform=True
    cont={
        'terms': terms, 
        'calendar':calendar,
        'form':form,
        'showform':showform,
        'school_id':school_id,
        'institution':institution
        }
    return render(request, 'templates/school_calendar/calendar_detail.html', cont)


# views.py
from django.shortcuts import render, redirect
from .models import CalendarEvent
from .forms import CalendarEventForm

# Display all events in the school calendar
def events(request, school_id):
    if is_approved_account(request)==False: return redirect('main:un_approved', school_id) 
    institution=get_institution(request, school_id)
    # calendar = AcademicYear.objects.get(id=calendar_id)
    # terms = Term.objects.filter(institution=institution, academic_year=calendar)
    form = CalendarEventForm()
    if request.method == 'POST':
        form = CalendarEventForm(request.POST)
        if form.is_valid():
            d=form.save(commit=False)
            d.institution=institution
            d.save()
             
    events = CalendarEvent.objects.filter(institution=institution)
    cont={
        'events': events, 
        'school_id':school_id,
        'institution':institution,
        'form':form
        }
    return render(request, 'templates/school_calendar/events.html', cont)

# Add a new event to the calendar
def event_detail(request, event_id, school_id):
    event = CalendarEvent.objects.get(id=event_id)
    if is_approved_account(request)==False: return redirect('main:un_approved', school_id) 
    institution=get_institution(request, school_id)
    cont={
        'school_id':school_id,
        'institution':institution,
        'event':event
    }
    return render(request, 'event_detail.html', cont)
