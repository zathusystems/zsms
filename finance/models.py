from django.db import models
from employee.models import Employee
from school_calendar.models import AcademicYear, Term
from schooladminstration.models import Institution
from student.models import Enrollment, Student
from teacher.models import Instructor

# Create your models here.


class FeeCategory(models.Model):
    school=models.ForeignKey(Institution, on_delete=models.CASCADE, related_name='fee_categories')
    title=models.CharField(max_length=50)
    enrollment=models.ManyToManyField(Enrollment, related_name='fee_category')
    description=models.TextField(null=True, blank=True, default=None)
    def __str__(self):
        return self.title

class Fee(models.Model):
    school=models.ForeignKey(Institution, on_delete=models.CASCADE, null=True, blank=True, default=None, related_name='fees')
    fee_title=models.CharField(max_length=50, null=True, blank=True, default=None)
    fee_category=models.ForeignKey(FeeCategory, on_delete=models.CASCADE, null=True, blank=True, default=None, related_name='fees')
    term=models.ForeignKey(Term, on_delete=models.CASCADE, null=True, blank=True, default=None, related_name='fees')
    academic_year=models.ForeignKey(AcademicYear, on_delete=models.CASCADE, null=True, blank=True, default=None, related_name='fees')
    fee_amount=models.DecimalField(max_digits=10, decimal_places=2, default=0)
    due_date=models.DateField()
    p=(
        ('once off', 'Once Off'),
        ('per month', 'Per Month'),
        ('per term', 'Per Term'),
        ('per semister', 'Per Semister'),
        ('per year', 'Per Year')
    )
    period=models.CharField(max_length=20, choices=p, default='per term', null=True, blank=True)
    closed=models.BooleanField(default=False)
    date=models.DateField(auto_now_add=True, null=True, blank=True)
    class Meta:
        ordering=['-date']
        unique_together=['term', 'academic_year']
    
    def __str__(self):
        return f'Tuition fee({self.fee_category.title}) - {self.fee_amount}'
    
class OtherFee(models.Model):
    school=models.ForeignKey(Institution, on_delete=models.CASCADE, null=True, blank=True, default=None, related_name='other_fees')
    fee_title=models.CharField(max_length=50, null=True, blank=True, default=None)
    enrollment=models.ManyToManyField(Enrollment, related_name='other_fees',  null=True, blank=True, default=None)
    p=(
        ('once off', 'Once Off'),
        ('per month', 'Per Month'),
        ('per term', 'Per Term'),
        ('per semister', 'Per Semister'),
        ('per year', 'Per Year')
    )
    period=models.CharField(max_length=20, choices=p)
    fee_amount=models.DecimalField(max_digits=10, decimal_places=2, default=0)
    # due_date=models.DateField()
    closed=models.BooleanField(default=False)
    date=models.DateField(auto_now_add=True, null=True, blank=True)
    class Meta:
        ordering=['-date']
    
    def __str__(self):
        return f'{self.fee_title } - MK{self.fee_amount} {self.period}'
    
class FeePayment(models.Model):
    school=models.ForeignKey(Institution, on_delete=models.CASCADE, null=True, blank=True, default=None, related_name='fee_payments')
    academic_year=models.ForeignKey(AcademicYear, on_delete=models.CASCADE, null=True, blank=True, default=None, related_name='fee_payments')
    term=models.ForeignKey(Term, on_delete=models.CASCADE, null=True, blank=True, default=None, related_name='fee_payments')
    student=models.ForeignKey(Student, on_delete=models.CASCADE, related_name='fee_payments')
    fee=models.ForeignKey(Fee, on_delete=models.CASCADE , related_name='fee_payments', null=True, blank=True, default=None)
    other_fee=models.ForeignKey(OtherFee, on_delete=models.CASCADE , related_name='other_fee_payments', null=True, blank=True, default=None)
    amount_paid=models.DecimalField(max_digits=10, decimal_places=2)
    fully_paid=models.BooleanField(default=False)
    payment_date=models.DateField(auto_now_add=True, null=True, blank=True)
    class Meta:
        ordering=['-payment_date']
    
    def __str__(self):
        return f'Payment of {self.amount_paid} for {self.student.first_name}'
    
    def save(self, *args, **kwargs):
        if self.amount_paid and self.fee:
            if self.amount_paid >= self.fee.fee_amount:
                self.fully_paid=True
        elif self.amount_paid and self.other_fee:
            if self.amount_paid >= self.other_fee.fee_amount:
                self.fully_paid=True
        super(FeePayment, self).save(*args, **kwargs)
        
    def is_fully_paid(self):
        student_payments=self.student.fee_payments.filter(fee=self.fee)
        total=0
        for payment in student_payments:
            amount=payment.amount_paid
            total=+amount
        if total>=self.fee.fee_amount:
            return True
        else:
            return False
    
    def balance(self):
        if self.fee:
            student_payments=self.student.fee_payments.filter(fee=self.fee)
            total=0
            for payment in student_payments:
                amount=payment.amount_paid
                total=+amount
            return self.fee.fee_amount-total
        elif self.other_fee:
            student_payments=self.student.fee_payments.filter(other_fee=self.other_fee)
            total=0
            for payment in student_payments:
                amount=payment.amount_paid
                total=+amount
            return self.other_fee.fee_amount-total
    
