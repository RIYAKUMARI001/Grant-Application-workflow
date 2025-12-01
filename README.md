# Grant Application System - Phase 1

A Django-based web application for managing grant applications with role-based workflows, blinded reviews, and automated scoring.

## Phase 1: Registration & Login ✅

This phase implements user registration and login with role-based access control.

### Features
- User registration with role selection (Applicant, Reviewer, Admin)
- Login with automatic role-based dashboard redirection
- Custom User model with role field
- Bootstrap 5 responsive UI
- Role-based navigation

### Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Start server
python manage.py runserver
```

Visit: **http://localhost:8000/**

### Test Accounts

| Username | Password | Role |
|----------|----------|------|
| test_applicant | testpass123 | Applicant |
| test_reviewer | testpass123 | Reviewer |
| test_admin | testpass123 | Admin |

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
    ├── models.py          # User model with role field
    ├── views.py           # Registration & login logic
    ├── forms.py           # UserRegistrationForm
    ├── urls.py            # URL routing
    ├── admin.py           # Admin configuration
    └── templates/
        ├── base.html
        ├── home.html
        ├── registration/
        │   ├── register.html
        │   └── login.html
        ├── applicant/
        │   └── dashboard.html
        ├── reviewer/
        │   └── dashboard.html
        └── admin_panel/
            └── dashboard.html
```

### How It Works

1. User visits homepage
2. Clicks "Register" and fills form with role selection
3. Django saves user with selected role
4. User is auto-logged in
5. System redirects based on role:
   - Applicant → `/applicant/dashboard/`
   - Reviewer → `/reviewer/dashboard/`
   - Admin → `/admin-panel/dashboard/`

### Tech Stack

- **Backend**: Django 5.0
- **Database**: SQLite
- **Frontend**: Django Templates + Bootstrap 5 (CDN)
- **Authentication**: Django built-in auth system

### Documentation

- **PHASE1_SUMMARY.md** - Complete implementation guide with step-by-step code explanation
- **PHASE1_GUIDE.md** - Detailed testing and usage guide
- **PHASE1_FLOW.txt** - Visual flow diagram

### Next Phases

- **Phase 2**: Applicant Workflow (Application submission)
- **Phase 3**: Admin Workflow (Assign reviewers)
- **Phase 4**: Reviewer Workflow (Blinded review)
- **Phase 5**: Score Aggregation & Decisions
- **Phase 6**: Export Data (CSV)

### Admin Panel

Create a superuser to access Django admin:

```bash
python manage.py createsuperuser
```

Visit: http://localhost:8000/admin/

