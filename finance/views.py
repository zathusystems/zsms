from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from staff_permision.permisions import can_manage_finances
from finance.utils import *
from main.utils import get_institution, is_ajax, is_approved_account
from subscription.utils import subs_plan
from .models import *
from .forms import *
from datetime import datetime
from main.topdf import render_to_pdf

def fee_categories(request, school_id):
    if is_approved_account(request)==False: return redirect('main:un_approved', school_id)
    if can_manage_finances(request): pass 
    else:return redirect('main:un_authorised', school_id)
    institution=get_institution(request, school_id)
    form=OtherFeeForm()
    cates = FeeCategory.objects.filter(school=institution)
    other_fees = OtherFee.objects.filter(school=institution)
    if request.method=='POST' and 'cate' in request.POST:
        title=request.POST.get('title')
        description=request.POST.get('description')
        FeeCategory.objects.create(school=institution, title=title, description=description)
    if request.method=='POST' and 'other' in request.POST:
        title=request.POST.get('fee_title')
        fee_amount=request.POST.get('fee_amount')
        period=request.POST.get('period')
        OtherFee.objects.create(school=institution, fee_title=title, fee_amount=fee_amount, period=period)
    cont={
        'other_fees':other_fees,
        'categories': cates,
        'school_id':school_id,
        'institution':institution,
        'form':form
        }
    return render(request, 'templates/finance/fee_categories.html', cont)

def fee_list(request, cate_id, school_id):
    if is_approved_account(request)==False: return redirect('main:un_approved', school_id)
    if can_manage_finances(request): pass 
    else:return redirect('main:un_authorised', school_id)
    institution=get_institution(request, school_id)
    cate = FeeCategory.objects.get(id=cate_id)
    fees = Fee.objects.filter(school=institution, fee_category=cate).order_by('-due_date')
    form = FeeForm()
    academic_year=AcademicYear.objects.get(institution=institution, closed=False)
    term=Term.objects.get(institution=institution, closed=False)
    if request.method=='POST':
        form = FeeForm(request.POST)
        last_fee=Fee.objects.filter(fee_category=cate).last()
        if 'close' in request.POST:
            fee_id=request.POST.get('fee_id', '')
            fee=Fee.objects.get(id=fee_id)
            fee.closed=True
            fee.save()
        if last_fee is not None:
            if last_fee.closed:
                if form.is_valid():
                    d=form.save(commit=False)
                    d.school=institution
                    d.fee_category=cate
                    d.save()
        else:
            if form.is_valid():
                d=form.save(commit=False)
                d.school=institution
                d.term=term
                d.academic_year=academic_year
                d.fee_category=cate
                d.save()
    last_fee=Fee.objects.filter(fee_category=cate).last()
    showform=False
    if last_fee is not None:
        if last_fee.closed:
            showform=True
    else:
        showform=True
        
    cont={
        'fees': fees, 
        'category':cate,
        'form':form,
        'showform':showform,
        'academic_year':academic_year,
        'term':term,
        'school_id':school_id,
        'institution':institution
        }
    return render(request, 'templates/finance/fee_list.html', cont)

def fee_list2(request, school_id):
    if is_approved_account(request)==False: return redirect('main:un_approved', school_id) 
    if can_manage_finances(request): pass 
    else:return redirect('main:un_authorised', school_id)
    institution=get_institution(request, school_id)
    academic_year=AcademicYear.objects.get(institution=institution, closed=False)
    term=Term.objects.get(institution=institution, closed=False)
    fee_list=Fee.objects.filter(school=institution, closed=False)
    other_fees = OtherFee.objects.filter(school=institution)
    cont={
        'fee_list':fee_list,
        'other_fees':other_fees,
        'academic_year':academic_year,
        'term':term,
        'school_id':school_id,
        'institution':institution
        }
    return render(request, 'templates/finance/fee_list2.html', cont)

