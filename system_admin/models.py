from django.db import models
from schooladminstration.models import Institution as School
# Create your models here.
from django.db import models

class Testimonial(models.Model):
    school=models.ForeignKey(School, on_delete=models.CASCADE, related_name='testimonials', null=True, blank=True)
    name = models.CharField(max_length=255)  # Name of the person giving the testimonial
    role = models.CharField(max_length=100, null=True, blank=True)  # e.g., 'Parent', 'Student', 'Teacher'
    message = models.TextField()  # Testimonial message
    photo = models.ImageField(upload_to='testimonials/', null=True, blank=True)  # Optional photo of the person
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp for when the testimonial was added

    def __str__(self):
        return f"{self.name} - {self.role}"

    class Meta:
        ordering = ['-created_at']

class TeamMember(models.Model):
    name = models.CharField(max_length=255)  # Name of the team member
    position = models.CharField(max_length=100)  # Job title, e.g., 'Principal', 'Administrator'
    bio = models.TextField(null=True, blank=True)  # Short biography of the team member
    photo = models.ImageField(upload_to='team/', null=True, blank=True)  # Photo of the team member
    linkedin = models.URLField(null=True, blank=True)  # Optional LinkedIn profile link
    twitter = models.URLField(null=True, blank=True)  # Optional Twitter profile link

    def __str__(self):
        return f"{self.name} - {self.position}"
    
    class Meta:
        ordering = ['name']

class SystemFeature(models.Model):
    title = models.CharField(max_length=255)  # Title of the feature, e.g., 'Library Management'
    description1 = models.TextField(default=None)  # Detailed description of the feature
    description2 = models.TextField(default=None)  # Detailed description of the feature
    description3 = models.TextField(default=None)  # Detailed description of the feature
    icon = models.ImageField(upload_to='features/', null=True, blank=True)  # Optional icon for the feature

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['title']


class Contact(models.Model):
    name = models.CharField(max_length=25)  # Title of the feature, e.g., 'Library Management'
    email = models.CharField(max_length=30, null=True, blank=True, default=None)   # Detailed description of the feature
    phone = models.IntegerField(max_length=15)  # Detailed description of the feature
    message = models.TextField()  # Detailed description of the feature
    icon = models.ImageField(upload_to='features/', null=True, blank=True)  # Optional icon for the feature
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created_at']


class About(models.Model):
    content1 = models.TextField()   # Title of the feature, e.g., 'Library Management'
    content2 = models.TextField()   # Detailed description of the feature
    vision = models.TextField()   # Detailed description of the feature
    mission = models.TextField()  # Detailed description of the feature
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['-created_at']

class Terms(models.Model):
    content = models.TextField()   # Title of the feature, e.g., 'Library Management'
    updated_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

class Privacy(models.Model):
    content = models.TextField()   # Title of the feature, e.g., 'Library Management'
    updated_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

class Faqs(models.Model):
    users=(
        ('school owners', 'School Owners'),
        ('teachers', 'Teachers'),
        ('parents', 'Parents'),
    )
    target = models.CharField(max_length=30, choices=users)   # Title of the feature, e.g., 'Library Management'
    quest = models.TextField()   # Detailed description of the feature
    ans = models.TextField()  # Detailed description of the feature
    created_at = models.DateTimeField(auto_now_add=True)
    

