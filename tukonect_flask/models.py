from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime, timezone
from werkzeug.security import generate_password_hash, check_password_hash

# This will be initialized in app.py
db = SQLAlchemy()

class User(UserMixin, db.Model):
    """User model for authentication"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    is_active = db.Column(db.Boolean, default=True)
    is_admin = db.Column(db.Boolean, default=False, nullable=False)
    date_joined = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    
    # Relationships
    profile = db.relationship('Profile', backref='user', uselist=False, cascade='all, delete-orphan')
    sent_connections = db.relationship('Connection', foreign_keys='Connection.requester_id', backref='requester', cascade='all, delete-orphan')
    received_connections = db.relationship('Connection', foreign_keys='Connection.receiver_id', backref='receiver', cascade='all, delete-orphan')
    sent_messages = db.relationship('Message', foreign_keys='Message.sender_id', backref='sender', cascade='all, delete-orphan')
    received_messages = db.relationship('Message', foreign_keys='Message.receiver_id', backref='receiver', cascade='all, delete-orphan')
    forum_posts = db.relationship('Forum', backref='author', cascade='all, delete-orphan')
    forum_replies = db.relationship('ForumReply', backref='user', cascade='all, delete-orphan')
    posted_jobs = db.relationship('Job', backref='posted_by', cascade='all, delete-orphan')
    mentor_relationships = db.relationship('Mentorship', foreign_keys='Mentorship.mentor_id', backref='mentor', cascade='all, delete-orphan')
    mentee_relationships = db.relationship('Mentorship', foreign_keys='Mentorship.mentee_id', backref='mentee', cascade='all, delete-orphan')
    created_events = db.relationship('Event', backref='created_by', cascade='all, delete-orphan')
    event_participations = db.relationship('EventParticipant', backref='user', cascade='all, delete-orphan')
    announcements = db.relationship('Announcement', backref='created_by', cascade='all, delete-orphan')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.username}>'


class Profile(db.Model):
    """Extended user profile with academic and professional information"""
    __tablename__ = 'profiles'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    phone_number = db.Column(db.String(20))
    bio = db.Column(db.Text)
    profile_picture = db.Column(db.String(200))
    course = db.Column(db.String(100))
    graduation_year = db.Column(db.Integer)
    skills = db.Column(db.Text)
    location = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    
    def get_skills_list(self):
        """Return skills as a list"""
        if self.skills:
            return [skill.strip() for skill in self.skills.split(',')]
        return []
    
    def __repr__(self):
        return f'<Profile {self.full_name}>'


class Connection(db.Model):
    """Friend/connection system between users"""
    __tablename__ = 'connections'
    
    id = db.Column(db.Integer, primary_key=True)
    requester_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    status = db.Column(db.String(10), default='pending')  # pending, accepted, rejected, blocked
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    
    __table_args__ = (db.UniqueConstraint('requester_id', 'receiver_id'),)
    
    def __repr__(self):
        return f'<Connection {self.requester.username} -> {self.receiver.username} ({self.status})>'


class Message(db.Model):
    """Direct messaging between users"""
    __tablename__ = 'messages'
    
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    
    def __repr__(self):
        return f'<Message {self.sender.username} -> {self.receiver.username}>'


class Forum(db.Model):
    """Discussion forums"""
    __tablename__ = 'forums'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    
    # Relationships
    replies = db.relationship('ForumReply', backref='forum', cascade='all, delete-orphan')
    
    def get_reply_count(self):
        return len(self.replies)
    
    def __repr__(self):
        return f'<Forum {self.title}>'


class ForumReply(db.Model):
    """Replies to forum posts"""
    __tablename__ = 'forum_replies'
    
    id = db.Column(db.Integer, primary_key=True)
    forum_id = db.Column(db.Integer, db.ForeignKey('forums.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    
    def __repr__(self):
        return f'<ForumReply by {self.user.username} on {self.forum.title}>'


class Job(db.Model):
    """Job postings"""
    __tablename__ = 'jobs'
    
    id = db.Column(db.Integer, primary_key=True)
    posted_by_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    company = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    job_type = db.Column(db.String(20), nullable=False)  # full-time, part-time, internship, contract, freelance
    deadline = db.Column(db.DateTime, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    
    def is_deadline_passed(self):
        # Ensure deadline is timezone-aware for comparison
        deadline = self.deadline
        if deadline.tzinfo is None:
            deadline = deadline.replace(tzinfo=timezone.utc)
        return datetime.now(timezone.utc) > deadline
    
    def __repr__(self):
        return f'<Job {self.title} at {self.company}>'


class Mentorship(db.Model):
    """Mentor-mentee relationships"""
    __tablename__ = 'mentorships'
    
    id = db.Column(db.Integer, primary_key=True)
    mentor_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    mentee_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    status = db.Column(db.String(20), default='pending')  # pending, active, completed, cancelled
    started_at = db.Column(db.DateTime)
    ended_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    
    __table_args__ = (db.UniqueConstraint('mentor_id', 'mentee_id'),)
    
    def __repr__(self):
        return f'<Mentorship {self.mentor.username} mentors {self.mentee.username} ({self.status})>'


class Event(db.Model):
    """Events and meetups"""
    __tablename__ = 'events'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    event_date = db.Column(db.DateTime, nullable=False)
    location = db.Column(db.String(200), nullable=False)
    created_by_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    
    # Relationships
    participants = db.relationship('EventParticipant', backref='event', cascade='all, delete-orphan')
    
    def get_participant_count(self):
        return len(self.participants)
    
    def is_past_event(self):
        # Ensure event_date is timezone-aware for comparison
        event_date = self.event_date
        if event_date.tzinfo is None:
            event_date = event_date.replace(tzinfo=timezone.utc)
        return datetime.now(timezone.utc) > event_date
    
    def __repr__(self):
        return f'<Event {self.title}>'


class EventParticipant(db.Model):
    """Event participants"""
    __tablename__ = 'event_participants'
    
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    status = db.Column(db.String(20), default='attending')  # attending, maybe, not_attending
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    
    __table_args__ = (db.UniqueConstraint('event_id', 'user_id'),)
    
    def __repr__(self):
        return f'<EventParticipant {self.user.username} - {self.event.title} ({self.status})>'


class Announcement(db.Model):
    """System announcements"""
    __tablename__ = 'announcements'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    announcement_type = db.Column(db.String(20), default='general')  # general, important, urgent, maintenance, update
    created_by_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    
    def __repr__(self):
        return f'<Announcement {self.title}>'

class PasswordResetToken(db.Model):
    """Password reset token model"""
    __tablename__ = 'password_reset_tokens'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    token = db.Column(db.String(100), unique=True, nullable=False)
    expires_at = db.Column(db.DateTime, nullable=False)
    used = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    
    user = db.relationship('User', backref='password_reset_tokens')
    
    def __repr__(self):
        return f'<PasswordResetToken {self.token}>'
