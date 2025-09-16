from django.contrib import admin
from .models import (
    Profile, Connection, Message, Forum, ForumReply, 
    Job, JobApplication, Mentorship, Event, EventParticipant, Announcement, PasswordResetToken
)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'full_name', 'course', 'graduation_year', 'location']
    list_filter = ['course', 'graduation_year', 'location']
    search_fields = ['user__username', 'full_name', 'course']


@admin.register(Connection)
class ConnectionAdmin(admin.ModelAdmin):
    list_display = ['requester', 'receiver', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['requester__username', 'receiver__username']


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['sender', 'receiver', 'content_preview', 'is_read', 'created_at']
    list_filter = ['is_read', 'created_at']
    search_fields = ['sender__username', 'receiver__username', 'content']

    def content_preview(self, obj):
        return obj.content[:50] + "..." if len(obj.content) > 50 else obj.content
    content_preview.short_description = 'Content Preview'


@admin.register(Forum)
class ForumAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'created_at', 'reply_count']
    list_filter = ['created_at']
    search_fields = ['title', 'content', 'author__username']

    def reply_count(self, obj):
        return obj.get_reply_count()
    reply_count.short_description = 'Replies'


@admin.register(ForumReply)
class ForumReplyAdmin(admin.ModelAdmin):
    list_display = ['forum', 'user', 'content_preview', 'created_at']
    list_filter = ['created_at']
    search_fields = ['forum__title', 'user__username', 'content']

    def content_preview(self, obj):
        return obj.content[:50] + "..." if len(obj.content) > 50 else obj.content
    content_preview.short_description = 'Content Preview'


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ['title', 'company', 'job_type', 'location', 'deadline', 'posted_by', 'application_count']
    list_filter = ['job_type', 'deadline', 'created_at']
    search_fields = ['title', 'company', 'description', 'posted_by__username']
    fields = ['title', 'description', 'company', 'location', 'job_type', 'deadline', 'posted_by']
    
    def application_count(self, obj):
        return obj.get_application_count()
    application_count.short_description = 'Applications'


@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ['job', 'applicant', 'status', 'applied_at']
    list_filter = ['status', 'applied_at', 'job__company']
    search_fields = ['job__title', 'applicant__username', 'cover_letter']
    readonly_fields = ['applied_at', 'updated_at']
    fields = ['job', 'applicant', 'cover_letter', 'status', 'applied_at', 'updated_at']


@admin.register(Mentorship)
class MentorshipAdmin(admin.ModelAdmin):
    list_display = ['mentor', 'mentee', 'status', 'started_at', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['mentor__username', 'mentee__username']


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'event_date', 'location', 'created_by', 'participant_count']
    list_filter = ['event_date', 'created_at']
    search_fields = ['title', 'description', 'location', 'created_by__username']

    def participant_count(self, obj):
        return obj.get_participant_count()
    participant_count.short_description = 'Participants'


@admin.register(EventParticipant)
class EventParticipantAdmin(admin.ModelAdmin):
    list_display = ['event', 'user', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['event__title', 'user__username']


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ['title', 'announcement_type', 'created_by', 'created_at']
    list_filter = ['announcement_type', 'created_at']
    search_fields = ['title', 'content', 'created_by__username']


@admin.register(PasswordResetToken)
class PasswordResetTokenAdmin(admin.ModelAdmin):
    list_display = ['user', 'token', 'used', 'expires_at', 'created_at']
    list_filter = ['used', 'created_at', 'expires_at']
    search_fields = ['user__username', 'user__email', 'token']
    readonly_fields = ['token', 'created_at']