class Invoice(models.Model):
    school=models.ForeignKey(Institution, on_delete=models.CASCADE, null=True, blank=True, default=None, related_name='invoices')
    academic_year=models.ForeignKey(AcademicYear, on_delete=models.CASCADE, null=True, blank=True, default=None, related_name='invoices')
    term=models.ForeignKey(Term, on_delete=models.CASCADE, null=True, blank=True, default=None, related_name='invoices')
    student=models.ForeignKey(Student, on_delete=models.CASCADE, related_name='invoices')
    fee=models.ForeignKey(Fee, on_delete=models.CASCADE , related_name='invoices')
    other_fee=models.ManyToManyField(OtherFee, related_name='invoices', null=True, blank=True, default=None)
    issue_discount=models.BooleanField(default=False)
    discount_percentage=models.IntegerField(max_length=2, null=True, blank=True, default=None)
    discount_amount=models.DecimalField(max_digits=10, decimal_places=2, default=False, null=True, blank=True)
    
    def __str__(self):
        return f'Invoice for {self.student}'
    
    def tuition_fee_amount(self):
        return self.fee.fee_amount
    
    def other_fee_amount(self):
        total=0
        for d in self.other_fee.all():
            total+=d.fee_amount
        return total
    
    def total_fees(self):
        return self.tuition_fee_amount()+self.other_fee_amount()
    
    def amount_paid(self):
        payments=FeePayment.objects.filter(student=self.student, academic_year=self.academic_year, term=self.term)
        total=0
        for payment in payments:
            total+=payment.amount_paid
        return total

    def after_discount_fee(self):
        if self.issue_discount:
            total=self.total_fees()
            dis=total*self.discount_percentage/100
            return total-dis
        
    def fee_balance(self):
        if self.issue_discount:
            b=self.after_discount_fee()-self.amount_paid()
            return b
        b=self.total_fees()-self.amount_paid()
        return b

class FeePaymentHistory(models.Model):
    school=models.ForeignKey(Institution, on_delete=models.CASCADE, null=True, blank=True, default=None, related_name='fee_payments_history')
    fee_payment=models.ForeignKey(FeePayment, on_delete=models.CASCADE, related_name='fee_payments_history')
    amount_paid=models.DecimalField(max_digits=10, decimal_places=2)
    payment_date=models.DateField(auto_now_add=True)
    class Meta:
        ordering=['-payment_date']
    
    def __str__(self):
        return f'Payment of {self.amount_paid}'
    
    def save(self, *args, **kwargs):
        self.amount_paid=self.fee_payment.amount_paid
        self.save()
        super(FeePaymentHistory, self).save(*args, **kwargs)
    
    
class Income(models.Model):
    institution=models.ForeignKey(Institution, on_delete=models.CASCADE, related_name='incomes')
    academic_year=models.ForeignKey(AcademicYear, on_delete=models.CASCADE, null=True, blank=True, default=None, related_name='incomes')
    term=models.ForeignKey(Term, on_delete=models.CASCADE, null=True, blank=True, default=None, related_name='incomes')
    source=models.CharField(max_length=50)
    description=models.TextField()
    amount=models.DecimalField(max_digits=10, decimal_places=2)
    date=models.DateTimeField(auto_now_add=True, null=True, blank=True)
    date_incurred=models.DateField(null=True, blank=True, default=None)
    class Meta:
        ordering=['-date']
    def __str__(self):
        return f'{self.source} - {self.amount}'
    
