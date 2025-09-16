from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Profile(models.Model):
    """Extended user profile with academic and professional information"""
    USER_TYPE_CHOICES = [
        ('student', 'Student'),
        ('alumni', 'Alumni'),
        ('mentor', 'Mentor'),
        ('faculty', 'Faculty'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    full_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20, blank=True)
    bio = models.TextField(blank=True)
    # profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='student')
    major = models.CharField(max_length=100, blank=True)
    course = models.CharField(max_length=100, blank=True)
    graduation_year = models.IntegerField(blank=True, null=True)
    skills = models.TextField(blank=True, help_text="Comma-separated list of skills")
    location = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.full_name} ({self.user.username})"

    def get_skills_list(self):
        """Return skills as a list"""
        if self.skills:
            return [skill.strip() for skill in self.skills.split(',')]
        return []


class Connection(models.Model):
    """Friend/connection system between users"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('blocked', 'Blocked'),
    ]
    
    requester = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_connections')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_connections')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['requester', 'receiver']

    def __str__(self):
        return f"{self.requester.username} -> {self.receiver.username} ({self.status})"


class Message(models.Model):
    """Direct messaging between users"""
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.sender.username} -> {self.receiver.username}: {self.content[:50]}..."


class Forum(models.Model):
    """Discussion forums"""
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='forum_posts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def get_reply_count(self):
        return self.replies.count()


class ForumReply(models.Model):
    """Replies to forum posts"""
    forum = models.ForeignKey(Forum, on_delete=models.CASCADE, related_name='replies')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='forum_replies')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"Reply by {self.user.username} on {self.forum.title}"


class Job(models.Model):
    """Job postings"""
    JOB_TYPE_CHOICES = [
        ('full-time', 'Full Time'),
        ('part-time', 'Part Time'),
        ('internship', 'Internship'),
        ('contract', 'Contract'),
        ('freelance', 'Freelance'),
    ]

    posted_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posted_jobs')
    title = models.CharField(max_length=200)
    description = models.TextField()
    company = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    job_type = models.CharField(max_length=20, choices=JOB_TYPE_CHOICES)
    deadline = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} at {self.company}"

    def is_deadline_passed(self):
        return timezone.now() > self.deadline
    
    def get_application_count(self):
        """Return the number of applications for this job"""
        return self.applications.count()


class JobApplication(models.Model):
    """Job applications"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('reviewed', 'Reviewed'),
        ('shortlisted', 'Shortlisted'),
        ('rejected', 'Rejected'),
        ('hired', 'Hired'),
    ]

    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')
    applicant = models.ForeignKey(User, on_delete=models.CASCADE, related_name='job_applications')
    cover_letter = models.TextField(blank=True, help_text="Optional cover letter")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    applied_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['job', 'applicant']  # Prevent duplicate applications
        ordering = ['-applied_at']

    def __str__(self):
        return f"{self.applicant.username} applied for {self.job.title}"


class Mentorship(models.Model):
    """Mentor-mentee relationships"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    mentor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mentor_relationships')
    mentee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mentee_relationships')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    started_at = models.DateTimeField(blank=True, null=True)
    ended_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['mentor', 'mentee']

    def __str__(self):
        return f"{self.mentor.username} mentors {self.mentee.username} ({self.status})"


class Event(models.Model):
    """Events and meetups"""
    title = models.CharField(max_length=200)
    description = models.TextField()
    event_date = models.DateTimeField()
    location = models.CharField(max_length=200)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_events')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['event_date']

    def __str__(self):
        return self.title

    def get_participant_count(self):
        return self.participants.count()

    def is_past_event(self):
        return timezone.now() > self.event_date


class EventParticipant(models.Model):
    """Event participants"""
    STATUS_CHOICES = [
        ('attending', 'Attending'),
        ('maybe', 'Maybe'),
        ('not_attending', 'Not Attending'),
    ]

    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='participants')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='event_participations')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='attending')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['event', 'user']

    def __str__(self):
        return f"{self.user.username} - {self.event.title} ({self.status})"


class Announcement(models.Model):
    """System announcements"""
    ANNOUNCEMENT_TYPE_CHOICES = [
        ('general', 'General'),
        ('important', 'Important'),
        ('urgent', 'Urgent'),
        ('maintenance', 'Maintenance'),
        ('update', 'Update'),
    ]
    
    title = models.CharField(max_length=200)
    content = models.TextField()
    announcement_type = models.CharField(max_length=20, choices=ANNOUNCEMENT_TYPE_CHOICES, default='general')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='announcements')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class PasswordResetToken(models.Model):
    """Password reset token model"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='password_reset_tokens')
    token = models.CharField(max_length=100, unique=True)
    expires_at = models.DateTimeField()
    used = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"PasswordResetToken {self.token}"
    
    def is_expired(self):
        return timezone.now() > self.expires_at
