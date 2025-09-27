# Data Design Document (DDD)
## Flask CRUD Internship Application

---

**Document Version:** 1.0  
**Date:** September 27, 2025  
**Author:** Yashas Patil  
**Project:** Flask CRUD User Management System  
**Repository:** [flask-crud-internship](https://github.com/yashas010/flask-crud-internship)  

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [System Overview](#system-overview)
3. [Database Design](#database-design)
4. [Data Models](#data-models)
5. [Data Flow Architecture](#data-flow-architecture)
6. [API Data Contracts](#api-data-contracts)
7. [Data Validation Rules](#data-validation-rules)
8. [File Storage Strategy](#file-storage-strategy)
9. [Data Security & Privacy](#data-security--privacy)
10. [Performance Considerations](#performance-considerations)
11. [Backup & Recovery](#backup--recovery)
12. [Scalability Planning](#scalability-planning)
13. [Technical Implementation](#technical-implementation)
14. [Appendices](#appendices)

---

## 1. Executive Summary

### 1.1 Purpose
This document outlines the data architecture for a Flask-based CRUD (Create, Read, Update, Delete) web application designed for user management. The system handles user profile data including personal information and photo uploads.

### 1.2 Scope
- **Data Storage**: SQLite database for structured data
- **File Storage**: Local filesystem for photo uploads
- **Data Operations**: Full CRUD operations with real-time search
- **Validation**: Client-side and server-side data validation
- **Security**: Input sanitization and file upload protection

### 1.3 Key Decisions
- **Database**: SQLite chosen for simplicity and deployment ease
- **ORM**: SQLAlchemy for database abstraction
- **File Storage**: Local filesystem with organized directory structure
- **Validation**: Dual-layer validation (frontend + backend)

---

## 2. System Overview

### 2.1 Architecture Pattern
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Backend       │    │   Data Layer    │
│   (HTML/JS)     │◄──►│   (Flask)       │◄──►│   (SQLite)      │
│   - Forms       │    │   - Routes      │    │   - Users       │
│   - Validation  │    │   - Validation  │    │   - Photos      │
│   - Real-time   │    │   - File Mgmt   │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### 2.2 Technology Stack
- **Backend Framework**: Flask 2.3.3
- **ORM**: SQLAlchemy 2.0.43
- **Database**: SQLite 3.x
- **File Handling**: Werkzeug utilities
- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **UI Framework**: Bootstrap 5.3.0

---

## 3. Database Design

### 3.1 Database Schema

#### 3.1.1 Entity Relationship Diagram
```
┌─────────────────────────────────────┐
│                USER                 │
├─────────────────────────────────────┤
│ PK  id          INTEGER             │
│     name        VARCHAR(100)        │
│     dob         VARCHAR(20)         │
│ UK  email       VARCHAR(120)        │
│ UK  mobile      VARCHAR(15)         │
│     photo       VARCHAR(120)        │
│     created_at  TIMESTAMP           │
│     updated_at  TIMESTAMP           │
└─────────────────────────────────────┘

Constraints:
- PK: Primary Key
- UK: Unique Key
- NOT NULL: name, dob, email, mobile
```

#### 3.1.2 Table Structure

**Users Table (`user`)**

| Column | Data Type | Constraints | Description |
|--------|-----------|-------------|-------------|
| `id` | INTEGER | PRIMARY KEY, AUTO_INCREMENT | Unique identifier |
| `name` | VARCHAR(100) | NOT NULL | Full name of user |
| `dob` | VARCHAR(20) | NOT NULL | Date of birth (YYYY-MM-DD) |
| `email` | VARCHAR(120) | NOT NULL, UNIQUE | Email address |
| `mobile` | VARCHAR(15) | NOT NULL, UNIQUE | Phone number with country code |
| `photo` | VARCHAR(120) | NULLABLE | Filename of uploaded photo |

### 3.2 Database Configuration

**Connection String:**
```python
# Development
SQLALCHEMY_DATABASE_URI = 'sqlite:///users.db'

# Production
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///users.db')
```

**SQLAlchemy Settings:**
```python
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ENGINE_OPTIONS = {
    'pool_timeout': 20,
    'pool_recycle': -1,
    'pool_pre_ping': True
}
```

---

## 4. Data Models

### 4.1 User Data Model

```python
class User(db.Model):
    __tablename__ = 'user'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    dob = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    mobile = db.Column(db.String(15), unique=True, nullable=False)
    photo = db.Column(db.String(120), nullable=True)
    
    def __repr__(self):
        return f'<User {self.name} - {self.email}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'dob': self.dob,
            'email': self.email,
            'mobile': self.mobile,
            'photo': self.photo
        }
```

### 4.2 Data Type Rationale

| Field | Type Choice | Reasoning |
|-------|-------------|-----------|
| `id` | INTEGER | Auto-incrementing primary key for unique identification |
| `name` | VARCHAR(100) | Supports international names, sufficient length |
| `dob` | VARCHAR(20) | Stores ISO format dates (YYYY-MM-DD) |
| `email` | VARCHAR(120) | Standard email length, supports most email formats |
| `mobile` | VARCHAR(15) | International format (+country code + number) |
| `photo` | VARCHAR(120) | Filename storage, nullable for optional photos |

---

## 5. Data Flow Architecture

### 5.1 Create Operation Flow
```mermaid
graph TD
    A[User Submits Form] --> B[Frontend Validation]
    B --> C{Valid?}
    C -->|No| D[Show Error Messages]
    C -->|Yes| E[Submit to Backend]
    E --> F[Server Validation]
    F --> G{Valid?}
    G -->|No| H[Return Error Response]
    G -->|Yes| I[Save Photo File]
    I --> J[Insert Database Record]
    J --> K[Return Success Response]
    K --> L[Redirect to Users List]
```

### 5.2 Read Operation Flow
```mermaid
graph TD
    A[User Request] --> B{Search Query?}
    B -->|No| C[Fetch All Users]
    B -->|Yes| D[Filter by Name]
    C --> E[Return JSON Response]
    D --> E
    E --> F[Render Table Rows]
    F --> G[Display to User]
```

### 5.3 Update Operation Flow
```mermaid
graph TD
    A[Edit Form Loaded] --> B[Pre-populate Fields]
    B --> C[User Modifies Data]
    C --> D[Frontend Validation]
    D --> E{Valid?}
    E -->|No| F[Show Errors]
    E -->|Yes| G[Submit Changes]
    G --> H[Server Validation]
    H --> I{Valid?}
    I -->|No| J[Return Errors]
    I -->|Yes| K[Update Database]
    K --> L[Handle Photo Update]
    L --> M[Return Success]
```

### 5.4 Delete Operation Flow
```mermaid
graph TD
    A[Delete Button Clicked] --> B[Show Confirmation Modal]
    B --> C{User Confirms?}
    C -->|No| D[Cancel Action]
    C -->|Yes| E[Send Delete Request]
    E --> F[Remove Photo File]
    F --> G[Delete Database Record]
    G --> H[Return Success]
    H --> I[Refresh Users List]
```

---

## 6. API Data Contracts

### 6.1 Request/Response Formats

#### 6.1.1 Create User (POST /)
**Request:**
```http
POST / HTTP/1.1
Content-Type: multipart/form-data

name=John Doe
dob=1990-01-15
email=john@example.com
mobile=+919876543210
photo=<file>
```

**Response (Success):**
```http
HTTP/1.1 302 Found
Location: /users
Set-Cookie: session=...
```

**Response (Error):**
```http
HTTP/1.1 200 OK
Content-Type: text/html

<!-- HTML with error messages -->
```

#### 6.1.2 Search Users (GET /api/search)
**Request:**
```http
GET /api/search?q=john HTTP/1.1
```

**Response:**
```json
[
  {
    "id": 1,
    "name": "John Doe",
    "dob": "1990-01-15",
    "email": "john@example.com",
    "mobile": "+919876543210",
    "photo": "john_profile.jpg"
  }
]
```

#### 6.1.3 Update User (POST /edit/<id>)
**Request:**
```http
POST /edit/1 HTTP/1.1
Content-Type: multipart/form-data

name=John Smith
dob=1990-01-15
email=johnsmith@example.com
mobile=+919876543210
photo=<file>
```

### 6.2 Error Response Format
```json
{
  "status": "error",
  "message": "Validation failed",
  "errors": {
    "email": "Invalid email format",
    "mobile": "Mobile number already registered"
  }
}
```

---

## 7. Data Validation Rules

### 7.1 Client-Side Validation

#### 7.1.1 Name Field
- **Required**: Yes
- **Type**: String
- **Min Length**: 1 character
- **Max Length**: 100 characters
- **Pattern**: Letters, spaces, hyphens, apostrophes
- **Sanitization**: Trim whitespace

#### 7.1.2 Email Field
- **Required**: Yes
- **Type**: Email
- **Format**: RFC 5322 compliant
- **Regex**: `/^[^\s@]+@[^\s@]+\.[^\s@]+$/`
- **Real-time Validation**: Yes
- **Visual Feedback**: Green/red border

#### 7.1.3 Date of Birth
- **Required**: Yes
- **Type**: Date
- **Format**: YYYY-MM-DD
- **Range**: 1900-01-01 to current date
- **Validation**: HTML5 date input

#### 7.1.4 Mobile Number
- **Required**: Yes
- **Type**: Tel
- **Format**: Country code + number
- **Validation Rules**:
  - India (+91): 10 digits
  - US/Canada (+1): 10 digits
  - UK (+44): 10-11 digits
  - Others: 7-15 digits
- **Pattern**: `/^\+\d{1,3}\d{7,15}$/`

#### 7.1.5 Photo Upload
- **Required**: No
- **File Types**: image/jpeg, image/png, image/gif, image/webp
- **Max Size**: 2MB
- **Validation**: File type and size check
- **Preview**: Live preview on selection

### 7.2 Server-Side Validation

#### 7.2.1 Duplicate Prevention
```python
# Email uniqueness
existing_email = User.query.filter_by(email=email).first()
if existing_email and existing_email.id != current_user_id:
    raise ValidationError("Email already registered")

# Mobile uniqueness  
existing_mobile = User.query.filter_by(mobile=mobile).first()
if existing_mobile and existing_mobile.id != current_user_id:
    raise ValidationError("Mobile number already registered")
```

#### 7.2.2 Input Sanitization
```python
from werkzeug.utils import secure_filename
import html

# Name sanitization
name = html.escape(request.form['name'].strip())

# File sanitization
if photo and photo.filename:
    filename = secure_filename(photo.filename)
```

---

## 8. File Storage Strategy

### 8.1 Directory Structure
```
project_root/
├── static/
│   └── uploads/
│       ├── user_1_profile.jpg
│       ├── user_2_avatar.png
│       └── user_3_photo.webp
├── instance/
│   └── users.db
└── app.py
```

### 8.2 File Naming Convention
```python
def generate_filename(user_id, original_filename):
    """Generate safe filename for user photos"""
    extension = os.path.splitext(original_filename)[1]
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    return f"user_{user_id}_{timestamp}{extension}"
```

### 8.3 Storage Configuration
```python
# Upload settings
UPLOAD_FOLDER = 'static/uploads/'
MAX_CONTENT_LENGTH = 2 * 1024 * 1024  # 2MB
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
```

### 8.4 File Operations

#### 8.4.1 Upload Process
1. **Validation**: Check file type and size
2. **Sanitization**: Secure filename generation
3. **Storage**: Save to uploads directory
4. **Database**: Store filename in user record

#### 8.4.2 Delete Process
1. **File Removal**: Delete from filesystem
2. **Database Update**: Remove filename reference
3. **Error Handling**: Continue if file doesn't exist

---

## 9. Data Security & Privacy

### 9.1 Input Security
- **SQL Injection**: Prevented by SQLAlchemy ORM
- **XSS Protection**: HTML escaping of user inputs
- **File Upload Security**: Type and size validation
- **Path Traversal**: Secure filename generation

### 9.2 Data Privacy
- **PII Handling**: Personal data stored securely
- **File Access**: Direct file serving through Flask
- **Session Management**: Flask session cookies
- **HTTPS**: Enforced in production (Render.com)

### 9.3 Validation Security
```python
# Server-side validation (critical)
def validate_user_data(data):
    errors = {}
    
    # Email validation with regex
    if not re.match(r'^[^\s@]+@[^\s@]+\.[^\s@]+$', data.get('email', '')):
        errors['email'] = 'Invalid email format'
    
    # Mobile validation with country-specific rules
    mobile = data.get('mobile', '')
    if not validate_mobile_format(mobile):
        errors['mobile'] = 'Invalid mobile number format'
    
    return errors
```

---

## 10. Performance Considerations

### 10.1 Database Performance
- **Indexing**: Automatic indexing on unique fields (email, mobile)
- **Query Optimization**: Simple queries with minimal joins
- **Connection Pooling**: SQLAlchemy connection management

### 10.2 File Performance
- **Size Limits**: 2MB maximum per file
- **Format Optimization**: Modern formats (WebP) supported
- **Caching**: Browser caching for static files

### 10.3 Frontend Performance
- **Real-time Search**: 300ms debounce to reduce API calls
- **Image Preview**: Client-side FileReader API
- **Form Validation**: Immediate feedback without server round-trips

### 10.4 Scalability Metrics
```python
# Current capacity estimates (SQLite)
MAX_USERS_RECOMMENDED = 100000
MAX_STORAGE_SIZE = "10GB"
CONCURRENT_USERS = 100
AVERAGE_RESPONSE_TIME = "200ms"
```

---

## 11. Backup & Recovery

### 11.1 Database Backup
```bash
# SQLite backup strategy
cp instance/users.db instance/users_backup_$(date +%Y%m%d_%H%M%S).db

# Automated backup (recommendation)
0 2 * * * /path/to/backup_script.sh
```

### 11.2 File Backup
```bash
# Upload files backup
tar -czf uploads_backup_$(date +%Y%m%d).tar.gz static/uploads/
```

### 11.3 Recovery Procedures
1. **Database Recovery**: Restore from latest backup
2. **File Recovery**: Extract from compressed backup
3. **Validation**: Verify data integrity post-recovery

---

## 12. Scalability Planning

### 12.1 Current Limitations (SQLite)
- **Concurrent Writes**: Limited
- **Database Size**: Practical limit ~100GB
- **Connection Pooling**: Single file database

### 12.2 Migration Path (Future)
```python
# PostgreSQL migration configuration
DATABASES = {
    'postgresql': {
        'ENGINE': 'postgresql',
        'URI': 'postgresql://user:pass@host:5432/dbname'
    }
}
```

### 12.3 Horizontal Scaling Options
- **Database**: PostgreSQL with read replicas
- **File Storage**: AWS S3 or similar cloud storage
- **Caching**: Redis for session management
- **Load Balancing**: Multiple Flask instances

---

## 13. Technical Implementation

### 13.1 Database Initialization
```python
# Database setup
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
    db.init_app(app)
    
    with app.app_context():
        db.create_all()
    
    return app
```

### 13.2 Model Definition
```python
class User(db.Model):
    __tablename__ = 'user'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    dob = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    mobile = db.Column(db.String(15), unique=True, nullable=False, index=True)
    photo = db.Column(db.String(120), nullable=True)
    
    def __init__(self, name, dob, email, mobile, photo=None):
        self.name = name
        self.dob = dob
        self.email = email
        self.mobile = mobile
        self.photo = photo
```

### 13.3 Data Access Layer
```python
class UserRepository:
    @staticmethod
    def create_user(user_data):
        user = User(**user_data)
        db.session.add(user)
        db.session.commit()
        return user
    
    @staticmethod
    def get_all_users():
        return User.query.all()
    
    @staticmethod
    def search_users(query):
        return User.query.filter(User.name.contains(query)).all()
    
    @staticmethod
    def update_user(user_id, user_data):
        user = User.query.get(user_id)
        for key, value in user_data.items():
            setattr(user, key, value)
        db.session.commit()
        return user
    
    @staticmethod
    def delete_user(user_id):
        user = User.query.get(user_id)
        if user:
            db.session.delete(user)
            db.session.commit()
        return user
```

---

## 14. Appendices

### Appendix A: SQL Schema Export
```sql
CREATE TABLE user (
    id INTEGER NOT NULL,
    name VARCHAR(100) NOT NULL,
    dob VARCHAR(20) NOT NULL,
    email VARCHAR(120) NOT NULL,
    mobile VARCHAR(15) NOT NULL,
    photo VARCHAR(120),
    PRIMARY KEY (id),
    UNIQUE (email),
    UNIQUE (mobile)
);

CREATE INDEX ix_user_email ON user (email);
CREATE INDEX ix_user_mobile ON user (mobile);
```

### Appendix B: Sample Data
```json
{
  "users": [
    {
      "id": 1,
      "name": "John Doe",
      "dob": "1990-01-15",
      "email": "john.doe@example.com",
      "mobile": "+919876543210",
      "photo": "user_1_20250927_143022.jpg"
    },
    {
      "id": 2,
      "name": "Jane Smith",
      "dob": "1985-06-22",
      "email": "jane.smith@example.com",
      "mobile": "+911234567890",
      "photo": null
    }
  ]
}
```

### Appendix C: Environment Configuration
```python
# Development
DEBUG = True
SQLALCHEMY_DATABASE_URI = 'sqlite:///users.db'
UPLOAD_FOLDER = 'static/uploads/'

# Production
DEBUG = False
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
SECRET_KEY = os.environ.get('SECRET_KEY')
```

### Appendix D: Testing Data Scenarios
```python
# Test cases for data validation
TEST_SCENARIOS = {
    'valid_user': {
        'name': 'Test User',
        'dob': '1990-01-01',
        'email': 'test@example.com',
        'mobile': '+919876543210'
    },
    'invalid_email': {
        'name': 'Test User',
        'dob': '1990-01-01',
        'email': 'invalid-email',
        'mobile': '+919876543210'
    },
    'duplicate_email': {
        'name': 'Another User',
        'dob': '1985-01-01',
        'email': 'test@example.com',  # Same as valid_user
        'mobile': '+911234567890'
    }
}
```

---

**Document End**

*This document serves as the comprehensive data design specification for the Flask CRUD Internship Application. It should be reviewed and updated as the system evolves.*