class Expense(models.Model):
    institution=models.ForeignKey(Institution, on_delete=models.CASCADE, related_name='expenses')
    academic_year=models.ForeignKey(AcademicYear, on_delete=models.CASCADE, null=True, blank=True, default=None, related_name='expenses')
    term=models.ForeignKey(Term, on_delete=models.CASCADE, null=True, blank=True, default=None, related_name='expenses')
    description=models.TextField()
    amount=models.DecimalField(max_digits=10, decimal_places=2)
    date=models.DateTimeField(auto_now_add=True, null=True, blank=True)
    date_incurred=models.DateField(null=True, blank=True, default=None)
    class Meta:
        ordering=['-date']
    def __str__(self):
        return f'{self.description} - {self.amount}'
    
class PayrollReconciliation(models.Model):
    school=models.ForeignKey(Institution, on_delete=models.CASCADE, null=True, blank=True, default=None, related_name='deductions_a')
    employee=models.ForeignKey(Employee, on_delete=models.CASCADE, null=True, blank=True, default=None, related_name='deductions_a')
    academic_year=models.ForeignKey(AcademicYear, on_delete=models.CASCADE, null=True, blank=True, default=None, related_name='deductions_a')
    term=models.ForeignKey(Term, on_delete=models.CASCADE, null=True, blank=True, default=None, related_name='deductions_a')
    month=models.IntegerField()
    year=models.IntegerField()
    allowances=models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, default=None)
    dedactions=models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, default=None)
    processed=models.BooleanField(default=False)
    class Meta:
        unique_together = ('month', 'employee', 'term')


class AdvancePayroll(models.Model):
    school=models.ForeignKey(Institution, on_delete=models.CASCADE, null=True, blank=True, default=None, related_name='advance_payroll')
    employee=models.ForeignKey(Employee, on_delete=models.CASCADE, null=True, blank=True, default=None, related_name='advance_payroll')
    academic_year=models.ForeignKey(AcademicYear, on_delete=models.CASCADE, null=True, blank=True, default=None, related_name='advance_payroll')
    term=models.ForeignKey(Term, on_delete=models.CASCADE, null=True, blank=True, default=None, related_name='advance_payroll')
    month=models.IntegerField()
    year=models.IntegerField()
    amount=models.DecimalField(max_digits=10, decimal_places=2)
    typs=(
        ('cash', 'Cash'),
        ('bank transfer', 'Bank Transfer'),
        ('cheque', 'Cheque')
    )
    payment_method=models.CharField(null=True, default=None, blank=True, choices=typs, max_length=15)
    payment_date = models.DateField(null=True, blank=True, default=None)
    class Meta:
        unique_together = ('month', 'employee', 'term')


class Payroll(models.Model):
    school=models.ForeignKey(Institution, on_delete=models.CASCADE, null=True, blank=True, default=None, related_name='payroll')
    employee=models.ForeignKey(Employee, on_delete=models.CASCADE, null=True, blank=True, default=None, related_name='payroll')
    academic_year=models.ForeignKey(AcademicYear, on_delete=models.CASCADE, null=True, blank=True, default=None, related_name='payroll')
    term=models.ForeignKey(Term, on_delete=models.CASCADE, null=True, blank=True, default=None, related_name='payroll')
    month=models.IntegerField()
    year=models.IntegerField()
    salary=models.DecimalField(max_digits=10, decimal_places=2)
    allowances=models.DecimalField(max_digits=10, decimal_places=2)
    dedactions=models.DecimalField(max_digits=10, decimal_places=2)
    typs=(
        ('cash', 'Cash'),
        ('bank transfer', 'Bank Transfer'),
        ('cheque', 'Cheque')
    )
    payment_method=models.CharField(null=True, default=None, blank=True, choices=typs, max_length=15)
    payment_date = models.DateField(null=True, blank=True, default=None)
    class Meta:
        unique_together = ('month', 'employee', 'term')

    def net_salary(self):
        gross_salary=self.employee.salary+self.allowances
        net_salary=gross_salary-self.dedactions
        return net_salary

    def gross_salary(self):
        gross_salary=self.employee.salary+self.allowances
        return gross_salary
    




class Payslip(models.Model):
    payroll = models.ForeignKey(Payroll, on_delete=models.CASCADE)
    month = models.DateField()
    total_payment = models.DecimalField(max_digits=10, decimal_places=2)

    def generate_payslip(self):
        # Logic for generating a payslip
        total = self.payroll.salary + self.payroll.allowances - self.payroll.dedactions
        self.total_payment = total
        self.save()