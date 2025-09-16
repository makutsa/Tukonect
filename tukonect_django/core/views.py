from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.admin.views.decorators import staff_member_required
from django.urls import reverse
import secrets
from datetime import timedelta
from .models import (
    Profile, Connection, Message, Forum, ForumReply, 
    Job, JobApplication, Mentorship, Event, EventParticipant, Announcement, PasswordResetToken
)
from .forms import (
    UserRegistrationForm, ProfileForm, ConnectionForm, MessageForm,
    ForumForm, ForumReplyForm, JobForm, JobApplicationForm, MentorshipForm, EventForm, 
    AnnouncementForm, ForgotPasswordForm, ResetPasswordForm
)


def get_or_create_profile(user):
    """Helper function to get or create a profile for a user"""
    profile, created = Profile.objects.get_or_create(
        user=user,
        defaults={
            'full_name': user.get_full_name() or user.username
        }
    )
    return profile


def home(request):
    """Home page with recent activity"""
    if request.user.is_authenticated:
        # Get recent forum posts
        recent_forums = Forum.objects.all()[:5]
        # Get recent jobs
        recent_jobs = Job.objects.all()[:5]
        # Get upcoming events
        upcoming_events = Event.objects.filter(event_date__gte=timezone.now()).order_by('event_date')[:5]
        # Get announcements
        announcements = Announcement.objects.all()[:3]
        
        context = {
            'recent_forums': recent_forums,
            'recent_jobs': recent_jobs,
            'upcoming_events': upcoming_events,
            'announcements': announcements,
        }
    else:
        context = {}
    
    return render(request, 'core/home.html', context)


def register(request):
    """User registration"""
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Create User Profile
            Profile.objects.create(
                user=user,
                full_name=form.cleaned_data['full_name']
            )
           
            messages.success(request, 'Registration successful! Please log in.')
            return redirect('login')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'core/register.html', {'form': form})


def user_login(request):
    """User login"""
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'core/login.html')


@login_required
def user_logout(request):
    """User logout"""
    logout(request)
    return redirect('home')


@login_required
def profile(request, user_id=None):
    """User profile view"""
    if user_id:
        profile_user = get_object_or_404(User, id=user_id)
    else:
        profile_user = request.user
    
    # Get or create profile
    profile = get_or_create_profile(profile_user)
    
    # Check connection status if viewing someone else's profile
    connection_status = None
    connection_obj = None
    
    if profile_user != request.user:
        # Check if there's a connection between current user and profile user
        connection = Connection.objects.filter(
            Q(requester=request.user, receiver=profile_user) |
            Q(requester=profile_user, receiver=request.user)
        ).first()
        
        if connection:
            if connection.status == 'accepted':
                connection_status = 'connected'
                connection_obj = connection
            elif connection.status == 'pending':
                if connection.requester == request.user:
                    connection_status = 'pending_sent'
                    connection_obj = connection
                else:
                    connection_status = 'pending_received'
                    connection_obj = connection
            elif connection.status == 'rejected':
                connection_status = 'rejected'
                connection_obj = connection
            elif connection.status == 'blocked':
                connection_status = 'blocked'
                connection_obj = connection
        else:
            connection_status = 'not_connected'
    
    context = {
        'profile_user': profile_user,
        'profile': profile,
        'connection_status': connection_status,
        'connection_obj': connection_obj,
    }
    
    return render(request, 'core/profile.html', context)


@login_required
def edit_profile(request):
    """Edit user profile"""
    # Get or create profile
    profile = get_or_create_profile(request.user)
    
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
    else:
        form = ProfileForm(instance=profile)
    
    return render(request, 'core/edit_profile.html', {'form': form})


