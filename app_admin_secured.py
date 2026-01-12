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
        {'student_name': 'Rahul Sharma', 'batch_number': 'AWS-2024-001', 'batch_start_date': '2024-01-15', 'batch_end_date': '2024-04-15', 'sixerclass_id': 'SIX001'},
        {'student_name': 'Priya Patel', 'batch_number': 'AWS-2024-001', 'batch_start_date': '2024-01-15', 'batch_end_date': '2024-04-15', 'sixerclass_id': 'SIX002'},
        {'student_name': 'Amit Kumar', 'batch_number': 'AWS-2024-002', 'batch_start_date': '2024-02-01', 'batch_end_date': '2024-05-01', 'sixerclass_id': 'SIX003'},
        {'student_name': 'Neha Gupta', 'batch_number': 'AWS-2024-002', 'batch_start_date': '2024-02-01', 'batch_end_date': '2024-05-01', 'sixerclass_id': 'SIX004'},
        {'student_name': 'Vikram Singh', 'batch_number': 'AWS-2024-002', 'batch_start_date': '2024-02-01', 'batch_end_date': '2024-05-01', 'sixerclass_id': 'SIX005'},
        {'student_name': 'Anjali Sharma', 'batch_number': 'AWS-2024-002', 'batch_start_date': '2024-02-01', 'batch_end_date': '2024-05-01', 'sixerclass_id': 'SIX006'}
    ]
    
    df = pd.DataFrame(sample_data)
    os.makedirs('excel-samples', exist_ok=True)
    df.to_excel('excel-samples/student-data.xlsx', index=False)
    logger.info("✅ Created sample Excel data with 6 students")
    return sample_data

def load_students_data():
    global students_data
    try:
        possible_paths = ['aws-final-deployment/excel-samples/student-data.xlsx', 'excel-samples/student-data.xlsx']
        
        for excel_path in possible_paths:
            if os.path.exists(excel_path):
                df = pd.read_excel(excel_path)
                students_data = df.to_dict('records')
                logger.info(f"✅ Loaded {len(students_data)} students from {excel_path}")
                return students_data
        
        students_data = create_sample_data()
        return students_data
        
    except Exception as e:
        logger.error(f"❌ Error loading students data: {e}")
        students_data = create_sample_data()
        return students_data

load_students_data()

@app.route('/')
def index():
    return '''
    <!DOCTYPE html>
    <html><head><title>AWS Training Certificate System</title>
    <style>body{font-family:Arial;background:linear-gradient(135deg,#667eea 0%,#764ba2 100%);min-height:100vh;display:flex;align-items:center;justify-content:center;margin:0}.container{background:white;padding:3rem;border-radius:15px;box-shadow:0 10px 30px rgba(0,0,0,0.2);max-width:500px;width:100%}.header{text-align:center;margin-bottom:2rem}.form-group{margin-bottom:1.5rem}.form-group input{width:100%;padding:1rem;border:2px solid #ddd;border-radius:8px;font-size:1rem}.btn{width:100%;padding:1rem;background:linear-gradient(135deg,#667eea 0%,#764ba2 100%);color:white;border:none;border-radius:8px;cursor:pointer}</style>
    </head><body>
    <div class="container">
        <div class="header"><h1>🎓 AWS Training Certificate System</h1></div>
        <form id="authForm">
            <div class="form-group"><input type="text" id="student_name" placeholder="Student Name" required></div>
            <div class="form-group"><input type="text" id="batch_number" placeholder="Batch Number" required></div>
            <div class="form-group"><input type="text" id="sixerclass_id" placeholder="SixerClass ID" required></div>
            <button type="submit" class="btn">Download Certificate</button>
        </form>
        <div style="text-align:center;margin-top:2rem"><a href="/admin" style="color:#667eea">🔧 Admin Panel</a></div>
    </div>
    <script>
    document.getElementById('authForm').addEventListener('submit', async (e) => {
        e.preventDefault();
        const data = {
            student_name: document.getElementById('student_name').value,
            batch_number: document.getElementById('batch_number').value,
            sixerclass_id: document.getElementById('sixerclass_id').value
        };
        
        try {
            const response = await fetch('/api/authenticate', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            });
            
            const result = await response.json();
            
            if (result.success) {
                const downloadResponse = await fetch('/api/download-certificate', { method: 'POST' });
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
    </body></html>
    '''

@app.route('/api/check-status')
def check_status():
    return jsonify({"status": "operational", "students_loaded": len(students_data), "timestamp": datetime.now().isoformat()})

