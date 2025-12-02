from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = [
        ('applicant', 'Applicant'),
        ('reviewer', 'Reviewer'),
        ('admin', 'Admin'),
    ]
    
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='applicant')
    
    def is_applicant(self):
        return self.role == 'applicant'
    
    def is_reviewer(self):
        return self.role == 'reviewer'
    
    def is_admin_role(self):
        return self.role == 'admin'
    
    def __str__(self):
        return f"{self.username} ({self.role})"

class Rubric(models.Model):
    name = models.CharField(max_length=100)
    max_score = models.IntegerField(default=10)
    weight = models.DecimalField(max_digits=5, decimal_places=2, default=1.00)  # Weight percentage
    active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.name} (Max: {self.max_score}, Weight: {self.weight}%)"

class Application(models.Model):
    STATUS_CHOICES = [
        ('submitted', 'Submitted'),
        ('in_review', 'In Review'),
        ('decided', 'Decided'),
    ]
    
    applicant = models.ForeignKey(User, on_delete=models.CASCADE, related_name='applications')
    title = models.CharField(max_length=200)
    description = models.TextField()
    amount_requested = models.DecimalField(max_digits=10, decimal_places=2)
    document = models.FileField(upload_to='applications/', null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='submitted')
    final_decision = models.BooleanField(null=True, blank=True)  # True=Approved, False=Rejected, None=Not decided
    submitted_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.title} by {self.applicant.username}"

class Review(models.Model):
    application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name='reviews')
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assigned_reviews')
    completed = models.BooleanField(default=False)
    assigned_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"Review of {self.application.title} by {self.reviewer.username}"

class Score(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='scores')
    rubric = models.ForeignKey(Rubric, on_delete=models.CASCADE)
    score = models.IntegerField()
    comments = models.TextField(blank=True)
    
    def __str__(self):
        return f"Score for {self.rubric.name}: {self.score}"