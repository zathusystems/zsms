from django.db import models
from django.contrib.auth.models import User
from schooladminstration.models import Institution
from django.utils import timezone
from datetime import timedelta
# Define subscription categories
class SubscriptionPlan(models.Model):
    PLAN_CHOICES = [
        ('Free', 'Free - Limited Features'),
        ('Basic', 'Basic - Least Limited Features'),
        ('Premium', 'Premium - Full Features')
    ]
    name = models.CharField(max_length=50, choices=PLAN_CHOICES, default='Free')
    price = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)  # For Basic and Premium plans
    yearly_price = models.DecimalField(max_digits=9, decimal_places=2, default=0.00, null=True, blank=True)  # For Basic and Premium plans
    half_year_price = models.DecimalField(max_digits=9, decimal_places=2, default=0.00, null=True, blank=True)
    description=models.TextField(default=None, null=True, blank=True)
    def __str__(self):
        return self.name
        
    
class Feature(models.Model):
    plan=models.ManyToManyField(SubscriptionPlan, related_name='plan_features', null=True)
    feature=models.CharField(max_length=50)
    description=models.TextField(default=None, null=True, blank=True)


class SchoolSubscription(models.Model):
    school = models.OneToOneField(Institution, on_delete=models.CASCADE, related_name='subscription')  # School owner's account
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.CASCADE, related_name='subscriptions')
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(null=True, blank=True, default=None)
    is_trial = models.BooleanField(default=False)
    def __str__(self):
        return f"{self.school.institution_name} - {self.plan.name}"
    def is_active(self):
        # Check if the subscription is still active
        if self.end_date:
            return timezone.now() < self.end_date
        else:
            if self.plan.name == 'Free':
                return True
            return False
    def remaining_trial_days(self):
        if self.is_trial and self.end_date:
            if (self.end_date - timezone.now()).days < 1:
                return 0
            return (self.end_date - timezone.now()).days
        return 0
    
    def remaining_days(self):
        if self.end_date:
            if (self.end_date - timezone.now()).days < 1:
                return 0
            return (self.end_date - timezone.now()).days
        return 0
    
    def duration(self):
        return (self.end_date-self.start_date).days

    # def activate_trial(self):
    #     if not self.is_trial:
    #         self.plan = SubscriptionPlan.objects.get(name='PREMIUM')  # Set trial to Premium features
    #         self.end_date = timezone.now() + timedelta(days=30)  # 30-day trial
    #         self.is_trial = True
    #         self.save()

class SubscriptionPayments(models.Model):
    school = models.ForeignKey(Institution, on_delete=models.CASCADE, related_name='subscription_payments')
    amount=models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    trans_id=models.IntegerField(max_length=30)
    successful=models.BooleanField(default=False)
    duration = models.CharField(max_length=20)  # Subscription duration (e.g., 30 days)

    def __str__(self):
        return f"{self.school} {self.duration}"