# Phase 1 Implementation Guide

## ✅ COMPLETED: Registration & Login with Role-Based Redirection

### What's Implemented

Phase 1 implements the complete user registration and login system with automatic role-based dashboard redirection.

### Key Features

1. **Custom User Model** with role field (Applicant, Reviewer, Admin)
2. **Registration Form** with role selection dropdown
3. **Login System** with automatic role-based redirection
4. **Role-Based Dashboards** (placeholder for future phases)
5. **Bootstrap 5 UI** with responsive design

### How to Run

```bash
# Navigate to project directory
cd grant_system

# Install dependencies (if not already installed)
pip install -r requirements.txt

# Run migrations (already done)
python manage.py makemigrations
python manage.py migrate

# Start development server
python manage.py runserver
```

### Access the Application

- **Homepage**: http://localhost:8000/
- **Register**: http://localhost:8000/register/
- **Login**: http://localhost:8000/login/

### Test Credentials

Three test users have been created:

| Username | Password | Role |
|----------|----------|------|
| test_applicant | testpass123 | Applicant |
| test_reviewer | testpass123 | Reviewer |
| test_admin | testpass123 | Admin |

### Testing the Flow

#### Test 1: Registration Flow

1. Visit http://localhost:8000/
2. Click "Register" button
3. Fill the form:
   - Username: `john_applicant`
   - Email: `john@test.com`
   - Password: `securepass123`
   - Confirm Password: `securepass123`
   - **Role**: Select "Applicant"
4. Click "Register"
5. **Expected**: Redirected to `/applicant/dashboard/`
6. **Verify**: Green success message appears
7. **Verify**: Navbar shows "john_applicant (Applicant)"

#### Test 2: Role-Based Redirection

**Test Applicant:**
1. Logout
2. Register new user with role "Applicant"
3. **Expected**: Redirected to `/applicant/dashboard/`

**Test Reviewer:**
1. Logout
2. Register new user with role "Reviewer"
3. **Expected**: Redirected to `/reviewer/dashboard/`

**Test Admin:**
1. Logout
2. Register new user with role "Admin"
3. **Expected**: Redirected to `/admin-panel/dashboard/`

#### Test 3: Login Flow

1. Logout
2. Click "Login"
3. Enter credentials: `test_applicant` / `testpass123`
4. Click "Login"
5. **Expected**: Redirected to `/applicant/dashboard/`

### Architecture Overview

#### User Model (`core/models.py`)

```python
class User(AbstractUser):
    ROLE_CHOICES = [
        ('applicant', 'Applicant'),
        ('reviewer', 'Reviewer'),
        ('admin', 'Admin'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
```

#### Registration View (`core/views.py`)

```python
def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            
            # Role-based redirect
            if user.is_applicant():
                return redirect('applicant_dashboard')
            elif user.is_reviewer():
                return redirect('reviewer_dashboard')
            elif user.is_admin_role():
                return redirect('admin_dashboard')
```

#### Login View (`core/views.py`)

```python
class CustomLoginView(LoginView):
    def get_success_url(self):
        user = self.request.user
        if user.is_applicant():
            return '/applicant/dashboard/'
        elif user.is_reviewer():
            return '/reviewer/dashboard/'
        elif user.is_admin_role():
            return '/admin-panel/dashboard/'
```

### URL Routing

```python
urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Role-based dashboards
    path('applicant/dashboard/', views.applicant_dashboard, name='applicant_dashboard'),
    path('reviewer/dashboard/', views.reviewer_dashboard, name='reviewer_dashboard'),
    path('admin-panel/dashboard/', views.admin_dashboard, name='admin_dashboard'),
]
```

### Database Schema

**User Table:**
- id (Primary Key)
- username (Unique)
- email
- password (Hashed)
- **role** (applicant/reviewer/admin)
- first_name
- last_name
- is_staff
- is_active
- date_joined

### File Structure