@login_required
def connections(request):
    """View and manage connections"""
    # Get accepted connections (both sent and received)
    sent_connections = Connection.objects.filter(requester=request.user, status='accepted').select_related('receiver')
    received_connections = Connection.objects.filter(receiver=request.user, status='accepted').select_related('requester')
    all_connections = list(sent_connections) + list(received_connections)
    
    # Ensure all connected users have profiles
    for connection in sent_connections:
        get_or_create_profile(connection.receiver)
    
    for connection in received_connections:
        get_or_create_profile(connection.requester)
    
    # Get pending connection requests sent by current user
    sent_pending = Connection.objects.filter(
        requester=request.user, 
        status='pending'
    ).select_related('receiver')
    
    # Get pending connection requests received by current user
    received_pending = Connection.objects.filter(
        receiver=request.user, 
        status='pending'
    ).select_related('requester')
    
    # Ensure all users have profiles
    for connection in sent_pending:
        get_or_create_profile(connection.receiver)
    
    for connection in received_pending:
        get_or_create_profile(connection.requester)
    
    # Get connection statistics
    student_connections = []
    alumni_connections = []
    mentor_connections = []
    
    for c in all_connections:
        # Ensure both users have profiles
        receiver_profile = get_or_create_profile(c.receiver)
        requester_profile = get_or_create_profile(c.requester)
        
        receiver_type = receiver_profile.user_type or 'student'
        requester_type = requester_profile.user_type or 'student'
        
        if receiver_type == 'student' or requester_type == 'student':
            student_connections.append(c)
        if receiver_type == 'alumni' or requester_type == 'alumni':
            alumni_connections.append(c)
        if receiver_type == 'mentor' or requester_type == 'mentor':
            mentor_connections.append(c)
    
    # Get recent connections (last 30 days)
    from datetime import timedelta
    thirty_days_ago = timezone.now() - timedelta(days=30)
    recent_connections = [c for c in all_connections if c.created_at >= thirty_days_ago]
    
    # Get recent activity (simplified for now)
    recent_activity = []
    
    # Get suggested connections (users not yet connected and no pending requests)
    # Get all users we've interacted with (connected, sent requests to, or received requests from)
    all_interactions = Connection.objects.filter(
        Q(requester=request.user) | Q(receiver=request.user)
    ).values_list('requester_id', 'receiver_id')
    
    interacted_user_ids = set()
    for requester_id, receiver_id in all_interactions:
        interacted_user_ids.add(requester_id)
        interacted_user_ids.add(receiver_id)
    
    # Exclude self and all users we've interacted with
    suggested_connections = Profile.objects.exclude(
        user_id__in=interacted_user_ids
    ).select_related('user')[:5]
    
    context = {
        'connections': all_connections,
        'sent_connections': sent_connections,
        'received_connections': received_connections,
        'sent_pending': sent_pending,
        'received_pending': received_pending,
        'student_connections': student_connections,
        'alumni_connections': alumni_connections,
        'mentor_connections': mentor_connections,
        'recent_connections': recent_connections,
        'recent_activity': recent_activity,
        'suggested_connections': suggested_connections,
    }
    return render(request, 'core/connections.html', context)


