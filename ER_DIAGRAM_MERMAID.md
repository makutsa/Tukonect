# 🗄️ Tukonect ER Diagram - Mermaid Version

## Visual Entity Relationship Diagram

```mermaid
erDiagram
    USER {
        int id PK
        string username UK
        string email UK
        string password_hash
        boolean is_active
        boolean is_admin
        datetime date_joined
    }
    
    PROFILE {
        int id PK
        int user_id FK
        string full_name
        string phone_number
        text bio
        string profile_picture
        string user_type
        string major
        string course
        int graduation_year
        text skills
        string location
        datetime created_at
        datetime updated_at
    }
    
    CONNECTION {
        int id PK
        int requester_id FK
        int receiver_id FK
        string status
        datetime created_at
        datetime updated_at
    }
    
    MESSAGE {
        int id PK
        int sender_id FK
        int receiver_id FK
        text content
        boolean is_read
        datetime created_at
    }
    
    FORUM {
        int id PK
        int author_id FK
        string title
        text content
        datetime created_at
        datetime updated_at
    }
    
    FORUM_REPLY {
        int id PK
        int forum_id FK
        int user_id FK
        text content
        datetime created_at
    }
    
    JOB {
        int id PK
        int posted_by_id FK
        string title
        text description
        string company
        string location
        string job_type
        datetime deadline
        datetime created_at
        datetime updated_at
    }
    
    JOB_APPLICATION {
        int id PK
        int job_id FK
        int applicant_id FK
        text cover_letter
        string status
        datetime applied_at
        datetime updated_at
    }
    
    MENTORSHIP {
        int id PK
        int mentor_id FK
        int mentee_id FK
        string status
        datetime started_at
        datetime ended_at
        datetime created_at
    }
    
    EVENT {
        int id PK
        int created_by_id FK
        string title
        text description
        datetime event_date
        string location
        datetime created_at
        datetime updated_at
    }
    
    EVENT_PARTICIPANT {
        int id PK
        int event_id FK
        int user_id FK
        string status
        datetime created_at
    }
    
    ANNOUNCEMENT {
        int id PK
        int created_by_id FK
        string title
        text content
        string announcement_type
        datetime created_at
        datetime updated_at
    }
    
    PASSWORD_RESET_TOKEN {
        int id PK
        int user_id FK
        string token UK
        datetime expires_at
        boolean used
        datetime created_at
    }

    %% Relationships
    USER ||--|| PROFILE : "has"
    USER ||--o{ CONNECTION : "requests"
    USER ||--o{ CONNECTION : "receives"
    USER ||--o{ MESSAGE : "sends"
    USER ||--o{ MESSAGE : "receives"
    USER ||--o{ FORUM : "authors"
    USER ||--o{ FORUM_REPLY : "writes"
    USER ||--o{ JOB : "posts"
    USER ||--o{ JOB_APPLICATION : "applies"
    USER ||--o{ MENTORSHIP : "mentors"
    USER ||--o{ MENTORSHIP : "is_mentored_by"
    USER ||--o{ EVENT : "creates"
    USER ||--o{ EVENT_PARTICIPANT : "participates"
    USER ||--o{ ANNOUNCEMENT : "creates"
    USER ||--o{ PASSWORD_RESET_TOKEN : "has"
    
    FORUM ||--o{ FORUM_REPLY : "has"
    JOB ||--o{ JOB_APPLICATION : "receives"
    EVENT ||--o{ EVENT_PARTICIPANT : "has"
```

## How to Use This Diagram

1. **Copy the Mermaid code** from the code block above
2. **Visit any Mermaid renderer**:
   - [Mermaid Live Editor](https://mermaid.live/)
   - [GitHub (supports Mermaid natively)](https://github.com/)
   - [GitLab (supports Mermaid natively)](https://gitlab.com/)
   - [Notion (supports Mermaid)](https://notion.so/)

3. **Export as Image**:
   - PNG: High quality for presentations
   - SVG: Scalable vector format
   - PDF: For documentation

## Alternative: Draw.io Version

If you prefer using Draw.io:

1. Go to [app.diagrams.net](https://app.diagrams.net/)
2. Create a new diagram
3. Use the "Entity Relationship" template
4. Recreate the diagram using the relationships described above

## Database Schema Summary

### Core Entities (10 tables)
- **USER**: Authentication and user management
- **PROFILE**: Extended user information
- **CONNECTION**: Social networking connections
- **MESSAGE**: Direct messaging system

### Content Entities (2 tables)
- **FORUM**: Discussion posts
- **FORUM_REPLY**: Forum post replies

### Career Development (2 tables)
- **JOB**: Job postings
- **JOB_APPLICATION**: Job applications with status tracking

### Event Management (2 tables)
- **EVENT**: Events and meetups
- **EVENT_PARTICIPANT**: Event participation tracking

### Mentorship (1 table)
- **MENTORSHIP**: Mentor-mentee relationships

### System Entities (2 tables)
- **ANNOUNCEMENT**: System announcements
- **PASSWORD_RESET_TOKEN**: Password recovery

### Total: 11 Entities with 19 Relationships

---

**Note**: This Mermaid diagram can be rendered in any Markdown viewer that supports Mermaid (like GitHub, GitLab, Notion) or converted to an image using online tools.
