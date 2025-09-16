from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile, Connection, Message, Forum, ForumReply, Job, JobApplication, Mentorship, Event, Announcement, PasswordResetToken


class UserRegistrationForm(UserCreationForm):
    """User registration form with additional fields"""
    email = forms.EmailField(required=True)
    full_name = forms.CharField(max_length=100, required=True)
    
    class Meta:
        model = User
        fields = ('username', 'email', 'full_name', 'password1', 'password2')
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class ProfileForm(forms.ModelForm):
    """Profile edit form"""
    class Meta:
        model = Profile
        fields = [
            'full_name', 'phone_number', 'bio', 'profile_picture',
            'user_type', 'major', 'course', 'graduation_year', 'skills', 'location'
        ]
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4}),
            'skills': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Enter skills separated by commas'}),
            'user_type': forms.Select(attrs={'class': 'form-control'}),
        }


class MessageForm(forms.ModelForm):
    """Message form"""
    class Meta:
        model = Message
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Type your message...'}),
        }


class ForumForm(forms.ModelForm):
    """Forum post form"""
    class Meta:
        model = Forum
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Enter a descriptive title'}),
            'content': forms.Textarea(attrs={'rows': 6, 'placeholder': 'Share your thoughts...'}),
        }


class ForumReplyForm(forms.ModelForm):
    """Forum reply form"""
    class Meta:
        model = ForumReply
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Write your reply...'}),
        }


class JobForm(forms.ModelForm):
    """Job posting form"""
    class Meta:
        model = Job
        fields = [
            'title', 'description', 'company', 'location', 
            'job_type', 'deadline'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Job title'}),
            'description': forms.Textarea(attrs={'rows': 6, 'placeholder': 'Job description and requirements'}),
            'company': forms.TextInput(attrs={'placeholder': 'Company name'}),
            'location': forms.TextInput(attrs={'placeholder': 'Job location'}),
            'deadline': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }


class EventForm(forms.ModelForm):
    """Event creation form"""
    class Meta:
        model = Event
        fields = ['title', 'description', 'event_date', 'location']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Event title'}),
            'description': forms.Textarea(attrs={'rows': 6, 'placeholder': 'Event description'}),
            'event_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'location': forms.TextInput(attrs={'placeholder': 'Event location'}),
        }


class ConnectionForm(forms.ModelForm):
    """Connection request form"""
    class Meta:
        model = Connection
        fields = ['receiver']
        widgets = {
            'receiver': forms.Select(attrs={'class': 'form-control'}),
        }


class MentorshipForm(forms.ModelForm):
    """Mentorship request form"""
    class Meta:
        model = Mentorship
        fields = ['mentee']
        widgets = {
            'mentee': forms.Select(attrs={'class': 'form-control'}),
        }


class AnnouncementForm(forms.ModelForm):
    """Announcement form"""
    class Meta:
        model = Announcement
        fields = ['title', 'content', 'announcement_type']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Announcement title'}),
            'content': forms.Textarea(attrs={'rows': 6, 'placeholder': 'Announcement content'}),
            'announcement_type': forms.Select(attrs={'class': 'form-control'}),
        }


class ForgotPasswordForm(forms.Form):
    """Forgot password form"""
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'placeholder': 'Enter your email address'})
    )


class ResetPasswordForm(forms.Form):
    """Reset password form"""
    password = forms.CharField(
        min_length=6,
        widget=forms.PasswordInput(attrs={'placeholder': 'New password'}),
        help_text="Password must be at least 6 characters long"
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm new password'})
    )
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        
        if password and confirm_password:
            if password != confirm_password:
                raise forms.ValidationError("Passwords don't match")
        
        return cleaned_data


class JobApplicationForm(forms.ModelForm):
    """Job application form"""
    class Meta:
        model = JobApplication
        fields = ['cover_letter']
        widgets = {
            'cover_letter': forms.Textarea(attrs={
                'rows': 6, 
                'placeholder': 'Write a cover letter explaining why you\'re interested in this position...',
                'class': 'form-control'
            }),
        }


