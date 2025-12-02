# Grant Application System - Complete Implementation

A Django-based web application for managing grant applications with role-based workflows, blinded reviews, and automated scoring.

## ✅ Complete Implementation

This project implements a full grant application system with:

### Features
- **Role-based Access Control**: Applicant, Reviewer, Admin roles
- **Blinded Review Process**: Reviewers cannot see applicant identities
- **Automated Scoring**: Real-time score aggregation and variance detection
- **File Validation**: PDF/DOCX only, 5MB size limit
- **State Management**: Application lifecycle from submission to decision
- **Data Export**: CSV export functionality for administrators
- **Responsive UI**: Bootstrap 5 responsive design

### Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create default rubrics
python manage.py create_rubrics

# Start server
python manage.py runserver
```

Visit: **http://localhost:8000/**

### User Roles

| Role | Description | Dashboard |
|------|-------------|-----------|
| Applicant | Submit grant applications | `/applicant/dashboard/` |
| Reviewer | Review applications anonymously | `/reviewer/dashboard/` |
| Admin | Manage system, assign reviewers, make decisions | `/admin-panel/dashboard/` |

### Project Structure

```
grant_system/
├── manage.py
├── requirements.txt
├── grant_system/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── core/
    ├── models.py          # All data models
    ├── views.py           # All view logic
    ├── forms.py           # Form validation
    ├── urls.py            # URL routing
    ├── admin.py           # Admin configuration
    ├── management/
    │   └── commands/
    │       └── create_rubrics.py  # Default rubric creation
    └── templates/
        ├── base.html
        ├── home.html
        ├── registration/
        │   ├── register.html
        │   └── login.html
        ├── applicant/
        │   ├── dashboard.html
        │   ├── submit_application.html
        │   └── view_application.html
        ├── reviewer/
        │   ├── dashboard.html
        │   └── blinded_review.html
        └── admin_panel/
            ├── dashboard.html
            ├── assign_reviewers.html
            ├── manage_rubrics.html
            └── view_scores.html
```

### Tech Stack

- **Backend**: Django 5.0
- **Database**: SQLite
- **Frontend**: Django Templates + Bootstrap 5 (CDN)
- **Authentication**: Django built-in auth system
- **File Handling**: Django FileField with custom validation

### How It Works

1. **Registration**: Users register and select their role
2. **Login**: Automatic redirection to role-specific dashboard
3. **Workflow**:
   - Applicants submit applications with documents
   - Admins assign reviewers to applications
   - Reviewers evaluate applications blindly
   - System automatically calculates scores and variance
   - Admins make final decisions and export data

### Security Features

- Role-based access control prevents unauthorized access
- Blinded review process maintains evaluation fairness
- File type and size validation prevents malicious uploads
- CSRF protection on all forms
- Secure password hashing

### Admin Panel

Create a superuser to access Django admin:

```bash
python manage.py createsuperuser
```

Visit: http://localhost:8000/admin/

---

**Status**: ✅ Complete Implementation  
**Author**: [Your Name]