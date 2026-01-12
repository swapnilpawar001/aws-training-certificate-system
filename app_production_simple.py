from flask import Flask, render_template, request, jsonify, send_file, session, redirect
from flask_cors import CORS
import pandas as pd
import logging
import os
from werkzeug.utils import secure_filename
from datetime import datetime
from certificate_generator import CertificateGenerator

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['CERTIFICATE_DIR'] = '/tmp/certificates'
app.config['EXCEL_DIR'] = '/tmp/excel-data'
app.config['UPLOAD_FOLDER'] = '/tmp/uploads'

# Ensure directories exist
os.makedirs(app.config['CERTIFICATE_DIR'], exist_ok=True)
os.makedirs(app.config['EXCEL_DIR'], exist_ok=True)
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

CORS(app)

# Initialize certificate generator
cert_generator = CertificateGenerator()

# Global students data
students_data = []

def create_sample_data():
    """Create sample student data"""
    sample_data = [
        {
            'student_name': 'Rahul Sharma',
            'batch_number': 'AWS-2024-001',
            'batch_start_date': '2024-01-15',
            'batch_end_date': '2024-04-15',
            'sixerclass_id': 'SIX001'
        },
        {
            'student_name': 'Priya Patel',
            'batch_number': 'AWS-2024-001',
            'batch_start_date': '2024-01-15',
            'batch_end_date': '2024-04-15',
            'sixerclass_id': 'SIX002'
        },
        {
            'student_name': 'Amit Kumar',
            'batch_number': 'AWS-2024-002',
            'batch_start_date': '2024-02-01',
            'batch_end_date': '2024-05-01',
            'sixerclass_id': 'SIX003'
        },
        {
            'student_name': 'Neha Gupta',
            'batch_number': 'AWS-2024-002',
            'batch_start_date': '2024-02-01',
            'batch_end_date': '2024-05-01',
            'sixerclass_id': 'SIX004'
        },
        {
            'student_name': 'Vikram Singh',
            'batch_number': 'AWS-2024-002',
            'batch_start_date': '2024-02-01',
            'batch_end_date': '2024-05-01',
            'sixerclass_id': 'SIX005'
        },
        {
            'student_name': 'Anjali Sharma',
            'batch_number': 'AWS-2024-002',
            'batch_start_date': '2024-02-01',
            'batch_end_date': '2024-05-01',
            'sixerclass_id': 'SIX006'
        }
    ]
    
    # Save sample data to Excel
    df = pd.DataFrame(sample_data)
    os.makedirs('excel-samples', exist_ok=True)
    df.to_excel('excel-samples/student-data.xlsx', index=False)
    logger.info("✅ Created sample Excel data with 6 students")
    
    return sample_data

# Load students data
def load_students_data():
    global students_data
    try:
        # Try multiple possible paths
        possible_paths = [
            'aws-final-deployment/excel-samples/student-data.xlsx',
            'excel-samples/student-data.xlsx',
            'data/excel-samples/student-data.xlsx',
            'aws-final-deployment/production/data/excel-samples/student-data.xlsx'
        ]
        
        for excel_path in possible_paths:
            if os.path.exists(excel_path):
                df = pd.read_excel(excel_path)
                students_data = df.to_dict('records')
                logger.info(f"✅ Loaded {len(students_data)} students from {excel_path}")
                return students_data
        
        # If no file found, create sample data
        logger.warning("❌ No Excel file found, creating sample data")
        students_data = create_sample_data()
        return students_data
        
    except Exception as e:
        logger.error(f"❌ Error loading students data: {e}")
        students_data = create_sample_data()
        return students_data

# Load initial data
load_students_data()

