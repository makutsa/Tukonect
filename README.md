# 🎓 Tukonect - Student Social Network Platform

<div align="center">
  <img src="https://img.shields.io/badge/Flask-2.3.3-green.svg" alt="Flask Version">
  <img src="https://img.shields.io/badge/Django-4.2.7-blue.svg" alt="Django Version">
  <img src="https://img.shields.io/badge/Bootstrap-5.1.3-purple.svg" alt="Bootstrap Version">
  <img src="https://img.shields.io/badge/Python-3.11+-yellow.svg" alt="Python Version">
  <img src="https://img.shields.io/badge/License-MIT-orange.svg" alt="License">
</div>

A comprehensive student social network platform built with both Django and Flask frameworks, designed to connect students, facilitate knowledge sharing, and provide career opportunities.

## 📋 Table of Contents

- [🌟 Features](#-features)
- [🚀 Quick Start](#-quick-start)
- [📁 Project Structure](#-project-structure)
- [🛠️ Technology Stack](#️-technology-stack)
- [📋 Available Pages](#-available-pages)
- [🎯 Key Features](#-key-features)
- [🔧 Development](#-development)
- [📱 Mobile Support](#-mobile-support)
- [🎨 UI/UX Features](#-uiux-features)
- [🔒 Security Features](#-security-features)
- [🚀 Deployment](#-deployment)
- [🤝 Contributing](#-contributing)
- [📄 License](#-license)
- [📞 Support](#-support)
- [🎉 Acknowledgments](#-acknowledgments)

## 🌟 Features

### 👥 **User Management**
- User registration and authentication
- Profile management with photo uploads
- User search and filtering by course, graduation year
- Connection system (send/accept/reject requests)
- Admin panel for user management
- Password reset functionality
- User status management (active/inactive)

### 💬 **Communication**
- Direct messaging between users
- Forum discussions with replies
- Real-time notifications
- Connection request management
- Social media sharing (LinkedIn, Twitter/X, Email)
- Message history and persistence

### 💼 **Career Development**
- Job posting and browsing
- Job application system with status tracking
- Event creation and management
- Professional networking opportunities
- Skills and interests tracking
- Application management (hire, shortlist, reject)

### 📱 **Responsive Design**
- Mobile-first Bootstrap 5.1.3 design
- Touch-friendly interface
- Works perfectly on all devices (desktop, tablet, mobile)
- Dark/Light mode support with persistence
- Sidebar navigation for better UX

## 🚀 Quick Start

### ⚡ 5-Minute Setup

#### Prerequisites
- Python 3.11 or higher
- pip (Python package installer)
- Git installed
- Internet connection

#### Step 1: Clone the Repository
```bash
git clone https://github.com/makutsa/Tukonect.git
cd Tukonect
```

#### Step 2: Set Up Flask Application (Recommended)
```bash
cd tukonect_flask
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate

pip install -r requirements.txt
```

#### Step 3: Run the Application
```bash
python app.py
```

#### Step 4: Access the Application
Open your browser and go to: **http://localhost:5000**

### 🎯 First Steps

#### 1. Create an Account
- Click "Register" in the top navigation
- Fill in your details
- Click "Register"

#### 2. Create Admin User (Optional)
- Visit: http://localhost:5000/create-admin
- Login with: `admin` / `admin123`
- Access admin panel at: http://localhost:5000/admin

#### 3. Complete Your Profile
- Click on your username in the navigation
- Select "Edit Profile"
- Add your information and upload a photo
- Click "Update Profile"

#### 4. Explore the Platform
- **Home**: View announcements and recent activity
- **Connections**: Manage your network
- **Search Users**: Find other students
- **Forum**: Join discussions
- **Jobs**: Browse job opportunities
- **Events**: Find and create events

### 🔧 Alternative Setup (Django)

If you prefer Django:

```bash
cd tukonect_django
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate

pip install -r requirements.txt
python manage.py migrate
python manage.py runserver 8000
```

Access at: **http://localhost:8000**

## 📁 Project Structure

```
Tukonect/
├── README.md                          # This comprehensive documentation
├── tukonect_flask/                    # Flask Application (Main)
│   ├── app.py                         # Main Flask application
│   ├── models.py                      # Database models
│   ├── templates/                     # HTML templates
│   ├── static/                        # Static files (CSS, JS, uploads)
│   ├── instance/                      # Flask instance folder
│   │   └── tukonect.db                # Flask database
│   ├── requirements.txt               # Flask dependencies
│   └── venv/                          # Flask virtual environment
└── tukonect_django/                   # Django Application (Alternative)
    ├── core/                          # Main Django app
    ├── templates/                     # HTML templates
    ├── static/                        # Static files
    ├── media/                         # User uploaded files
    ├── migrations/                    # Database migrations
    ├── tukonect/                      # Django project settings
    ├── manage.py                      # Django management script
    ├── requirements.txt               # Django dependencies
    └── db.sqlite3                     # Django database
```

## 🛠️ Technology Stack

### Flask Application (Main)
- **Framework**: Flask 2.3.3
- **Database**: SQLite with SQLAlchemy
- **Templates**: Jinja2
- **Static Files**: Bootstrap 5.1.3, Font Awesome
- **Authentication**: Flask-Login
- **Admin Panel**: Flask-Admin

### Django Application (Alternative)
- **Framework**: Django 4.2.7
- **Database**: SQLite
- **Templates**: Django Templates
- **Static Files**: Bootstrap 5.1.3, Font Awesome
- **Authentication**: Django built-in auth system

## 📋 Available Pages

### Flask Application (http://localhost:5000/)
- **Home**: `/` - Landing page with features overview
- **Authentication**: 
  - `/register` - User registration
  - `/login` - User login
  - `/logout` - User logout
  - `/forgot-password` - Password reset
- **Profile**: 
  - `/profile` - User profile
  - `/edit-profile` - Edit profile
- **Social Features**:
  - `/connections` - User connections with pending requests
  - `/messages` - Direct messaging
  - `/search-users` - Search for users
- **Content**:
  - `/forum` - Forum discussions
  - `/jobs` - Job listings with application system
  - `/events` - Event listings
  - `/announcements` - System announcements
- **Admin**:
  - `/admin` - Admin panel (admin users only)
  - `/admin/users` - User management

## 🎯 Key Features

### User Management
- **Registration**: Create new user accounts
- **Authentication**: Secure login/logout system
- **Profile Management**: Upload photos, update information
- **User Search**: Find users by name, course, graduation year
- **Admin Panel**: Manage users, content, and system settings
- **Password Reset**: Secure password recovery system

### Social Networking
- **Connections**: Send/accept/reject connection requests
- **Messaging**: Direct messages between connected users
- **Forums**: Create and participate in discussions
- **User Discovery**: Search and filter users
- **Notifications**: Real-time connection request notifications
- **Unfriend**: Remove accepted connections
- **Social Sharing**: Share content on LinkedIn, Twitter/X, Email

### Career Development
- **Job Postings**: Create and browse job opportunities
- **Job Applications**: Apply for jobs with cover letters
- **Application Management**: Job posters can hire, shortlist, reject applicants
- **Events**: Create and join networking events
- **Professional Profiles**: Showcase skills and experience

### Responsive Design
- **Mobile-First**: Optimized for mobile devices
- **Bootstrap 5.1.3**: Modern, responsive UI framework
- **Font Awesome**: Professional icons throughout
- **Touch-Friendly**: Easy to use on tablets and phones
- **Dark/Light Mode**: Theme switching with persistence
- **Sidebar Navigation**: Improved navigation experience

## 🔧 Development

### Running in Development Mode

**Flask (Recommended):**
```bash
cd tukonect_flask
venv\Scripts\activate
python app.py
```

**Django (Alternative):**
```bash
cd tukonect_django
venv\Scripts\activate
python manage.py runserver 8000
```

### Database Management

**Flask:**
The database is automatically created when you first run the application.

**Django:**
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

### Creating Admin User

**Flask:**
1. Visit: http://localhost:5000/create-admin
2. Login with: `admin` / `admin123`
3. Access admin panel at: http://localhost:5000/admin

## 📱 Mobile Support

The applications are fully responsive and work perfectly on:
- 📱 Mobile phones (iOS, Android)
- 📱 Tablets (iPad, Android tablets)
- 💻 Desktop computers (Windows, macOS, Linux)

## 🎨 UI/UX Features

- **Modern Design**: Clean, professional interface
- **Bootstrap 5.1.3**: Responsive grid system
- **Font Awesome Icons**: Consistent iconography
- **Color Scheme**: Professional blue and white theme
- **Typography**: Clear, readable fonts
- **Navigation**: Intuitive sidebar menu system
- **Dark/Light Mode**: Theme switching capability
- **Accessibility**: WCAG 2.1 compliance features

## 🔒 Security Features

- **Authentication**: Secure user login system
- **Authorization**: Protected routes and views
- **File Uploads**: Secure image upload handling
- **CSRF Protection**: Cross-site request forgery protection
- **Input Validation**: Form validation and sanitization
- **Admin Access Control**: Restricted admin panel access
- **Password Hashing**: Secure password storage

## 🚀 Deployment

### Production Considerations

1. **Database**: Consider using PostgreSQL or MySQL for production
2. **Static Files**: Use a CDN for static file serving
3. **Media Files**: Use cloud storage for user uploads
4. **Environment Variables**: Use environment variables for sensitive settings
5. **HTTPS**: Enable SSL/TLS for secure connections

### Environment Setup

Create `.env` files for each application with production settings:

**Flask (.env):**
```
FLASK_ENV=production
SECRET_KEY=your-secret-key
DATABASE_URL=your-database-url
```

**Django (.env):**
```
DEBUG=False
SECRET_KEY=your-secret-key
DATABASE_URL=your-database-url
```

## 🤝 Contributing

### Code of Conduct

We are committed to providing a welcoming and inclusive environment for all contributors. By participating in this project, you agree to:
- Be respectful and inclusive
- Accept constructive criticism gracefully
- Focus on what's best for the community
- Show empathy towards other community members

### Getting Started

1. **Fork the Repository**
   ```bash
   # Fork on GitHub, then clone your fork
   git clone https://github.com/makutsa/Tukonect.git
   cd Tukonect
   ```

2. **Set up Development Environment**
   ```bash
   cd tukonect_flask
   python -m venv venv
   venv\Scripts\activate  # On Windows
   # source venv/bin/activate  # On macOS/Linux
   pip install -r requirements.txt
   ```

3. **Create a Branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

4. **Make Your Changes**
   - Write clean, readable code
   - Follow PEP 8 coding standards
   - Add tests for new functionality
   - Update documentation as needed

5. **Test Your Changes**
   ```bash
   # Run the application and test manually
   python app.py
   ```

6. **Submit a Pull Request**
   ```bash
   git add .
   git commit -m "Add feature: brief description of changes"
   git push origin feature/your-feature-name
   ```

### Coding Standards

#### Python Code Style
We follow PEP 8 with some modifications:

```python
# Good
def create_user_profile(user_id, full_name, email):
    """Create a new user profile.
    
    Args:
        user_id (int): The user's ID
        full_name (str): The user's full name
        email (str): The user's email address
    
    Returns:
        Profile: The created profile object
    """
    profile = Profile(
        user_id=user_id,
        full_name=full_name,
        email=email
    )
    db.session.add(profile)
    db.session.commit()
    return profile
```

#### HTML/CSS Standards
```html
<!-- Good -->
<div class="card mb-4">
    <div class="card-header">
        <h5 class="card-title">User Profile</h5>
    </div>
    <div class="card-body">
        <p class="card-text">Profile information goes here.</p>
    </div>
</div>
```

### Issue Reporting

Before creating an issue:
1. Check if the issue already exists
2. Search the documentation
3. Try to reproduce the issue
4. Check if it's a duplicate

Use this template for bug reports:
```markdown
**Describe the bug**
A clear and concise description of what the bug is.

**To Reproduce**
Steps to reproduce the behavior:
1. Go to '...'
2. Click on '....'
3. Scroll down to '....'
4. See error

**Expected behavior**
A clear and concise description of what you expected to happen.

**Environment:**
- OS: [e.g. Windows 10, macOS 12.0, Ubuntu 20.04]
- Python version: [e.g. 3.11.0]
- Browser: [e.g. Chrome 91, Firefox 89]
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📞 Support

For support or questions:
- Create an issue in the repository
- Contact the development team
- Check the documentation

## 🎉 Acknowledgments

- Bootstrap for the responsive UI framework
- Font Awesome for the icon library
- Flask and Django communities for excellent documentation
- All contributors who helped build this platform

---

## 📝 Changelog

### [1.2.0] - 2024-01-15

#### Added
- **Admin Panel**: Complete admin interface for user management
- **Connection System**: Enhanced social networking features
- **Profile Management**: Improved user profiles
- **Forum System**: Discussion platform
- **Messaging System**: Direct communication
- **Job Application System**: Complete job application workflow
- **Social Sharing**: LinkedIn, Twitter/X, Email sharing
- **Dark/Light Mode**: Theme switching capability
- **Sidebar Navigation**: Improved navigation experience
- **Password Reset**: Secure password recovery

#### Changed
- **Database Models**: Updated and optimized
- **Templates**: Enhanced user interface
- **Security**: Enhanced security measures

#### Fixed
- **Profile Issues**: Fixed NoneType errors
- **Template Errors**: Fixed rendering issues
- **Connection System**: Fixed request handling

### [1.1.0] - 2024-01-10

#### Added
- **User Authentication**: Complete auth system
- **Profile System**: User profile management
- **Basic UI**: Initial user interface

#### Changed
- **Project Structure**: Organized codebase

#### Fixed
- **Initial Setup**: Fixed project initialization

### [1.0.0] - 2024-01-01

#### Added
- **Initial Release**: First version of Tukonect
- **Core Features**: Essential functionality
- **Documentation**: Initial documentation

---

**Built with ❤️ for students, by students**

*Tukonect - Connecting Students, Building Futures* 🎓✨
=======
# Tukonect
Tukonect is a Django-based social networking platform designed for students and alumni. It enables users to create accounts, build profiles, connect with peers, and engage with their school community. The system supports features such as posting updates, managing connections, and fostering collaboration between current students and graduates
 83a04f05e75e6d8df74a776f42f720e89491e8bb
