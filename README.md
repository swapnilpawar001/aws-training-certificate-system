# 🎓 AWS Training Certificate System

A complete web-based certificate management system for AWS training programs with student authentication, admin panel, and automated certificate generation.

## ✨ Features

### 🔐 Student Portal
- **Student Authentication** - Secure login with name, batch number, and SixerClass ID
- **Certificate Download** - Automated PDF certificate generation and download
- **Modern UI** - Responsive design with gradient backgrounds and smooth animations

### 👨‍💼 Admin Panel
- **Secure Login** - Password-protected admin access
- **Student Management** - Add, edit, delete students manually
- **Excel Operations** - Import/export student data via Excel files
- **Certificate Generation** - Generate certificates for individual students
- **Search & Filter** - Real-time student search functionality
- **Statistics Dashboard** - View total students, batches, and recent additions

### 📊 Data Management
- **Excel Import/Export** - Bulk student data operations
- **Drag & Drop Upload** - Modern file upload interface
- **Data Validation** - Duplicate detection and error handling
- **Persistent Storage** - Excel-based data persistence

## 🚀 Quick Start

### Prerequisites
```bash
pip install flask flask-cors pandas openpyxl pillow reportlab
```

### Installation
1. Clone or download the project
2. Install dependencies
3. Run the application:
```bash
python app_production_simple.py
```

### Access Points
- **Student Portal**: http://localhost:5000
- **Admin Login**: http://localhost:5000/admin/login
- **Admin Panel**: http://localhost:5000/admin/students

### Default Credentials
- **Admin Username**: `admin`
- **Admin Password**: `admin123`

## 📁 Project Structure

```
aws-training-certificate-system/
├── app_production_simple.py          # Main Flask application
├── certificate_generator.py          # PDF certificate generation
├── excel-samples/
│   └── student-data.xlsx             # Student database
├── aws-final-deployment/
│   ├── certificate-templates/raw/
│   │   └── certificate-template.png  # Certificate template
│   └── excel-samples/
│       └── student-data.xlsx         # Backup student data
└── /tmp/                             # Runtime directories
    ├── certificates/                 # Generated certificates
    ├── excel-data/                   # Excel exports
    └── uploads/                      # File uploads
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

### Security Settings
- Change admin credentials in `app_production_simple.py` line 334-340
- Update Flask secret key for production
- Enable HTTPS for production deployment

### Certificate Template
- Template location: `aws-final-deployment/certificate-templates/raw/certificate-template.png`
- Modify `certificate_generator.py` for custom positioning

## 🌐 API Endpoints

### Public APIs
- `GET /` - Student portal
- `POST /api/authenticate` - Student authentication
- `POST /api/download-certificate` - Certificate generation
- `GET /api/check-status` - System status

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

## 🛡️ Security Features

- Session-based authentication
- File type validation
- Secure filename handling
- Duplicate prevention
- Input sanitization
- Error handling

## 📈 Production Deployment

### Environment Variables
```bash
export ADMIN_USERNAME=your_admin_username
export ADMIN_PASSWORD=your_secure_password
export FLASK_SECRET_KEY=your_secret_key
```

### Recommended Improvements
- Use PostgreSQL/MySQL for data storage
- Implement password hashing
- Add rate limiting
- Enable HTTPS
- Add logging and monitoring
- Implement backup strategies

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
1. Check the Developer Reference Guide
2. Review the API documentation
3. Examine the sample data format
4. Test with provided sample students

---

**Built with ❤️ for AWS Training Programs**