@app.route('/api/authenticate', methods=['POST'])
def authenticate():
    try:
        data = request.get_json()
        student_name = data.get('student_name')
        batch_number = data.get('batch_number')
        sixerclass_id = data.get('sixerclass_id')

        student = None
        for s in students_data:
            if (s['student_name'] == student_name and s['batch_number'] == batch_number and s['sixerclass_id'] == sixerclass_id):
                student = s
                break

        if student:
            session['student'] = student
            return jsonify({"success": True, "student": student})
        else:
            return jsonify({"error": "Student not found"}), 404
    except Exception as e:
        return jsonify({"error": "Authentication failed"}), 500

@app.route('/api/download-certificate', methods=['POST'])
def download_certificate():
    try:
        if 'student' not in session:
            return jsonify({"error": "Please authenticate first"}), 401

        student = session['student']
        safe_name = secure_filename(student['student_name'].replace(' ', '_'))
        filename = f"certificate_{student['sixerclass_id']}_{safe_name}.pdf"
        filepath = os.path.join(app.config['CERTIFICATE_DIR'], filename)
        
        success = cert_generator.create_certificate(student, filepath)
        
        if success:
            return jsonify({"success": True, "download_url": f"/api/serve-certificate/{filename}", "filename": filename})
        else:
            return jsonify({"error": "Certificate generation failed"}), 500
    except Exception as e:
        return jsonify({"error": "Certificate generation failed"}), 500

@app.route('/api/serve-certificate/<filename>')
def serve_certificate(filename):
    try:
        if not filename.startswith('certificate_') or not filename.endswith('.pdf'):
            return jsonify({"error": "Invalid filename"}), 400
        filepath = os.path.join(app.config['CERTIFICATE_DIR'], filename)
        if os.path.exists(filepath):
            return send_file(filepath, as_attachment=True, download_name=filename)
        else:
            return jsonify({"error": "Certificate not found"}), 404
    except Exception as e:
        return jsonify({"error": "File serving failed"}), 500

# ADMIN AUTHENTICATION
@app.route('/admin')
def admin_redirect():
    return redirect('/admin/login')

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        data = request.get_json()
        if data.get('username') == 'admin' and data.get('password') == 'admin123':
            session['admin_logged_in'] = True
            return jsonify({"success": True})
        else:
            return jsonify({"error": "Invalid credentials"}), 401
    
    return '''<!DOCTYPE html><html><head><title>Admin Login</title>
    <style>body{font-family:Arial;background:linear-gradient(135deg,#667eea 0%,#764ba2 100%);min-height:100vh;display:flex;align-items:center;justify-content:center;margin:0}.container{background:white;padding:3rem;border-radius:15px;box-shadow:0 10px 30px rgba(0,0,0,0.2);max-width:400px;width:100%}.form-group{margin-bottom:1.5rem}.form-group input{width:100%;padding:1rem;border:2px solid #ddd;border-radius:8px}.btn{width:100%;padding:1rem;background:linear-gradient(135deg,#667eea 0%,#764ba2 100%);color:white;border:none;border-radius:8px;cursor:pointer}.error{color:red;margin-top:1rem;text-align:center}</style>
    </head><body>
    <div class="container">
        <div style="text-align:center;margin-bottom:2rem"><h1>🔐 Admin Login</h1></div>
        <form id="loginForm">
            <div class="form-group"><input type="text" id="username" placeholder="Username" required></div>
            <div class="form-group"><input type="password" id="password" placeholder="Password" required></div>
            <button type="submit" class="btn">Login</button>
        </form>
        <div id="error" class="error"></div>
    </div>
    <script>
    document.getElementById('loginForm').addEventListener('submit', async (e) => {
        e.preventDefault();
        const data = {username: document.getElementById('username').value, password: document.getElementById('password').value};
        try {
            const response = await fetch('/admin/login', {method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify(data)});
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
    </script></body></html>'''

