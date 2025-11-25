from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Placeholder dashboards
    path('applicant/dashboard/', views.applicant_dashboard, name='applicant_dashboard'),
    path('reviewer/dashboard/', views.reviewer_dashboard, name='reviewer_dashboard'),
    path('admin-panel/dashboard/', views.admin_dashboard, name='admin_dashboard'),
]
