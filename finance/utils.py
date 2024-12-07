from finance.models import Expense, Fee, Income, OtherFee

def total_fee(institution):
    current_fees=Fee.objects.filter(school=institution)
    other_fees=OtherFee.objects.filter(school=institution)
    total_fee_collected=0
    for fee in current_fees:
        for payment in fee.fee_payments.all():
            total_fee_collected+=payment.amount_paid

    for other in other_fees:
        for payment in other.other_fee_payments.all():
            total_fee_collected+=payment.amount_paid
    return total_fee_collected

def total_income(institution):
    incomes=Income.objects.filter(institution=institution)
    total_income=0
    for income in incomes:
        total_income+=income.amount
    overall_income=total_fee(institution)+total_income
    return overall_income

def total_expense(institution):
    expenses=Expense.objects.filter(institution=institution)
    total_expense=0
    for expense in expenses:
        total_expense+=expense.amount
    return total_expense

def total_balance(institution):
    balance=total_income(institution)-total_expense(institution)
    return balance
        
        
        
        
def total_fee_this_year(institution, academic_year):
    current_fees=Fee.objects.filter(school=institution)
    other_fees=OtherFee.objects.filter(school=institution)
    total_fee_collected=0
    for fee in current_fees:
        for payment in fee.fee_payments.filter(academic_year=academic_year):
            total_fee_collected+=payment.amount_paid

    for other in other_fees:
        for payment in other.other_fee_payments.filter(academic_year=academic_year):
            total_fee_collected+=payment.amount_paid
    return total_fee_collected


def total_income_this_year(institution, academic_year):
    incomes=Income.objects.filter(institution=institution, academic_year=academic_year)
    total_income=0
    for income in incomes:
        total_income+=income.amount
    overall_income=total_fee_this_year(institution, academic_year)+total_income
    return overall_income

def total_other_income_year(institution, academic_year):
    incomes=Income.objects.filter(institution=institution, academic_year=academic_year)
    total_income=0
    for income in incomes:
        total_income+=income.amount
    return total_income

def total_expense_this_year(institution, academic_year):
    expenses=Expense.objects.filter(institution=institution, academic_year=academic_year)
    total_expense=0
    for expense in expenses:
        total_expense+=expense.amount
    return total_expense

def total_balance_this_year(institution, academic_year):
    balance=total_income_this_year(institution, academic_year)-total_expense_this_year(institution, academic_year)
    return balance







def total_fee_this_term(institution, term):
    current_fees=Fee.objects.filter(school=institution)
    other_fees=OtherFee.objects.filter(school=institution)
    total_fee_collected=0
    for fee in current_fees:
        for payment in fee.fee_payments.filter(term=term):
            total_fee_collected+=payment.amount_paid

    for other in other_fees:
        for payment in other.other_fee_payments.filter(term=term):
            total_fee_collected+=payment.amount_paid
    return total_fee_collected

def total_income_this_term(institution, term):
    incomes=Income.objects.filter(institution=institution, term=term)
    total_income=0
    for income in incomes:
        total_income+=income.amount
    overall_income=total_fee_this_term(institution, term)+total_income
    return overall_income

def total_other_income_term(institution, term):
    incomes=Income.objects.filter(institution=institution, term=term)
    total_income=0
    for income in incomes:
        total_income+=income.amount
    return total_income

def total_expense_this_term(institution, term):
    expenses=Expense.objects.filter(institution=institution, term=term)
    total_expense=0
    for expense in expenses:
        total_expense+=expense.amount
    return total_expense

def total_balance_this_term(institution, term):
    balance=total_income_this_term(institution, term)-total_expense_this_term(institution, term)
    return balance



def total_fee_this_month(institution, date):
    current_fees=Fee.objects.filter(school=institution)
    other_fees=OtherFee.objects.filter(school=institution)
    total_fee_collected=0
    for fee in current_fees:
        for payment in fee.fee_payments.filter(payment_date__month=date.month, payment_date__year=date.year):
            total_fee_collected+=payment.amount_paid

    for other in other_fees:
        for payment in other.other_fee_payments.filter(payment_date__month=date.month, payment_date__year=date.year):
            total_fee_collected+=payment.amount_paid
    return total_fee_collected


def total_income_this_month(institution, date):
    incomes=Income.objects.filter(institution=institution, date__month=date.month, date__year=date.year)
    total_income=0
    for income in incomes:
        total_income+=income.amount
    overall_income=total_fee_this_month(institution, date)+total_income
    return overall_income

def total_other_income_month(institution, date):
    incomes=Income.objects.filter(institution=institution, date__year=date.year, date__month=date.month)
    total_income=0
    for income in incomes:
        total_income+=income.amount
    return total_income

def total_expense_this_month(institution, date):
    expenses=Expense.objects.filter(institution=institution, date__year=date.year, date__month=date.month)
    total_expense=0
    for expense in expenses:
        total_expense+=expense.amount
    return total_expense

def total_balance_this_month(institution, date):
    balance=total_income_this_month(institution, date)-total_expense_this_month(institution, date)
    return balance



def total_fee_this_today(institution, date):
    current_fees=Fee.objects.filter(school=institution)
    other_fees=OtherFee.objects.filter(school=institution)
    total_fee_collected=0
    for fee in current_fees:
        for payment in fee.fee_payments.filter(payment_date__day=date.day, payment_date__year=date.year):
            total_fee_collected+=payment.amount_paid

    for other in other_fees:
        for payment in other.other_fee_payments.filter(payment_date__day=date.day, payment_date__year=date.year):
            total_fee_collected+=payment.amount_paid
    return total_fee_collected


    # current_fees=Fee.objects.filter(school=institution, closed=False)
    # total_fee_collected=0
    # for fee in current_fees:
    #     for payment in fee.fee_payments.filter(payment_date__day=date.day, payment_date__year=date.year):
    #         total_fee_collected+=payment.amount_paid
    # return total_fee_collected

def total_income_this_today(institution, date):
    incomes=Income.objects.filter(institution=institution, date__day=date.day, date__year=date.year)
    total_income=0
    for income in incomes:
        total_income+=income.amount
    overall_income=total_fee_this_today(institution, date)+total_income
    return overall_income

def total_other_income_today(institution, date):
    incomes=Income.objects.filter(institution=institution, date__year=date.year, date__day=date.day)
    total_income=0
    for income in incomes:
        total_income+=income.amount
    return total_income

def total_expense_this_today(institution, date):
    expenses=Expense.objects.filter(institution=institution, date__year=date.year, date__day=date.day)
    total_expense=0
    for expense in expenses:
        total_expense+=expense.amount
    return total_expense

def total_balance_this_today(institution, date):
    balance=total_income_this_today(institution, date)-total_expense_this_today(institution, date)
    return balance
