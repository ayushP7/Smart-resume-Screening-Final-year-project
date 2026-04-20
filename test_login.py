import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'resume_screener.settings')
django.setup()
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.http import QueryDict

# Let's say user tries to login
user = User.objects.last()
print(f"Trying to login as {user.username}")

data = {'username': user.username, 'password': '123'} # Let's assume password is 123
form = AuthenticationForm(data=data)
print(f"Form is valid? {form.is_valid()}")
if not form.is_valid():
    print(f"Errors: {form.errors}")

