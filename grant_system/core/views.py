from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, HttpResponse
from .forms import UserRegistrationForm, ApplicationForm
from .models import User, Application, Review, Score, Rubric
import csv
from django.db.models import Avg
from decimal import Decimal

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

# Applicant Views
@login_required
def applicant_dashboard(request):
    if not request.user.is_applicant():
        return HttpResponseForbidden("Access denied.")
    
    # Get statistics for the applicant
    applications = Application.objects.filter(applicant=request.user)
    total_apps = applications.count()
    submitted_apps = applications.filter(status='submitted').count()
    in_review_apps = applications.filter(status='in_review').count()
    decided_apps = applications.filter(status='decided').count()
    
    context = {
        'applications': applications,
        'total_apps': total_apps,
        'submitted_apps': submitted_apps,
        'in_review_apps': in_review_apps,
        'decided_apps': decided_apps,
    }
    return render(request, 'applicant/dashboard.html', context)

@login_required
def submit_application(request):
    if not request.user.is_applicant():
        return HttpResponseForbidden("Access denied.")
    
    if request.method == 'POST':
        form = ApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.applicant = request.user
            application.save()
            messages.success(request, 'Application submitted successfully!')
            return redirect('applicant_dashboard')
    else:
        form = ApplicationForm()
    
    return render(request, 'applicant/submit_application.html', {'form': form})

@login_required
def view_application(request, app_id):
    if not request.user.is_applicant():
        return HttpResponseForbidden("Access denied.")
    
    application = get_object_or_404(Application, id=app_id, applicant=request.user)
    
    # Get reviews for this application (for displaying feedback if decided)
    reviews = Review.objects.filter(application=application, completed=True)
    
    context = {
        'application': application,
        'reviews': reviews,
    }
    return render(request, 'applicant/view_application.html', context)

# Reviewer Views
@login_required
def reviewer_dashboard(request):
    if not request.user.is_reviewer():
        return HttpResponseForbidden("Access denied.")
    
    # Get statistics for the reviewer
    reviews = Review.objects.filter(reviewer=request.user)
    pending_reviews = reviews.filter(completed=False).count()
    completed_reviews = reviews.filter(completed=True).count()
    
    # Get assigned reviews with application details
    assigned_reviews = reviews.select_related('application')
    
    context = {
        'pending_reviews': pending_reviews,
        'completed_reviews': completed_reviews,
        'assigned_reviews': assigned_reviews,
    }
    return render(request, 'reviewer/dashboard.html', context)

@login_required
def blinded_review(request, review_id):
    if not request.user.is_reviewer():
        return HttpResponseForbidden("Access denied.")
    
    review = get_object_or_404(Review, id=review_id, reviewer=request.user, completed=False)
    application = review.application
    
    # Get active rubrics for scoring
    rubrics = Rubric.objects.filter(active=True)
    
    if request.method == 'POST':
        # Process the review scores
        scores_data = []
        total_score = 0
        
        for rubric in rubrics:
            score_value = request.POST.get(f'score_{rubric.id}')
            comments = request.POST.get(f'comments_{rubric.id}', '')
            
            if score_value:
                try:
                    score_int = int(score_value)
                    # Validate score is within range
                    if 0 <= score_int <= rubric.max_score:
                        scores_data.append({
                            'rubric': rubric,
                            'score': score_int,
                            'comments': comments
                        })
                        total_score += score_int
                except ValueError:
                    pass  # Invalid score, skip
        
        # Save scores if all rubrics have been scored
        if len(scores_data) == len(rubrics):
            # Create Score objects
            for score_data in scores_data:
                Score.objects.create(
                    review=review,
                    rubric=score_data['rubric'],
                    score=score_data['score'],
                    comments=score_data['comments']
                )
            
            # Mark review as completed
            review.completed = True
            review.save()
            
            # Check if all reviews for this application are completed
            all_reviews = Review.objects.filter(application=application)
            if all_reviews.filter(completed=False).count() == 0:
                # All reviews completed, mark application as decided
                application.status = 'decided'
                application.save()
            
            messages.success(request, 'Review submitted successfully!')
            return redirect('reviewer_dashboard')
        else:
            messages.error(request, 'Please provide scores for all criteria.')
    
    context = {
        'review': review,
        'application': application,
        'rubrics': rubrics,
    }
    return render(request, 'reviewer/blinded_review.html', context)

# Admin Views
@login_required
def admin_dashboard(request):
    if not request.user.is_admin_role():
        return HttpResponseForbidden("Access denied.")
    
    # Get statistics
    total_applications = Application.objects.count()
    pending_assignment = Application.objects.filter(status='submitted').count()
    in_review = Application.objects.filter(status='in_review').count()
    decided = Application.objects.filter(status='decided').count()
    
    # Get all applications with applicant info
    applications = Application.objects.select_related('applicant').all()
    
    context = {
        'total_applications': total_applications,
        'pending_assignment': pending_assignment,
        'in_review': in_review,
        'decided': decided,
        'applications': applications,
    }
    return render(request, 'admin_panel/dashboard.html', context)

