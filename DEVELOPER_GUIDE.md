# 🔧 AWS Training Certificate System - Developer Reference Guide

## 📋 Table of Contents
1. [System Architecture](#system-architecture)
2. [File Structure](#file-structure)
3. [Database Schema](#database-schema)
4. [API Reference](#api-reference)
5. [Authentication System](#authentication-system)
6. [Certificate Generation](#certificate-generation)
7. [Excel Operations](#excel-operations)
8. [Frontend Components](#frontend-components)
9. [Configuration](#configuration)
10. [Troubleshooting](#troubleshooting)
11. [Future Enhancements](#future-enhancements)

## 🏗️ System Architecture

### Technology Stack
- **Backend**: Flask (Python)
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Data Storage**: Excel files (xlsx format)
- **PDF Generation**: ReportLab + Pillow
- **File Handling**: Pandas, Werkzeug

### Application Flow
```
Student Portal → Authentication → Certificate Generation → PDF Download
Admin Panel → Login → Student Management → CRUD Operations → Excel I/O
```

## 📁 File Structure

### Core Files
```
app_production_simple.py          # Main Flask application (1000+ lines)
├── Flask routes and handlers
├── Authentication logic
├── Admin panel HTML templates
├── API endpoints
└── Session management

certificate_generator.py         # PDF certificate creation
├── Template loading
├── Text positioning
├── PDF generation
└── File handling

excel-samples/student-data.xlsx   # Primary data storage
├── Student records
├── Batch information
└── SixerClass IDs
```

### Directory Structure
```
/tmp/certificates/               # Generated PDF certificates
/tmp/excel-data/                # Excel export files
/tmp/uploads/                   # Temporary file uploads
aws-final-deployment/           # Template and backup data
```

## 🗃️ Database Schema

### Student Record Structure
```python
{
    'student_name': str,        # Full name of student
    'batch_number': str,        # Format: AWS-YYYY-XXX
    'batch_start_date': str,    # Format: YYYY-MM-DD
    'batch_end_date': str,      # Format: YYYY-MM-DD
    'sixerclass_id': str        # Unique ID: SIXNNN
}
```

### Sample Data
```python
students_data = [
    {
        'student_name': 'Rahul Sharma',
        'batch_number': 'AWS-2024-001',
        'batch_start_date': '2024-01-15',
        'batch_end_date': '2024-04-15',
        'sixerclass_id': 'SIX001'
    }
    # ... more records
]
```

## 🔌 API Reference

### Public Endpoints

#### GET /
**Purpose**: Student portal homepage
**Response**: HTML page with authentication form

#### POST /api/authenticate
**Purpose**: Authenticate student for certificate download
**Request Body**:
```json
{
    "student_name": "Rahul Sharma",
    "batch_number": "AWS-2024-001",
    "sixerclass_id": "SIX001"
}
```
**Response**:
```json
{
    "success": true,
    "student": { /* student object */ }
}
```

#### POST /api/download-certificate
**Purpose**: Generate and download certificate
**Authentication**: Requires student session
**Response**:
```json
{
    "success": true,
    "download_url": "/api/serve-certificate/certificate_SIX001_Rahul_Sharma.pdf",
    "filename": "certificate_SIX001_Rahul_Sharma.pdf",
    "student_name": "Rahul Sharma"
}
```

#### GET /api/check-status
**Purpose**: System health check
**Response**:
```json
{
    "status": "operational",
    "students_loaded": 6,
    "timestamp": "2024-01-15T10:30:00",
    "version": "4.0.0-Production-Ready"
}
```

### Admin Endpoints

#### POST /admin/login
**Purpose**: Admin authentication
**Request Body**:
```json
{
    "username": "admin",
    "password": "admin123"
}
```

#### GET /admin/api/students
**Purpose**: Get all students with optional search
**Authentication**: Admin session required
**Query Parameters**: `search` (optional)
**Response**:
```json
{
    "success": true,
    "total": 6,
    "students": [ /* array of student objects */ ]
}
```

#### POST /admin/api/students/add
**Purpose**: Add new student
**Request Body**:
```json
{
    "student_name": "New Student",
    "batch_number": "AWS-2024-003",
    "batch_start_date": "2024-07-01",
    "batch_end_date": "2024-10-01",
    "sixerclass_id": "SIX007"
}
```

#### POST /admin/api/students/update
**Purpose**: Update existing student
**Request Body**:
```json
{
    "original_sixerclass_id": "SIX001",
    "student_name": "Updated Name",
    "batch_number": "AWS-2024-001",
    "batch_start_date": "2024-01-15",
    "batch_end_date": "2024-04-15",
    "sixerclass_id": "SIX001"
}
```

#### POST /admin/api/students/delete
**Purpose**: Delete student
**Request Body**:
```json
{
    "sixerclass_id": "SIX001"
}
```

#### GET /admin/api/students/export
**Purpose**: Export students to Excel
**Response**: Excel file download

#### POST /admin/api/students/import
**Purpose**: Import students from Excel
**Request**: Multipart form with Excel file
**Response**:
```json
{
    "success": true,
    "message": "Successfully imported 3 students",
    "imported_count": 3,
    "errors": []
}
```

## 🔐 Authentication System

### Student Authentication
**Location**: `app_production_simple.py` lines 240-270
**Method**: Three-factor verification (name + batch + ID)
**Session**: Stores student object in Flask session
**Security**: No password required, relies on unique ID combination

### Admin Authentication
**Location**: `app_production_simple.py` lines 334-340
**Credentials**: Hardcoded in source code
```python
if username == 'admin' and password == 'admin123':
    session['admin_logged_in'] = True
```
**Session**: Boolean flag in Flask session
**Protection**: All admin routes check `session.get('admin_logged_in')`

### Session Management
```python
# Student session
session['student'] = student_object

# Admin session
session['admin_logged_in'] = True

# Logout
session.pop('admin_logged_in', None)
```

## 📄 Certificate Generation

### Certificate Generator Class
**File**: `certificate_generator.py`
**Template**: PNG image loaded from filesystem
**Text Positioning**: Hardcoded coordinates for name placement
**Output**: PDF file with embedded certificate image

### Key Methods
```python
def create_certificate(student_data, output_path):
    # Load template image
    # Add student name to certificate
    # Save as PDF
    return success_boolean
```

### Customization Points
- Template image path
- Text positioning coordinates
- Font selection and sizing
- PDF metadata

## 📊 Excel Operations

### Import Process
1. **File Upload**: Multipart form handling
2. **Validation**: Check file extension (.xlsx, .xls)
3. **Reading**: Pandas `read_excel()` with sheet_name=0
4. **Column Validation**: Check required columns exist
5. **Data Processing**: Clean and validate each row
6. **Duplicate Check**: Prevent duplicate SixerClass IDs
7. **Database Update**: Add to global `students_data` list
8. **Persistence**: Save to Excel file

### Export Process
1. **Data Conversion**: Convert list to Pandas DataFrame
2. **File Generation**: Create timestamped Excel file
3. **Download**: Send file as attachment

### Required Excel Columns
```
student_name | batch_number | batch_start_date | batch_end_date | sixerclass_id
```

## 🎨 Frontend Components

### Student Portal
**File**: Embedded in `app_production_simple.py` lines 110-200
**Features**:
- Gradient background design
- Responsive form layout
- JavaScript form handling
- Certificate download automation

### Admin Panel
**File**: Embedded in `app_production_simple.py` lines 400-800
**Components**:
- Statistics dashboard
- Student table with actions
- Add/Edit modals
- File upload area
- Search functionality

### JavaScript Functions
```javascript
// Core functions
loadStudents()           // Fetch and display students
displayStudents()        // Render student table
updateStats()           // Update dashboard statistics
filterStudents()        // Search functionality

// CRUD operations
showAddModal()          // Show add student form
editStudent(id)         // Show edit student form
deleteStudent(id)       // Delete student with confirmation
exportStudents()        // Download Excel export
uploadFile(file)        // Handle Excel import

// UI helpers
showAlert(msg, type)    // Display notifications
refreshData()           // Reload student data
logout()               // Admin logout
```

## ⚙️ Configuration

### Flask Configuration
```python
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['CERTIFICATE_DIR'] = '/tmp/certificates'
app.config['EXCEL_DIR'] = '/tmp/excel-data'
app.config['UPLOAD_FOLDER'] = '/tmp/uploads'
```

### File Paths
```python
# Student data locations (in order of preference)
possible_paths = [
    'aws-final-deployment/excel-samples/student-data.xlsx',
    'excel-samples/student-data.xlsx',
    'data/excel-samples/student-data.xlsx',
    'aws-final-deployment/production/data/excel-samples/student-data.xlsx'
]

# Certificate template
template_path = 'aws-final-deployment/certificate-templates/raw/certificate-template.png'
```

### Security Settings
```python
# File upload restrictions
ALLOWED_EXTENSIONS = {'.xlsx', '.xls'}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

# Session configuration
PERMANENT_SESSION_LIFETIME = timedelta(hours=2)
```

## 🐛 Troubleshooting

### Common Issues

#### 1. Port Already in Use
```bash
# Kill existing processes
pkill -f "python.*app"
# Or use different port
app.run(port=5001)
```

#### 2. Excel File Not Found
- Check file exists in `excel-samples/` directory
- Verify file permissions
- Ensure correct file format (.xlsx)

#### 3. Certificate Generation Fails
- Verify template image exists
- Check write permissions to `/tmp/certificates/`
- Ensure ReportLab and Pillow are installed

#### 4. Admin Login Issues
- Verify credentials: admin/admin123
- Check Flask session configuration
- Clear browser cookies

#### 5. Excel Import Errors
- Verify column names match exactly
- Check for duplicate SixerClass IDs
- Ensure date format is consistent

### Debug Mode
```python
# Enable debug mode for development
app.run(debug=True)

# Add logging
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Log Analysis
```python
# Key log messages to monitor
logger.info(f"✅ Loaded {len(students_data)} students")
logger.error(f"❌ Error loading students data: {e}")
logger.warning(f"❌ Authentication failed for: {student_name}")
```

## 🚀 Future Enhancements

### Database Migration
```python
# Replace Excel with SQLite/PostgreSQL
from flask_sqlalchemy import SQLAlchemy

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_name = db.Column(db.String(100), nullable=False)
    batch_number = db.Column(db.String(20), nullable=False)
    sixerclass_id = db.Column(db.String(10), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
```

### Enhanced Security
```python
# Password hashing
from werkzeug.security import generate_password_hash, check_password_hash

# Rate limiting
from flask_limiter import Limiter

# CSRF protection
from flask_wtf.csrf import CSRFProtect
```

### Advanced Features
- Bulk certificate generation
- Email certificate delivery
- Batch management system
- Analytics dashboard
- Multi-admin support
- Role-based permissions
- API authentication tokens
- Automated backups

### Performance Optimizations
- Database indexing
- Caching with Redis
- Async certificate generation
- CDN for static files
- Load balancing
- Connection pooling

### Monitoring & Logging
```python
# Application monitoring
from flask_monitoring_dashboard import dashboard

# Structured logging
import structlog

# Health checks
@app.route('/health')
def health_check():
    return {"status": "healthy", "timestamp": datetime.utcnow()}
```

## 📞 Development Workflow

### Making Changes

1. **Backend Changes**: Modify `app_production_simple.py`
2. **Certificate Updates**: Edit `certificate_generator.py`
3. **Data Changes**: Update Excel files in `excel-samples/`
4. **Testing**: Use sample students for validation
5. **Deployment**: Restart Flask application

### Code Organization Tips
- Keep HTML templates in separate files for larger projects
- Extract JavaScript to separate files
- Use environment variables for configuration
- Implement proper error handling
- Add comprehensive logging
- Write unit tests for critical functions

### Version Control
```bash
# Ignore temporary files
echo "/tmp/" >> .gitignore
echo "*.pyc" >> .gitignore
echo "__pycache__/" >> .gitignore
echo ".env" >> .gitignore
```

---

**This guide covers all aspects of the AWS Training Certificate System. Keep it handy for future development and maintenance!** 🎯