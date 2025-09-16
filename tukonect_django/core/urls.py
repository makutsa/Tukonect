from django.urls import path
from . import views

urlpatterns = [
    # Home
    path('', views.home, name='home'),
    
    # Authentication
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('reset-password/<str:token>/', views.reset_password, name='reset_password'),
    
    # Profile
    path('profile/', views.profile, name='profile'),
    path('profile/<int:user_id>/', views.profile, name='profile'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    
    # Connections
    path('connections/', views.connections, name='connections'),
    path('search-users/', views.search_users, name='search_users'),
    path('send-connection-request/<int:user_id>/', views.send_connection_request, name='send_connection_request'),
    path('accept-connection/<int:connection_id>/', views.accept_connection, name='accept_connection'),
    path('reject-connection/<int:connection_id>/', views.reject_connection, name='reject_connection'),
    path('cancel-connection-request/<int:connection_id>/', views.cancel_connection_request, name='cancel_connection_request'),
    path('unfriend-connection/<int:connection_id>/', views.unfriend_connection, name='unfriend_connection'),
    
    # Messages
    path('messages/', views.messages_list, name='messages'),
    path('messages/<int:user_id>/', views.message_detail, name='message_detail'),
    
    # Forum
    path('forum/', views.forum_list, name='forum_list'),
    path('forum/<int:forum_id>/', views.forum_detail, name='forum_detail'),
    path('create-forum-post/', views.create_forum_post, name='create_forum_post'),
    path('delete-forum/<int:forum_id>/', views.delete_forum, name='delete_forum'),
    
    # Jobs
    path('jobs/', views.jobs_list, name='jobs_list'),
    path('jobs/<int:job_id>/', views.job_detail, name='job_detail'),
    path('create-job/', views.create_job, name='create_job'),
    path('delete-job/<int:job_id>/', views.delete_job, name='delete_job'),
    path('jobs/<int:job_id>/apply/', views.apply_for_job, name='apply_for_job'),
    path('jobs/<int:job_id>/applications/', views.job_applications, name='job_applications'),
    path('applications/<int:application_id>/update-status/', views.update_application_status, name='update_application_status'),
    
    # Events
    path('events/', views.events_list, name='events_list'),
    path('events/<int:event_id>/', views.event_detail, name='event_detail'),
    path('create-event/', views.create_event, name='create_event'),
    path('edit-event/<int:event_id>/', views.edit_event, name='edit_event'),
    path('delete-event/<int:event_id>/', views.delete_event, name='delete_event'),
    path('join-event/<int:event_id>/', views.join_event, name='join_event'),
    path('leave-event/<int:event_id>/', views.leave_event, name='leave_event'),
    
    # Announcements
    path('announcements/', views.announcements_list, name='announcements_list'),
    path('create-announcement/', views.create_announcement, name='create_announcement'),
    path('edit-announcement/<int:announcement_id>/', views.edit_announcement, name='edit_announcement'),
    path('delete-announcement/<int:announcement_id>/', views.delete_announcement, name='delete_announcement'),
    
    # Admin functionality
    path('admin/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/users/', views.admin_users, name='admin_users'),
    path('admin/users/<int:user_id>/toggle-admin/', views.toggle_admin, name='toggle_admin'),
    path('admin/users/<int:user_id>/toggle-active/', views.toggle_active, name='toggle_active'),
    path('admin/users/<int:user_id>/delete/', views.delete_user, name='delete_user'),
    path('admin/users/<int:user_id>/reset-password/', views.reset_user_password, name='reset_user_password'),
    path('admin/users/<int:user_id>/edit/', views.edit_user, name='edit_user'),
    path('create-admin/', views.create_admin, name='create_admin'),
]
