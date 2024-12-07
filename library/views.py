from datetime import datetime
from django.shortcuts import redirect, render

from main.utils import get_institution, is_approved_account
from staff_permision.permisions import can_manage_library
from subscription.utils import subs_plan
from .models import Book, BookCopy, Checkout
from.forms import BookCheckoutForm, BookCopyForm, BookForm
# Create your views here.
def books(request, school_id):
    if is_approved_account(request)==False: return redirect('main:un_approved', school_id) 
    institution=get_institution(request, school_id)
    if can_manage_library(request): pass 
    else:return redirect('main:un_authorised', school_id)
    
    book_list=Book.objects.filter(school=institution)
    form = BookForm()
    if request.method == 'POST':
        plan_name=subs_plan(request, school_id)
        if plan_name=='Free':return redirect('subs:upgrade', school_id)
        if plan_name=='Basic':return redirect('subs:upgrade', school_id)
        if plan_name=='expired':return redirect('subs:expired', school_id)
        form = BookForm(request.POST)
        if form.is_valid():
            d=form.save(commit=False)
            d.school=institution
            d.save() 
    cont={
        'book_list':book_list,
        'form':form,
        'school_id':school_id,
        'institution':institution
    }
    return render(request, 'templates/library/book_list.html', cont)

def book_copies(request, book_id, school_id):
    if is_approved_account(request)==False: return redirect('main:un_approved', school_id) 
    if can_manage_library(request): pass 
    else:return redirect('main:un_authorised', school_id)
    institution=get_institution(request, school_id)
    book=Book.objects.get(id=book_id)
    book_copies=BookCopy.objects.filter(book=book)
    form = BookCopyForm()
    if request.method == 'POST':
        plan_name=subs_plan(request, school_id)
        if plan_name=='Free':return redirect('subs:upgrade', school_id)
        if plan_name=='Basic':return redirect('subs:upgrade', school_id)
        if plan_name=='expired':return redirect('subs:expired', school_id)
        form = BookCopyForm(request.POST)
        if form.is_valid():
            d=form.save(commit=False)
            d.book=book
            d.school=institution
            d.save() 
    cont={
        'book_copies':book_copies,
        'form':form,
        'book':book,
        'school_id':school_id,
        'institution':institution
    }
    return render(request, 'templates/library/book_copies.html', cont)

def book_checkout(request, book_id, copy_id, school_id):
    if is_approved_account(request)==False: return redirect('main:un_approved', school_id) 
    if can_manage_library(request): pass 
    else:return redirect('main:un_authorised', school_id)
    institution=get_institution(request, school_id)
    book_copy=BookCopy.objects.get(id=copy_id)
    form = BookCheckoutForm()
    if request.method == 'POST':
        plan_name=subs_plan(request, school_id)
        if plan_name=='Free':return redirect('subs:upgrade', school_id)
        if plan_name=='Basic':return redirect('subs:upgrade', school_id)
        if plan_name=='expired':return redirect('subs:expired', school_id)
        form = BookCheckoutForm(request.POST)
        if form.is_valid():
            d=form.save(commit=False)
            d.book_copy=book_copy
            d.school=institution
            d.save()
            book_copy.is_available=False
            book_copy.save()
            return redirect('library:book_copies', book_id, school_id)
    cont={
        'book_copies':book_copies,
        'form':form,
        'school_id':school_id,
        'institution':institution
    }
    return render(request, 'templates/library/check_out_form.html', cont)

def checkouts(request, school_id):
    if is_approved_account(request)==False: return redirect('main:un_approved', school_id) 
    if can_manage_library(request): pass 
    else:return redirect('main:un_authorised', school_id)
    institution=get_institution(request, school_id)
    c_outs=Checkout.objects.filter(school=institution)
    if request.method == 'POST':
        checkout_id=request.POST.get('c_out', '')
        c_out=Checkout.objects.get(id=checkout_id)
        c_out.returned_date=datetime.today().date()
        c_out.save()
    cont={
        'checkouts':c_outs,
        'school_id':school_id,
        'institution':institution
    }
    return render(request, 'templates/library/book_checkouts.html', cont)