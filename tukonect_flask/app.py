from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_admin import Admin, AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView
from flask_admin.form import SecureForm
from wtforms import StringField, BooleanField, PasswordField
from wtforms.validators import DataRequired, Email, Optional
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timezone, timedelta
import os
import secrets
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)

app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tukonect.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/uploads'

# Initialize extensions
from models import db
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Please log in to access this page.'

# Admin setup
class AdminIndexView(AdminIndexView):
    @expose('/')
    def index(self):
        if not current_user.is_authenticated or not current_user.is_admin:
            return redirect(url_for('login'))
        
        # Get dashboard statistics
        total_users = User.query.count()
        active_users = User.query.filter_by(is_active=True).count()
        admin_users = User.query.filter_by(is_admin=True).count()
        total_profiles = Profile.query.count()
        total_connections = Connection.query.count()
        total_messages = Message.query.count()
        total_forum_posts = Forum.query.count()
        total_jobs = Job.query.count()
        total_events = Event.query.count()
        
        # Get recent users (last 7 days)
        from datetime import datetime, timedelta
        week_ago = datetime.utcnow() - timedelta(days=7)
        recent_users = User.query.filter(User.date_joined >= week_ago).count()
        
        # Get recent activity
        recent_connections = Connection.query.filter(Connection.created_at >= week_ago).count()
        recent_messages = Message.query.filter(Message.created_at >= week_ago).count()
        
        return self.render('admin/dashboard.html',
                         total_users=total_users,
                         active_users=active_users,
                         admin_users=admin_users,
                         total_profiles=total_profiles,
                         total_connections=total_connections,
                         total_messages=total_messages,
                         total_forum_posts=total_forum_posts,
                         total_jobs=total_jobs,
                         total_events=total_events,
                         recent_users=recent_users,
                         recent_connections=recent_connections,
                         recent_messages=recent_messages)

class AdminModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin
    
    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login'))

