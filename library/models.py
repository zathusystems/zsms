from django.db import models
from datetime import date

from schooladminstration.models import Institution
from student.models import Student


# Create your models here.
# Model to represent a book
class Book(models.Model):
    school=models.ForeignKey(Institution, on_delete=models.CASCADE, null=True, blank=True, default=None, related_name='books')
    title = models.CharField(max_length=200)  # Title of the book
    author = models.CharField(max_length=200)  # Author of the book
    isbn = models.CharField(max_length=13, unique=True, null=True, blank=True, default=None)  # ISBN number for the book
    publication_date = models.DateField()  # Date when the book was published
    description = models.TextField()  # Description of the book
    date = models.DateField(auto_now_add=True, null=True, blank=True) 
    def __str__(self):
        return self.title

# Model to represent a copy of a book
class BookCopy(models.Model):
    school=models.ForeignKey(Institution, on_delete=models.CASCADE, null=True, blank=True, default=None, related_name='book_copies')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='book_copies')  # Link to the Book model
    copy_number = models.PositiveIntegerField()  # Number to differentiate copies of the same book
    is_available = models.BooleanField(default=True)  # Availability status of the copy
    date = models.DateField(auto_now_add=True, null=True, blank=True) 
    def __str__(self):
        return f"{self.book.title} - Copy {self.copy_number}"

# Model to represent a book checkout
class Checkout(models.Model):
    school=models.ForeignKey(Institution, on_delete=models.CASCADE, null=True, blank=True, default=None, related_name='book_checkouts')
    book_copy = models.ForeignKey(BookCopy, on_delete=models.CASCADE, related_name='book_checkouts', null=True, blank=True, default=None)  # Link to the BookCopy model
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='book_checkouts')  # Link to the StudentProfile model
    checkout_date = models.DateField(auto_now_add=True)  # Date when the book was checked out
    due_date = models.DateField()  # Date when the book is due to be returned
    returned_date = models.DateField(null=True, blank=True)  # Date when the book was actually returned

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.returned_date:
            self.book_copy.is_available=True
            self.book_copy.save()
        
    # Method to check if the book is overdue
    def is_overdue(self):
        if self.returned_date is None:  # If the book hasn't been returned yet
            return self.due_date < date.today()  # Check if the due date has passed
        return self.returned_date > self.due_date  # If the book was returned late

    def __str__(self):
        return f"{self.book_copy.book.title} - {self.student}"

# Model to represent a book reservation
class Reservation(models.Model):
    book_copy = models.ForeignKey(BookCopy, on_delete=models.CASCADE)  # Link to the BookCopy model
    student = models.ForeignKey(Student, on_delete=models.CASCADE)  # Link to the StudentProfile model
    reservation_date = models.DateField(auto_now_add=True)  # Date when the book was reserved
    is_active = models.BooleanField(default=True)  # Status of the reservation

    def __str__(self):
        return f"{self.book_copy.book.title} - {self.student}"

# Model to represent a fine for overdue books
class Fine(models.Model):
    checkout = models.ForeignKey(Checkout, on_delete=models.CASCADE)  # Link to the Checkout model
    amount = models.DecimalField(max_digits=5, decimal_places=2)  # Fine amount
    paid = models.BooleanField(default=False)  # Whether the fine has been paid
    date = models.DateField(auto_now_add=True, null=True, blank=True) 
    def __str__(self):
        return f"Fine for {self.checkout.book_copy.book.title} - {self.amount}"