@app.route('/admin/students')
def admin_students():
    if not session.get('admin_logged_in'):
        return redirect('/admin/login')
    
    return '''<!DOCTYPE html><html><head><title>Student Management</title>
    <style>body{font-family:Arial;margin:0;background:#f5f5f5}.header{background:#007bff;color:white;padding:1rem;display:flex;justify-content:space-between;align-items:center}.container{max-width:1200px;margin:2rem auto;padding:2rem;background:white;border-radius:10px}.actions{display:flex;gap:1rem;margin-bottom:2rem;flex-wrap:wrap}.btn{padding:0.75rem 1.5rem;background:#007bff;color:white;border:none;border-radius:5px;cursor:pointer;text-decoration:none}.btn-success{background:#28a745}.btn-danger{background:#dc3545}.stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:1rem;margin-bottom:2rem}.stat-card{background:#f8f9fa;padding:1.5rem;border-radius:8px;text-align:center;border-left:4px solid #007bff}.stat-card h3{margin:0;font-size:2rem;color:#007bff}.table-container{overflow-x:auto}table{width:100%;border-collapse:collapse;margin-top:1rem}th,td{padding:0.75rem;text-align:left;border-bottom:1px solid #ddd}th{background:#f8f9fa}tr:hover{background:#f8f9fa}.search-box{width:100%;padding:0.75rem;border:1px solid #ddd;border-radius:5px;margin-bottom:1rem}.upload-area{border:2px dashed #007bff;border-radius:10px;padding:2rem;text-align:center;margin:1rem 0;background:#f8f9fa}#fileInput{display:none}.alert{padding:1rem;border-radius:5px;margin:1rem 0}.alert-success{background:#d4edda;color:#155724}.alert-error{background:#f8d7da;color:#721c24}.modal{display:none;position:fixed;z-index:1000;left:0;top:0;width:100%;height:100%;background-color:rgba(0,0,0,0.5)}.modal-content{background-color:white;margin:15% auto;padding:20px;border-radius:10px;width:80%;max-width:500px}.form-group{margin-bottom:1rem}.form-group label{display:block;margin-bottom:0.5rem;font-weight:bold}.form-group input{width:100%;padding:0.5rem;border:1px solid #ddd;border-radius:5px}</style>
    </head><body>
    <div class="header">
        <div><h1>📊 Student Management</h1></div>
        <button class="btn btn-danger" onclick="logout()">Logout</button>
    </div>
    
    <div class="container">
        <div class="stats">
            <div class="stat-card"><h3 id="totalStudents">0</h3><p>Total Students</p></div>
            <div class="stat-card"><h3 id="totalBatches">0</h3><p>Total Batches</p></div>
        </div>
        
        <div class="actions">
            <button class="btn btn-success" onclick="showAddModal()">➕ Add Student</button>
            <button class="btn btn-success" onclick="exportStudents()">📥 Export Excel</button>
            <button class="btn btn-success" onclick="document.getElementById('fileInput').click()">📤 Import Excel</button>
            <button class="btn" onclick="refreshData()">🔄 Refresh</button>
            <a href="/" class="btn">← Back to Main</a>
        </div>
        
        <div class="upload-area">
            <h3>📤 Import Students from Excel</h3>
            <p>Drag and drop an Excel file here</p>
            <input type="file" id="fileInput" accept=".xlsx,.xls" onchange="handleFileSelect(event)">
        </div>
        
        <div id="alertContainer"></div>
        
        <input type="text" class="search-box" id="searchBox" placeholder="🔍 Search students..." onkeyup="filterStudents()">
        
        <div class="table-container">
            <table>
                <thead>
                    <tr><th>SixerClass ID</th><th>Student Name</th><th>Batch Number</th><th>Start Date</th><th>End Date</th><th>Actions</th></tr>
                </thead>
                <tbody id="studentsTableBody">
                    <tr><td colspan="6" style="text-align:center;padding:2rem">Loading students...</td></tr>
                </tbody>
            </table>
        </div>
    </div>
    
    <div id="addModal" class="modal">
        <div class="modal-content">
            <h2>➕ Add New Student</h2>
            <form id="addStudentForm">
                <div class="form-group"><label>Student Name:</label><input type="text" id="addName" required></div>
                <div class="form-group"><label>Batch Number:</label><input type="text" id="addBatch" placeholder="AWS-2024-001" required></div>
                <div class="form-group"><label>Start Date:</label><input type="date" id="addStartDate" required></div>
                <div class="form-group"><label>End Date:</label><input type="date" id="addEndDate" required></div>
                <div class="form-group"><label>SixerClass ID:</label><input type="text" id="addId" placeholder="SIX001" required></div>
                <div style="display:flex;gap:1rem;margin-top:2rem">
                    <button type="submit" class="btn btn-success">Add Student</button>
                    <button type="button" class="btn" onclick="closeAddModal()">Cancel</button>
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
            }
        } catch (error) {
            showAlert('Error loading students', 'error');
        }
    }
    
    function displayStudents(students) {
        const tbody = document.getElementById('studentsTableBody');
        if (students.length === 0) {
            tbody.innerHTML = '<tr><td colspan="6" style="text-align:center;padding:2rem">No students found</td></tr>';
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
                    <button class="btn btn-danger" onclick="deleteStudent('${student.sixerclass_id}')">🗑️ Delete</button>
                </td>
            </tr>
        `).join('');
    }
    
    function updateStats() {
        document.getElementById('totalStudents').textContent = allStudents.length;
        const batches = new Set(allStudents.map(s => s.batch_number));
        document.getElementById('totalBatches').textContent = batches.size;
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
            }
        } catch (error) {
            showAlert('Export error', 'error');
        }
    }
    
    function handleFileSelect(event) {
        const file = event.target.files[0];
        if (file) uploadFile(file);
    }
    
    async function uploadFile(file) {
        const formData = new FormData();
        formData.append('file', file);
        try {
            showAlert('Uploading...', 'success');
            const response = await fetch('/admin/api/students/import', {method: 'POST', body: formData});
            const result = await response.json();
            if (result.success) {
                showAlert(`Import successful! ${result.imported_count} students imported.`, 'success');
                loadStudents();
            } else {
                showAlert(`Import failed: ${result.error}`, 'error');
            }
        } catch (error) {
            showAlert('Upload failed', 'error');
        }
    }
    
    async function generateCertificate(sixerclassId) {
        try {
            const student = allStudents.find(s => s.sixerclass_id === sixerclassId);
            showAlert('Generating certificate...', 'success');
            const response = await fetch('/admin/api/generate-certificate', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ student: student })
            });
            const result = await response.json();
            if (result.success) {
                const link = document.createElement('a');
                link.href = result.download_url;
                link.download = result.filename;
                document.body.appendChild(link);
                link.click();
                document.body.removeChild(link);
                showAlert(`Certificate generated!`, 'success');
            }
        } catch (error) {
            showAlert('Certificate generation error', 'error');
        }
    }
    
    async function deleteStudent(sixerclassId) {
        if (!confirm('Are you sure you want to delete this student?')) return;
        try {
            const response = await fetch('/admin/api/students/delete', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ sixerclass_id: sixerclassId })
            });
            const result = await response.json();
            if (result.success) {
                showAlert('Student deleted successfully!', 'success');
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
    
    function showAlert(message, type) {
        const container = document.getElementById('alertContainer');
        const alert = document.createElement('div');
        alert.className = `alert alert-${type}`;
        alert.textContent = message;
        container.innerHTML = '';
        container.appendChild(alert);
        setTimeout(() => container.innerHTML = '', 5000);
    }
    
    function refreshData() {
        loadStudents();
        showAlert('Data refreshed!', 'success');
    }
    
    function logout() {
        if (confirm('Are you sure you want to logout?')) {
            fetch('/admin/logout', { method: 'POST' })
                .then(() => window.location.href = '/admin/login');
        }
    }
    
    loadStudents();
    </script></body></html>'''

