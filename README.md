# Grant Application System - Complete Implementation

A Django-based web application for managing grant applications with role-based workflows, blinded reviews, and automated scoring.

## 📋 Table of Contents
- [Features](#features)
- [Quick Start](#quick-start)
- [User Roles](#user-roles)
- [Project Structure](#project-structure)
- [Tech Stack](#tech-stack)
- [How It Works](#how-it-works)
- [Security Features](#security-features)
- [Deployment](#deployment)
- [Screenshots](#screenshots)
- [Contributing](#contributing)
- [License](#license)

## ✨ Features

### Core Functionality
- **Role-based Access Control**: Distinct dashboards and permissions for Applicants, Reviewers, and Admins
- **Blinded Review Process**: Reviewers evaluate applications without knowing applicant identities
- **Automated Scoring**: Real-time score aggregation with variance detection algorithms
- **File Validation**: Secure PDF/DOCX upload with 5MB size restriction
- **State Management**: Complete application lifecycle from submission to final decision
- **Data Export**: CSV export functionality for administrative reporting
- **Responsive UI**: Mobile-first design using Bootstrap 5 framework

### Advanced Features
- **Rubric-based Evaluation**: Customizable scoring criteria with weighted assessments
- **Reviewer Assignment**: Admin-controlled distribution of applications to reviewers
- **Real-time Analytics**: Dashboard statistics and performance metrics
- **Audit Trail**: Comprehensive logging of all system activities
- **Search & Filter**: Advanced filtering capabilities for applications and reviews

  
Image Glimpse:
  <img width="1494" height="865" alt="image" src="https://github.com/user-attachments/assets/e8622cf6-e7df-4204-8352-d656a5cccce7" />

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip package manager
- Virtual environment (recommended)

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd grant_system

# Create virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create default rubrics
python manage.py create_rubrics

# Create a superuser (optional)
python manage.py createsuperuser

# Start development server
python manage.py runserver
```

Visit: **http://localhost:8000/**

## 👥 User Roles

| Role | Description | Key Responsibilities | Dashboard |
|------|-------------|---------------------|-----------|
| **Applicant** | Submit grant applications | Create applications, upload documents, track status | `/applicant/dashboard/` |
| **Reviewer** | Evaluate applications anonymously | Review assigned applications, provide scores and feedback | `/reviewer/dashboard/` |
| **Admin** | Manage system operations | Assign reviewers, manage rubrics, make decisions, export data | `/admin-panel/dashboard/` |

## 📁 Project Structure

```
grant_system/
├── manage.py
├── requirements.txt
├── runtime.txt
├── Procfile
├── render.yaml
├── .env.example
├── build.sh
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

## 💻 Tech Stack

### Backend
- **Framework**: Django 4.2+
- **Database**: SQLite (development), PostgreSQL (production)
- **Authentication**: Django built-in auth system
- **File Handling**: Django FileField with custom validation
- **Task Queue**: None (synchronous processing)

### Frontend
- **Templates**: Django Templates
- **Styling**: Bootstrap 5 (CDN)
- **Icons**: Feather Icons
- **JavaScript**: Vanilla JS for interactivity

### Deployment
- **Platform**: Render.com
- **Web Server**: Gunicorn
- **Static Files**: WhiteNoise
- **Environment Management**: python-decouple

## ⚙️ How It Works

### Application Workflow
1. **Registration**: Users register and select their role (Applicant, Reviewer, or Admin)
2. **Authentication**: Automatic redirection to role-specific dashboard upon login
3. **Submission**: Applicants create and submit grant applications with supporting documents
4. **Assignment**: Admins assign reviewers to applications through the admin panel
5. **Review**: Reviewers evaluate applications using blinded review forms
6. **Scoring**: System automatically calculates aggregate scores and detects scoring variance
7. **Decision**: Admins review scores and make final funding decisions
8. **Export**: Data can be exported to CSV for reporting purposes

### Review Process
- Reviewers cannot see applicant identities (blinded review)
- Each application is evaluated against predefined rubrics
- Scores are automatically aggregated and displayed
- Variance detection alerts admins to significant scoring discrepancies

## 🔒 Security Features

### Access Control
- Role-based permissions prevent unauthorized access to sensitive areas
- Django's built-in authentication system ensures secure user management
- Session management with automatic timeout

### Data Protection
- Blinded review process maintains evaluation fairness and prevents bias
- File type and size validation prevents malicious file uploads
- CSRF protection on all forms to prevent cross-site request forgery
- Secure password hashing using Django's built-in mechanisms

### Network Security
- HTTPS enforcement in production environments
- Security headers to prevent common web vulnerabilities
- Content Security Policy implementation

## ☁️ Deployment

### Local Development
```bash
# Set environment variables (copy .env.example to .env and modify)
cp .env.example .env

# Run with development settings
python manage.py runserver
```

### Production Deployment (Render.com)
1. Fork this repository to your GitHub account
2. Create a new Web Service on Render
3. Connect your forked repository
4. Configure environment variables in Render dashboard:
   - `SECRET_KEY`: Your Django secret key
   - `DEBUG`: False
   - Database credentials (if using external database)
5. Deploy!

The `render.yaml` file automates database provisioning and service configuration.

### Manual Deployment
```bash
# Install production dependencies
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --noinput

# Run migrations
python manage.py migrate

# Start server with Gunicorn
gunicorn grant_system.wsgi:application
```


1. **Home Page** - Welcoming interface with role selection
2. **Applicant Dashboard** - Application management and tracking
3. **Reviewer Dashboard** - Assigned applications for evaluation
4. **Admin Dashboard** - System overview and management tools
5. **Blinded Review Form** - Anonymous evaluation interface
6. **Rubric Management** - Custom scoring criteria configuration