```
grant_system/
├── manage.py
├── requirements.txt
├── README.md
├── PHASE1_GUIDE.md
├── test_phase1.py
├── db.sqlite3 (created after migrations)
│
├── grant_system/
│   ├── __init__.py
│   ├── settings.py (AUTH_USER_MODEL = 'core.User')
│   ├── urls.py
│   └── wsgi.py
│
└── core/
    ├── __init__.py
    ├── models.py (User model)
    ├── views.py (Registration, Login, Dashboards)
    ├── forms.py (UserRegistrationForm)
    ├── urls.py
    ├── admin.py (Custom User Admin)
    ├── migrations/
    │   ├── __init__.py
    │   └── 0001_initial.py
    └── templates/
        ├── base.html (Master template with navbar)
        ├── home.html (Landing page)
        ├── registration/
        │   ├── register.html (Registration form)
        │   └── login.html (Login form)
        ├── applicant/
        │   └── dashboard.html (Placeholder)
        ├── reviewer/
        │   └── dashboard.html (Placeholder)
        └── admin_panel/
            └── dashboard.html (Placeholder)
```

### Key Implementation Details

#### 1. Role Selection Dropdown

The registration form includes a dropdown with three role options:

```html
<select name="role" class="form-control">
    <option value="applicant">Applicant</option>
    <option value="reviewer">Reviewer</option>
    <option value="admin">Admin</option>
</select>
```

#### 2. Automatic Login After Registration

After successful registration, the user is automatically logged in:

```python
user = form.save()
login(request, user)  # Auto-login
```

#### 3. Role-Based Redirection Logic

Both registration and login use the same redirection logic:

```python
if user.is_applicant():
    return redirect('applicant_dashboard')
elif user.is_reviewer():
    return redirect('reviewer_dashboard')
elif user.is_admin_role():
    return redirect('admin_dashboard')
```

#### 4. Bootstrap 5 Integration

All templates use Bootstrap 5 via CDN (no installation needed):

```html
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
```

### Security Features

1. **Password Hashing**: Django's built-in password hashing
2. **CSRF Protection**: `{% csrf_token %}` in all forms
3. **Password Validation**: Minimum 8 characters, complexity checks
4. **Session Management**: Django's secure session handling

### What's NOT in Phase 1

Phase 1 is intentionally minimal and focused only on authentication:

- ❌ No application submission (Phase 2)
- ❌ No reviewer assignment (Phase 3)
- ❌ No blinded review (Phase 4)
- ❌ No scoring system (Phase 5)
- ❌ No CSV export (Phase 6)

The dashboards are placeholders that will be implemented in future phases.

### Troubleshooting

**Issue: "No module named 'django'"**
```bash
pip install Django==5.0
```

**Issue: "Table doesn't exist"**
```bash
python manage.py migrate
```

**Issue: "Port already in use"**
```bash
# Use different port
python manage.py runserver 8001
```

**Issue: "CSRF verification failed"**
- Make sure `{% csrf_token %}` is in all forms
- Check that CSRF middleware is enabled in settings.py

### Next Steps

Phase 1 is complete! You can now:

1. ✅ Register users with different roles
2. ✅ Login and see role-based redirection
3. ✅ View placeholder dashboards

**Ready for Phase 2?** Phase 2 will implement the Applicant workflow:
- Application submission form
- File upload (PDF/DOCX)
- Application listing
- Status tracking

### Admin Panel Access

To access Django's built-in admin panel:

```bash
# Create superuser
python manage.py createsuperuser

# Visit http://localhost:8000/admin/
```

You can manage users, view roles, and perform admin tasks.

### Success Criteria

Phase 1 is successful if:

- ✅ Users can register with role selection
- ✅ Registration redirects to correct dashboard based on role
- ✅ Login redirects to correct dashboard based on role
- ✅ Navbar shows username and role
- ✅ Logout works correctly
- ✅ No errors in console
- ✅ Database has User table with role field

### Demo Video Script

1. Show homepage with Register/Login buttons
2. Click Register
3. Fill form and select "Applicant" role
4. Submit and show redirect to Applicant Dashboard
5. Logout
6. Login with test_reviewer credentials
7. Show redirect to Reviewer Dashboard
8. Logout
9. Login with test_admin credentials
10. Show redirect to Admin Dashboard

---

**Phase 1 Status**: ✅ COMPLETE

**Author**: Kiro AI Assistant  
**Date**: November 26, 2025