def fee_payments(request, cate_id, fee_id, school_id):
    if is_approved_account(request)==False: return redirect('main:un_approved', school_id)
    if can_manage_finances(request): pass 
    else:return redirect('main:un_authorised', school_id)
    institution=get_institution(request, school_id)
    fee = Fee.objects.get(id=fee_id)
    cate = FeeCategory.objects.get(id=cate_id)
    academic_year=AcademicYear.objects.get(institution=institution,closed=False)
    term=Term.objects.get(institution=institution,closed=False)
    form = FeePaymentForm()
    if request.method == 'POST':
        plan_name=subs_plan(request, school_id)
        if plan_name=='Free':return redirect('subs:upgrade', school_id)
        if plan_name=='Basic':return redirect('subs:upgrade', school_id)
        if plan_name=='expired':return redirect('subs:expired', school_id)
        form = FeePaymentForm(request.POST)
        stu_id=request.POST.get('student_id', '')
        stutent=Student.objects.get(id=stu_id)
        if form.is_valid():
            d=form.save(commit=False)
            d.fee=fee
            d.school=institution
            d.academic_year=academic_year
            d.term=term
            d.student=stutent
            d.save()
  
    cont={
        'form': form,
        'fee':fee,
        'category':cate,
        'academic_year':academic_year,
        'school_id':school_id,
        'institution':institution
        }
    return render(request, 'templates/finance/fee_payments.html', cont)

def add_payment(request, cate_id, fee_id, school_id):
    if is_approved_account(request)==False: return redirect('main:un_approved', school_id)
    if can_manage_finances(request): pass 
    else:return redirect('main:un_authorised', school_id)
    institution=get_institution(request, school_id)
    fee = Fee.objects.get(id=fee_id)
    cate = FeeCategory.objects.get(id=cate_id)
    academic_year=AcademicYear.objects.get(institution=institution,closed=False)
    term=Term.objects.get(institution=institution,closed=False)
    form = FeePaymentForm()
    if request.method == 'POST':
        plan_name=subs_plan(request, school_id)
        if plan_name=='Free':return redirect('subs:upgrade', school_id)
        if plan_name=='Basic':return redirect('subs:upgrade', school_id)
        if plan_name=='expired':return redirect('subs:expired', school_id)
        form = FeePaymentForm(request.POST)
        stu_id=request.POST.get('student_id', '')
        stutent=Student.objects.get(id=stu_id)
        if form.is_valid():
            d=form.save(commit=False)
            d.fee=fee
            d.school=institution
            d.academic_year=academic_year
            d.term=term
            d.student=stutent
            d.save()
            if 'add-onother' in request.POST:pass
            else:return redirect('../')
    cont={
        'form': form,
        'fee':fee,
        'category':cate,
        'academic_year':academic_year,
        'school_id':school_id,
        'institution':institution
        }
    return render(request, 'templates/finance/add_payment.html', cont)

def other_fee_payments(request, fee_id, school_id):
    if is_approved_account(request)==False: return redirect('main:un_approved', school_id)
    if can_manage_finances(request): pass 
    else:return redirect('main:un_authorised', school_id)
    institution=get_institution(request, school_id)
    fee = OtherFee.objects.get(id=fee_id)
    academic_year=AcademicYear.objects.get(institution=institution,closed=False)
    term=Term.objects.get(institution=institution,closed=False)
    form = FeePaymentForm()
    if request.method == 'POST':
        plan_name=subs_plan(request, school_id)
        if plan_name=='Free':return redirect('subs:upgrade', school_id)
        if plan_name=='Basic':return redirect('subs:upgrade', school_id)
        if plan_name=='expired':return redirect('subs:expired', school_id)
        form = FeePaymentForm(request.POST)
        stu_id=request.POST.get('student_id', '')
        stutent=Student.objects.get(id=stu_id)
        if form.is_valid():
            d=form.save(commit=False)
            d.other_fee=fee
            d.school=institution
            d.academic_year=academic_year
            d.term=term
            d.student=stutent
            d.save()
  
    cont={
        'form': form,
        'fee':fee,
        'academic_year':academic_year,
        'school_id':school_id,
        'institution':institution,
        'is_other':True
        }
    return render(request, 'templates/finance/fee_payments.html', cont)


def add_other_payment(request, fee_id, school_id):
    if is_approved_account(request)==False: return redirect('main:un_approved', school_id)
    if can_manage_finances(request): pass 
    else:return redirect('main:un_authorised', school_id)
    institution=get_institution(request, school_id)
    fee = OtherFee.objects.get(id=fee_id)
    academic_year=AcademicYear.objects.get(institution=institution,closed=False)
    term=Term.objects.get(institution=institution,closed=False)
    form = FeePaymentForm()
    students=Student.objects.filter(school=institution)
    if request.method == 'POST':
        plan_name=subs_plan(request, school_id)
        if plan_name=='Free':return redirect('subs:upgrade', school_id)
        if plan_name=='Basic':return redirect('subs:upgrade', school_id)
        if plan_name=='expired':return redirect('subs:expired', school_id)
        form = FeePaymentForm(request.POST)
        stu_id=request.POST.get('student_id', '')
        stutent=Student.objects.get(id=stu_id)
        if form.is_valid():
            d=form.save(commit=False)
            d.other_fee=fee
            d.school=institution
            d.academic_year=academic_year
            d.term=term
            d.student=stutent
            d.save()
            if 'add-onother' in request.POST:pass
            else:return redirect('../')
    cont={
        'form': form,
        'fee':fee,
        'academic_year':academic_year,
        'school_id':school_id,
        'institution':institution,
        'students':students,
        'is_other':True
        }
    return render(request, 'templates/finance/add_payment.html', cont)