class UserForm(SecureForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    is_active = BooleanField('Is Active')
    is_admin = BooleanField('Is Admin')
    password = PasswordField('Password (leave blank to keep current)', validators=[Optional()])

class UserAdminView(AdminModelView):
    column_list = ['id', 'username', 'email', 'is_active', 'is_admin', 'date_joined']
    column_searchable_list = ['username', 'email']
    column_filters = ['is_active', 'is_admin', 'date_joined']
    form = UserForm
    can_create = True
    can_edit = False  # Disable default editing to prevent duplication
    can_delete = True
    can_view_details = True
    
    def on_model_change(self, form, model, is_created):
        """Handle model changes - only set password if provided"""
        if form.password.data and form.password.data.strip():
            model.set_password(form.password.data)
    
    def on_model_delete(self, model):
        """Prevent admin from deleting themselves"""
        if hasattr(model, 'id') and current_user.id == model.id:
            flash('You cannot delete your own account.', 'error')
            return False
        return True

admin = Admin(app, name='Tukonect Admin', index_view=AdminIndexView(), template_mode='bootstrap4')

# Add explicit admin access control
@app.route('/admin')
@login_required
def admin_redirect():
    if not current_user.is_admin:
        flash('Access denied. Admin privileges required.', 'error')
        return redirect(url_for('home'))
    return redirect('/admin/')

@app.route('/admin/users')
@login_required
def admin_users():
    if not current_user.is_admin:
        flash('Access denied. Admin privileges required.', 'error')
        return redirect(url_for('home'))
    
    users = User.query.all()
    return render_template('admin_users.html', users=users)

@app.route('/admin/users/<int:user_id>/toggle_admin', methods=['POST'])
@login_required
def toggle_admin(user_id):
    if not current_user.is_admin:
        flash('Access denied. Admin privileges required.', 'error')
        return redirect(url_for('home'))
    
    user = User.query.get_or_404(user_id)
    user.is_admin = not user.is_admin
    db.session.commit()
    
    status = 'admin' if user.is_admin else 'regular user'
    flash(f'User {user.username} is now a {status}.', 'success')
    return redirect(url_for('admin_users'))

@app.route('/admin/users/<int:user_id>/toggle_active', methods=['POST'])
@login_required
def toggle_active(user_id):
    if not current_user.is_admin:
        flash('Access denied. Admin privileges required.', 'error')
        return redirect(url_for('home'))
    
    user = User.query.get_or_404(user_id)
    user.is_active = not user.is_active
    db.session.commit()
    
    status = 'active' if user.is_active else 'inactive'
    flash(f'User {user.username} is now {status}.', 'success')
    return redirect(url_for('admin_users'))

@app.route('/admin/users/<int:user_id>/delete', methods=['POST'])
@login_required
def delete_user(user_id):
    if not current_user.is_admin:
        flash('Access denied. Admin privileges required.', 'error')
        return redirect(url_for('home'))
    
    # Prevent admin from deleting themselves
    if user_id == current_user.id:
        flash('You cannot delete your own account.', 'error')
        return redirect(url_for('admin_users'))
    
    try:
        user = User.query.get_or_404(user_id)
        username = user.username
        
        # Delete the user (cascade will handle related records)
        db.session.delete(user)
        db.session.commit()
        
        flash(f'User {username} has been permanently deleted.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting user: {str(e)}', 'error')
    
    return redirect(url_for('admin_users'))

@app.route('/admin/users/<int:user_id>/reset_password', methods=['POST'])
@login_required
def reset_user_password(user_id):
    if not current_user.is_admin:
        flash('Access denied. Admin privileges required.', 'error')
        return redirect(url_for('home'))
    
    try:
        user = User.query.get_or_404(user_id)
        new_password = 'tukonect123'  # Default reset password
        user.set_password(new_password)
        db.session.commit()
        
        flash(f'Password for {user.username} has been reset to: {new_password}', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error resetting password: {str(e)}', 'error')
    
    return redirect(url_for('admin_users'))

@app.route('/admin/users/<int:user_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_user(user_id):
    """Custom route for editing users to prevent duplication"""
    if not current_user.is_admin:
        flash('Access denied. Admin privileges required.', 'error')
        return redirect(url_for('home'))
    
    user = User.query.get_or_404(user_id)
    
    if request.method == 'POST':
        try:
            new_username = request.form['username'].strip()
            new_email = request.form['email'].strip()
            
            # Check if email is being changed and if it already exists
            if new_email != user.email:
                existing_user = User.query.filter_by(email=new_email).first()
                if existing_user and existing_user.id != user.id:
                    flash(f'Email {new_email} is already in use by another user.', 'error')
                    return render_template('edit_user.html', user=user)
            
            # Check if username is being changed and if it already exists
            if new_username != user.username:
                existing_user = User.query.filter_by(username=new_username).first()
                if existing_user and existing_user.id != user.id:
                    flash(f'Username {new_username} is already in use by another user.', 'error')
                    return render_template('edit_user.html', user=user)
            
            # Update user fields
            user.username = new_username
            user.email = new_email
            user.is_active = 'is_active' in request.form
            user.is_admin = 'is_admin' in request.form
            
            # Only update password if provided
            new_password = request.form.get('password', '').strip()
            if new_password:
                user.set_password(new_password)
            
            db.session.commit()
            flash(f'User {user.username} has been updated successfully.', 'success')
            return redirect(url_for('admin_users'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating user: {str(e)}', 'error')
    
    return render_template('edit_user.html', user=user)

@app.route('/create-admin')
def create_admin():
    """Create an admin user - only for initial setup"""
    # Check if any admin users exist
    admin_exists = User.query.filter_by(is_admin=True).first()
    if admin_exists:
        return "Admin user already exists!"
    
    # Create admin user
    admin_user = User(
        username='admin',
        email='admin@tukonect.com',
        is_admin=True,
        is_active=True
    )
    admin_user.set_password('admin123')
    db.session.add(admin_user)
    db.session.commit()
    
    return """
    <h1>Admin User Created!</h1>
    <p><strong>Email:</strong> admin@tukonect.com</p>
    <p><strong>Password:</strong> admin123</p>
    <p><strong>Login with EMAIL and password</strong></p>
    <p><a href="/login">Click here to login</a></p>
    """

# Create upload folder
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'profiles'), exist_ok=True)

# Import models after db initialization
from models import User, Profile, Connection, Message, Forum, ForumReply, Job, Mentorship, Event, EventParticipant, Announcement, PasswordResetToken

# Add admin views
admin.add_view(UserAdminView(User, db.session, name='Users'))
admin.add_view(AdminModelView(Profile, db.session, name='Profiles'))
admin.add_view(AdminModelView(Connection, db.session, name='Connections'))
admin.add_view(AdminModelView(Message, db.session, name='Messages'))
admin.add_view(AdminModelView(Forum, db.session, name='Forum Posts'))
admin.add_view(AdminModelView(ForumReply, db.session, name='Forum Replies'))
admin.add_view(AdminModelView(Job, db.session, name='Jobs'))
admin.add_view(AdminModelView(Mentorship, db.session, name='Mentorships'))
admin.add_view(AdminModelView(Event, db.session, name='Events'))
admin.add_view(AdminModelView(EventParticipant, db.session, name='Event Participants'))
admin.add_view(AdminModelView(Announcement, db.session, name='Announcements'))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Routes
@app.route('/')
def home():
    """Home page with recent activity"""
    if current_user.is_authenticated:
        recent_forums = Forum.query.order_by(Forum.created_at.desc()).limit(5).all()
        # Get current time for comparison
        now = datetime.now(timezone.utc)
        recent_jobs = Job.query.filter(Job.deadline >= now).order_by(Job.created_at.desc()).limit(5).all()
        upcoming_events = Event.query.filter(Event.event_date >= now).order_by(Event.event_date).limit(5).all()
        announcements = Announcement.query.order_by(Announcement.created_at.desc()).limit(3).all()
        
        return render_template('home.html', 
                             recent_forums=recent_forums,
                             recent_jobs=recent_jobs,
                             upcoming_events=upcoming_events,
                             announcements=announcements)
    else:
        return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration"""
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        full_name = request.form['full_name']
        
        # Check if user already exists
        if User.query.filter_by(username=username).first():
            flash('Username already exists!', 'error')
            return render_template('register.html')
        
        if User.query.filter_by(email=email).first():
            flash('Email already exists!', 'error')
            return render_template('register.html')
        
        # Create new user
        user = User(username=username, email=email, password_hash=generate_password_hash(password))
        db.session.add(user)
        db.session.commit()
        
        # Create profile
        profile = Profile(user_id=user.id, full_name=full_name)
        db.session.add(profile)
        db.session.commit()
        
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login"""
    if request.method == 'POST':
        # Handle both email and username for backward compatibility
        login_field = request.form.get('email') or request.form.get('username')
        password = request.form['password']
        remember_me = 'remember_me' in request.form
        
        # Try to find user by email first, then by username
        user = User.query.filter_by(email=login_field).first()
        if not user:
            user = User.query.filter_by(username=login_field).first()
        
        if user and check_password_hash(user.password_hash, password):
            login_user(user, remember=remember_me)
            return redirect(url_for('home'))
        else:
            flash('Invalid email/username or password.', 'error')
    
    return render_template('login.html')

@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    """Handle forgot password requests"""
    if request.method == 'POST':
        email = request.form['email']
        user = User.query.filter_by(email=email).first()
        
        if user:
            # Generate reset token
            token = secrets.token_urlsafe(32)
            expires_at = datetime.utcnow() + timedelta(hours=1)
            
            # Create or update reset token
            existing_token = PasswordResetToken.query.filter_by(user_id=user.id, used=False).first()
            if existing_token:
                existing_token.token = token
                existing_token.expires_at = expires_at
            else:
                reset_token = PasswordResetToken(
                    user_id=user.id,
                    token=token,
                    expires_at=expires_at
                )
                db.session.add(reset_token)
            
            db.session.commit()
            
            # Send email (in production, use proper email service)
            try:
                reset_url = url_for('reset_password', token=token, _external=True)
                send_password_reset_email(user.email, reset_url)
                flash('Password reset instructions have been sent to your email.', 'success')
            except Exception as e:
                flash('Error sending email. Please try again later.', 'error')
        else:
            flash('No account found with that email address.', 'error')
    
    return render_template('forgot_password.html')

@app.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    """Handle password reset with token"""
    reset_token = PasswordResetToken.query.filter_by(token=token, used=False).first()
    
    if not reset_token or reset_token.expires_at < datetime.utcnow():
        flash('Invalid or expired reset token.', 'error')
        return redirect(url_for('forgot_password'))
    
    if request.method == 'POST':
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        
        if password != confirm_password:
            flash('Passwords do not match.', 'error')
            return render_template('reset_password.html', token=token)
        
        if len(password) < 6:
            flash('Password must be at least 6 characters long.', 'error')
            return render_template('reset_password.html', token=token)
        
        # Update user password
        user = reset_token.user
        user.set_password(password)
        
        # Mark token as used
        reset_token.used = True
        
        db.session.commit()
        
        flash('Your password has been reset successfully. You can now login with your new password.', 'success')
        return redirect(url_for('login'))
    
    return render_template('reset_password.html', token=token)

def send_password_reset_email(email, reset_url):
    """Send password reset email"""
    # In production, use proper email service like SendGrid, AWS SES, etc.
    # For now, we'll just print the reset URL to console
    print(f"Password reset for {email}: {reset_url}")
    
    # You can implement actual email sending here
    # Example with SMTP:
    # msg = MIMEMultipart()
    # msg['From'] = "noreply@tukonect.com"
    # msg['To'] = email
    # msg['Subject'] = "Password Reset - Tukonect"
    # 
    # body = f"""
    # You requested a password reset for your Tukonect account.
    # 
    # Click the link below to reset your password:
    # {reset_url}
    # 
    # This link will expire in 1 hour.
    # 
    # If you didn't request this, please ignore this email.
    # """
    # 
    # msg.attach(MIMEText(body, 'plain'))
    # 
    # server = smtplib.SMTP('smtp.gmail.com', 587)
    # server.starttls()
    # server.login("your_email@gmail.com", "your_password")
    # text = msg.as_string()
    # server.sendmail("noreply@tukonect.com", email, text)
    # server.quit()

@app.route('/logout')
@login_required
def logout():
    """User logout"""
    logout_user()
    return redirect(url_for('home'))

@app.route('/profile')
@app.route('/profile/<int:user_id>')
@login_required
def profile(user_id=None):
    """User profile view"""
    if user_id:
        user = User.query.get_or_404(user_id)
    else:
        user = current_user
    
    profile = user.profile
    
    # Create profile if it doesn't exist (for viewing)
    if profile is None:
        profile = Profile(
            user_id=user.id,
            full_name=user.username,  # Default to username
            phone_number='',
            bio='',
            course='',
            graduation_year=None,
            skills='',
            location=''
        )
        db.session.add(profile)
        db.session.commit()
        # Refresh the profile reference
        profile = user.profile
    
    return render_template('profile.html', profile_user=user, profile=profile)

@app.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    """Edit user profile"""
    profile = current_user.profile
    
    # Create profile if it doesn't exist
    if profile is None:
        profile = Profile(
            user_id=current_user.id,
            full_name=current_user.username,  # Default to username
            phone_number='',
            bio='',
            course='',
            graduation_year=None,
            skills='',
            location=''
        )
        db.session.add(profile)
        db.session.commit()
        # Refresh the profile reference
        profile = current_user.profile
    
    if request.method == 'POST':
        profile.full_name = request.form['full_name']
        profile.phone_number = request.form['phone_number']
        profile.bio = request.form['bio']
        profile.course = request.form['course']
        profile.graduation_year = int(request.form['graduation_year']) if request.form['graduation_year'] else None
        profile.skills = request.form['skills']
        profile.location = request.form['location']
        
        # Handle profile picture upload
        if 'profile_picture' in request.files:
            file = request.files['profile_picture']
            if file and file.filename:
                filename = f"profile_{current_user.id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], 'profiles', filename))
                profile.profile_picture = f"profiles/{filename}"
        
        db.session.commit()
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('profile'))
    
    return render_template('edit_profile.html', profile=profile)

@app.route('/connections')
@login_required
def connections():
    """View and manage connections"""
    # Get accepted connections (both directions)
    accepted_connections = db.session.query(Connection).join(User, 
        (Connection.requester_id == User.id) | (Connection.receiver_id == User.id)
    ).filter(
        ((Connection.requester_id == current_user.id) | (Connection.receiver_id == current_user.id)) &
        (Connection.status == 'accepted')
    ).all()
    
    # Get pending connection requests sent by current user
    sent_pending = Connection.query.filter_by(
        requester_id=current_user.id, 
        status='pending'
    ).all()
    
    # Get pending connection requests received by current user
    received_pending = Connection.query.filter_by(
        receiver_id=current_user.id, 
        status='pending'
    ).all()
    
    # Get all connections for stats
    all_connections = Connection.query.filter(
        ((Connection.requester_id == current_user.id) | (Connection.receiver_id == current_user.id)) &
        (Connection.status == 'accepted')
    ).all()
    
    # Calculate connection statistics (simplified since user_type doesn't exist)
    student_connections = all_connections  # All connections for now
    alumni_connections = []
    mentor_connections = []
    
    # Get recent connections (this month)
    from datetime import datetime, timezone
    current_month = datetime.now(timezone.utc).month
    recent_connections = [c for c in all_connections if c.created_at.month == current_month]
    
    # Get suggested connections (users not yet connected)
    connected_user_ids = set()
    for conn in all_connections:
        connected_user_ids.add(conn.requester_id)
        connected_user_ids.add(conn.receiver_id)
    
    suggested_connections = User.query.filter(
        User.id != current_user.id,
        ~User.id.in_(connected_user_ids)
    ).join(Profile).all()
    
    return render_template('connections.html', 
                         connections=accepted_connections,
                         sent_pending=sent_pending,
                         received_pending=received_pending,
                         all_connections=all_connections,
                         student_connections=student_connections,
                         alumni_connections=alumni_connections,
                         mentor_connections=mentor_connections,
                         recent_connections=recent_connections,
                         suggested_connections=suggested_connections,
                         recent_activity=[])  # Empty for now

@app.route('/send-connection/<int:user_id>')
@login_required
def send_connection_request(user_id):
    """Send connection request"""
    receiver = User.query.get_or_404(user_id)
    
    if current_user.id != receiver.id:
        # Check if connection already exists
        existing = Connection.query.filter_by(
            requester_id=current_user.id, 
            receiver_id=receiver.id
        ).first()
        
        if not existing:
            connection = Connection(
                requester_id=current_user.id,
                receiver_id=receiver.id,
                status='pending'
            )
            db.session.add(connection)
            db.session.commit()
            flash(f'Connection request sent to {receiver.username}', 'success')
        else:
            flash('Connection request already exists', 'info')
    
    return redirect(url_for('profile', user_id=user_id))

@app.route('/accept-connection/<int:connection_id>')
@login_required
def accept_connection(connection_id):
    """Accept a connection request"""
    connection = Connection.query.get_or_404(connection_id)
    
    # Check if current user is the receiver
    if connection.receiver_id != current_user.id:
        flash('You are not authorized to accept this connection request.', 'error')
        return redirect(url_for('connections'))
    
    connection.status = 'accepted'
    db.session.commit()
    
    flash('Connection request accepted!', 'success')
    return redirect(url_for('connections'))

@app.route('/reject-connection/<int:connection_id>')
@login_required
def reject_connection(connection_id):
    """Reject a connection request"""
    connection = Connection.query.get_or_404(connection_id)
    
    # Check if current user is the receiver
    if connection.receiver_id != current_user.id:
        flash('You are not authorized to reject this connection request.', 'error')
        return redirect(url_for('connections'))
    
    connection.status = 'rejected'
    db.session.commit()
    
    flash('Connection request rejected.', 'info')
    return redirect(url_for('connections'))


@app.route('/messages')
@login_required
def messages_list():
    """View messages"""
    # Get conversations
    sent_messages = Message.query.filter_by(sender_id=current_user.id).all()
    received_messages = Message.query.filter_by(receiver_id=current_user.id).all()
    
    # Group by conversation partner
    conversation_partners = {}
    
    for message in sent_messages:
        partner = message.receiver
        if partner.id not in conversation_partners:
            conversation_partners[partner.id] = {
                'partner': partner,
                'last_message': message,
                'unread_count': 0
            }
    
    for message in received_messages:
        partner = message.sender
        if partner.id not in conversation_partners:
            conversation_partners[partner.id] = {
                'partner': partner,
                'last_message': message,
                'unread_count': 0
            }
        if not message.is_read:
            conversation_partners[partner.id]['unread_count'] += 1
    
    return render_template('messages.html', conversations=conversation_partners.values())

@app.route('/messages/<int:user_id>', methods=['GET', 'POST'])
@login_required
def message_detail(user_id):
    """Message conversation with specific user"""
    other_user = User.query.get_or_404(user_id)
    
    # Mark messages as read
    Message.query.filter_by(sender_id=other_user.id, receiver_id=current_user.id, is_read=False).update({'is_read': True})
    db.session.commit()
    
    # Get messages
    messages = Message.query.filter(
        ((Message.sender_id == current_user.id) & (Message.receiver_id == other_user.id)) |
        ((Message.sender_id == other_user.id) & (Message.receiver_id == current_user.id))
    ).order_by(Message.created_at).all()
    
    if request.method == 'POST':
        content = request.form['content']
        message = Message(
            sender_id=current_user.id,
            receiver_id=other_user.id,
            content=content
        )
        db.session.add(message)
        db.session.commit()
        return redirect(url_for('message_detail', user_id=user_id))
    
    return render_template('message_detail.html', other_user=other_user, messages=messages)

@app.route('/forum')
def forum_list():
    """List all forum posts"""
    page = request.args.get('page', 1, type=int)
    forums = Forum.query.order_by(Forum.created_at.desc()).paginate(
        page=page, per_page=10, error_out=False
    )
    
    # Calculate total replies across all forums
    total_replies = 0
    if forums.items:
        for forum in forums.items:
            total_replies += forum.get_reply_count()
    
    return render_template('forum_list.html', forums=forums, total_replies=total_replies)

@app.route('/forum/<int:forum_id>', methods=['GET', 'POST'])
def forum_detail(forum_id):
    """Forum post detail with replies"""
    forum = Forum.query.get_or_404(forum_id)
    replies = ForumReply.query.filter_by(forum_id=forum_id).order_by(ForumReply.created_at).all()
    
    if request.method == 'POST' and current_user.is_authenticated:
        content = request.form['content']
        reply = ForumReply(
            forum_id=forum_id,
            user_id=current_user.id,
            content=content
        )
        db.session.add(reply)
        db.session.commit()
        return redirect(url_for('forum_detail', forum_id=forum_id))
    
    return render_template('forum_detail.html', forum=forum, replies=replies)

@app.route('/create-forum-post', methods=['GET', 'POST'])
@login_required
def create_forum_post():
    """Create new forum post"""
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        forum = Forum(
            title=title,
            content=content,
            author_id=current_user.id
        )
        db.session.add(forum)
        db.session.commit()
        flash('Forum post created successfully!', 'success')
        return redirect(url_for('forum_detail', forum_id=forum.id))
    
    return render_template('create_forum_post.html')

@app.route('/jobs')
def jobs_list():
    """List all job postings"""
    page = request.args.get('page', 1, type=int)
    # Get current time for comparison
    now = datetime.now(timezone.utc)
    jobs = Job.query.filter(Job.deadline >= now).order_by(Job.created_at.desc()).paginate(
        page=page, per_page=10, error_out=False
    )
    return render_template('jobs_list.html', jobs=jobs)

@app.route('/jobs/<int:job_id>')
def job_detail(job_id):
    """Job posting detail"""
    job = Job.query.get_or_404(job_id)
    return render_template('job_detail.html', job=job)

@app.route('/create-job', methods=['GET', 'POST'])
@login_required
def create_job():
    """Create new job posting"""
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        company = request.form['company']
        location = request.form['location']
        job_type = request.form['job_type']
        # Parse datetime and make it timezone-aware
        deadline = datetime.fromisoformat(request.form['deadline'].replace('T', ' '))
        deadline = deadline.replace(tzinfo=timezone.utc)
        
        job = Job(
            title=title,
            description=description,
            company=company,
            location=location,
            job_type=job_type,
            deadline=deadline,
            posted_by_id=current_user.id
        )
        db.session.add(job)
        db.session.commit()
        flash('Job posting created successfully!', 'success')
        return redirect(url_for('job_detail', job_id=job.id))
    
    return render_template('create_job.html')

@app.route('/events')
def events_list():
    """List all events"""
    page = request.args.get('page', 1, type=int)
    events = Event.query.order_by(Event.event_date).paginate(
        page=page, per_page=10, error_out=False
    )
    return render_template('events_list.html', events=events)

@app.route('/events/<int:event_id>')
def event_detail(event_id):
    """Event detail"""
    event = Event.query.get_or_404(event_id)
    participants = EventParticipant.query.filter_by(event_id=event_id).all()
    
    user_participation = None
    if current_user.is_authenticated:
        user_participation = EventParticipant.query.filter_by(
            event_id=event_id, user_id=current_user.id
        ).first()
    
    return render_template('event_detail.html', 
                         event=event, 
                         participants=participants,
                         user_participation=user_participation)

@app.route('/join-event/<int:event_id>')
@login_required
def join_event(event_id):
    """Join an event"""
    event = Event.query.get_or_404(event_id)
    
    # Check if already participating
    existing = EventParticipant.query.filter_by(
        event_id=event_id, user_id=current_user.id
    ).first()
    
    if not existing:
        participation = EventParticipant(
            event_id=event_id,
            user_id=current_user.id,
            status='attending'
        )
        db.session.add(participation)
        db.session.commit()
        flash(f'You are now attending {event.title}', 'success')
    else:
        flash('You are already registered for this event', 'info')
    
    return redirect(url_for('event_detail', event_id=event_id))

@app.route('/leave-event/<int:event_id>')
@login_required
def leave_event(event_id):
    """Leave an event"""
    event = Event.query.get_or_404(event_id)
    EventParticipant.query.filter_by(event_id=event_id, user_id=current_user.id).delete()
    db.session.commit()
    flash(f'You have left {event.title}', 'info')
    return redirect(url_for('event_detail', event_id=event_id))

@app.route('/search-users')
@login_required
def search_users():
    """Search for users to connect with"""
    query = request.args.get('q', '')
    major = request.args.get('major', '')
    user_type = request.args.get('user_type', '')
    graduation_year = request.args.get('graduation_year', '')
    
    # Start with all profiles excluding current user
    profiles_query = Profile.query.filter(Profile.user_id != current_user.id)
    
    # Apply filters using database queries
    if query:
        profiles_query = profiles_query.join(User).filter(
            db.or_(
                Profile.full_name.ilike(f'%{query}%'),
                User.username.ilike(f'%{query}%')
            )
        )
    
    if major:
        profiles_query = profiles_query.filter(Profile.major.ilike(f'%{major}%'))
    
    if user_type:
        profiles_query = profiles_query.filter(Profile.user_type == user_type)
    
    if graduation_year:
        try:
            graduation_year_int = int(graduation_year)
            profiles_query = profiles_query.filter(Profile.graduation_year == graduation_year_int)
        except ValueError:
            pass  # Invalid graduation year, ignore filter
    
    profiles = profiles_query.all()
    
    return render_template('search_users.html', 
                         profiles=profiles,
                         query=query,
                         major=major,
                         user_type=user_type,
                         graduation_year=graduation_year)

@app.route('/create-event', methods=['GET', 'POST'])
@login_required
def create_event():
    """Create new event"""
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        # Parse datetime and make it timezone-aware
        event_date = datetime.fromisoformat(request.form['event_date'].replace('T', ' '))
        event_date = event_date.replace(tzinfo=timezone.utc)
        location = request.form['location']
        
        event = Event(
            title=title,
            description=description,
            event_date=event_date,
            location=location,
            created_by_id=current_user.id
        )
        db.session.add(event)
        db.session.commit()
        flash('Event created successfully!', 'success')
        return redirect(url_for('event_detail', event_id=event.id))
    
    return render_template('create_event.html')

@app.route('/edit-event/<int:event_id>', methods=['GET', 'POST'])
@login_required
def edit_event(event_id):
    """Edit event (only by creator)"""
    event = Event.query.get_or_404(event_id)
    
    # Check if user is the creator
    if event.created_by_id != current_user.id:
        flash('You can only edit events you created.', 'error')
        return redirect(url_for('event_detail', event_id=event_id))
    
    if request.method == 'POST':
        event.title = request.form['title']
        event.description = request.form['description']
        # Parse datetime and make it timezone-aware
        event_date = datetime.fromisoformat(request.form['event_date'].replace('T', ' '))
        event.event_date = event_date.replace(tzinfo=timezone.utc)
        event.location = request.form['location']
        
        db.session.commit()
        flash('Event updated successfully!', 'success')
        return redirect(url_for('event_detail', event_id=event.id))
    
    # Pre-fill form with current values
    event_date_formatted = event.event_date.strftime('%Y-%m-%dT%H:%M')
    return render_template('edit_event.html', event=event, event_date_formatted=event_date_formatted)

@app.route('/delete-job/<int:job_id>')
@login_required
def delete_job(job_id):
    """Delete job (only by creator)"""
    job = Job.query.get_or_404(job_id)
    
    # Check if user is the creator
    if job.posted_by_id != current_user.id:
        flash('You can only delete jobs you created.', 'error')
        return redirect(url_for('job_detail', job_id=job_id))
    
    db.session.delete(job)
    db.session.commit()
    flash('Job deleted successfully!', 'success')
    return redirect(url_for('jobs_list'))

@app.route('/delete-forum/<int:forum_id>')
@login_required
def delete_forum(forum_id):
    """Delete forum post (only by author)"""
    forum = Forum.query.get_or_404(forum_id)
    
    # Check if user is the author
    if forum.author_id != current_user.id:
        flash('You can only delete forum posts you created.', 'error')
        return redirect(url_for('forum_detail', forum_id=forum_id))
    
    db.session.delete(forum)
    db.session.commit()
    flash('Forum post deleted successfully!', 'success')
    return redirect(url_for('forum_list'))

@app.route('/delete-event/<int:event_id>')
@login_required
def delete_event(event_id):
    """Delete event (only by creator)"""
    event = Event.query.get_or_404(event_id)
    
    # Check if user is the creator
    if event.created_by_id != current_user.id:
        flash('You can only delete events you created.', 'error')
        return redirect(url_for('event_detail', event_id=event_id))
    
    db.session.delete(event)
    db.session.commit()
    flash('Event deleted successfully!', 'success')
    return redirect(url_for('events_list'))

@app.route('/create-announcement', methods=['GET', 'POST'])
@login_required
def create_announcement():
    """Create new announcement (admin only)"""
    # Check if user is admin
    if not current_user.is_admin:
        flash('Only administrators can create announcements.', 'error')
        return redirect(url_for('announcements_list'))
    
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        announcement_type = request.form.get('announcement_type', 'general')
        
        announcement = Announcement(
            title=title,
            content=content,
            announcement_type=announcement_type,
            created_by_id=current_user.id
        )
        db.session.add(announcement)
        db.session.commit()
        flash('Announcement created successfully!', 'success')
        return redirect(url_for('announcements_list'))
    
    return render_template('create_announcement.html')

@app.route('/edit-announcement/<int:announcement_id>', methods=['GET', 'POST'])
@login_required
def edit_announcement(announcement_id):
    """Edit announcement (admin only)"""
    announcement = Announcement.query.get_or_404(announcement_id)
    
    # Check if user is admin
    if not current_user.is_admin:
        flash('Only administrators can edit announcements.', 'error')
        return redirect(url_for('announcements_list'))
    
    if request.method == 'POST':
        announcement.title = request.form['title']
        announcement.content = request.form['content']
        announcement.announcement_type = request.form.get('announcement_type', 'general')
        
        db.session.commit()
        flash('Announcement updated successfully!', 'success')
        return redirect(url_for('announcements_list'))
    
    return render_template('edit_announcement.html', announcement=announcement)

@app.route('/delete-announcement/<int:announcement_id>')
@login_required
def delete_announcement(announcement_id):
    """Delete announcement (admin only)"""
    announcement = Announcement.query.get_or_404(announcement_id)
    
    # Check if user is admin
    if not current_user.is_admin:
        flash('Only administrators can delete announcements.', 'error')
        return redirect(url_for('announcements_list'))
    
    db.session.delete(announcement)
    db.session.commit()
    flash('Announcement deleted successfully!', 'success')
    return redirect(url_for('announcements_list'))

@app.route('/announcements')
def announcements_list():
    """List all announcements"""
    announcements = Announcement.query.order_by(Announcement.created_at.desc()).all()
    return render_template('announcements_list.html', announcements=announcements)

# Error handlers
@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500

@app.context_processor
def inject_user():
    pending_count = 0
    if current_user.is_authenticated:
        pending_count = Connection.query.filter_by(
            receiver_id=current_user.id, 
            status='pending'
        ).count()
    return dict(current_user=current_user, pending_connections_count=pending_count)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)