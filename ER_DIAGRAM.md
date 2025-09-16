# 🗄️ Entity Relationship Diagram - Tukonect

## Database Schema Overview

This document provides a comprehensive Entity Relationship Diagram for both the Flask and Django implementations of Tukonect.

## 📊 ER Diagram

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                               TUKONECT DATABASE SCHEMA                          │
└─────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────┐
│      USER       │ ◄────────── Primary Entity
├─────────────────┤
│ PK: id          │
│ username        │
│ email           │
│ password_hash   │
│ is_active       │
│ is_admin        │
│ date_joined     │
└─────────────────┘
         │
         │ 1:1
         ▼
┌─────────────────┐
│     PROFILE     │
├─────────────────┤
│ PK: id          │
│ FK: user_id     │
│ full_name       │
│ phone_number    │
│ bio             │
│ profile_picture │
│ user_type       │
│ major           │
│ course          │
│ graduation_year │
│ skills          │
│ location        │
│ created_at      │
│ updated_at      │
└─────────────────┘

┌─────────────────┐
│   CONNECTION    │
├─────────────────┤
│ PK: id          │
│ FK: requester_id│ ◄───┐
│ FK: receiver_id │ ◄───┤
│ status          │     │
│ created_at      │     │
│ updated_at      │     │
└─────────────────┘     │
                        │
┌─────────────────┐     │     ┌─────────────────┐
│      USER       │ ────┴─────│      USER       │
├─────────────────┤           ├─────────────────┤
│ PK: id          │           │ PK: id          │
│ username        │           │ username        │
│ email           │           │ email           │
│ password_hash   │           │ password_hash   │
│ is_active       │           │ is_active       │
│ is_admin        │           │ is_admin        │
│ date_joined     │           │ date_joined     │
└─────────────────┘           └─────────────────┘
         │                             │
         │ 1:N                         │ 1:N
         ▼                             ▼
┌─────────────────┐           ┌─────────────────┐
│     MESSAGE     │           │     MESSAGE     │
├─────────────────┤           ├─────────────────┤
│ PK: id          │           │ PK: id          │
│ FK: sender_id   │           │ FK: sender_id   │
│ FK: receiver_id │           │ FK: receiver_id │
│ content         │           │ content         │
│ is_read         │           │ is_read         │
│ created_at      │           │ created_at      │
└─────────────────┘           └─────────────────┘

┌─────────────────┐
│      USER       │
├─────────────────┤
│ PK: id          │
│ username        │
│ email           │
│ password_hash   │
│ is_active       │
│ is_admin        │
│ date_joined     │
└─────────────────┘
         │
         │ 1:N
         ▼
┌─────────────────┐
│      FORUM      │
├─────────────────┤
│ PK: id          │
│ FK: author_id   │
│ title           │
│ content         │
│ created_at      │
│ updated_at      │
└─────────────────┘
         │
         │ 1:N
         ▼
┌─────────────────┐
│   FORUM_REPLY   │
├─────────────────┤
│ PK: id          │
│ FK: forum_id    │
│ FK: user_id     │ ◄───────────┐
│ content         │             │
│ created_at      │             │
└─────────────────┘             │
                                │
┌─────────────────┐             │
│      USER       │ ────────────┘
├─────────────────┤
│ PK: id          │
│ username        │
│ email           │
│ password_hash   │
│ is_active       │
│ is_admin        │
│ date_joined     │
└─────────────────┘
         │
         │ 1:N
         ▼
┌─────────────────┐
│       JOB       │
├─────────────────┤
│ PK: id          │
│ FK: posted_by_id│
│ title           │
│ description     │
│ company         │
│ location        │
│ job_type        │
│ deadline        │
│ created_at      │
│ updated_at      │
└─────────────────┘
         │
         │ 1:N
         ▼
┌─────────────────┐
│ JOB_APPLICATION │
├─────────────────┤
│ PK: id          │
│ FK: job_id      │
│ FK: applicant_id│ ◄───────────┐
│ cover_letter    │             │
│ status          │             │
│ applied_at      │             │
│ updated_at      │             │
└─────────────────┘             │
                                │
┌─────────────────┐             │
│      USER       │ ────────────┘
├─────────────────┤
│ PK: id          │
│ username        │
│ email           │
│ password_hash   │
│ is_active       │
│ is_admin        │
│ date_joined     │
└─────────────────┘
         │
         │ 1:N (as mentor)
         ▼