def income_expense(request, school_id):
    if is_approved_account(request)==False: return redirect('main:un_approved', school_id) 
    if can_manage_finances(request): pass 
    else:return redirect('main:un_authorised', school_id)
    institution=get_institution(request, school_id)
    academic_year=AcademicYear.objects.get(institution=institution, closed=False)
    term=Term.objects.get(institution=institution, closed=False)
    ex_form=ExpenseForm()
    in_form=IncomeForm()
    if request.method=='POST':
        plan_name=subs_plan(request, school_id)
        if plan_name=='Free':return redirect('subs:upgrade', school_id)
        if plan_name=='Basic':return redirect('subs:upgrade', school_id)
        if plan_name=='expired':return redirect('subs:expired', school_id)
        if 'ex_form' in request.POST:
            ex_form=ExpenseForm(request.POST)
            if ex_form.is_valid():
                d=ex_form.save(commit=False)
                d.institution=institution
                d.academic_year=academic_year
                d.term=term
                if d.amount<=total_balance(institution):
                    d.save()
        
        if 'in_form' in request.POST:
            in_form=IncomeForm(request.POST)
            if in_form.is_valid():
                d=in_form.save(commit=False)
                d.institution=institution
                d.academic_year=academic_year
                d.term=term
                d.save()
    
    current_fees=Fee.objects.filter(school=institution, closed=False)
    other_fees=OtherFee.objects.filter(school=institution)
    total_fee_collected=0
    for fee in current_fees:
        for payment in fee.fee_payments.filter(academic_year=academic_year):
            total_fee_collected+=payment.amount_paid
    
    for other in other_fees:
        for payment in other.other_fee_payments.filter(academic_year=academic_year):
            total_fee_collected+=payment.amount_paid


    incomes=Income.objects.filter(academic_year=academic_year)
    total_income=0
    for income in incomes:
        total_income+=income.amount
    overall_income=total_fee_collected+total_income
    expenses=Expense.objects.filter(academic_year=academic_year)
    total_expense=0
    for expense in expenses:
        total_expense+=expense.amount
    cont={
        'overall_income':overall_income,
        'total_fee_collected':total_fee_collected,
        'incomes':incomes,
        'total_income':total_income,
        'expenses':expenses,
        'total_expense':total_expense,
        'academic_year':academic_year,
        'ex_form':ex_form,
        'in_form':in_form,
        'balance':overall_income-total_expense,
        'school_id':school_id,
        'institution':institution
    }
    return render(request, 'templates/finance/income_expense.html', cont)


def advance_payroll_list(request, school_id):
    if is_approved_account(request)==False: return redirect('main:un_approved', school_id) 
    if can_manage_finances(request): pass 
    else:return redirect('main:un_authorised', school_id)
    institution=get_institution(request, school_id)
    payrolls = AdvancePayroll.objects.filter(school=institution)
    # form=AdvancePayrollForm()
    employees=Employee.objects.filter(school=institution)
    # year=datetime.today().year
    # month=datetime.today().month
    # paid_employees=employees.filter(payroll__year=year, payroll__month=month)

   
    cont={
        'payrolls': payrolls,
        'employees':employees,
        # 'form':form,
        # 'year':year,
        # 'month':month,
        'school_id':school_id,
        'institution':institution
        }
    return render(request, 'templates/finance/advance_payroll_list.html', cont)


