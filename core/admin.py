from django.contrib import admin
from .models import UploadedResume, JobRecommendation, AppliedJob

admin.site.register(UploadedResume)
admin.site.register(JobRecommendation)
admin.site.register(AppliedJob)