┌─────────────────┐
│   MENTORSHIP    │
├─────────────────┤
│ PK: id          │
│ FK: mentor_id   │ ◄───┐
│ FK: mentee_id   │ ◄───┤
│ status          │     │
│ started_at      │     │
│ ended_at        │     │
│ created_at      │     │
└─────────────────┘     │
                        │
┌─────────────────┐     │     ┌─────────────────┐
│      USER       │ ────┴─────│      USER       │
├─────────────────┤           ├─────────────────┤
│ PK: id          │           │ PK: id          │
│ username        │           │ username        │
│ email           │           │ email           │
│ password_hash   │           │ password_hash   │
│ is_active       │           │ is_active       │
│ is_admin        │           │ is_admin        │
│ date_joined     │           │ date_joined     │
└─────────────────┘           └─────────────────┘
         │                             │
         │ 1:N                         │ 1:N
         ▼                             ▼
┌─────────────────┐           ┌─────────────────┐
│      EVENT      │           │ EVENT_PARTICIPANT│
├─────────────────┤           ├─────────────────┤
│ PK: id          │           │ PK: id          │
│ FK: created_by_id│          │ FK: event_id    │ ◄───┐
│ title           │           │ FK: user_id     │ ◄───┤
│ description     │           │ status          │     │
│ event_date      │           │ created_at      │     │
│ location        │           └─────────────────┘     │
│ created_at      │                                   │
│ updated_at      │                                   │
└─────────────────┘                                   │
         │                                             │
         │ 1:N                                         │
         ▼                                             │
┌─────────────────┐                                   │
│ EVENT_PARTICIPANT│                                   │
├─────────────────┤                                   │
│ PK: id          │                                   │
│ FK: event_id    │ ───────────────────────────────────┘
│ FK: user_id     │ ◄───────────┐
│ status          │             │
│ created_at      │             │
└─────────────────┘             │
                                │
┌─────────────────┐             │
│      USER       │ ────────────┘
├─────────────────┤
│ PK: id          │
│ username        │
│ email           │
│ password_hash   │
│ is_active       │
│ is_admin        │
│ date_joined     │
└─────────────────┘
         │
         │ 1:N
         ▼
┌─────────────────┐
│  ANNOUNCEMENT   │
├─────────────────┤
│ PK: id          │
│ FK: created_by_id│
│ title           │
│ content         │
│ announcement_type│
│ created_at      │
│ updated_at      │
└─────────────────┘

┌─────────────────┐
│      USER       │
├─────────────────┤
│ PK: id          │
│ username        │
│ email           │
│ password_hash   │
│ is_active       │
│ is_admin        │
│ date_joined     │
└─────────────────┘
         │
         │ 1:N
         ▼
