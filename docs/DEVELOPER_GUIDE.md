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
10. [AWS Deployment](#aws-deployment)
11. [Troubleshooting](#troubleshooting)
12. [Future Enhancements](#future-enhancements)

## 🏗️ System Architecture

### Technology Stack
- **Backend**: Flask (Python)
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Data Storage**: Excel files (xlsx format)
- **PDF Generation**: ReportLab + Pillow
- **File Handling**: Pandas, Werkzeug
- **Deployment**: AWS Elastic Beanstalk, Docker, EC2

### Application Flow
```
Student Portal → Authentication → Certificate Generation → PDF Download
Admin Panel → Login → Student Management → CRUD Operations → Excel I/O
```

## 📁 File Structure

### Core Files
```
src/app.py                           # Main Flask application (1500+ lines)
├── Environment-based configuration
├── AWS-compatible path resolution
├── Flask routes and handlers
├── Authentication logic
├── Admin panel HTML templates
├── API endpoints
└── Session management

src/certificate_generator.py        # PDF certificate creation
├── Configurable template loading
├── Text positioning
├── PDF generation
└── AWS-compatible file handling

data/excel/student-data.xlsx        # Primary data storage
├── Student records
├── Batch information
└── SixerClass IDs
```

### AWS Deployment Files
```
application.py                      # Elastic Beanstalk entry point
Dockerfile                         # Container deployment
docker-compose.yml                 # Local development
deploy.sh                         # Deployment automation
.env.example                      # Environment template
AWS_DEPLOYMENT.md                 # Deployment guide
```

### Directory Structure
```
data/certificates/                 # Generated PDF certificates
data/excel/                       # Excel data files
data/uploads/                     # Temporary file uploads
data/templates/                   # Certificate templates
assets/                          # Static assets (logos, images)
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

### Download Log Structure
```python
{
    'student_name': str,
    'sixerclass_id': str,
    'batch_number': str,
    'download_time': str,       # ISO format timestamp
    'filename': str
}
```

## 🔌 API Reference

### Public Endpoints

#### GET /
**Purpose**: Student portal homepage
**Response**: HTML page with Magic Bus branding and authentication form

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

#### GET /api/check-status
**Purpose**: System health check and monitoring
**Response**:
```json
{
    "status": "operational",
    "students_loaded": 6,
    "timestamp": "2024-01-15T10:30:00",
    "version": "4.0.0-Production-Ready"
}
```

#### GET /static/<filename>
**Purpose**: Serve static assets (logos, images)
**Files**: `Magicbus_logo.png`, `bus.png`
**Path Resolution**: Uses `app.config['ASSETS_DIR']` for AWS compatibility

### Admin Endpoints

#### GET /admin/api/reports
**Purpose**: Get certificate download analytics
**Response**:
```json
{
    "success": true,
    "reports": {
        "total_downloads": 15,
        "unique_students": 4,
        "avg_downloads": 3.8,
        "student_downloads": [...]
    }
}
```

#### GET /admin/api/reports/export
**Purpose**: Export download reports to Excel
**Response**: Excel file download

#### GET /admin/api/download-status/export
**Purpose**: Export student download status
**Response**: Excel file with download status for all students

## 🔐 Authentication System

### Environment-Based Configuration
**Location**: `src/app.py` lines 15-20
```python
app.config['ADMIN_USERNAME'] = os.environ.get('ADMIN_USERNAME', 'admin')
app.config['ADMIN_PASSWORD'] = os.environ.get('ADMIN_PASSWORD', 'admin123')
```

### Student Authentication
**Method**: Three-factor verification (name + batch + ID)
**Session**: Stores student object in Flask session
**Security**: No password required, relies on unique ID combination

### Admin Authentication
**Credentials**: Environment-configurable
**Session**: Boolean flag in Flask session
**Protection**: All admin routes check `session.get('admin_logged_in')`

## 📄 Certificate Generation

### Certificate Generator Class
**File**: `src/certificate_generator.py`
**Template**: Configurable PNG image path
**Initialization**:
```python
cert_generator = CertificateGenerator(app.config['TEMPLATE_DIR'])
```

### AWS-Compatible Template Loading
```python
def __init__(self, template_dir=None):
    if template_dir:
        self.template_path = os.path.join(template_dir, 'certificate-template.png')
    else:
        # Fallback paths for backward compatibility
        possible_paths = [
            'data/templates/certificate-template.png',
            '../data/templates/certificate-template.png'
        ]
```

## 📊 Excel Operations

### AWS-Compatible Path Resolution
```python
# Load students data
excel_path = os.path.join(app.config['EXCEL_DIR'], 'student-data.xlsx')

# Save updated data
df = pd.DataFrame(students_data)
excel_path = os.path.join(app.config['EXCEL_DIR'], 'student-data.xlsx')
df.to_excel(excel_path, index=False)
```

### Import Process
1. **File Upload**: Multipart form handling with validation
2. **Path Resolution**: Uses `app.config['UPLOAD_FOLDER']`
3. **Processing**: Pandas DataFrame operations
4. **Persistence**: Saves to configured Excel directory

## ⚙️ Configuration

### Environment-Based Configuration
```python
# AWS-compatible paths
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
app.config['BASE_DIR'] = base_dir
app.config['ASSETS_DIR'] = os.path.join(base_dir, 'assets')
app.config['DATA_DIR'] = os.path.join(base_dir, 'data')
app.config['CERTIFICATE_DIR'] = os.path.join(base_dir, 'data', 'certificates')
app.config['EXCEL_DIR'] = os.path.join(base_dir, 'data', 'excel')
app.config['UPLOAD_FOLDER'] = os.path.join(base_dir, 'data', 'uploads')
app.config['TEMPLATE_DIR'] = os.path.join(base_dir, 'data', 'templates')
```

### Environment Variables
```bash
SECRET_KEY=your-super-secret-key-change-this-in-production
ADMIN_USERNAME=admin
ADMIN_PASSWORD=secure-password-here
FLASK_ENV=production
FLASK_DEBUG=False
```

## 🚀 AWS Deployment

### Deployment Options

#### 1. AWS Elastic Beanstalk (Recommended)
```bash
# Prepare deployment
./deploy.sh

# Create deployment package
zip -r certificate-system.zip . -x "*.git*" "__pycache__/*" "*.pyc"

# Deploy via EB console or CLI
eb init
eb create production-env
eb deploy
```

#### 2. AWS EC2 with Docker
```bash
# Build and run container
docker build -t certificate-system .
docker run -d -p 80:5000 --name cert-app certificate-system
```

#### 3. AWS ECS with Fargate
```bash
# Push to ECR
docker tag certificate-system:latest your-account.dkr.ecr.region.amazonaws.com/certificate-system:latest
docker push your-account.dkr.ecr.region.amazonaws.com/certificate-system:latest
```

### Environment Configuration for AWS
```python
# Production settings
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'fallback-key')
app.config['ADMIN_USERNAME'] = os.environ.get('ADMIN_USERNAME', 'admin')
app.config['ADMIN_PASSWORD'] = os.environ.get('ADMIN_PASSWORD', 'admin123')
```

### File Structure Requirements
- All paths must be absolute and configurable
- No hardcoded `/tmp/` dependencies
- Assets must be accessible via static routes
- Data directories must be writable

## 🐛 Troubleshooting

### AWS-Specific Issues

#### 1. Static Files Not Loading
```python
# Check asset paths
logo_path = os.path.join(app.config['ASSETS_DIR'], 'Magicbus_logo.png')
if not os.path.exists(logo_path):
    logger.error(f"Logo not found at: {logo_path}")
```

#### 2. Template Not Found
```python
# Verify template path
template_path = os.path.join(app.config['TEMPLATE_DIR'], 'certificate-template.png')
if not os.path.exists(template_path):
    logger.error(f"Certificate template not found at: {template_path}")
```

#### 3. Permission Issues
```bash
# Ensure write permissions
chmod -R 755 data/
chown -R app:app data/
```

#### 4. Environment Variables
```bash
# Check environment variables are set
echo $SECRET_KEY
echo $ADMIN_USERNAME
echo $ADMIN_PASSWORD
```

### Debug Mode for Development
```python
# Enable debug logging
import logging
logging.basicConfig(level=logging.DEBUG)

# Check configuration
logger.info(f"Base directory: {app.config['BASE_DIR']}")
logger.info(f"Assets directory: {app.config['ASSETS_DIR']}")
logger.info(f"Data directory: {app.config['DATA_DIR']}")
```

## 🚀 Future Enhancements

### Database Migration
```python
# Replace Excel with PostgreSQL
from flask_sqlalchemy import SQLAlchemy

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
db = SQLAlchemy(app)

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_name = db.Column(db.String(100), nullable=False)
    batch_number = db.Column(db.String(20), nullable=False)
    sixerclass_id = db.Column(db.String(10), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
```

### AWS Services Integration
```python
# S3 for file storage
import boto3
s3_client = boto3.client('s3')

# RDS for database
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('RDS_DATABASE_URL')

# SES for email notifications
ses_client = boto3.client('ses')
```

### Enhanced Security
```python
# Environment-based secrets
from flask_talisman import Talisman
Talisman(app, force_https=True)

# Rate limiting
from flask_limiter import Limiter
limiter = Limiter(app, key_func=get_remote_address)

# CSRF protection
from flask_wtf.csrf import CSRFProtect
csrf = CSRFProtect(app)
```

### Monitoring & Logging
```python
# CloudWatch integration
import watchtower
logger.addHandler(watchtower.CloudWatchLogsHandler())

# Health checks
@app.route('/health')
def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "4.0.0",
        "environment": os.environ.get('FLASK_ENV', 'development')
    }
```

## 📞 Development Workflow

### Local Development
```bash
# Setup environment
cp .env.example .env
# Edit .env with your values

# Install dependencies
pip install -r requirements.txt

# Run locally
python src/app.py
```

### Testing with Docker
```bash
# Build and test locally
docker-compose up

# Test production build
docker build -t certificate-system .
docker run -p 5000:5000 certificate-system
```

### Deployment Checklist
- [ ] Environment variables configured
- [ ] Certificate template in place
- [ ] Assets directory accessible
- [ ] Data directories writable
- [ ] SSL certificate configured
- [ ] Domain name pointed to deployment
- [ ] Monitoring and logging enabled
- [ ] Backup strategy implemented

---

**This guide covers all aspects of the AWS Training Certificate System with focus on AWS deployment readiness!** 🎯