import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'resume_screener.settings')
django.setup()

from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from core.forms import UserRegisterForm

print('Testing registration flow...')
# Create post data
post_data = {'username': 'test_auth_user', 'email': 'test@test.com', 'password': 'TestPassword123!', 'password_confirm': 'TestPassword123!'}
form = UserRegisterForm(data=post_data)

if form.is_valid():
    user = form.save(commit=False)
    user.set_password(form.cleaned_data['password'])
    user.save()
    print('User registered.')
    
    # Try to authenticate
    auth_user = authenticate(username='test_auth_user', password='TestPassword123!')
    if auth_user:
        print('Login SUCCESS!')
    else:
        print('Login FAILED!')
else:
    print('Form errors:', form.errors)

