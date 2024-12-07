from datetime import datetime
from django import forms
from .models import AdvancePayroll, Fee, Income, OtherFee, Payroll, Expense, FeePayment, PayrollReconciliation

class FeeForm(forms.ModelForm):
    due_date = forms.DateField(
        widget=forms.TextInput(
            attrs={
                'class':'form-control',
                'type':'date'
            }
        )
    )
 
    class Meta:
        model = Fee
        fields = ['fee_title', 'fee_amount', 'due_date']
    def __init__(self, *args, **kwargs):
        super(FeeForm, self).__init__(*args, **kwargs)
        self.fields['fee_amount'].widget.attrs.update({'class':'form-control'})
        self.fields['fee_title'].widget.attrs.update({'class':'form-control'})

class OtherFeeForm(forms.ModelForm):
    class Meta:
        model = OtherFee
        fields = ['fee_title', 'fee_amount', 'period']
    def __init__(self, *args, **kwargs):
        super(OtherFeeForm, self).__init__(*args, **kwargs)
        self.fields['fee_amount'].widget.attrs.update({'class':'form-control'})
        self.fields['fee_title'].widget.attrs.update({'class':'form-control'})
        self.fields['period'].widget.attrs.update({'class':'form-control'})

class FeePaymentForm(forms.ModelForm):
    class Meta:
        model = FeePayment
        fields = ['amount_paid']
    def __init__(self, *args, **kwargs):
        super(FeePaymentForm, self).__init__(*args, **kwargs)
        self.fields['amount_paid'].widget.attrs.update({'class':'form-control'})


# class InvoiceForm(forms.ModelForm):
#     date_incurred = forms.DateField(widget=forms.TextInput(attrs={
#                 'class':'form-control',
#                 'type':'date'
#             }))
#     class Meta:
#         model = Expense
#         fields = ['amount', 'description', 'date_incurred']
#     def __init__(self, *args, **kwargs):
#         super(InvoiceForm, self).__init__(*args, **kwargs)
#         self.fields['amount'].widget.attrs.update({'class':'form-control'})
#         self.fields['description'].widget.attrs.update({'class':'form-control'})
        
# months=['jan', feb, mar, april, may, jun, july, aug, sep]
class PayrollForm(forms.ModelForm):
    payment_date = forms.DateField(
        widget=forms.TextInput(
            attrs={
                'class':'form-control',
                'type':'date'
            }
        )
    )
    year = forms.IntegerField(
        # label='Date started working',
        # help_text='e.g 32 inch, 40 inch, 50 inch',
        widget=forms.TextInput(
            attrs={
                'class':'form-control',
                'value':f'{datetime.today().year}'
            }
        )
    )
    month = forms.IntegerField(
        # label='Date started working',
        # help_text='e.g 32 inch, 40 inch, 50 inch',
        widget=forms.TextInput(
            attrs={
                'class':'form-control',
                'value':f'{datetime.today().month}'
            }
        )
    )
    salary = forms.IntegerField(
        # label='Date started working',
        # help_text='e.g 32 inch, 40 inch, 50 inch',
        widget=forms.TextInput(
            attrs={
                'class':'form-control',
                'readonly':True
            }
        )
    )
    class Meta:
        model = Payroll
        fields = ['year', 'month', 'salary', 'allowances', 'dedactions', 'payment_date']
    def __init__(self, *args, **kwargs):
        super(PayrollForm, self).__init__(*args, **kwargs)
        self.fields['year'].widget.attrs.update({'class':'form-control'})
        self.fields['month'].widget.attrs.update({'class':'form-control'})
        self.fields['salary'].widget.attrs.update({'class':'form-control'})
        self.fields['allowances'].widget.attrs.update({'class':'form-control'})
        self.fields['dedactions'].widget.attrs.update({'class':'form-control'})
        self.fields['payment_date'].widget.attrs.update({'class':'form-control'})



# months=['jan', feb, mar, april, may, jun, july, aug, sep]
class AdvancePayrollForm(forms.ModelForm):
    payment_date = forms.DateField(
        widget=forms.TextInput(
            attrs={
                'class':'form-control',
                'type':'date'
            }
        )
    )
    year = forms.IntegerField(
        # label='Date started working',
        # help_text='e.g 32 inch, 40 inch, 50 inch',
        widget=forms.TextInput(
            attrs={
                'class':'form-control',
                'value':f'{datetime.today().year}'
            }
        )
    )
    month = forms.IntegerField(
        # label='Date started working',
        # help_text='e.g 32 inch, 40 inch, 50 inch',
        widget=forms.TextInput(
            attrs={
                'class':'form-control',
                'value':f'{datetime.today().month}'
            }
        )
    )
    amount = forms.IntegerField(
        label='Amount',
        # help_text='e.g 32 inch, 40 inch, 50 inch',
        widget=forms.TextInput(
            attrs={
                'class':'form-control',
            }
        )
    )
    class Meta:
        model = AdvancePayroll
        fields = ['year', 'month', 'amount', 'payment_date']
    def __init__(self, *args, **kwargs):
        super(AdvancePayrollForm, self).__init__(*args, **kwargs)
        self.fields['year'].widget.attrs.update({'class':'form-control'})
        self.fields['month'].widget.attrs.update({'class':'form-control'})
        self.fields['amount'].widget.attrs.update({'class':'form-control'})
        # self.fields['allowances'].widget.attrs.update({'class':'form-control'})
        # self.fields['dedactions'].widget.attrs.update({'class':'form-control'})
        self.fields['payment_date'].widget.attrs.update({'class':'form-control'})



class ExpenseForm(forms.ModelForm):
    date_incurred = forms.DateField(widget=forms.TextInput(attrs={
                'class':'form-control',
                'type':'date'
            }))
    class Meta:
        model = Expense
        fields = ['amount', 'description', 'date_incurred']
    def __init__(self, *args, **kwargs):
        super(ExpenseForm, self).__init__(*args, **kwargs)
        self.fields['amount'].widget.attrs.update({'class':'form-control'})
        self.fields['description'].widget.attrs.update({'class':'form-control'})
        
        
class IncomeForm(forms.ModelForm):
    date_incurred = forms.DateField(widget=forms.TextInput(attrs={
                'class':'form-control',
                'type':'date'
            }))
    class Meta:
        model = Income
        fields = ['source', 'amount', 'description', 'date_incurred']
    def __init__(self, *args, **kwargs):
        super(IncomeForm, self).__init__(*args, **kwargs)
        self.fields['source'].widget.attrs.update({'class':'form-control'})
        self.fields['amount'].widget.attrs.update({'class':'form-control'})
        self.fields['description'].widget.attrs.update({'class':'form-control'})
        
class ReconciliationForm(forms.ModelForm):
    class Meta:
        model = PayrollReconciliation
        fields = ['allowances','dedactions']
    def __init__(self, *args, **kwargs):
        super(ReconciliationForm, self).__init__(*args, **kwargs)
        # self.fields['employee'].widget.attrs.update({'class':'form-control'})
        self.fields['allowances'].widget.attrs.update({'class':'form-control', 'required':'true'})
        self.fields['dedactions'].widget.attrs.update({'class':'form-control', 'required':'true'})