┌─────────────────┐
│PASSWORD_RESET_TOKEN│
├─────────────────┤
│ PK: id          │
│ FK: user_id     │
│ token           │
│ expires_at      │
│ used            │
│ created_at      │
└─────────────────┘
```

## 🔗 Relationship Summary

### One-to-One (1:1) Relationships
- **User ↔ Profile**: Each user has exactly one profile

### One-to-Many (1:N) Relationships
- **User → Messages**: A user can send/receive multiple messages
- **User → Forums**: A user can create multiple forum posts
- **User → Forum Replies**: A user can create multiple forum replies
- **User → Jobs**: A user can post multiple jobs
- **User → Job Applications**: A user can apply to multiple jobs
- **User → Events**: A user can create multiple events
- **User → Event Participants**: A user can participate in multiple events
- **User → Announcements**: A user can create multiple announcements
- **User → Password Reset Tokens**: A user can have multiple reset tokens
- **Forum → Forum Replies**: A forum post can have multiple replies
- **Job → Job Applications**: A job can have multiple applications
- **Event → Event Participants**: An event can have multiple participants

### Many-to-Many (M:N) Relationships
- **User ↔ User (Connections)**: Users can be connected to multiple other users
- **User ↔ User (Mentorship)**: Users can mentor/be mentored by multiple users
- **User ↔ Event (Participation)**: Users can participate in multiple events

## 📋 Entity Descriptions

### Core Entities

#### User
- **Primary Key**: id
- **Description**: Main user entity for authentication and user management
- **Key Attributes**: username, email, password_hash, is_admin, is_active

#### Profile
- **Primary Key**: id
- **Foreign Key**: user_id → User.id
- **Description**: Extended user information including academic and professional details
- **Key Attributes**: full_name, user_type, major, course, graduation_year, skills, location

### Social Networking Entities

#### Connection
- **Primary Key**: id
- **Foreign Keys**: requester_id → User.id, receiver_id → User.id
- **Description**: Friend/connection system between users
- **Key Attributes**: status (pending, accepted, rejected, blocked)

#### Message
- **Primary Key**: id
- **Foreign Keys**: sender_id → User.id, receiver_id → User.id
- **Description**: Direct messaging between users
- **Key Attributes**: content, is_read

### Content Entities

#### Forum
- **Primary Key**: id
- **Foreign Key**: author_id → User.id
- **Description**: Discussion forum posts
- **Key Attributes**: title, content

#### Forum Reply
- **Primary Key**: id
- **Foreign Keys**: forum_id → Forum.id, user_id → User.id
- **Description**: Replies to forum posts
- **Key Attributes**: content

### Career Development Entities

#### Job
- **Primary Key**: id
- **Foreign Key**: posted_by_id → User.id
- **Description**: Job postings
- **Key Attributes**: title, description, company, location, job_type, deadline

#### Job Application
- **Primary Key**: id
- **Foreign Keys**: job_id → Job.id, applicant_id → User.id
- **Description**: Job applications with status tracking
- **Key Attributes**: cover_letter, status (pending, reviewed, shortlisted, rejected, hired)

### Event Management Entities

#### Event
- **Primary Key**: id
- **Foreign Key**: created_by_id → User.id
- **Description**: Events and meetups
- **Key Attributes**: title, description, event_date, location

#### Event Participant
- **Primary Key**: id
- **Foreign Keys**: event_id → Event.id, user_id → User.id
- **Description**: Event participation tracking
- **Key Attributes**: status (attending, maybe, not_attending)

### Mentorship Entities

#### Mentorship
- **Primary Key**: id
- **Foreign Keys**: mentor_id → User.id, mentee_id → User.id
- **Description**: Mentor-mentee relationships
- **Key Attributes**: status (pending, active, completed, cancelled), started_at, ended_at

### System Entities

#### Announcement
- **Primary Key**: id
- **Foreign Key**: created_by_id → User.id
- **Description**: System announcements
- **Key Attributes**: title, content, announcement_type

#### Password Reset Token
- **Primary Key**: id
- **Foreign Key**: user_id → User.id
- **Description**: Password reset functionality
- **Key Attributes**: token, expires_at, used

## 🔄 Database Differences Between Flask and Django

### Flask Implementation
- Uses SQLAlchemy ORM
- Custom User model with UserMixin
- Explicit relationship definitions with backref
- Custom table names with `__tablename__`

### Django Implementation
- Uses Django's built-in User model
- Django ORM with related_name for relationships
- Built-in admin interface
- Automatic table naming

### Key Similarities
- Same entity structure and relationships
- Similar field types and constraints
- Same business logic and data flow
- Identical foreign key relationships

## 📊 Indexes and Constraints

### Unique Constraints
- **Connection**: (requester_id, receiver_id) - prevents duplicate connections
- **Job Application**: (job_id, applicant_id) - prevents duplicate applications
- **Mentorship**: (mentor_id, mentee_id) - prevents duplicate mentorship relationships
- **Event Participant**: (event_id, user_id) - prevents duplicate event participation
- **Password Reset Token**: token - ensures unique reset tokens

### Foreign Key Constraints
- All foreign keys have CASCADE delete behavior
- Ensures referential integrity
- Automatic cleanup when parent records are deleted

## 🚀 Performance Considerations

### Recommended Indexes
- **User**: username, email
- **Connection**: requester_id, receiver_id, status
- **Message**: sender_id, receiver_id, created_at
- **Job**: posted_by_id, deadline, created_at
- **Event**: event_date, created_by_id

### Query Optimization
- Use select_related() for foreign key relationships
- Use prefetch_related() for reverse foreign key relationships
- Implement pagination for large result sets
- Add database indexes for frequently queried fields

---

**Note**: This ER diagram represents the complete database schema for both Flask and Django implementations of Tukonect. The relationships and constraints ensure data integrity and support all platform functionality.