def advance_payroll_form(request, school_id):
    if is_approved_account(request)==False: return redirect('main:un_approved', school_id) 
    if can_manage_finances(request): pass 
    else:return redirect('main:un_authorised', school_id)
    institution=get_institution(request, school_id)
    payrolls = AdvancePayroll.objects.filter(school=institution)
    form=AdvancePayrollForm()
    employees=Employee.objects.filter(school=institution)
    year=datetime.today().year
    month=datetime.today().month
    paid_employees=employees.filter(payroll__year=year, payroll__month=month)

    if request.method=='POST':
        plan_name=subs_plan(request, school_id)
        if plan_name=='Free':return redirect('subs:upgrade', school_id)
        if plan_name=='Basic':return redirect('subs:upgrade', school_id)
        if plan_name=='expired':return redirect('subs:expired', school_id)
        form=AdvancePayrollForm(request.POST)
        employee_id=request.POST.get('employee')
        employee=Employee.objects.get(id=employee_id)
        academic_year=AcademicYear.objects.get(institution=institution, closed=False)
        term=Term.objects.get(institution=institution, closed=False)
        if is_ajax(request):
            # reco=PayrollReconciliation.objects.get(employee=employee, processed=False)
            employee_salary=employee.salary
            return JsonResponse({'salary':employee_salary})
        else:
            if form.is_valid():
                d=form.save(commit=False)
                d.school=institution
                d.employee=employee
                d.term=term
                d.academic_year=academic_year
                d.save()
                Expense.objects.create(
                    institution=institution,
                    academic_year=academic_year,
                    term=term,
                    description='Salary payment(advance)',
                    amount=d.amount,
                    date_incurred=d.payment_date
                )
       
    cont={
        'payrolls': payrolls,
        'employees':employees,
        'form':form,
        'year':year,
        'month':month,
        'school_id':school_id,
        'institution':institution
        }
    return render(request, 'templates/finance/advance_payroll_form.html', cont)



def payroll_list(request, school_id):
    if is_approved_account(request)==False: return redirect('main:un_approved', school_id) 
    if can_manage_finances(request): pass 
    else:return redirect('main:un_authorised', school_id)
    institution=get_institution(request, school_id)
    payrolls = Payroll.objects.filter(school=institution)
    # form=PayrollForm()
    # employees=Employee.objects.filter(school=institution)
    # year=datetime.today().year
    # month=datetime.today().month
    # paid_employees=employees.filter(payroll__year=year, payroll__month=month)

    # if request.method=='POST':
    #     plan_name=subs_plan(request, school_id)
    #     if plan_name=='Free':return redirect('subs:upgrade', school_id)
    #     if plan_name=='Basic':return redirect('subs:upgrade', school_id)
    #     if plan_name=='expired':return redirect('subs:expired', school_id)
    #     form=PayrollForm(request.POST)
    #     employee_id=request.POST.get('employee')
    #     employee=Employee.objects.get(id=employee_id)
    #     academic_year=AcademicYear.objects.get(institution=institution, closed=False)
    #     term=Term.objects.get(institution=institution, closed=False)
    #     employee_salary=employee.salary

    #     if is_ajax(request):
    #         try:
    #             reco=PayrollReconciliation.objects.get(employee=employee, processed=False)
    #             return JsonResponse({'salary':employee_salary, 'allowance':reco.allowances, 'deductions':reco.dedactions})
    #         except:
    #             pass
    #         return JsonResponse({'salary':employee_salary})
    #     else:
    #         if form.is_valid():
    #             d=form.save(commit=False)
    #             d.school=institution
    #             d.employee=employee
    #             d.term=term
    #             d.academic_year=academic_year
    #             d.save()
    #             Expense.objects.create(
    #                 institution=institution,
    #                 academic_year=academic_year,
    #                 term=term,
    #                 description='Salary payment',
    #                 amount=d.salary,
    #                 date_incurred=d.payment_date
    #             )
       
    cont={
        'payrolls': payrolls,
        # 'employees':employees,
        # 'form':form,
        # 'year':year,
        # 'month':month,
        'school_id':school_id,
        'institution':institution
        }
    return render(request, 'templates/finance/payroll_list.html', cont)


