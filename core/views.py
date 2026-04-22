from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import UploadedResume, JobRecommendation, AppliedJob
from .forms import UserRegisterForm, ResumeUploadForm, JDMatcherForm
from .utils.parser import parse_resume
from .utils.jd_matcher import match_resume_to_jd
from .utils.job_recommender import recommend_jobs
import json

def home_redirect(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return redirect('login')

def custom_logout_view(request):
    logout(request)
    return redirect('login')

def custom_login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        user_id = request.POST.get('username', '').strip()
        pass_key = request.POST.get('password', '')
        
        # Standard username authentication
        user = authenticate(request, username=user_id, password=pass_key)
        
        # Fallback: Check if they typed an email instead of username
        if user is None and '@' in user_id:
            from django.contrib.auth.models import User
            matching_users = User.objects.filter(email=user_id)
            for u in matching_users:
                user = authenticate(request, username=u.username, password=pass_key)
                if user is not None:
                    break
                
        if user is not None:
            login(request, user)
            # Set a session flag so the dashboard knows they just logged in
            request.session['just_logged_in'] = True
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid username or password.")
            
    return render(request, 'auth/login.html')

def register_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            messages.success(request, "Registration successful! Please log in.")
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'auth/register.html', {'form': form})

@login_required
def dashboard_view(request):
    show_welcome = request.session.pop('just_logged_in', False)
    
    resumes = UploadedResume.objects.filter(user=request.user).order_by('-uploaded_at')
    recommendations = JobRecommendation.objects.filter(user=request.user).order_by('-created_at')
    latest_resume = resumes.first()

    # If we have a resume, let's prepare some data for the premium dashboard
    ats_score = 0
    matched_skills = []
    missing_skills = []
    
    if latest_resume:
        # For the dashboard "Score", we take the average or latest
        # In this project, let's assume a default high-demand skill list for "Missing Skills" comparison
        industry_standard_skills = ["Python", "AWS", "Docker", "Mysql", "Machine Learning", "System Design", "Kubernetes", "Django", "React", "Terraform"]
        user_skills = latest_resume.get_skills_list()
        
        matched_skills = [s for s in user_skills if s.lower() in [i.lower() for i in industry_standard_skills]]
        # If we have very few matches, just show some user skills as "Matched"
        if not matched_skills and user_skills:
            matched_skills = user_skills[:8]
            
        missing_skills = [s for s in industry_standard_skills if s.lower() not in [u.lower() for u in user_skills]][:5]
        
        # Simplified ATS Score for dashboard if not explicitly stored
        ats_score = min(len(user_skills) * 8 + 40, 95) if user_skills else 0

    context = {
        'resumes': resumes,
        'recommendations': recommendations,
        'latest_resume': latest_resume,
        'show_welcome': show_welcome,
        'ats_score': ats_score,
        'matched_skills': matched_skills,
        'missing_skills': missing_skills,
    }
    return render(request, 'dashboard.html', context)

@login_required
def ats_checker_view(request):
    if request.method == 'POST':
        form = ResumeUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = request.FILES['resume']
            
            # Parse Resume
            try:
                parsed_data = parse_resume(uploaded_file, uploaded_file.name)
            except Exception as e:
                messages.error(request, f"Failed to parse resume: {e}")
                return redirect('ats_checker')

            # Save Resume
            skills = parsed_data.get('skills', [])
            resume_obj = UploadedResume.objects.create(
                user=request.user,
                file=uploaded_file,
                parsed_skills=",".join(skills),
                experience_level=parsed_data.get('seniority'),
            )

            # ATS Score is now automatically added by parser.py as parsed_data['ats_score']

            # Recommend Jobs based on Skills (Threshold 70%)
            jobs = recommend_jobs(skills, parsed_data.get('text', ''))
            
            # Save recommended jobs (Saving all 30 for high volume)
            for job in jobs: 
                JobRecommendation.objects.create(
                    user=request.user,
                    resume=resume_obj,
                    job_title=job['title'],
                    company_name=job['company'],
                    job_url=job['url'],
                    match_score=job['score']
                )
            
            return render(request, 'ats_checker_result.html', {
                'parsed_data': parsed_data,
                'jobs': jobs,
                'resume': resume_obj
            })
    else:
        form = ResumeUploadForm()
    return render(request, 'ats_checker.html', {'form': form})

@login_required
def jd_matcher_view(request):
    if request.method == 'POST':
        form = JDMatcherForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = request.FILES['resume']
            jd_text = form.cleaned_data['job_description']

            # Parse Resume
            try:
                parsed_data = parse_resume(uploaded_file, uploaded_file.name)
            except Exception as e:
                messages.error(request, f"Failed to parse resume: {e}")
                return redirect('jd_matcher')

            # JD Match
            match_result = match_resume_to_jd(
                resume_skills=parsed_data.get('skills', []),
                jd_text=jd_text,
                resume_full_text=parsed_data.get('text', '')
            )

            return render(request, 'jd_matcher_result.html', {
                'match_result': match_result,
                'parsed_data': parsed_data
            })
    else:
        form = JDMatcherForm()
    return render(request, 'jd_matcher.html', {'form': form})

@login_required
def apply_job_view(request, job_id):
    try:
        rec = JobRecommendation.objects.get(id=job_id, user=request.user)
        rec.is_applied = True
        rec.save()

        AppliedJob.objects.create(
            user=request.user,
            job_title=rec.job_title,
            company_name=rec.company_name,
            status='Applied'
        )
        messages.success(request, f"Successfully marked as applied for {rec.job_title} at {rec.company_name}")
    except Exception as e:
        messages.error(request, "Error applying for job.")
    
    return redirect('dashboard')
