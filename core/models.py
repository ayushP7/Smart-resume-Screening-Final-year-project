from django.db import models
from django.contrib.auth.models import User


class UploadedResume(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='resumes')
    file = models.FileField(upload_to='resumes/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    parsed_skills = models.TextField(blank=True, null=True, help_text="JSON or comma separated skills parsed from resume")
    education_level = models.IntegerField(default=0)
    experience_level = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - Resume {self.id}"

    def get_skills_list(self):
        if not self.parsed_skills:
            return []
        return [skill.strip() for skill in self.parsed_skills.split(',') if skill.strip()]

class JobRecommendation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recommendations')
    resume = models.ForeignKey(UploadedResume, on_delete=models.CASCADE, null=True, blank=True)
    job_title = models.CharField(max_length=255)
    company_name = models.CharField(max_length=255)
    job_url = models.URLField(max_length=1000)
    match_score = models.FloatField(help_text="ATS Match Score (0-100)")
    created_at = models.DateTimeField(auto_now_add=True)
    is_applied = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.job_title} at {self.company_name} ({self.match_score}%)"

class AppliedJob(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='applied_jobs')
    job_title = models.CharField(max_length=255)
    company_name = models.CharField(max_length=255)
    applied_on = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, default='Applied')

    def __str__(self):
        return f"{self.user.username} applied for {self.job_title}"