def finance_reports(request, school_id):
    if is_approved_account(request)==False: return redirect('main:un_approved', school_id)
    if can_manage_finances(request): pass 
    else:return redirect('main:un_authorised', school_id)
    institution=get_institution(request, school_id)
    academic_year=AcademicYear.objects.get(institution=institution, closed=False)
    term=Term.objects.get(institution=institution, closed=False)
    
    date=datetime.today().date()
    cont={
        'total_balance':total_balance(institution),
        
        'total_other_income_year':total_other_income_year(institution, academic_year),
        'total_fee_year':total_fee_this_year(institution, academic_year),
        'total_income_year':total_income_this_year(institution, academic_year),
        'total_expense_year':total_expense_this_year(institution, academic_year),
        'total_balance_year':total_balance_this_year(institution, academic_year),
        
        'total_fee_term':total_fee_this_term(institution, term),
        'total_other_income_term':total_other_income_term(institution, term),
        'total_income_term':total_income_this_term(institution, term),
        'total_expense_term':total_expense_this_term(institution, term),
        'total_balance_term':total_balance_this_term(institution, term),
        
        'total_fee_month':total_fee_this_month(institution, date),
        'total_other_income_month':total_other_income_month(institution, date),
        'total_income_month':total_income_this_month(institution, date),
        'total_expense_month':total_expense_this_month(institution, date),
        'total_balance_month':total_balance_this_month(institution, date),
        
        'total_fee_today':total_fee_this_today(institution, date),
        'total_other_income_today':total_other_income_today(institution, date),
        'total_income_today':total_income_this_today(institution, date),
        'total_expense_today':total_expense_this_today(institution, date),
        'total_balance_today':total_balance_this_today(institution, date),
        
        'academic_year':academic_year,
        'school_id':school_id,
        'institution':institution
    }
    return render(request, 'templates/finance/reports.html', cont)


def payroll_form(request, school_id):
    if is_approved_account(request)==False: return redirect('main:un_approved', school_id) 
    if can_manage_finances(request): pass 
    else:return redirect('main:un_authorised', school_id)
    institution=get_institution(request, school_id)
    payrolls = Payroll.objects.filter(school=institution)
    form=PayrollForm()
    employees=Employee.objects.filter(school=institution)
    year=datetime.today().year
    month=datetime.today().month
    paid_employees=employees.filter(payroll__year=year, payroll__month=month)

    if request.method=='POST':
        plan_name=subs_plan(request, school_id)
        if plan_name=='Free':return redirect('subs:upgrade', school_id)
        if plan_name=='Basic':return redirect('subs:upgrade', school_id)
        if plan_name=='expired':return redirect('subs:expired', school_id)
        form=PayrollForm(request.POST)
        employee_id=request.POST.get('employee')
        employee=Employee.objects.get(id=employee_id)
        academic_year=AcademicYear.objects.get(institution=institution, closed=False)
        term=Term.objects.get(institution=institution, closed=False)
        employee_salary=employee.salary
        print(employee_salary, 'jjjjjjjjjjjjjjjjjjjjjjjjjjjje')
        if is_ajax(request):
            print(employee_salary, 'jjjjjjjjjjjjjjjjjjjjjjjjjjjje')

            try:
                reco=PayrollReconciliation.objects.get(employee=employee, processed=False)
                return JsonResponse({'salary':employee_salary, 'allowance':reco.allowances, 'deductions':reco.dedactions})
            except:
                pass
            return JsonResponse({'salary':employee_salary})
        else:
            if form.is_valid():
                d=form.save(commit=False)
                d.school=institution
                d.employee=employee
                d.term=term
                d.academic_year=academic_year
                d.save()
                Expense.objects.create(
                    institution=institution,
                    academic_year=academic_year,
                    term=term,
                    description='Salary payment',
                    amount=d.salary,
                    date_incurred=d.payment_date
                )
       
    cont={
        'payrolls': payrolls,
        'employees':employees,
        'form':form,
        'year':year,
        'month':month,
        'school_id':school_id,
        'institution':institution
        }
    return render(request, 'templates/finance/payroll_form.html', cont)

def invoicing(request, school_id):
    if is_approved_account(request)==False: return redirect('main:un_approved', school_id) 
    if can_manage_finances(request): pass 
    else:return redirect('main:un_authorised', school_id)
    institution=get_institution(request, school_id)
    invoices=Invoice.objects.filter(school=institution)

    cont={
        'school_id':school_id,
        'institution':institution,
        'invoices':invoices
    }
    return render(request, 'templates/finance/invoicing.html', cont)

