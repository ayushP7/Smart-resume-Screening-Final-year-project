import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'resume_screener.settings')
django.setup()
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
user = User.objects.last()
print(f'Latest User: {user.username}')
print(f'Hashed Pwd: {user.password}')