@app.route('/')
def index():
    return '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>AWS Training Certificate System</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 0; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; display: flex; align-items: center; justify-content: center; }
            .container { background: white; padding: 3rem; border-radius: 15px; box-shadow: 0 10px 30px rgba(0,0,0,0.2); max-width: 500px; width: 100%; }
            .header { text-align: center; margin-bottom: 2rem; }
            .header h1 { color: #333; margin-bottom: 0.5rem; }
            .header p { color: #666; }
            .form-group { margin-bottom: 1.5rem; }
            .form-group label { display: block; margin-bottom: 0.5rem; color: #555; font-weight: bold; }
            .form-group input { width: 100%; padding: 1rem; border: 2px solid #ddd; border-radius: 8px; font-size: 1rem; transition: border-color 0.3s; }
            .form-group input:focus { outline: none; border-color: #667eea; }
            .btn { width: 100%; padding: 1rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border: none; border-radius: 8px; font-size: 1rem; cursor: pointer; transition: transform 0.2s; }
            .btn:hover { transform: translateY(-2px); }
            .admin-link { text-align: center; margin-top: 2rem; }
            .admin-link a { color: #667eea; text-decoration: none; }
            .admin-link a:hover { text-decoration: underline; }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🎓 AWS Training Certificate System</h1>
                <p>Enter your details to download your certificate</p>
            </div>
            
            <form id="authForm">
                <div class="form-group">
                    <label for="student_name">Student Name:</label>
                    <input type="text" id="student_name" name="student_name" required>
                </div>
                
                <div class="form-group">
                    <label for="batch_number">Batch Number:</label>
                    <input type="text" id="batch_number" name="batch_number" required>
                </div>
                
                <div class="form-group">
                    <label for="sixerclass_id">SixerClass ID:</label>
                    <input type="text" id="sixerclass_id" name="sixerclass_id" required>
                </div>
                
                <button type="submit" class="btn">Download Certificate</button>
            </form>
            
            <div class="admin-link">
                <a href="/admin/students">🔧 Admin Panel</a>
            </div>
        </div>
        
        <script>
            document.getElementById('authForm').addEventListener('submit', async (e) => {
                e.preventDefault();
                
                const formData = new FormData(e.target);
                const data = Object.fromEntries(formData);
                
                try {
                    const response = await fetch('/api/authenticate', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify(data)
                    });
                    
                    const result = await response.json();
                    
                    if (result.success) {
                        // Download certificate
                        const downloadResponse = await fetch('/api/download-certificate', {
                            method: 'POST'
                        });
                        
                        const downloadResult = await downloadResponse.json();
                        
                        if (downloadResult.success) {
                            const link = document.createElement('a');
                            link.href = downloadResult.download_url;
                            link.download = downloadResult.filename;
                            document.body.appendChild(link);
                            link.click();
                            document.body.removeChild(link);
                            alert('Certificate downloaded successfully!');
                        } else {
                            alert('Certificate generation failed: ' + downloadResult.error);
                        }
                    } else {
                        alert('Authentication failed: ' + result.error);
                    }
                } catch (error) {
                    alert('Error: ' + error.message);
                }
            });
        </script>
    </body>
    </html>
    '''

@app.route('/api/check-status')
def check_status():
    return jsonify({
        "status": "operational",
        "students_loaded": len(students_data),
        "timestamp": datetime.now().isoformat(),
        "version": "4.0.0-Production-Ready"
    })

@app.route('/api/authenticate', methods=['POST'])
def authenticate():
    try:
        data = request.get_json()
        student_name = data.get('student_name')
        batch_number = data.get('batch_number')
        sixerclass_id = data.get('sixerclass_id')

        # Find student
        student = None
        for s in students_data:
            if (s['student_name'] == student_name and 
                s['batch_number'] == batch_number and 
                s['sixerclass_id'] == sixerclass_id):
                student = s
                break

        if student:
            session['student'] = student
            logger.info(f"✅ Student authenticated: {student_name}")
            return jsonify({"success": True, "student": student})
        else:
            logger.warning(f"❌ Authentication failed for: {student_name}")
            return jsonify({"error": "Student not found. Please check your details."}), 404

    except Exception as e:
        logger.error(f"❌ Authentication error: {e}")
        return jsonify({"error": "Authentication failed"}), 500

@app.route('/api/download-certificate', methods=['POST'])
def download_certificate():
    try:
        if 'student' not in session:
            return jsonify({"error": "Please authenticate first"}), 401

        student = session['student']
        
        # Generate certificate
        safe_name = secure_filename(student['student_name'].replace(' ', '_'))
        filename = f"certificate_{student['sixerclass_id']}_{safe_name}.pdf"
        filepath = os.path.join(app.config['CERTIFICATE_DIR'], filename)
        
        # Create certificate
        success = cert_generator.create_certificate(student, filepath)
        
        if success:
            logger.info(f"✅ Certificate generated: {filename}")
            return jsonify({
                "success": True,
                "download_url": f"/api/serve-certificate/{filename}",
                "filename": filename,
                "student_name": student['student_name']
            })
        else:
            return jsonify({"error": "Certificate generation failed"}), 500

    except Exception as e:
        logger.error(f"❌ Certificate error: {e}")
        return jsonify({"error": "Certificate generation failed"}), 500

@app.route('/api/serve-certificate/<filename>')
def serve_certificate(filename):
    try:
        if not filename.startswith('certificate_') or not filename.endswith('.pdf'):
            return jsonify({"error": "Invalid filename"}), 400
            
        filepath = os.path.join(app.config['CERTIFICATE_DIR'], filename)
        
        if os.path.exists(filepath):
            logger.info(f"✅ Serving certificate: {filename}")
            return send_file(filepath, as_attachment=True, download_name=filename)
        else:
            return jsonify({"error": "Certificate not found"}), 404
            
    except Exception as e:
        logger.error(f"❌ File serving error: {e}")
        return jsonify({"error": "File serving failed"}), 500

@app.route('/api/students')
def get_students():
    return jsonify({
        "success": True,
        "count": len(students_data),
        "students": students_data
    })

# ADMIN ROUTES WITH AUTHENTICATION
@app.route('/admin')
def admin_redirect():
    return redirect('/admin/login')

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        
        # Simple admin credentials (change these for production)
        if username == 'admin' and password == 'admin123':
            session['admin_logged_in'] = True
            return jsonify({"success": True})
        else:
            return jsonify({"error": "Invalid credentials"}), 401
    
    return '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Admin Login - AWS Certificate System</title>
        <style>
            body { font-family: Arial, sans-serif; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; display: flex; align-items: center; justify-content: center; margin: 0; }
            .login-container { background: white; padding: 3rem; border-radius: 15px; box-shadow: 0 10px 30px rgba(0,0,0,0.2); max-width: 400px; width: 100%; }
            .header { text-align: center; margin-bottom: 2rem; }
            .header h1 { color: #333; margin-bottom: 0.5rem; }
            .form-group { margin-bottom: 1.5rem; }
            .form-group label { display: block; margin-bottom: 0.5rem; color: #555; font-weight: bold; }
            .form-group input { width: 100%; padding: 1rem; border: 2px solid #ddd; border-radius: 8px; font-size: 1rem; }
            .btn { width: 100%; padding: 1rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border: none; border-radius: 8px; font-size: 1rem; cursor: pointer; }
            .error { color: red; margin-top: 1rem; text-align: center; }
        </style>
    </head>
    <body>
        <div class="login-container">
            <div class="header">
                <h1>🔐 Admin Login</h1>
                <p>AWS Training Certificate System</p>
            </div>
            
            <form id="loginForm">
                <div class="form-group">
                    <label for="username">Username:</label>
                    <input type="text" id="username" name="username" required>
                </div>
                
                <div class="form-group">
                    <label for="password">Password:</label>
                    <input type="password" id="password" name="password" required>
                </div>
                
                <button type="submit" class="btn">Login</button>
            </form>
            
            <div id="error" class="error"></div>
        </div>
        
        <script>
            document.getElementById('loginForm').addEventListener('submit', async (e) => {
                e.preventDefault();
                
                const formData = new FormData(e.target);
                const data = Object.fromEntries(formData);
                
                try {
                    const response = await fetch('/admin/login', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify(data)
                    });
                    
                    const result = await response.json();
                    
                    if (result.success) {
                        window.location.href = '/admin/students';
                    } else {
                        document.getElementById('error').textContent = result.error;
                    }
                } catch (error) {
                    document.getElementById('error').textContent = 'Login failed';
                }
            });
        </script>
    </body>
    </html>
    '''

def require_admin_auth():
    """Check if admin is logged in"""
    if not session.get('admin_logged_in'):
        return redirect('/admin/login')
    return None

@app.route('/admin/students')
def admin_students():
    # Check authentication
    auth_check = require_admin_auth()
    if auth_check:
        return auth_check
    
    return '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Student Management - AWS Certificate System</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 0; background: #f5f5f5; }
            .header { background: #007bff; color: white; padding: 1rem; display: flex; justify-content: space-between; align-items: center; }
            .container { max-width: 1200px; margin: 2rem auto; padding: 2rem; background: white; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
            .actions { display: flex; gap: 1rem; margin-bottom: 2rem; flex-wrap: wrap; }
            .btn { padding: 0.75rem 1.5rem; background: #007bff; color: white; border: none; border-radius: 5px; cursor: pointer; text-decoration: none; display: inline-block; }
            .btn:hover { background: #0056b3; }
            .btn-success { background: #28a745; }
            .btn-success:hover { background: #1e7e34; }
            .btn-danger { background: #dc3545; }
            .btn-danger:hover { background: #c82333; }
            .stats { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem; margin-bottom: 2rem; }
            .stat-card { background: #f8f9fa; padding: 1.5rem; border-radius: 8px; text-align: center; border-left: 4px solid #007bff; }
            .stat-card h3 { margin: 0; font-size: 2rem; color: #007bff; }
            .stat-card p { margin: 0.5rem 0 0 0; color: #666; }
            .table-container { overflow-x: auto; }
            table { width: 100%; border-collapse: collapse; margin-top: 1rem; }
            th, td { padding: 0.75rem; text-align: left; border-bottom: 1px solid #ddd; }
            th { background: #f8f9fa; font-weight: bold; }
            tr:hover { background: #f8f9fa; }
            .search-box { width: 100%; padding: 0.75rem; border: 1px solid #ddd; border-radius: 5px; margin-bottom: 1rem; }
            .upload-area { border: 2px dashed #007bff; border-radius: 10px; padding: 2rem; text-align: center; margin: 1rem 0; background: #f8f9fa; }
            .upload-area.dragover { background: #e3f2fd; border-color: #0056b3; }
            #fileInput { display: none; }
            .alert { padding: 1rem; border-radius: 5px; margin: 1rem 0; }
            .alert-success { background: #d4edda; color: #155724; border: 1px solid #c3e6cb; }
            .alert-error { background: #f8d7da; color: #721c24; border: 1px solid #f5c6cb; }
            .modal { display: none; position: fixed; z-index: 1000; left: 0; top: 0; width: 100%; height: 100%; background-color: rgba(0,0,0,0.5); overflow: auto; }
            .modal-content { background-color: white; margin: 5% auto; padding: 20px; border-radius: 10px; width: 90%; max-width: 500px; max-height: 80vh; overflow-y: auto; }
            .form-group { margin-bottom: 1rem; }
            .form-group label { display: block; margin-bottom: 0.5rem; font-weight: bold; }
            .form-group input { width: 100%; padding: 0.5rem; border: 1px solid #ddd; border-radius: 5px; }
        </style>
    </head>
    <body>
        <div class="header">
            <div>
                <h1>📋 Student Management</h1>
                <p>AWS Training Certificate System</p>
            </div>
            <button class="btn btn-danger" onclick="logout()">Logout</button>
        </div>
        
        <div class="container">
            <div class="stats" id="stats">
                <div class="stat-card">
                    <h3 id="totalStudents">0</h3>
                    <p>Total Students</p>
                </div>
                <div class="stat-card">
                    <h3 id="totalBatches">0</h3>
                    <p>Total Batches</p>
                </div>
                <div class="stat-card">
                    <h3 id="recentStudents">0</h3>
                    <p>Recent Additions</p>
                </div>
            </div>
            
            <div class="actions">
                <button class="btn btn-success" onclick="showAddModal()">➕ Add Student</button>
                <button class="btn btn-success" onclick="exportStudents()">📅 Export Excel</button>
                <button class="btn btn-success" onclick="document.getElementById('fileInput').click()">📄 Import Excel</button>
                <button class="btn" onclick="refreshData()">🔄 Refresh</button>
                <a href="/" class="btn">← Back to Main</a>
            </div>
            
            <div class="upload-area" id="uploadArea">
                <h3>📄 Import Students from Excel</h3>
                <p>Drag and drop an Excel file here, or click "Import Excel" to select a file</p>
                <p><small>Supported formats: .xlsx, .xls</small></p>
                <input type="file" id="fileInput" accept=".xlsx,.xls" onchange="handleFileSelect(event)">
            </div>
            
            <div id="alertContainer"></div>
            
            <input type="text" class="search-box" id="searchBox" placeholder="🔍 Search students by name, batch, or ID..." onkeyup="filterStudents()">
            
            <div class="table-container">
                <table id="studentsTable">
                    <thead>
                        <tr>
                            <th>SixerClass ID</th>
                            <th>Student Name</th>
                            <th>Batch Number</th>
                            <th>Start Date</th>
                            <th>End Date</th>
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody id="studentsTableBody">
                        <tr>
                            <td colspan="6" style="text-align: center; padding: 2rem;">Loading students...</td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
        
        <!-- Add Student Modal -->
        <div id="addModal" class="modal">
            <div class="modal-content">
                <h2>➕ Add New Student</h2>
                <form id="addStudentForm">
                    <div class="form-group">
                        <label for="addName">Student Name:</label>
                        <input type="text" id="addName" required>
                    </div>
                    <div class="form-group">
                        <label for="addBatch">Batch Number:</label>
                        <input type="text" id="addBatch" placeholder="AWS-2024-001" required>
                    </div>
                    <div class="form-group">
                        <label for="addStartDate">Start Date:</label>
                        <input type="date" id="addStartDate" required>
                    </div>
                    <div class="form-group">
                        <label for="addEndDate">End Date:</label>
                        <input type="date" id="addEndDate" required>
                    </div>
                    <div class="form-group">
                        <label for="addId">SixerClass ID:</label>
                        <input type="text" id="addId" placeholder="SIX001" required>
                    </div>
                    <div style="display: flex; gap: 1rem; margin-top: 2rem;">
                        <button type="submit" class="btn btn-success">Add Student</button>
                        <button type="button" class="btn" onclick="closeAddModal()">Cancel</button>
                    </div>
                </form>
            </div>
        </div>
        
        <!-- Edit Student Modal -->
        <div id="editModal" class="modal">
            <div class="modal-content">
                <h2>✏️ Edit Student</h2>
                <form id="editStudentForm">
                    <input type="hidden" id="editOriginalId">
                    <div class="form-group">
                        <label for="editName">Student Name:</label>
                        <input type="text" id="editName" required>
                    </div>
                    <div class="form-group">
                        <label for="editBatch">Batch Number:</label>
                        <input type="text" id="editBatch" required>
                    </div>
                    <div class="form-group">
                        <label for="editStartDate">Start Date:</label>
                        <input type="date" id="editStartDate" required>
                    </div>
                    <div class="form-group">
                        <label for="editEndDate">End Date:</label>
                        <input type="date" id="editEndDate" required>
                    </div>
                    <div class="form-group">
                        <label for="editId">SixerClass ID:</label>
                        <input type="text" id="editId" required>
                    </div>
                    <div style="display: flex; gap: 1rem; margin-top: 2rem;">
                        <button type="submit" class="btn btn-success">Update Student</button>
                        <button type="button" class="btn" onclick="closeEditModal()">Cancel</button>
                    </div>
                </form>
            </div>
        </div>
        
        <script>
            let allStudents = [];
            
            async function loadStudents() {
                try {
                    const response = await fetch('/admin/api/students');
                    const data = await response.json();
                    
                    if (data.success) {
                        allStudents = data.students;
                        displayStudents(allStudents);
                        updateStats();
                    } else {
                        showAlert('Failed to load students', 'error');
                    }
                } catch (error) {
                    console.error('Error loading students:', error);
                    showAlert('Error loading students', 'error');
                }
            }
            
            function displayStudents(students) {
                const tbody = document.getElementById('studentsTableBody');
                
                if (students.length === 0) {
                    tbody.innerHTML = '<tr><td colspan="6" style="text-align: center; padding: 2rem;">No students found</td></tr>';
                    return;
                }
                
                tbody.innerHTML = students.map(student => `
                    <tr>
                        <td>${student.sixerclass_id}</td>
                        <td>${student.student_name}</td>
                        <td>${student.batch_number}</td>
                        <td>${student.batch_start_date}</td>
                        <td>${student.batch_end_date}</td>
                        <td>
                            <button class="btn" onclick="generateCertificate('${student.sixerclass_id}')">📄 Certificate</button>
                            <button class="btn" onclick="editStudent('${student.sixerclass_id}')">✏️ Edit</button>
                            <button class="btn btn-danger" onclick="deleteStudent('${student.sixerclass_id}')">🗑️ Delete</button>
                        </td>
                    </tr>
                `).join('');
            }
            
            function updateStats() {
                document.getElementById('totalStudents').textContent = allStudents.length;
                
                const batches = new Set(allStudents.map(s => s.batch_number));
                document.getElementById('totalBatches').textContent = batches.size;
                
                const recentCount = Math.ceil(allStudents.length * 0.1);
                document.getElementById('recentStudents').textContent = recentCount;
            }
            
            function filterStudents() {
                const searchTerm = document.getElementById('searchBox').value.toLowerCase();
                const filtered = allStudents.filter(student => 
                    student.student_name.toLowerCase().includes(searchTerm) ||
                    student.batch_number.toLowerCase().includes(searchTerm) ||
                    student.sixerclass_id.toLowerCase().includes(searchTerm)
                );
                displayStudents(filtered);
            }
            
            async function exportStudents() {
                try {
                    const response = await fetch('/admin/api/students/export');
                    if (response.ok) {
                        const blob = await response.blob();
                        const url = window.URL.createObjectURL(blob);
                        const a = document.createElement('a');
                        a.href = url;
                        a.download = `students_export_${new Date().toISOString().split('T')[0]}.xlsx`;
                        document.body.appendChild(a);
                        a.click();
                        document.body.removeChild(a);
                        window.URL.revokeObjectURL(url);
                        showAlert('Students exported successfully!', 'success');
                    } else {
                        showAlert('Export failed', 'error');
                    }
                } catch (error) {
                    console.error('Export error:', error);
                    showAlert('Export error', 'error');
                }
            }
            
            function handleFileSelect(event) {
                const file = event.target.files[0];
                if (file) {
                    uploadFile(file);
                }
            }
            
            async function uploadFile(file) {
                const formData = new FormData();
                formData.append('file', file);
                
                try {
                    showAlert('Uploading and processing file...', 'success');
                    
                    const response = await fetch('/admin/api/students/import', {
                        method: 'POST',
                        body: formData
                    });
                    
                    const result = await response.json();
                    
                    if (result.success) {
                        showAlert(`Import successful! ${result.imported_count} students imported.`, 'success');
                        loadStudents();
                    } else {
                        showAlert(`Import failed: ${result.error}`, 'error');
                    }
                } catch (error) {
                    console.error('Upload error:', error);
                    showAlert('Upload failed', 'error');
                }
            }
            
            function showAlert(message, type) {
                const container = document.getElementById('alertContainer');
                const alert = document.createElement('div');
                alert.className = `alert alert-${type}`;
                alert.textContent = message;
                container.innerHTML = '';
                container.appendChild(alert);
                
                setTimeout(() => {
                    container.innerHTML = '';
                }, 5000);
            }
            
            function refreshData() {
                loadStudents();
                showAlert('Data refreshed!', 'success');
            }
            
            const uploadArea = document.getElementById('uploadArea');
            
            uploadArea.addEventListener('dragover', (e) => {
                e.preventDefault();
                uploadArea.classList.add('dragover');
            });
            
            uploadArea.addEventListener('dragleave', () => {
                uploadArea.classList.remove('dragover');
            });
            
            uploadArea.addEventListener('drop', (e) => {
                e.preventDefault();
                uploadArea.classList.remove('dragover');
                
                const files = e.dataTransfer.files;
                if (files.length > 0) {
                    uploadFile(files[0]);
                }
            });
            
            async function deleteStudent(sixerclassId) {
                if (!confirm('Are you sure you want to delete this student?')) {
                    return;
                }
                
                try {
                    const response = await fetch('/admin/api/students/delete', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ sixerclass_id: sixerclassId })
                    });
                    
                    const result = await response.json();
                    
                    if (result.success) {
                        showAlert(`Student deleted successfully!`, 'success');
                        loadStudents();
                    } else {
                        showAlert(`Delete failed: ${result.error}`, 'error');
                    }
                } catch (error) {
                    showAlert('Delete error', 'error');
                }
            }
            
            function showAddModal() {
                document.getElementById('addModal').style.display = 'block';
            }
            
            function closeAddModal() {
                document.getElementById('addModal').style.display = 'none';
                document.getElementById('addStudentForm').reset();
            }
            
            document.getElementById('addStudentForm').addEventListener('submit', async (e) => {
                e.preventDefault();
                
                const studentData = {
                    student_name: document.getElementById('addName').value,
                    batch_number: document.getElementById('addBatch').value,
                    batch_start_date: document.getElementById('addStartDate').value,
                    batch_end_date: document.getElementById('addEndDate').value,
                    sixerclass_id: document.getElementById('addId').value
                };
                
                try {
                    const response = await fetch('/admin/api/students/add', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify(studentData)
                    });
                    
                    const result = await response.json();
                    
                    if (result.success) {
                        showAlert('Student added successfully!', 'success');
                        closeAddModal();
                        loadStudents();
                    } else {
                        showAlert(`Add failed: ${result.error}`, 'error');
                    }
                } catch (error) {
                    showAlert('Add student error', 'error');
                }
            });
            
            async function generateCertificate(sixerclassId) {
                const student = allStudents.find(s => s.sixerclass_id === sixerclassId);
                if (!student) {
                    showAlert('Student not found', 'error');
                    return;
                }
                
                try {
                    const response = await fetch('/admin/api/generate-certificate', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ student: student })
                    });
                    
                    const result = await response.json();
                    
                    if (result.success) {
                        // Download certificate
                        const link = document.createElement('a');
                        link.href = result.download_url;
                        link.download = result.filename;
                        document.body.appendChild(link);
                        link.click();
                        document.body.removeChild(link);
                        showAlert(`Certificate generated for ${result.student_name}!`, 'success');
                    } else {
                        showAlert(`Certificate generation failed: ${result.error}`, 'error');
                    }
                } catch (error) {
                    showAlert('Certificate generation error', 'error');
                }
            }
            
            function editStudent(sixerclassId) {
                const student = allStudents.find(s => s.sixerclass_id === sixerclassId);
                if (!student) {
                    showAlert('Student not found', 'error');
                    return;
                }
                
                // Populate edit form
                document.getElementById('editOriginalId').value = student.sixerclass_id;
                document.getElementById('editName').value = student.student_name;
                document.getElementById('editBatch').value = student.batch_number;
                document.getElementById('editStartDate').value = student.batch_start_date;
                document.getElementById('editEndDate').value = student.batch_end_date;
                document.getElementById('editId').value = student.sixerclass_id;
                
                document.getElementById('editModal').style.display = 'block';
            }
            
            function closeEditModal() {
                document.getElementById('editModal').style.display = 'none';
                document.getElementById('editStudentForm').reset();
            }
            
            document.getElementById('editStudentForm').addEventListener('submit', async (e) => {
                e.preventDefault();
                
                const updateData = {
                    original_sixerclass_id: document.getElementById('editOriginalId').value,
                    student_name: document.getElementById('editName').value,
                    batch_number: document.getElementById('editBatch').value,
                    batch_start_date: document.getElementById('editStartDate').value,
                    batch_end_date: document.getElementById('editEndDate').value,
                    sixerclass_id: document.getElementById('editId').value
                };
                
                try {
                    const response = await fetch('/admin/api/students/update', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify(updateData)
                    });
                    
                    const result = await response.json();
                    
                    if (result.success) {
                        showAlert('Student updated successfully!', 'success');
                        closeEditModal();
                        loadStudents();
                    } else {
                        showAlert(`Update failed: ${result.error}`, 'error');
                    }
                } catch (error) {
                    showAlert('Update student error', 'error');
                }
            });
            
            function logout() {
                if (confirm('Are you sure you want to logout?')) {
                    fetch('/admin/logout', { method: 'POST' })
                        .then(response => response.json())
                        .then(data => {
                            if (data.success) {
                                window.location.href = '/admin/login';
                            }
                        })
                        .catch(() => {
                            window.location.href = '/admin/login';
                        });
                }
            }
            
            loadStudents();
        </script>
    </body>
    </html>
    '''

# ADMIN API ROUTES
@app.route('/admin/api/students')
def admin_api_students():
    """Get all students with optional search"""
    # Check authentication
    if not session.get('admin_logged_in'):
        return jsonify({"error": "Unauthorized"}), 401
    
    try:
        search = request.args.get('search', '').lower()
        
        if search:
            filtered_students = [
                s for s in students_data 
                if search in s['student_name'].lower() or 
                   search in s['batch_number'].lower() or 
                   search in s['sixerclass_id'].lower()
            ]
        else:
            filtered_students = students_data
        
        return jsonify({
            "success": True,
            "total": len(filtered_students),
            "students": filtered_students
        })
    except Exception as e:
        logger.error(f"❌ Error getting students: {e}")
        return jsonify({"error": "Failed to get students"}), 500

@app.route('/admin/api/students/export')
def admin_export_students():
    """Export students to Excel"""
    # Check authentication
    if not session.get('admin_logged_in'):
        return jsonify({"error": "Unauthorized"}), 401
    
    try:
        df = pd.DataFrame(students_data)
        
        # Create filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"students_export_{timestamp}.xlsx"
        filepath = os.path.join(app.config['EXCEL_DIR'], filename)
        
        # Export to Excel
        df.to_excel(filepath, index=False, engine='openpyxl')
        
        logger.info(f"✅ Students exported to: {filename}")
        return send_file(filepath, as_attachment=True, download_name=filename)
        
    except Exception as e:
        logger.error(f"❌ Error exporting students: {e}")
        return jsonify({"error": "Export failed"}), 500

@app.route('/admin/api/students/import', methods=['POST'])
def admin_import_students():
    """Import students from Excel file"""
    global students_data
    
    # Check authentication
    if not session.get('admin_logged_in'):
        return jsonify({"error": "Unauthorized"}), 401
    
    try:
        if 'file' not in request.files:
            return jsonify({"error": "No file uploaded"}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({"error": "No file selected"}), 400
        
        if not file.filename.lower().endswith(('.xlsx', '.xls')):
            return jsonify({"error": "Invalid file format. Please upload Excel file (.xlsx or .xls)"}), 400
        
        # Save uploaded file
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Read Excel file - try first sheet
        try:
            df = pd.read_excel(filepath, sheet_name=0)
        except Exception as e:
            logger.error(f"Error reading Excel: {e}")
            return jsonify({"error": f"Cannot read Excel file: {str(e)}"}), 400
        
        # Validate required columns
        required_columns = ['student_name', 'batch_number', 'batch_start_date', 'batch_end_date', 'sixerclass_id']
        missing_columns = [col for col in required_columns if col not in df.columns]
        
        if missing_columns:
            return jsonify({
                "error": f"Missing required columns: {', '.join(missing_columns)}"
            }), 400
        
        # Convert to records and clean data
        new_students = []
        for _, row in df.iterrows():
            try:
                student = {
                    'student_name': str(row['student_name']).strip(),
                    'batch_number': str(row['batch_number']).strip(),
                    'batch_start_date': str(row['batch_start_date']).strip(),
                    'batch_end_date': str(row['batch_end_date']).strip(),
                    'sixerclass_id': str(row['sixerclass_id']).strip()
                }
                new_students.append(student)
            except Exception as e:
                logger.error(f"Error processing row: {e}")
                continue
        
        # Validate and add students
        imported_count = 0
        errors = []
        
        for student in new_students:
            # Check for duplicates
            if any(s['sixerclass_id'] == student['sixerclass_id'] for s in students_data):
                errors.append(f"Duplicate SixerClass ID: {student['sixerclass_id']}")
                continue
            
            # Add to students_data
            students_data.append(student)
            imported_count += 1
        
        # Save updated data to Excel
        try:
            updated_df = pd.DataFrame(students_data)
            updated_df.to_excel('excel-samples/student-data.xlsx', index=False)
        except Exception as e:
            logger.error(f"Error saving data: {e}")
        
        logger.info(f"✅ Imported {imported_count} students from {filename}")
        
        return jsonify({
            "success": True,
            "message": f"Successfully imported {imported_count} students",
            "imported_count": imported_count,
            "errors": errors[:5]  # Return first 5 errors
        })
        
    except Exception as e:
        logger.error(f"❌ Error importing students: {e}")
        return jsonify({"error": f"Import failed: {str(e)}"}), 500

@app.route('/admin/api/students/update', methods=['POST'])
def admin_update_student():
    """Update student details"""
    global students_data
    
    # Check authentication
    if not session.get('admin_logged_in'):
        return jsonify({"error": "Unauthorized"}), 401
    
    try:
        data = request.get_json()
        original_id = data.get('original_sixerclass_id')
        
        if not original_id:
            return jsonify({"error": "Original SixerClass ID required"}), 400
        
        # Find student to update
        student_index = None
        for i, s in enumerate(students_data):
            if s['sixerclass_id'] == original_id:
                student_index = i
                break
        
        if student_index is None:
            return jsonify({"error": "Student not found"}), 404
        
        # Validate required fields
        required_fields = ['student_name', 'batch_number', 'batch_start_date', 'batch_end_date', 'sixerclass_id']
        for field in required_fields:
            if not data.get(field):
                return jsonify({"error": f"Missing required field: {field}"}), 400
        
        # Check for duplicate SixerClass ID (if changed)
        new_id = data['sixerclass_id']
        if new_id != original_id:
            if any(s['sixerclass_id'] == new_id for s in students_data):
                return jsonify({"error": f"SixerClass ID {new_id} already exists"}), 400
        
        # Update student
        students_data[student_index] = {
            'student_name': data['student_name'].strip(),
            'batch_number': data['batch_number'].strip(),
            'batch_start_date': data['batch_start_date'].strip(),
            'batch_end_date': data['batch_end_date'].strip(),
            'sixerclass_id': data['sixerclass_id'].strip()
        }
        
        # Save to Excel file
        try:
            df = pd.DataFrame(students_data)
            df.to_excel('excel-samples/student-data.xlsx', index=False)
        except Exception as e:
            logger.error(f"Error saving data: {e}")
        
        logger.info(f"✅ Updated student: {data['student_name']} ({data['sixerclass_id']})")
        
        return jsonify({
            "success": True,
            "message": f"Student {data['student_name']} updated successfully",
            "student": students_data[student_index]
        })
        
    except Exception as e:
        logger.error(f"❌ Error updating student: {e}")
        return jsonify({"error": "Failed to update student"}), 500

@app.route('/admin/logout', methods=['POST'])
def admin_logout():
    """Admin logout"""
    session.pop('admin_logged_in', None)
    return jsonify({"success": True})

@app.route('/admin/api/students/add', methods=['POST'])
def admin_add_student():
    """Add a new student manually"""
    global students_data
    
    # Check authentication
    if not session.get('admin_logged_in'):
        return jsonify({"error": "Unauthorized"}), 401
    
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['student_name', 'batch_number', 'batch_start_date', 'batch_end_date', 'sixerclass_id']
        for field in required_fields:
            if not data.get(field):
                return jsonify({"error": f"Missing required field: {field}"}), 400
        
        # Check for duplicate SixerClass ID
        if any(s['sixerclass_id'] == data['sixerclass_id'] for s in students_data):
            return jsonify({"error": f"SixerClass ID {data['sixerclass_id']} already exists"}), 400
        
        # Create new student
        new_student = {
            'student_name': data['student_name'].strip(),
            'batch_number': data['batch_number'].strip(),
            'batch_start_date': data['batch_start_date'].strip(),
            'batch_end_date': data['batch_end_date'].strip(),
            'sixerclass_id': data['sixerclass_id'].strip()
        }
        
        # Add to students_data
        students_data.append(new_student)
        
        # Save to Excel file
        try:
            df = pd.DataFrame(students_data)
            df.to_excel('excel-samples/student-data.xlsx', index=False)
        except Exception as e:
            logger.error(f"Error saving data: {e}")
        
        logger.info(f"✅ Added new student: {new_student['student_name']} ({new_student['sixerclass_id']})")
        
        return jsonify({
            "success": True,
            "message": f"Student {new_student['student_name']} added successfully",
            "student": new_student
        })
        
    except Exception as e:
        logger.error(f"❌ Error adding student: {e}")
        return jsonify({"error": "Failed to add student"}), 500

@app.route('/admin/api/students/delete', methods=['POST'])
def admin_delete_student():
    """Delete a student"""
    global students_data
    
    # Check authentication
    if not session.get('admin_logged_in'):
        return jsonify({"error": "Unauthorized"}), 401
    
    try:
        data = request.get_json()
        sixerclass_id = data.get('sixerclass_id')
        
        if not sixerclass_id:
            return jsonify({"error": "SixerClass ID required"}), 400
        
        # Find and remove student
        original_count = len(students_data)
        students_data = [s for s in students_data if s['sixerclass_id'] != sixerclass_id]
        
        if len(students_data) == original_count:
            return jsonify({"error": "Student not found"}), 404
        
        # Save updated data to Excel
        try:
            df = pd.DataFrame(students_data)
            df.to_excel('excel-samples/student-data.xlsx', index=False)
        except Exception as e:
            logger.error(f"Error saving data: {e}")
        
        logger.info(f"✅ Deleted student with ID: {sixerclass_id}")
        
        return jsonify({
            "success": True,
            "message": f"Student with ID {sixerclass_id} deleted successfully"
        })
        
    except Exception as e:
        logger.error(f"❌ Error deleting student: {e}")
        return jsonify({"error": "Failed to delete student"}), 500

@app.route('/admin/api/generate-certificate', methods=['POST'])
def admin_generate_certificate():
    """Generate certificate for a student from admin panel"""
    # Check authentication
    if not session.get('admin_logged_in'):
        return jsonify({"error": "Unauthorized"}), 401
    
    try:
        data = request.get_json()
        student = data.get('student')
        
        if not student:
            return jsonify({"error": "Student data required"}), 400
        
        # Generate certificate
        safe_name = secure_filename(student['student_name'].replace(' ', '_'))
        filename = f"certificate_{student['sixerclass_id']}_{safe_name}.pdf"
        filepath = os.path.join(app.config['CERTIFICATE_DIR'], filename)
        
        success = cert_generator.create_certificate(student, filepath)
        
        if success:
            logger.info(f"✅ Admin certificate generated: {filename}")
            return jsonify({
                "success": True,
                "download_url": f"/api/serve-certificate/{filename}",
                "filename": filename,
                "student_name": student['student_name']
            })
        else:
            return jsonify({"error": "Certificate generation failed"}), 500
            
    except Exception as e:
        logger.error(f"❌ Admin certificate error: {e}")
        return jsonify({"error": "Certificate generation failed"}), 500

if __name__ == '__main__':
    logger.info("🚀 Starting AWS Training Certificate System - Production Ready")
    logger.info(f"📊 Loaded {len(students_data)} students")
    app.run(host='0.0.0.0', port=5000, debug=False)