from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Applicant URLs
    path('applicant/dashboard/', views.applicant_dashboard, name='applicant_dashboard'),
    path('applicant/submit/', views.submit_application, name='submit_application'),
    path('applicant/application/<int:app_id>/', views.view_application, name='view_application'),
    
    # Reviewer URLs
    path('reviewer/dashboard/', views.reviewer_dashboard, name='reviewer_dashboard'),
    path('reviewer/review/<int:review_id>/', views.blinded_review, name='blinded_review'),
    
    # Admin URLs
    path('admin-panel/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-panel/assign/<int:app_id>/', views.assign_reviewers, name='assign_reviewers'),
    path('admin-panel/rubrics/', views.manage_rubrics, name='manage_rubrics'),
    path('admin-panel/users/', views.manage_users, name='manage_users'),
    path('admin-panel/users/change-role/<int:user_id>/', views.change_user_role, name='change_user_role'),
    path('admin-panel/users/delete/<int:user_id>/', views.delete_user, name='delete_user'),
    
    # Phase 5: Score Aggregation & Decision URLs
    path('admin-panel/scores/<int:app_id>/', views.view_scores, name='view_scores'),
    path('admin-panel/finalize/<int:app_id>/<str:decision>/', views.finalize_decision, name='finalize_decision'),
    
    # Phase 6: Export Data
    path('admin-panel/export/csv/', views.export_applications_csv, name='export_applications_csv'),
]