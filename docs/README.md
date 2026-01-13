# 🎓 AWS Training Certificate System

A complete web-based certificate management system for AWS training programs with student authentication, admin panel, and automated certificate generation.

## ✨ Features

### 🔐 Student Portal
- **Student Authentication** - Secure login with name, batch number, and SixerClass ID
- **Certificate Download** - Automated PDF certificate generation and download
- **Modern UI** - Responsive design with Magic Bus branding and bus animations

### 👨💼 Admin Panel
- **Secure Login** - Environment-configurable admin credentials
- **Student Management** - Add, edit, delete students manually
- **Excel Operations** - Import/export student data via Excel files
- **Certificate Generation** - Generate certificates for individual students
- **Download Reports** - Track certificate downloads with comprehensive analytics
- **Search & Filter** - Real-time student search functionality
- **Statistics Dashboard** - View total students, batches, and recent additions

### 📊 Data Management
- **Excel Import/Export** - Bulk student data operations
- **Drag & Drop Upload** - Modern file upload interface
- **Data Validation** - Duplicate detection and error handling
- **Persistent Storage** - Excel-based data persistence with AWS-compatible paths

## 🚀 Quick Start

### Prerequisites
```bash
pip install -r requirements.txt
```

### Installation
1. Clone or download the project
2. Install dependencies: `pip install -r requirements.txt`
3. Configure environment (copy `.env.example` to `.env`)
4. Run the application:
```bash
python src/app.py
```

### Access Points
- **Student Portal**: http://localhost:5000
- **Admin Login**: http://localhost:5000/admin/login
- **Admin Panel**: http://localhost:5000/admin/students

### Default Credentials
- **Admin Username**: `admin` (configurable via `ADMIN_USERNAME`)
- **Admin Password**: `admin123` (configurable via `ADMIN_PASSWORD`)

## 📁 Project Structure

```
aws-training-certificate-system/
├── src/
│   ├── app.py                        # Main Flask application
│   └── certificate_generator.py      # PDF certificate generation
├── data/
│   ├── excel/
│   │   └── student-data.xlsx         # Student database
│   ├── templates/
│   │   └── certificate-template.png  # Certificate template
│   ├── certificates/                 # Generated certificates
│   └── uploads/                      # File uploads
├── assets/
│   ├── Magicbus_logo.png            # Company logo
│   └── bus.png                      # Bus animation image
├── docs/
│   ├── README.md                    # This file
│   └── DEVELOPER_GUIDE.md           # Technical documentation
├── application.py                   # AWS Elastic Beanstalk entry point
├── Dockerfile                       # Container deployment
├── docker-compose.yml              # Local development
├── deploy.sh                       # Deployment script
├── .env.example                    # Environment variables template
└── AWS_DEPLOYMENT.md               # AWS deployment guide
```

## 🎯 Sample Data

The system includes 6 sample students:
- **SIX001** - Rahul Sharma (AWS-2024-001)
- **SIX002** - Priya Patel (AWS-2024-001)
- **SIX003** - Amit Kumar (AWS-2024-002)
- **SIX004** - Neha Gupta (AWS-2024-002)
- **SIX005** - Vikram Singh (AWS-2024-002)
- **SIX006** - Anjali Sharma (AWS-2024-002)

## 📋 Excel Format

Required columns for Excel import:
- `student_name`
- `batch_number`
- `batch_start_date`
- `batch_end_date`
- `sixerclass_id`

## 🔧 Configuration

### Environment Variables
Copy `.env.example` to `.env` and configure:
```bash
SECRET_KEY=your-super-secret-key-change-this-in-production
ADMIN_USERNAME=admin
ADMIN_PASSWORD=secure-password-here
FLASK_ENV=production
FLASK_DEBUG=False
```

### Certificate Template
- Template location: `data/templates/certificate-template.png`
- Modify `certificate_generator.py` for custom positioning

## 🌐 API Endpoints

### Public APIs
- `GET /` - Student portal
- `POST /api/authenticate` - Student authentication
- `POST /api/download-certificate` - Certificate generation
- `GET /api/check-status` - System status
- `GET /static/<filename>` - Static file serving

### Admin APIs (Authentication Required)
- `GET /admin/login` - Admin login page
- `POST /admin/login` - Admin authentication
- `GET /admin/students` - Admin panel
- `GET /admin/api/students` - Get students list
- `POST /admin/api/students/add` - Add student
- `POST /admin/api/students/update` - Update student
- `POST /admin/api/students/delete` - Delete student
- `GET /admin/api/students/export` - Export Excel
- `POST /admin/api/students/import` - Import Excel
- `POST /admin/api/generate-certificate` - Generate certificate
- `GET /admin/api/reports` - Download reports
- `GET /admin/api/reports/export` - Export reports
- `GET /admin/api/download-status/export` - Export download status

## 🛡️ Security Features

- Environment-based configuration
- Session-based authentication
- File type validation
- Secure filename handling
- Duplicate prevention
- Input sanitization
- Error handling
- AWS-compatible absolute paths

## 🚀 AWS Deployment

### Quick Deploy
```bash
./deploy.sh
```

### Deployment Options
1. **AWS Elastic Beanstalk** (Recommended)
2. **AWS EC2 with Docker**
3. **AWS ECS with Fargate**

See `AWS_DEPLOYMENT.md` for detailed deployment instructions.

### Environment Setup for AWS
```bash
export SECRET_KEY=your-production-secret-key
export ADMIN_USERNAME=your_admin_username
export ADMIN_PASSWORD=your_secure_password
export FLASK_ENV=production
export FLASK_DEBUG=False
```

## 🐳 Docker Deployment

### Local Development
```bash
docker-compose up
```

### Production Container
```bash
docker build -t certificate-system .
docker run -d -p 5000:5000 --name cert-app certificate-system
```

## 📊 Monitoring & Reports

- **Certificate Download Tracking** - Track which students downloaded certificates
- **Download Analytics** - View download statistics and patterns
- **Export Reports** - Generate Excel reports of download activity
- **System Health** - Monitor application status via `/api/check-status`

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🆘 Support

For issues and questions:
1. Check the `DEVELOPER_GUIDE.md` for technical details
2. Review the `AWS_DEPLOYMENT.md` for deployment issues
3. Examine the sample data format
4. Test with provided sample students
5. Check application logs for errors

---

**Built with ❤️ for AWS Training Programs by Magic Bus India Foundation**