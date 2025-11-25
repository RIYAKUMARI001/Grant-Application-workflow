# Phase 1 Implementation Summary

## ✅ COMPLETED: Registration & Login System

Phase 1 implements a complete user authentication system with role-based access control. Users can register, select their role (Applicant/Reviewer/Admin), and are automatically redirected to their appropriate dashboard.

---

## 🚀 Quick Start

```bash
cd grant_system
pip install -r requirements.txt
python manage.py runserver
```

Visit: **http://localhost:8000/**

### Test Accounts
- `test_applicant` / `testpass123` → Applicant Dashboard
- `test_reviewer` / `testpass123` → Reviewer Dashboard  
- `test_admin` / `testpass123` → Admin Dashboard

---

## 📚 Complete Implementation Guide - Step by Step

### Step 1: Django Project Setup

**What is Django?**
Django is a Python web framework used to build web applications. It has three main components:
- **Models** - Define database structure
- **Views** - Handle logic and data processing
- **Templates** - HTML pages shown to users

**Project Structure:**
```
grant_system/
├── manage.py              # Django ka main command-line tool
├── grant_system/          # Project settings folder
│   ├── settings.py        # Configuration file
│   ├── urls.py            # Main URL routing
│   └── wsgi.py            # Server deployment file
└── core/                  # Main application folder
    ├── models.py          # Database models
    ├── views.py           # Business logic
    ├── forms.py           # Form handling
    ├── urls.py            # App-specific URLs
    └── templates/         # HTML files
```

---

### Step 2: Custom User Model (models.py)

**What we did:**
Extended Django's default User model to create a custom User model with an added `role` field.

**Code:**
```python
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
```

**Explanation:**
1. `AbstractUser` - Django's built-in User model that provides username, password, email
2. `ROLE_CHOICES` - Defined options for dropdown (Applicant, Reviewer, Admin)
3. `role` field - CharField that stores the user's role
4. Helper methods - `is_applicant()`, `is_reviewer()`, `is_admin_role()` - To check user role

**Configured in settings.py:**
```python
AUTH_USER_MODEL = 'core.User'  # Tells Django to use our custom User model
```

---

### Step 3: Registration Form (forms.py)

**What we did:**
Extended Django's `UserCreationForm` to create a registration form with an added role selection dropdown.

**Code:**
```python
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    role = forms.ChoiceField(
        choices=User.ROLE_CHOICES,
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'role']
```

**Explanation:**
1. `UserCreationForm` - Django's built-in form that provides username and password fields
2. `email` field - Added extra email field
3. `role` field - Dropdown field that gets options from ROLE_CHOICES
4. `Meta` class - Links form to User model and specifies fields
5. `widget` - Added Bootstrap CSS class for styling

---

### Step 4: Views - Registration & Login Logic (views.py)

**What we did:**
Created registration and login views that handle role-based redirection.

#### A) Registration View

**Code:**
```python
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from .forms import UserRegistrationForm

def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()              # User ko database mein save kiya
            login(request, user)            # User ko automatically login kiya
            messages.success(request, f'Welcome {user.username}!')
            
            # Role-based redirect - MOST IMPORTANT PART
            if user.is_applicant():
                return redirect('applicant_dashboard')
            elif user.is_reviewer():
                return redirect('reviewer_dashboard')
            elif user.is_admin_role():
                return redirect('admin_dashboard')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'registration/register.html', {'form': form})
```

**Explanation:**
1. `request.method == 'POST'` - Checks if form was submitted
2. `form.is_valid()` - Form validation (password match, email format, etc.)
3. `form.save()` - Saves user to database
4. `login(request, user)` - Automatically logs in user (creates session)
5. **Role-based redirect** - Redirects to different dashboard based on user's role
6. `messages.success()` - Displays success message

#### B) Login View

**Code:**
```python
from django.contrib.auth.views import LoginView

class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    
    def get_success_url(self):
        user = self.request.user
        if user.is_applicant():
            return '/applicant/dashboard/'
        elif user.is_reviewer():
            return '/reviewer/dashboard/'
        elif user.is_admin_role():
            return '/admin-panel/dashboard/'
        return '/'
```

**Explanation:**
1. `LoginView` - Extended Django's built-in login view
2. `get_success_url()` - Determines where to redirect after successful login
3. Same role-based logic as registration

#### C) Dashboard Views (Placeholders)

**Code:**
```python
def applicant_dashboard(request):
    return render(request, 'applicant/dashboard.html')

def reviewer_dashboard(request):
    return render(request, 'reviewer/dashboard.html')

def admin_dashboard(request):
    return render(request, 'admin_panel/dashboard.html')
```

**Explanation:**
These are just placeholder views for now. We'll implement them in Phases 2, 3, and 4.

---

### Step 5: URL Routing (urls.py)

**What we did:**
Connected URLs to views.

**Code:**
```python
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Dashboards
    path('applicant/dashboard/', views.applicant_dashboard, name='applicant_dashboard'),
    path('reviewer/dashboard/', views.reviewer_dashboard, name='reviewer_dashboard'),
    path('admin-panel/dashboard/', views.admin_dashboard, name='admin_dashboard'),
]
```

**Explanation:**
1. `path()` - Defines URL pattern
2. First argument - URL path (e.g., 'register/')
3. Second argument - View function
4. `name` - Used in templates (e.g., `{% url 'register' %}`)

---

### Step 6: Django Templates - HTML Pages

**What we did:**
Created responsive HTML templates using Bootstrap 5.

#### A) Base Template (base.html)

