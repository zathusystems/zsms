from django import forms
from .models import Book, BookCopy, Checkout

class BookForm(forms.ModelForm):
    publication_date = forms.DateField(
        required=False,
        widget=forms.TextInput(
            attrs={
                'class':'form-control',
                'type':'date'
            }
        )
    )
    class Meta:
        model = Book
        fields = ['title', 'author', 'description', 'isbn', 'publication_date']
    def __init__(self, *args, **kwargs):
        super(BookForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'class':'form-control'})
        self.fields['author'].widget.attrs.update({'class':'form-control'})
        self.fields['description'].widget.attrs.update({'class':'form-control'})
        self.fields['isbn'].widget.attrs.update({'class':'form-control'})
        
        
class BookCheckoutForm(forms.ModelForm):
    due_date = forms.DateField(
        widget=forms.TextInput(
            attrs={
                'class':'form-control',
                'type':'date'
            }
        )
    )
    class Meta:
        model = Checkout
        fields = ['student', 'due_date']
    def __init__(self, *args, **kwargs):
        super(BookCheckoutForm, self).__init__(*args, **kwargs)
        self.fields['student'].widget.attrs.update({'class':'form-control select2', 'style':'width;100%'})


class BookCopyForm(forms.ModelForm):
    class Meta:
        model = BookCopy
        fields = ['copy_number',]
    def __init__(self, *args, **kwargs):
        super(BookCopyForm, self).__init__(*args, **kwargs)
        self.fields['copy_number'].widget.attrs.update({'class':'form-control'})

