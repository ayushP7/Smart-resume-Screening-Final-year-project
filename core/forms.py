from django import forms
from django.contrib.auth.models import User

class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("Passwords do not match!")
        return cleaned_data

class ResumeUploadForm(forms.Form):
    resume = forms.FileField(label="Upload Resume (PDF/DOCX)", widget=forms.FileInput(attrs={'accept': '.pdf,.docx'}))

class JDMatcherForm(forms.Form):
    resume = forms.FileField(label="Resume", widget=forms.FileInput(attrs={'accept': '.pdf,.docx'}))
    job_description = forms.CharField(widget=forms.Textarea(attrs={'rows': 5, 'placeholder': 'Paste Job Description here...'}), required=True)