# ADMIN API ROUTES (Protected)
@app.route('/admin/api/students')
def admin_api_students():
    if not session.get('admin_logged_in'):
        return jsonify({"error": "Unauthorized"}), 401
    
    try:
        search = request.args.get('search', '').lower()
        if search:
            filtered_students = [s for s in students_data if search in s['student_name'].lower() or search in s['batch_number'].lower() or search in s['sixerclass_id'].lower()]
        else:
            filtered_students = students_data
        return jsonify({"success": True, "total": len(filtered_students), "students": filtered_students})
    except Exception as e:
        return jsonify({"error": "Failed to get students"}), 500

@app.route('/admin/api/students/export')
def admin_export_students():
    if not session.get('admin_logged_in'):
        return jsonify({"error": "Unauthorized"}), 401
    
    try:
        df = pd.DataFrame(students_data)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"students_export_{timestamp}.xlsx"
        filepath = os.path.join(app.config['EXCEL_DIR'], filename)
        df.to_excel(filepath, index=False, engine='openpyxl')
        return send_file(filepath, as_attachment=True, download_name=filename)
    except Exception as e:
        return jsonify({"error": "Export failed"}), 500

@app.route('/admin/api/students/import', methods=['POST'])
def admin_import_students():
    global students_data
    if not session.get('admin_logged_in'):
        return jsonify({"error": "Unauthorized"}), 401
    
    try:
        if 'file' not in request.files:
            return jsonify({"error": "No file uploaded"}), 400
        
        file = request.files['file']
        if not file.filename.lower().endswith(('.xlsx', '.xls')):
            return jsonify({"error": "Invalid file format"}), 400
        
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        df = pd.read_excel(filepath, sheet_name=0)
        required_columns = ['student_name', 'batch_number', 'batch_start_date', 'batch_end_date', 'sixerclass_id']
        missing_columns = [col for col in required_columns if col not in df.columns]
        
        if missing_columns:
            return jsonify({"error": f"Missing columns: {', '.join(missing_columns)}"}), 400
        
        imported_count = 0
        errors = []
        
        for _, row in df.iterrows():
            try:
                student = {
                    'student_name': str(row['student_name']).strip(),
                    'batch_number': str(row['batch_number']).strip(),
                    'batch_start_date': str(row['batch_start_date']).strip(),
                    'batch_end_date': str(row['batch_end_date']).strip(),
                    'sixerclass_id': str(row['sixerclass_id']).strip()
                }
                
                if any(s['sixerclass_id'] == student['sixerclass_id'] for s in students_data):
                    errors.append(f"Duplicate ID: {student['sixerclass_id']}")
                    continue
                
                students_data.append(student)
                imported_count += 1
            except Exception as e:
                continue
        
        df = pd.DataFrame(students_data)
        df.to_excel('excel-samples/student-data.xlsx', index=False)
        
        return jsonify({"success": True, "message": f"Imported {imported_count} students", "imported_count": imported_count, "errors": errors[:5]})
        
    except Exception as e:
        return jsonify({"error": f"Import failed: {str(e)}"}), 500

