from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.contrib import messages
from .forms import UserRegistrationForm

def home(request):
    if request.user.is_authenticated:
        # Redirect based on role
        if request.user.is_applicant():
            return redirect('applicant_dashboard')
        elif request.user.is_reviewer():
            return redirect('reviewer_dashboard')
        elif request.user.is_admin_role():
            return redirect('admin_dashboard')
    return render(request, 'home.html')

def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Welcome {user.username}! Registration successful.')
            
            # Role-based redirect
            if user.is_applicant():
                return redirect('applicant_dashboard')
            elif user.is_reviewer():
                return redirect('reviewer_dashboard')
            elif user.is_admin_role():
                return redirect('admin_dashboard')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'registration/register.html', {'form': form})

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

def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('home')

# Placeholder dashboards for Phase 1
def applicant_dashboard(request):
    return render(request, 'applicant/dashboard.html')

def reviewer_dashboard(request):
    return render(request, 'reviewer/dashboard.html')

def admin_dashboard(request):
    return render(request, 'admin_panel/dashboard.html')