**Code:**
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{% block title %}Grant System{% endblock %}</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
    <nav class="navbar navbar-dark bg-dark">
        <div class="container">
            <a class="navbar-brand" href="{% url 'home' %}">Grant System</a>
            {% if user.is_authenticated %}
                <span class="text-white">{{ user.username }} ({{ user.get_role_display }})</span>
                <a href="{% url 'logout' %}" class="btn btn-outline-light">Logout</a>
            {% endif %}
        </div>
    </nav>

    <div class="container mt-4">
        {% if messages %}
            {% for message in messages %}
                <div class="alert alert-{{ message.tags }}">{{ message }}</div>
            {% endfor %}
        {% endif %}

        {% block content %}
        {% endblock %}
    </div>
</body>
</html>
```

**Explanation:**
1. **Bootstrap CDN** - CSS framework for styling (no installation needed)
2. `{% block title %}` - Child templates can change the title
3. `{% if user.is_authenticated %}` - Checks if user is logged in
4. `{{ user.username }}` - Displays logged in user's name
5. `{{ user.get_role_display }}` - Displays role (Applicant/Reviewer/Admin)
6. `{% block content %}` - Child templates insert their content here

#### B) Registration Template (register.html)

**Code:**
```html
{% extends 'base.html' %}

{% block content %}
<div class="row justify-content-center mt-5">
    <div class="col-md-6">
        <div class="card">
            <div class="card-header bg-primary text-white">
                <h4>Register New Account</h4>
            </div>
            <div class="card-body">
                <form method="post">
                    {% csrf_token %}
                    
                    <div class="mb-3">
                        <label>Username</label>
                        {{ form.username }}
                    </div>

                    <div class="mb-3">
                        <label>Email</label>
                        {{ form.email }}
                    </div>

                    <div class="mb-3">
                        <label>Password</label>
                        {{ form.password1 }}
                    </div>

                    <div class="mb-3">
                        <label>Confirm Password</label>
                        {{ form.password2 }}
                    </div>

                    <div class="mb-3">
                        <label><strong>Select Role</strong></label>
                        {{ form.role }}
                        <small>Choose: Applicant, Reviewer, or Admin</small>
                    </div>

                    <button type="submit" class="btn btn-primary">Register</button>
                </form>
            </div>
        </div>
    </div>
</div>
{% endblock %}
```

**Explanation:**
1. `{% extends 'base.html' %}` - Inherits from base template
2. `{% csrf_token %}` - Security token (Django requirement for forms)
3. `{{ form.username }}` - Renders form field
4. `{{ form.role }}` - **MOST IMPORTANT** - Renders role dropdown
5. Bootstrap classes (`card`, `mb-3`, `btn-primary`) - For styling

#### C) Login Template (login.html)

Similar structure, only has username and password fields.

---

### Step 7: Database Migrations

**What we did:**
Created the custom User model in the database.

**Commands:**
```bash
python manage.py makemigrations  # Migration file create kiya
python manage.py migrate         # Database mein tables create kiye
```

**Explanation:**
1. `makemigrations` - Looks at models and creates migration file
2. `migrate` - Executes migration file to create database tables
3. Result: `User` table created with `role` field

---

### Step 8: Admin Panel Configuration (admin.py)

**What we did:**
Registered custom User model in Django admin panel.

**Code:**
```python
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'role', 'is_staff']
    list_filter = ['role', 'is_staff']
    fieldsets = UserAdmin.fieldsets + (
        ('Role Information', {'fields': ('role',)}),
    )
```

**Explanation:**
Can manage users in admin panel and the role field will be visible.

---

## 🔄 Complete Flow Diagram

```
User visits homepage
    ↓
Clicks "Register"
    ↓
Fills form:
  - Username: john
  - Email: john@test.com
  - Password: pass123
  - Role: Applicant ← DROPDOWN
    ↓
Submits form
    ↓
Django View (register_view):
  1. Validates form
  2. Saves user to database
  3. Auto-login user
  4. Checks user.role
  5. IF role == 'applicant' → redirect('/applicant/dashboard/')
    ↓
Applicant Dashboard displays
  - Shows: "Welcome john! You are logged in as Applicant"
```

---

## 🎯 Key Technologies Used

### 1. Django Framework
- **Models** - Database structure (User model with role field)
- **Views** - Business logic (registration, login, redirection)
- **Templates** - HTML pages (registration form, dashboards)
- **Forms** - Form handling (UserRegistrationForm)
- **Authentication** - Built-in login/logout system

### 2. Bootstrap 5
- **CDN** - No installation needed, loaded from internet
- **Components** - Cards, buttons, forms, navbar
- **Grid System** - Responsive layout (col-md-6, container)
- **Utilities** - Spacing (mt-4, mb-3), colors (bg-primary)

### 3. SQLite Database
- **Default Django database** - No setup needed
- **User table** - Stores username, email, password (hashed), role
- **Automatic** - Django ORM handles all SQL queries

---

## ✅ Success Checklist

- ✅ Custom User model with role field
- ✅ Registration form with role dropdown
- ✅ Role-based redirection after registration
- ✅ Role-based redirection after login
- ✅ Bootstrap 5 UI
- ✅ Navbar shows username and role
- ✅ Logout functionality
- ✅ Three placeholder dashboards
- ✅ Database migrations completed
- ✅ Test users created

---

## 📊 Technical Summary

| Component | Technology | Purpose |
|-----------|-----------|---------|
| Backend Framework | Django 5.0 | Web application structure |
| Database | SQLite | User data storage |
| Frontend | Django Templates + Bootstrap 5 | HTML pages with styling |
| Authentication | Django Auth System | Login/logout/sessions |
| Forms | Django Forms | Form validation & handling |
| Styling | Bootstrap 5 CDN | Responsive UI |

---

**Status**: ✅ Phase 1 Complete  
**Next**: Phase 2 - Applicant Workflow (Application submission)