@login_required
def assign_reviewers(request, app_id):
    if not request.user.is_admin_role():
        return HttpResponseForbidden("Access denied.")
    
    application = get_object_or_404(Application, id=app_id)
    
    # Get all reviewers
    reviewers = User.objects.filter(role='reviewer')
    
    if request.method == 'POST':
        # Get selected reviewers
        selected_reviewer_ids = request.POST.getlist('reviewers')
        selected_reviewers = User.objects.filter(id__in=selected_reviewer_ids, role='reviewer')
        
        # Create Review objects for each selected reviewer
        for reviewer in selected_reviewers:
            Review.objects.get_or_create(
                application=application,
                reviewer=reviewer
            )
        
        # Update application status
        application.status = 'in_review'
        application.save()
        
        messages.success(request, 'Reviewers assigned successfully!')
        return redirect('admin_dashboard')
    
    # Get already assigned reviewers for this application
    assigned_reviewers = Review.objects.filter(application=application).values_list('reviewer_id', flat=True)
    
    context = {
        'application': application,
        'reviewers': reviewers,
        'assigned_reviewers': list(assigned_reviewers),
    }
    return render(request, 'admin_panel/assign_reviewers.html', context)

@login_required
def manage_rubrics(request):
    if not request.user.is_admin_role():
        return HttpResponseForbidden("Access denied.")
    
    rubrics = Rubric.objects.all()
    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'add':
            # Add new rubric
            name = request.POST.get('name')
            max_score = request.POST.get('max_score', 10)
            weight = request.POST.get('weight', 1.00)
            
            if name:
                try:
                    max_score = int(max_score)
                    weight = Decimal(str(weight))  # Convert to Decimal
                    
                    # Validate weight doesn't exceed 100%
                    total_weight = sum(r.weight for r in rubrics if r.active) + weight
                    if total_weight > 100:
                        messages.error(request, f'Total weight cannot exceed 100%. Current total: {total_weight}%')
                    else:
                        Rubric.objects.create(
                            name=name,
                            max_score=max_score,
                            weight=weight
                        )
                        messages.success(request, 'Rubric created successfully!')
                except (ValueError, Exception) as e:
                    messages.error(request, 'Invalid values for max score or weight.')
        
        elif action == 'edit':
            # Edit existing rubric
            rubric_id = request.POST.get('rubric_id')
            name = request.POST.get('name')
            max_score = request.POST.get('max_score')
            weight = request.POST.get('weight')
            active = request.POST.get('active') == 'on'
            
            try:
                rubric = Rubric.objects.get(id=rubric_id)
                max_score = int(max_score)
                weight = Decimal(str(weight))  # Convert to Decimal
                
                # Validate weight doesn't exceed 100%
                total_weight = sum(r.weight for r in rubrics if r.active and r.id != rubric.id)
                if active:
                    total_weight += weight
                
                if total_weight > 100:
                    messages.error(request, f'Total weight cannot exceed 100%. Current total would be: {total_weight}%')
                else:
                    rubric.name = name
                    rubric.max_score = max_score
                    rubric.weight = weight
                    rubric.active = active
                    rubric.save()
                    messages.success(request, 'Rubric updated successfully!')
            except (Rubric.DoesNotExist, ValueError, Exception):
                messages.error(request, 'Invalid rubric or values.')
        
        elif action == 'delete':
            # Delete rubric
            rubric_id = request.POST.get('rubric_id')
            try:
                rubric = Rubric.objects.get(id=rubric_id)
                rubric.delete()
                messages.success(request, 'Rubric deleted successfully!')
            except Rubric.DoesNotExist:
                messages.error(request, 'Rubric not found.')
        
        return redirect('manage_rubrics')
    
    # Calculate total weight
    total_weight = sum(r.weight for r in rubrics if r.active)
    
    context = {
        'rubrics': rubrics,
        'total_weight': total_weight,
    }
    return render(request, 'admin_panel/manage_rubrics.html', context)

@login_required
def manage_users(request):
    if not request.user.is_admin_role():
        return HttpResponseForbidden("Access denied.")
    
    # Get all users
    users = User.objects.all().order_by('role', 'username')
    
    # Count by role
    applicants_count = User.objects.filter(role='applicant').count()
    reviewers_count = User.objects.filter(role='reviewer').count()
    admins_count = User.objects.filter(role='admin').count()
    
    # Find duplicate emails
    from django.db.models import Count
    duplicate_emails = User.objects.values('email').annotate(
        count=Count('email')
    ).filter(count__gt=1)
    
    context = {
        'users': users,
        'applicants_count': applicants_count,
        'reviewers_count': reviewers_count,
        'admins_count': admins_count,
        'duplicate_emails': duplicate_emails,
    }
    return render(request, 'admin_panel/manage_users.html', context)