@app.route('/admin/api/students/add', methods=['POST'])
def admin_add_student():
    global students_data
    if not session.get('admin_logged_in'):
        return jsonify({"error": "Unauthorized"}), 401
    
    try:
        data = request.get_json()
        required_fields = ['student_name', 'batch_number', 'batch_start_date', 'batch_end_date', 'sixerclass_id']
        
        for field in required_fields:
            if not data.get(field):
                return jsonify({"error": f"Missing field: {field}"}), 400
        
        if any(s['sixerclass_id'] == data['sixerclass_id'] for s in students_data):
            return jsonify({"error": "SixerClass ID already exists"}), 400
        
        new_student = {k: data[k].strip() if isinstance(data[k], str) else data[k] for k in required_fields}
        students_data.append(new_student)
        
        df = pd.DataFrame(students_data)
        df.to_excel('excel-samples/student-data.xlsx', index=False)
        
        return jsonify({"success": True, "message": "Student added successfully"})
        
    except Exception as e:
        return jsonify({"error": "Failed to add student"}), 500

@app.route('/admin/api/students/delete', methods=['POST'])
def admin_delete_student():
    global students_data
    if not session.get('admin_logged_in'):
        return jsonify({"error": "Unauthorized"}), 401
    
    try:
        data = request.get_json()
        sixerclass_id = data.get('sixerclass_id')
        
        original_count = len(students_data)
        students_data = [s for s in students_data if s['sixerclass_id'] != sixerclass_id]
        
        if len(students_data) < original_count:
            df = pd.DataFrame(students_data)
            df.to_excel('excel-samples/student-data.xlsx', index=False)
            return jsonify({"success": True, "message": "Student deleted successfully"})
        else:
            return jsonify({"error": "Student not found"}), 404
        
    except Exception as e:
        return jsonify({"error": "Failed to delete student"}), 500

@app.route('/admin/logout', methods=['POST'])
def admin_logout():
    session.pop('admin_logged_in', None)
    return jsonify({"success": True})

@app.route('/admin/api/generate-certificate', methods=['POST'])
def admin_generate_certificate():
    if not session.get('admin_logged_in'):
        return jsonify({"error": "Unauthorized"}), 401
    
    try:
        data = request.get_json()
        student = data.get('student')
        
        safe_name = secure_filename(student['student_name'].replace(' ', '_'))
        filename = f"certificate_{student['sixerclass_id']}_{safe_name}.pdf"
        filepath = os.path.join(app.config['CERTIFICATE_DIR'], filename)
        
        success = cert_generator.create_certificate(student, filepath)
        
        if success:
            return jsonify({"success": True, "download_url": f"/api/serve-certificate/{filename}", "filename": filename})
        else:
            return jsonify({"error": "Certificate generation failed"}), 500
    except Exception as e:
        return jsonify({"error": "Certificate generation failed"}), 500

if __name__ == '__main__':
    logger.info("🚀 Starting AWS Training Certificate System - Admin Secured")
    logger.info(f"📊 Loaded {len(students_data)} students")
    logger.info("🔐 Admin Login: username=admin, password=admin123")
    app.run(host='0.0.0.0', port=5000, debug=False)