def invoice_add(request, school_id):
    if is_approved_account(request)==False: return redirect('main:un_approved', school_id) 
    if can_manage_finances(request): pass 
    else:return redirect('main:un_authorised', school_id)
    institution=get_institution(request, school_id)
    invoices=Invoice.objects.filter(school=institution)
    students=Student.objects.filter(school=institution)
    fees=Fee.objects.filter(school=institution, closed=False)
    other_fees=OtherFee.objects.filter(school=institution)
    if request.method=='POST':
        plan_name=subs_plan(request, school_id)
        if plan_name=='Free':return redirect('subs:upgrade', school_id)
        if plan_name=='Basic':return redirect('subs:upgrade', school_id)
        if plan_name=='expired':return redirect('subs:expired', school_id)
        form=PayrollForm(request.POST)
        student_id=request.POST.get('student')
        fee_id=request.POST.get('fee')
        other_fee_ids=request.POST.getlist('other_fee')
        issue_dis=request.POST.get('issue_discount')
        percentage=request.POST.get('percentage')

        student=Student.objects.get(id=student_id)
        fee=Fee.objects.get(id=fee_id)
        academic_year=AcademicYear.objects.get(institution=institution, closed=False)
        term=Term.objects.get(institution=institution, closed=False)

        inv=Invoice()
        inv.school=institution
        inv.fee=fee
        inv.student=student
        inv.academic_year=academic_year
        inv.term=term
        if issue_dis:
            inv.issue_discount=True
            inv.discount_percentage=percentage
        inv.save()
        for other_id in other_fee_ids:
            other_fee=OtherFee.objects.get(id=other_id)
            inv.other_fee.add(other_fee)

    cont={
        'school_id':school_id,
        'institution':institution,
        'students':students,
        'other_fees':other_fees,
        'fees':fees
    }
    return render(request, 'templates/finance/invoice_form.html', cont)

def invoice_view(request, inv_id, school_id):
    institution=get_institution(request, school_id)
    invoice=Invoice.objects.get(id=inv_id)
    cont={
        'school_id':school_id,
        'institution':institution,
        'invoice':invoice,
       
    }
    if request.method=='POST':
        return render_to_pdf('templates/finance/invoice_pdf.html', cont)
    
    return render(request, 'templates/finance/invoice_view.html', cont)

# def payment_list(request):
#     payments = FeePayment.objects.all()
#     return render(request, 'accounting/payment_list.html', {'payments': payments})


# def payment_update(request, pk):
#     payment = get_object_or_404(FeePayment, pk=pk)
#     if request.method == 'POST':
#         form = FeePaymentForm(request.POST, instance=payment)
#         if form.is_valid():
#             form.save()
#             return redirect('payment_list')
#     else:
#         form = FeePaymentForm(instance=payment)
#     return render(request, 'accounting/payment_form.html', {'form': form})

# def payment_delete(request, pk):
#     payment = get_object_or_404(FeePayment, pk=pk)
#     if request.method == 'POST':
#         payment.delete()
#         return redirect('payment_list')
#     return render(request, 'accounting/payment_confirm_delete.html', {'payment': payment})



# def payroll_add(request):
#     if request.method == 'POST':
#         form = PayrollForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('payroll_list')
#     else:
#         form = PayrollForm()
#     return render(request, 'payroll/payroll_form.html', {'form': form})

# def payroll_update(request, pk):
#     payroll = get_object_or_404(Payroll, pk=pk)
#     if request.method == 'POST':
#         form = PayrollForm(request.POST, instance=payroll)
#         if form.is_valid():
#             form.save()
#             return redirect('payroll_list')
#     else:
#         form = PayrollForm(instance=payroll)
#     return render(request, 'payroll/payroll_form.html', {'form': form})

# def payroll_delete(request, pk):
#     payroll = get_object_or_404(Payroll, pk=pk)
#     if request.method == 'POST':
#         payroll.delete()
#         return redirect('payroll_list')
#     return render(request, 'payroll/payroll_confirm_delete.html', {'payroll': payroll})

# def expense_list(request):
#     expenses = Expense.objects.all()
#     return render(request, 'payroll/expense_list.html', {'expenses': expenses})

# def expense_add(request):
#     if request.method == 'POST':
#         form = ExpenseForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('expense_list')
#     else:
#         form = ExpenseForm()
#     return render(request, 'payroll/expense_form.html', {'form': form})

# def expense_update(request, pk):
#     expense = get_object_or_404(Expense, pk=pk)
#     if request.method == 'POST':
#         form = ExpenseForm(request.POST, instance=expense)
#         if form.is_valid():
#             form.save()
#             return redirect('expense_list')
#     else:
#         form = ExpenseForm(instance=expense)
#     return render(request, 'payroll/expense_form.html', {'form': form})

# def expense_delete(request, pk):
#     expense = get_object_or_404(Expense, pk=pk)
#     if request.method == 'POST':
#         expense.delete()
#         return redirect('expense_list')
#     return render(request, 'payroll/expense_confirm_delete.html', {'expense': expense})