@login_required
def change_user_role(request, user_id):
    if not request.user.is_admin_role():
        return HttpResponseForbidden("Access denied.")
    
    if request.method == 'POST':
        try:
            user = User.objects.get(id=user_id)
            
            # Prevent changing your own role
            if user.id == request.user.id:
                messages.error(request, 'You cannot change your own role!')
                return redirect('manage_users')
            
            new_role = request.POST.get('new_role')
            if new_role in ['applicant', 'reviewer', 'admin']:
                old_role = user.get_role_display()
                user.role = new_role
                user.save()
                messages.success(request, f'User "{user.username}" role changed from {old_role} to {user.get_role_display()}!')
            else:
                messages.error(request, 'Invalid role selected.')
        except User.DoesNotExist:
            messages.error(request, 'User not found.')
    
    return redirect('manage_users')

@login_required
def delete_user(request, user_id):
    if not request.user.is_admin_role():
        return HttpResponseForbidden("Access denied.")
    
    if request.method == 'POST':
        try:
            user = User.objects.get(id=user_id)
            
            # Prevent deleting yourself
            if user.id == request.user.id:
                messages.error(request, 'You cannot delete your own account!')
                return redirect('manage_users')
            
            username = user.username
            user.delete()
            messages.success(request, f'User "{username}" deleted successfully!')
        except User.DoesNotExist:
            messages.error(request, 'User not found.')
    
    return redirect('manage_users')

# Phase 5: Score Aggregation & Decision Views
@login_required
def view_scores(request, app_id):
    # Check if user is admin
    if not request.user.is_admin_role():
        return HttpResponseForbidden("Access denied.")
    
    # Get the application
    application = get_object_or_404(Application, id=app_id)
    
    # Get all completed reviews for this application
    reviews = Review.objects.filter(application=application, completed=True).select_related('reviewer')
    
    # Calculate scores for each review
    review_scores = []
    for review in reviews:
        scores = Score.objects.filter(review=review).select_related('rubric')
        total_score = 0
        max_possible_score = 0
        
        score_details = []
        for score in scores:
            score_details.append({
                'rubric': score.rubric.name,
                'score': score.score,
                'max_score': score.rubric.max_score,
                'comments': score.comments
            })
            total_score += score.score
            max_possible_score += score.rubric.max_score
            
        # Calculate average score (out of 10)
        average_score = (total_score / max_possible_score * 10) if max_possible_score > 0 else 0
        
        review_scores.append({
            'review': review,
            'scores': score_details,
            'total_score': total_score,
            'max_possible_score': max_possible_score,
            'average_score': round(average_score, 2)
        })
    
    # Calculate overall average
    if review_scores:
        overall_average = sum(r['average_score'] for r in review_scores) / len(review_scores)
        
        # Calculate variance
        if len(review_scores) > 1:
            scores_list = [r['average_score'] for r in review_scores]
            variance = sum((s - overall_average) ** 2 for s in scores_list) / len(scores_list)
        else:
            variance = 0
    else:
        overall_average = 0
        variance = 0
    
    context = {
        'application': application,
        'review_scores': review_scores,
        'overall_average': round(overall_average, 2),
        'variance': round(variance, 2)
    }
    
    return render(request, 'admin_panel/view_scores.html', context)

@login_required
def finalize_decision(request, app_id, decision):
    # Check if user is admin
    if not request.user.is_admin_role():
        return HttpResponseForbidden("Access denied.")
    
    # Get the application
    application = get_object_or_404(Application, id=app_id)
    
    # Update the application with the decision
    if decision == 'approve':
        application.final_decision = True
        application.status = 'decided'
        messages.success(request, f"Application '{application.title}' has been approved.")
    elif decision == 'reject':
        application.final_decision = False
        application.status = 'decided'
        messages.success(request, f"Application '{application.title}' has been rejected.")
    
    application.save()
    
    return redirect('admin_dashboard')

# Phase 6: Export Data
@login_required
def export_applications_csv(request):
    # Check if user is admin
    if not request.user.is_admin_role():
        return HttpResponseForbidden("Access denied.")
    
    # Create the HttpResponse object with CSV header
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="applications_export.csv"'
    
    writer = csv.writer(response)
    
    # Write header row
    writer.writerow(['ID', 'Title', 'Applicant', 'Amount', 'Status', 'Score', 'Decision'])
    
    # Get all applications with their aggregated scores
    applications = Application.objects.all()
    
    for app in applications:
        # Calculate average score for the application
        reviews = Review.objects.filter(application=app, completed=True)
        all_scores = []
        
        for review in reviews:
            scores = Score.objects.filter(review=review)
            if scores.exists():
                avg_score = sum(s.score for s in scores) / len(scores)
                all_scores.append(avg_score)
        
        # Calculate overall average score
        if all_scores:
            overall_avg_score = sum(all_scores) / len(all_scores)
        else:
            overall_avg_score = 0
        
        # Determine decision text
        if app.final_decision is None:
            decision_text = "Pending"
        elif app.final_decision:
            decision_text = "Approved"
        else:
            decision_text = "Rejected"
        
        # Write data row
        writer.writerow([
            app.id,
            app.title,
            app.applicant.email,  # Using email as it's more informative than username
            app.amount_requested,
            app.get_status_display(),  # This will show the human-readable status
            round(overall_avg_score, 2),
            decision_text
        ])
    
    return response