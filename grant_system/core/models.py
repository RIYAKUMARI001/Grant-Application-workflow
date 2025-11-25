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