@login_required
def search_users(request):
    """Search for users to connect with"""
    query = request.GET.get('q', '')
    major = request.GET.get('major', '')
    user_type = request.GET.get('user_type', '')
    graduation_year = request.GET.get('graduation_year', '')
    course = request.GET.get('course', '')
    skills = request.GET.get('skills', '')
    location = request.GET.get('location', '')
    sort_by = request.GET.get('sort_by', 'created_at')
    
    # Only show results if there's a search query or filters applied
    has_search_criteria = any([query, major, user_type, graduation_year, course, skills, location])
    
    if not has_search_criteria:
        # No search criteria - return empty results
        profiles = Profile.objects.none()
    else:
        # Start with all profiles excluding current user
        profiles = Profile.objects.exclude(user=request.user).select_related('user')
        
        # Apply filters
        if query:
            profiles = profiles.filter(
                Q(user__username__icontains=query) |
                Q(full_name__icontains=query) |
                Q(user__first_name__icontains=query) |
                Q(user__last_name__icontains=query) |
                Q(user__email__icontains=query)
            )
    
        if major:
            profiles = profiles.filter(major__icontains=major)
        
        if user_type:
            profiles = profiles.filter(user_type=user_type)
        
        if graduation_year:
            profiles = profiles.filter(graduation_year=graduation_year)
        
        if course:
            profiles = profiles.filter(course__icontains=course)
        
        if skills:
            # Search for skills (comma-separated)
            skill_list = [skill.strip() for skill in skills.split(',') if skill.strip()]
            for skill in skill_list:
                profiles = profiles.filter(skills__icontains=skill)
        
        if location:
            profiles = profiles.filter(location__icontains=location)
    
    # Get connection status for all users (don't exclude anyone)
    # We'll show all users but indicate their connection status
    
    # Sort results
    if has_search_criteria:
        if sort_by == 'name':
            profiles = profiles.order_by('full_name')
        elif sort_by == 'username':
            profiles = profiles.order_by('user__username')
        elif sort_by == 'user_type':
            profiles = profiles.order_by('user_type', 'full_name')
        elif sort_by == 'graduation_year':
            profiles = profiles.order_by('-graduation_year')
        else:
            profiles = profiles.order_by('-created_at')
    
    # Paginate results
    paginator = Paginator(profiles, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get connection status for each user in the results
    user_connections = {}
    if request.user.is_authenticated and has_search_criteria:
        for profile in page_obj:
            connection = Connection.objects.filter(
                Q(requester=request.user, receiver=profile.user) |
                Q(requester=profile.user, receiver=request.user)
            ).first()
            
            if connection:
                if connection.status == 'accepted':
                    user_connections[profile.user.id] = 'connected'
                elif connection.status == 'pending':
                    if connection.requester == request.user:
                        user_connections[profile.user.id] = 'pending_sent'
                    else:
                        user_connections[profile.user.id] = 'pending_received'
                elif connection.status == 'rejected':
                    user_connections[profile.user.id] = 'rejected'
                elif connection.status == 'blocked':
                    user_connections[profile.user.id] = 'blocked'
            else:
                user_connections[profile.user.id] = 'not_connected'
    
    # Get unique values for filter dropdowns
    all_majors = Profile.objects.exclude(major='').values_list('major', flat=True).distinct().order_by('major')
    all_courses = Profile.objects.exclude(course='').values_list('course', flat=True).distinct().order_by('course')
    all_locations = Profile.objects.exclude(location='').values_list('location', flat=True).distinct().order_by('location')
    
    context = {
        'page_obj': page_obj,
        'user_connections': user_connections,
        'has_search_criteria': has_search_criteria,
        'query': query,
        'major': major,
        'user_type': user_type,
        'graduation_year': graduation_year,
        'course': course,
        'skills': skills,
        'location': location,
        'sort_by': sort_by,
        'all_majors': all_majors,
        'all_courses': all_courses,
        'all_locations': all_locations,
        'user_type_choices': Profile.USER_TYPE_CHOICES,
    }
    return render(request, 'core/search_users.html', context)


@login_required
def send_connection_request(request, user_id):
    """Send connection request"""
    receiver = get_object_or_404(User, id=user_id)
    
    if request.user == receiver:
        messages.error(request, 'You cannot send a connection request to yourself.')
        return redirect('profile', user_id=user_id)
    
    # Check if there's already a connection between these users (in any direction)
    existing_connection = Connection.objects.filter(
        Q(requester=request.user, receiver=receiver) |
        Q(requester=receiver, receiver=request.user)
    ).first()
    
    if existing_connection:
        if existing_connection.status == 'pending':
            if existing_connection.requester == request.user:
                messages.info(request, f'You have already sent a connection request to {receiver.username}.')
            else:
                messages.info(request, f'{receiver.username} has already sent you a connection request.')
        elif existing_connection.status == 'accepted':
            messages.info(request, f'You are already connected with {receiver.username}.')
        elif existing_connection.status == 'rejected':
            messages.info(request, f'Previous connection request was rejected. You cannot send another request.')
        elif existing_connection.status == 'blocked':
            messages.error(request, f'Connection request cannot be sent.')
    else:
        # Create new connection request
        connection = Connection.objects.create(
            requester=request.user,
            receiver=receiver,
            status='pending'
        )
        messages.success(request, f'Connection request sent to {receiver.username}!')
    
    return redirect('profile', user_id=user_id)


@login_required
def accept_connection(request, connection_id):
    """Accept connection request"""
    connection = get_object_or_404(Connection, id=connection_id, receiver=request.user)
    connection.status = 'accepted'
    connection.save()
    messages.success(request, 'Connection accepted!')
    return redirect('connections')


@login_required
def reject_connection(request, connection_id):
    """Reject connection request"""
    connection = get_object_or_404(Connection, id=connection_id, receiver=request.user)
    connection.status = 'rejected'
    connection.save()
    messages.success(request, 'Connection rejected')
    return redirect('connections')


@login_required
def cancel_connection_request(request, connection_id):
    """Cancel/withdraw a connection request"""
    connection = get_object_or_404(Connection, id=connection_id, requester=request.user, status='pending')
    receiver_username = connection.receiver.username
    connection.delete()
    messages.success(request, f'Connection request to {receiver_username} has been cancelled.')
    return redirect('connections')


@login_required
def unfriend_connection(request, connection_id):
    """Unfriend/remove an accepted connection"""
    connection = get_object_or_404(Connection, id=connection_id, status='accepted')
    
    # Check if the current user is either the requester or receiver of this connection
    if connection.requester != request.user and connection.receiver != request.user:
        messages.error(request, 'You are not authorized to perform this action.')
        return redirect('connections')
    
    # Get the other user's username for the message
    other_user = connection.receiver if connection.requester == request.user else connection.requester
    other_username = other_user.username
    
    # Delete the connection
    connection.delete()
    messages.success(request, f'You have unfriended {other_username}.')
    return redirect('connections')


@login_required
def messages_list(request):
    """View messages"""
    conversations = Message.objects.filter(
        Q(sender=request.user) | Q(receiver=request.user)
    ).order_by('-created_at').distinct()
    
    # Group by conversation partner
    conversation_partners = {}
    for message in conversations:
        partner = message.sender if message.receiver == request.user else message.receiver
        if partner.id not in conversation_partners:
            conversation_partners[partner.id] = {
                'partner': partner,
                'last_message': message,
                'unread_count': 0
            }
        if message.receiver == request.user and not message.is_read:
            conversation_partners[partner.id]['unread_count'] += 1
    
    context = {
        'conversations': conversation_partners.values(),
    }
    return render(request, 'core/messages.html', context)


@login_required
def message_detail(request, user_id):
    """Message conversation with specific user"""
    other_user = get_object_or_404(User, id=user_id)
    
    # Mark messages as read
    Message.objects.filter(sender=other_user, receiver=request.user, is_read=False).update(is_read=True)
    
    messages_list = Message.objects.filter(
        Q(sender=request.user, receiver=other_user) | 
        Q(sender=other_user, receiver=request.user)
    ).order_by('created_at')
    
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            Message.objects.create(
                sender=request.user,
                receiver=other_user,
                content=form.cleaned_data['content']
            )
            return redirect('message_detail', user_id=user_id)
    else:
        form = MessageForm()
    
    context = {
        'other_user': other_user,
        'messages': messages_list,
        'form': form,
    }
    return render(request, 'core/message_detail.html', context)


def forum_list(request):
    """List all forum posts"""
    forums = Forum.objects.all()
    paginator = Paginator(forums, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'core/forum_list.html', {'page_obj': page_obj})


def forum_detail(request, forum_id):
    """Forum post detail with replies"""
    forum = get_object_or_404(Forum, id=forum_id)
    replies = forum.replies.all()
    
    if request.method == 'POST' and request.user.is_authenticated:
        form = ForumReplyForm(request.POST)
        if form.is_valid():
            ForumReply.objects.create(
                forum=forum,
                user=request.user,
                content=form.cleaned_data['content']
            )
            return redirect('forum_detail', forum_id=forum_id)
    else:
        form = ForumReplyForm()
    
    context = {
        'forum': forum,
        'replies': replies,
        'form': form,
    }
    return render(request, 'core/forum_detail.html', context)


@login_required
def create_forum_post(request):
    """Create new forum post"""
    if request.method == 'POST':
        form = ForumForm(request.POST)
        if form.is_valid():
            forum = form.save(commit=False)
            forum.author = request.user
            forum.save()
            messages.success(request, 'Forum post created successfully!')
            return redirect('forum_detail', forum_id=forum.id)
    else:
        form = ForumForm()
    
    return render(request, 'core/create_forum_post.html', {'form': form})


def jobs_list(request):
    """List all job postings"""
    jobs = Job.objects.filter(deadline__gte=timezone.now())
    paginator = Paginator(jobs, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'core/jobs_list.html', {'page_obj': page_obj})


def job_detail(request, job_id):
    """Job posting detail"""
    job = get_object_or_404(Job, id=job_id)
    
    # Check if user has already applied
    has_applied = False
    user_application = None
    if request.user.is_authenticated:
        try:
            user_application = JobApplication.objects.get(job=job, applicant=request.user)
            has_applied = True
        except JobApplication.DoesNotExist:
            has_applied = False
    
    # Get applications for job poster
    applications = []
    if request.user.is_authenticated and request.user == job.posted_by:
        applications = JobApplication.objects.filter(job=job).select_related('applicant').order_by('-applied_at')
    
    context = {
        'job': job,
        'has_applied': has_applied,
        'user_application': user_application,
        'applications': applications,
    }
    
    return render(request, 'core/job_detail.html', context)


@login_required
def create_job(request):
    """Create new job posting"""
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.posted_by = request.user
            job.save()
            messages.success(request, 'Job posting created successfully!')
            return redirect('job_detail', job_id=job.id)
    else:
        form = JobForm()
    
    return render(request, 'core/create_job.html', {'form': form})


@login_required
def apply_for_job(request, job_id):
    """Apply for a job"""
    job = get_object_or_404(Job, id=job_id)
    
    # Check if user is trying to apply to their own job
    if job.posted_by == request.user:
        messages.error(request, 'You cannot apply to your own job posting.')
        return redirect('job_detail', job_id=job_id)
    
    # Check if deadline has passed
    if job.is_deadline_passed():
        messages.error(request, 'The application deadline for this job has passed.')
        return redirect('job_detail', job_id=job_id)
    
    # Check if user has already applied
    if JobApplication.objects.filter(job=job, applicant=request.user).exists():
        messages.warning(request, 'You have already applied for this job.')
        return redirect('job_detail', job_id=job_id)
    
    if request.method == 'POST':
        form = JobApplicationForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.job = job
            application.applicant = request.user
            application.save()
            messages.success(request, 'Your application has been submitted successfully!')
            return redirect('job_detail', job_id=job_id)
    else:
        form = JobApplicationForm()
    
    context = {
        'job': job,
        'form': form,
    }
    
    return render(request, 'core/apply_for_job.html', context)


@login_required
def job_applications(request, job_id):
    """View applications for a job (job poster only)"""
    job = get_object_or_404(Job, id=job_id)
    
    # Check if user is the job poster
    if job.posted_by != request.user and not request.user.is_staff:
        messages.error(request, 'You can only view applications for your own jobs.')
        return redirect('job_detail', job_id=job_id)
    
    applications = JobApplication.objects.filter(job=job).select_related('applicant').order_by('-applied_at')
    
    context = {
        'job': job,
        'applications': applications,
    }
    
    return render(request, 'core/job_applications.html', context)


@login_required
def update_application_status(request, application_id):
    """Update application status (job poster only)"""
    application = get_object_or_404(JobApplication, id=application_id)
    
    # Check if user is the job poster
    if application.job.posted_by != request.user and not request.user.is_staff:
        messages.error(request, 'You can only update applications for your own jobs.')
        return redirect('job_detail', job_id=application.job.id)
    
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in ['pending', 'reviewed', 'shortlisted', 'rejected', 'hired']:
            application.status = new_status
            application.save()
            messages.success(request, f'Application status updated to {application.get_status_display()}.')
        else:
            messages.error(request, 'Invalid status selected.')
    
    return redirect('job_applications', job_id=application.job.id)


@login_required
def create_event(request):
    """Create new event"""
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.created_by = request.user
            event.save()
            messages.success(request, 'Event created successfully!')
            return redirect('event_detail', event_id=event.id)
    else:
        form = EventForm()
    
    return render(request, 'core/create_event.html', {'form': form})


def events_list(request):
    """List all events"""
    events = Event.objects.all().order_by('event_date')
    paginator = Paginator(events, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'core/events_list.html', {'page_obj': page_obj})


def event_detail(request, event_id):
    """Event detail"""
    event = get_object_or_404(Event, id=event_id)
    participants = event.participants.all()
    
    if request.user.is_authenticated:
        user_participation = EventParticipant.objects.filter(
            event=event, user=request.user
        ).first()
    else:
        user_participation = None
    
    return render(request, 'core/event_detail.html', {
        'event': event,
        'participants': participants,
        'user_participation': user_participation,
    })


@login_required
def join_event(request, event_id):
    """Join an event"""
    event = get_object_or_404(Event, id=event_id)
    participation, created = EventParticipant.objects.get_or_create(
        event=event,
        user=request.user,
        defaults={'status': 'attending'}
    )
    
    if created:
        messages.success(request, f'You are now attending {event.title}')
    else:
        messages.info(request, 'You are already registered for this event')
    
    return redirect('event_detail', event_id=event_id)


@login_required
def leave_event(request, event_id):
    """Leave an event"""
    event = get_object_or_404(Event, id=event_id)
    EventParticipant.objects.filter(event=event, user=request.user).delete()
    messages.success(request, f'You have left {event.title}')
    return redirect('event_detail', event_id=event_id)


def announcements_list(request):
    """List all announcements"""
    announcements = Announcement.objects.all()
    return render(request, 'core/announcements_list.html', {'announcements': announcements})


# Password reset functionality
def forgot_password(request):
    """Handle forgot password requests"""
    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user = User.objects.get(email=email)
                # Generate reset token
                token = secrets.token_urlsafe(32)
                expires_at = timezone.now() + timedelta(hours=1)
                
                # Create or update reset token
                reset_token, created = PasswordResetToken.objects.get_or_create(
                    user=user,
                    used=False,
                    defaults={'token': token, 'expires_at': expires_at}
                )
                if not created:
                    reset_token.token = token
                    reset_token.expires_at = expires_at
                    reset_token.used = False
                    reset_token.save()
                
                # Send email (in production, use proper email service)
                reset_url = request.build_absolute_uri(
                    reverse('reset_password', kwargs={'token': token})
                )
                send_password_reset_email(email, reset_url)
                messages.success(request, 'Password reset instructions have been sent to your email.')
            except User.DoesNotExist:
                messages.error(request, 'No account found with that email address.')
            return redirect('forgot_password')
    else:
        form = ForgotPasswordForm()
    
    return render(request, 'core/forgot_password.html', {'form': form})


def reset_password(request, token):
    """Handle password reset with token"""
    try:
        reset_token = PasswordResetToken.objects.get(token=token, used=False)
        if reset_token.is_expired():
            messages.error(request, 'Invalid or expired reset token.')
            return redirect('forgot_password')
    except PasswordResetToken.DoesNotExist:
        messages.error(request, 'Invalid or expired reset token.')
        return redirect('forgot_password')
    
    if request.method == 'POST':
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            # Update user password
            user = reset_token.user
            user.set_password(form.cleaned_data['password'])
            user.save()
            
            # Mark token as used
            reset_token.used = True
            reset_token.save()
            
            messages.success(request, 'Your password has been reset successfully. You can now login with your new password.')
            return redirect('login')
    else:
        form = ResetPasswordForm()
    
    return render(request, 'core/reset_password.html', {'form': form, 'token': token})


def send_password_reset_email(email, reset_url):
    """Send password reset email"""
    # In production, use proper email service like SendGrid, AWS SES, etc.
    # For now, we'll just print the reset URL to console
    print(f"Password reset for {email}: {reset_url}")
    
    # You can implement actual email sending here
    # Example with Django's email functionality:
    # from django.core.mail import send_mail
    # send_mail(
    #     'Password Reset - Tukonect',
    #     f'Click the link to reset your password: {reset_url}',
    #     'noreply@tukonect.com',
    #     [email],
    #     fail_silently=False,
    # )


# Admin functionality
def is_admin(user):
    """Check if user is admin"""
    return user.is_authenticated and user.is_staff


@user_passes_test(is_admin)
def admin_dashboard(request):
    """Admin dashboard with statistics"""
    # Get dashboard statistics
    total_users = User.objects.count()
    active_users = User.objects.filter(is_active=True).count()
    admin_users = User.objects.filter(is_staff=True).count()
    total_profiles = Profile.objects.count()
    total_connections = Connection.objects.count()
    total_messages = Message.objects.count()
    total_forum_posts = Forum.objects.count()
    total_jobs = Job.objects.count()
    total_events = Event.objects.count()
    
    # Get recent users (last 7 days)
    week_ago = timezone.now() - timedelta(days=7)
    recent_users = User.objects.filter(date_joined__gte=week_ago).count()
    
    # Get recent activity
    recent_connections = Connection.objects.filter(created_at__gte=week_ago).count()
    recent_messages = Message.objects.filter(created_at__gte=week_ago).count()
    
    context = {
        'total_users': total_users,
        'active_users': active_users,
        'admin_users': admin_users,
        'total_profiles': total_profiles,
        'total_connections': total_connections,
        'total_messages': total_messages,
        'total_forum_posts': total_forum_posts,
        'total_jobs': total_jobs,
        'total_events': total_events,
        'recent_users': recent_users,
        'recent_connections': recent_connections,
        'recent_messages': recent_messages,
    }
    return render(request, 'core/admin/dashboard.html', context)


@user_passes_test(is_admin)
def admin_users(request):
    """Admin user management"""
    users = User.objects.all().order_by('-date_joined')
    return render(request, 'core/admin_users.html', {'users': users})


@user_passes_test(is_admin)
def toggle_admin(request, user_id):
    """Toggle admin status"""
    user = get_object_or_404(User, id=user_id)
    user.is_staff = not user.is_staff
    user.save()
    
    status = 'admin' if user.is_staff else 'regular user'
    messages.success(request, f'User {user.username} is now a {status}.')
    return redirect('admin_users')


@user_passes_test(is_admin)
def toggle_active(request, user_id):
    """Toggle active status"""
    user = get_object_or_404(User, id=user_id)
    user.is_active = not user.is_active
    user.save()
    
    status = 'active' if user.is_active else 'inactive'
    messages.success(request, f'User {user.username} is now {status}.')
    return redirect('admin_users')


@user_passes_test(is_admin)
def delete_user(request, user_id):
    """Delete user"""
    # Prevent admin from deleting themselves
    if user_id == request.user.id:
        messages.error(request, 'You cannot delete your own account.')
        return redirect('admin_users')
    
    try:
        user = get_object_or_404(User, id=user_id)
        username = user.username
        user.delete()
        messages.success(request, f'User {username} has been permanently deleted.')
    except Exception as e:
        messages.error(request, f'Error deleting user: {str(e)}')
    
    return redirect('admin_users')


@user_passes_test(is_admin)
def reset_user_password(request, user_id):
    """Reset user password"""
    try:
        user = get_object_or_404(User, id=user_id)
        new_password = 'tukonect123'  # Default reset password
        user.set_password(new_password)
        user.save()
        messages.success(request, f'Password for {user.username} has been reset to: {new_password}')
    except Exception as e:
        messages.error(request, f'Error resetting password: {str(e)}')
    
    return redirect('admin_users')


@user_passes_test(is_admin)
def edit_user(request, user_id):
    """Edit user"""
    user = get_object_or_404(User, id=user_id)
    
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        
        # Check if email is being changed and if it already exists
        if email != user.email:
            if User.objects.filter(email=email).exclude(id=user.id).exists():
                messages.error(request, f'Email {email} is already in use by another user.')
                return render(request, 'core/edit_user.html', {'user': user})
        
        # Check if username is being changed and if it already exists
        if username != user.username:
            if User.objects.filter(username=username).exclude(id=user.id).exists():
                messages.error(request, f'Username {username} is already in use by another user.')
                return render(request, 'core/edit_user.html', {'user': user})
        
        # Update user fields
        user.username = username
        user.email = email
        user.is_active = 'is_active' in request.POST
        user.is_staff = 'is_staff' in request.POST
        
        # Only update password if provided
        new_password = request.POST.get('password', '').strip()
        if new_password:
            user.set_password(new_password)
        
        user.save()
        messages.success(request, f'User {user.username} has been updated successfully.')
        return redirect('admin_users')
    
    return render(request, 'core/edit_user.html', {'user': user})


def create_admin(request):
    """Create an admin user - only for initial setup"""
    # Check if any admin users exist
    if User.objects.filter(is_staff=True).exists():
        return render(request, 'core/create_admin.html', {'message': 'Admin user already exists!'})
    
    # Create admin user
    admin_user = User.objects.create_user(
        username='admin',
        email='admin@tukonect.com',
        password='admin123',
        is_staff=True,
        is_superuser=True
    )
    
    return render(request, 'core/create_admin.html', {
        'message': 'Admin user created!',
        'email': 'admin@tukonect.com',
        'password': 'admin123'
    })


# Delete functionality
@login_required
def delete_job(request, job_id):
    """Delete job (only by creator)"""
    job = get_object_or_404(Job, id=job_id)
    
    # Check if user is the creator
    if job.posted_by != request.user and not request.user.is_staff:
        messages.error(request, 'You can only delete jobs you created.')
        return redirect('job_detail', job_id=job_id)
    
    job.delete()
    messages.success(request, 'Job deleted successfully!')
    return redirect('jobs_list')


@login_required
def delete_forum(request, forum_id):
    """Delete forum post (only by author)"""
    forum = get_object_or_404(Forum, id=forum_id)
    
    # Check if user is the author
    if forum.author != request.user and not request.user.is_staff:
        messages.error(request, 'You can only delete forum posts you created.')
        return redirect('forum_detail', forum_id=forum_id)
    
    forum.delete()
    messages.success(request, 'Forum post deleted successfully!')
    return redirect('forum_list')


@login_required
def delete_event(request, event_id):
    """Delete event (only by creator)"""
    event = get_object_or_404(Event, id=event_id)
    
    # Check if user is the creator
    if event.created_by != request.user and not request.user.is_staff:
        messages.error(request, 'You can only delete events you created.')
        return redirect('event_detail', event_id=event_id)
    
    event.delete()
    messages.success(request, 'Event deleted successfully!')
    return redirect('events_list')


@user_passes_test(is_admin)
def delete_announcement(request, announcement_id):
    """Delete announcement (admin only)"""
    announcement = get_object_or_404(Announcement, id=announcement_id)
    announcement.delete()
    messages.success(request, 'Announcement deleted successfully!')
    return redirect('announcements_list')


# Edit functionality
@login_required
def edit_event(request, event_id):
    """Edit event (only by creator)"""
    event = get_object_or_404(Event, id=event_id)
    
    # Check if user is the creator
    if event.created_by != request.user and not request.user.is_staff:
        messages.error(request, 'You can only edit events you created.')
        return redirect('event_detail', event_id=event_id)
    
    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            messages.success(request, 'Event updated successfully!')
            return redirect('event_detail', event_id=event.id)
    else:
        form = EventForm(instance=event)
    
    return render(request, 'core/edit_event.html', {'form': form, 'event': event})


@user_passes_test(is_admin)
def create_announcement(request):
    """Create new announcement (admin only)"""
    if request.method == 'POST':
        form = AnnouncementForm(request.POST)
        if form.is_valid():
            announcement = form.save(commit=False)
            announcement.created_by = request.user
            announcement.save()
            messages.success(request, 'Announcement created successfully!')
            return redirect('announcements_list')
    else:
        form = AnnouncementForm()
    
    return render(request, 'core/create_announcement.html', {'form': form})


@user_passes_test(is_admin)
def edit_announcement(request, announcement_id):
    """Edit announcement (admin only)"""
    announcement = get_object_or_404(Announcement, id=announcement_id)
    
    if request.method == 'POST':
        form = AnnouncementForm(request.POST, instance=announcement)
        if form.is_valid():
            form.save()
            messages.success(request, 'Announcement updated successfully!')
            return redirect('announcements_list')
    else:
        form = AnnouncementForm(instance=announcement)
    
    return render(request, 'core/edit_announcement.html', {'form': form, 'announcement': announcement})
