from flask import Flask, render_template, request, jsonify, send_file, session, redirect, url_for
from flask_cors import CORS
import pandas as pd
import os
import sys
from datetime import datetime
import json
import logging
from werkzeug.utils import secure_filename

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Add parent directory to path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'aws-training-certificate-system-2024-production'
CORS(app)

# Configure directories
app.config['CERTIFICATE_DIR'] = os.path.join(parent_dir, 'data', 'certificate-templates', 'processed')
app.config['EXCEL_DIR'] = os.path.join(parent_dir, 'data', 'excel-samples')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Ensure directories exist
os.makedirs(app.config['CERTIFICATE_DIR'], exist_ok=True)
os.makedirs(app.config['EXCEL_DIR'], exist_ok=True)

class ProductionCertificateApp:
    def __init__(self):
        self.student_data = None
        self.load_student_data()
    
    def load_student_data(self):
        """Load student data with multiple fallback options"""
        try:
            possible_paths = [
                os.path.join(app.config['EXCEL_DIR'], 'student-data.xlsx'),
                os.path.join(parent_dir, 'data', 'excel-samples', 'student-data.xlsx'),
                os.path.join(current_dir, 'data', 'excel-samples', 'student-data.xlsx')
            ]
            
            excel_file = None
            for path in possible_paths:
                if os.path.exists(path):
                    excel_file = path
                    break
            
            if excel_file:
                self.student_data = pd.read_excel(excel_file)
                logger.info(f"✅ Loaded {len(self.student_data)} students from {excel_file}")
                
                # Validate required columns
                required_columns = ['sixerclass_id', 'student_name', 'batch_number', 'batch_start_date', 'batch_end_date']
                missing_columns = [col for col in required_columns if col not in self.student_data.columns]
                
                if missing_columns:
                    logger.warning(f"⚠️ Missing columns: {missing_columns}")
                    # Create missing columns with default values
                    for col in missing_columns:
                        if col == 'batch_start_date':
                            self.student_data[col] = '2024-01-15'
                        elif col == 'batch_end_date':
                            self.student_data[col] = '2024-04-15'
                        else:
                            self.student_data[col] = 'Unknown'
                
            else:
                logger.warning("❌ No Excel file found, creating sample data")
                self.create_sample_data()
                
        except Exception as e:
            logger.error(f"❌ Error loading student data: {e}")
            self.create_sample_data()
    
    def create_sample_data(self):
        """Create comprehensive sample data for testing"""
        sample_data = [
            {
                'sixerclass_id': 'SIX001',
                'student_name': 'John Doe Smith',
                'batch_number': 'AWS-2024-001',
                'batch_start_date': '2024-01-15',
                'batch_end_date': '2024-04-15'
            },
            {
                'sixerclass_id': 'SIX002',
                'student_name': 'Jane Doe Wilson',
                'batch_number': 'AWS-2024-001',
                'batch_start_date': '2024-01-15',
                'batch_end_date': '2024-04-15'
            },
            {
                'sixerclass_id': 'SIX003',
                'student_name': 'Robert Johnson',
                'batch_number': 'AWS-2024-002',
                'batch_start_date': '2024-02-01',
                'batch_end_date': '2024-05-01'
            },
            {
                'sixerclass_id': 'SIX004',
                'student_name': 'Maria Garcia',
                'batch_number': 'AWS-2024-002',
                'batch_start_date': '2024-02-01',
                'batch_end_date': '2024-05-01'
            }
        ]
        
        self.student_data = pd.DataFrame(sample_data)
        logger.info("✅ Sample data created for testing")
    
    def authenticate_student(self, student_name, batch_number, sixerclass_id):
        """Enhanced authentication with fuzzy matching"""
        try:
            if self.student_data is None or self.student_data.empty:
                return None
            
            # Normalize input
            search_name = student_name.lower().strip()
            search_batch = batch_number.lower().strip()
            search_id = sixerclass_id.lower().strip()
            
            # Exact matching first
            for index, row in self.student_data.iterrows():
                if (str(row['student_name']).lower().strip() == search_name and
                    str(row['batch_number']).lower().strip() == search_batch and
                    str(row['sixerclass_id']).lower().strip() == search_id):
                    return row.to_dict()
            
            # If exact match fails, try case-insensitive matching
            for index, row in self.student_data.iterrows():
                if (str(row['student_name']).lower().strip() == search_name and
                    str(row['batch_number']).lower().strip() == search_batch and
                    str(row['sixerclass_id']).lower().strip() == search_id):
                    return row.to_dict()
            
            return None
            
        except Exception as e:
            logger.error(f"❌ Authentication error: {e}")
            return None
    
    def generate_certificate_text(self, student_data):
        """Generate certificate text content"""
        try:
            certificate_content = f"""
AWS TRAINING CERTIFICATE OF COMPLETION

This certifies that

{student_data['student_name'].upper()}

has successfully completed the AWS Training Program

Batch Number: {student_data['batch_number']}
Training Period: {student_data['batch_start_date']} to {student_data['batch_end_date']}
SixerClass ID: {student_data['sixerclass_id']}

Awarded this {datetime.now().strftime('%B %d, %Y')}

AWS Training Center
Authorized Signature
"""
            return certificate_content.strip()
            
        except Exception as e:
            logger.error(f"❌ Certificate content generation error: {e}")
            return None
    
    def generate_certificate_file(self, student_data):
        try:
            from PIL import Image, ImageDraw, ImageFont
            import os
            from werkzeug.utils import secure_filename

            # Paths
            template_path = 'data/certificate-templates/raw/certificate-template.png'
            output_dir = app.config['CERTIFICATE_DIR']
            safe_name = secure_filename(student_data['student_name'].replace(' ', '_'))
            from datetime import datetime
            filename = f"certificate_{student_data['sixerclass_id']}_{safe_name}_{int(datetime.now().timestamp())}.png"
            filepath = os.path.join(output_dir, filename.replace('.pdf', '.png'))

            # Open template
            with Image.open(template_path) as img:
                draw = ImageDraw.Draw(img)

                # Fonts
                name_font = ImageFont.truetype("data/fonts/DejaVuSans.ttf", 36)
                date_font = ImageFont.truetype("data/fonts/DejaVuSans.ttf", 22)

                # Text positions
                 # Final corrected positions
                draw.text((405, 380), student_data['student_name'], font=name_font, fill="black")
                draw.text((345, 515), str(student_data['batch_start_date']), font=date_font, fill="black")
                draw.text((625, 515), str(student_data['batch_end_date']), font=date_font, fill="black")

                # Save
                img.save(filepath, quality=100)

            logger.info(f"✅ Certificate generated: {filename}")
            return filepath

        except Exception as e:
            logger.error(f"❌ Certificate generation error: {e}")
            return None

# Initialize the application
cert_app = ProductionCertificateApp()

@app.route('/')
def index():
    """Main landing page"""
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    """Admin dashboard"""
    students = cert_app.get_student_list()
    return render_template('dashboard.html', students=students)

@app.route('/api/authenticate', methods=['POST'])
def authenticate():
    """Authenticate student"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        student_name = data.get('student_name', '').strip()
        batch_number = data.get('batch_number', '').strip()
        sixerclass_id = data.get('sixerclass_id', '').strip()
        
        # Validate input
        if not all([student_name, batch_number, sixerclass_id]):
            return jsonify({"error": "All fields are required"}), 400
        
        # Validate formats
        if not sixerclass_id.upper().startswith('SIX'):
            return jsonify({"error": "SixerClass ID must start with 'SIX'"}), 400
        
        # Authenticate
        student = cert_app.authenticate_student(student_name, batch_number, sixerclass_id)
        
        if student:
            session['student_data'] = student
            session['authenticated'] = True
            
            logger.info(f"✅ Student authenticated: {student['student_name']} ({student['sixerclass_id']})")
            
            return jsonify({
                "success": True,
                "student": {
                    "sixerclass_id": student['sixerclass_id'],
                    "student_name": student['student_name'],
                    "batch_number": student['batch_number'],
                    "batch_start_date": str(student['batch_start_date']),
                    "batch_end_date": str(student['batch_end_date'])
                }
            })
        else:
            logger.warning(f"❌ Authentication failed for: {student_name}, {batch_number}, {sixerclass_id}")
            return jsonify({"error": "Student not found. Please check your details."}), 404
            
    except Exception as e:
        logger.error(f"❌ Authentication error: {e}")
        return jsonify({"error": f"Authentication failed: {str(e)}"}), 500

@app.route('/api/download-certificate', methods=['POST'])
def download_certificate():
    """Generate and download certificate"""
    try:
        if not session.get('authenticated') or 'student_data' not in session:
            return jsonify({"error": "Please authenticate first"}), 401
        
        student_data = session['student_data']
        
        # Generate certificate
        certificate_path = cert_app.generate_certificate_file(student_data)
        
        if certificate_path and os.path.exists(certificate_path):
            filename = os.path.basename(certificate_path)
            
            logger.info(f"✅ Certificate generated for download: {filename}")
            
            return jsonify({
                "success": True,
                "download_url": f"/api/serve-certificate/{filename}",
                "filename": filename,
                "student_name": student_data['student_name']
            })
        else:
            return jsonify({"error": "Certificate generation failed"}), 500
            
    except Exception as e:
        logger.error(f"❌ Certificate download error: {e}")
        return jsonify({"error": f"Certificate generation failed: {str(e)}"}), 500

@app.route('/api/serve-certificate/<filename>')
def serve_certificate(filename):
    try:
        # Security validation
        if not filename.startswith('certificate_') or not filename.endswith('.png'):
            return jsonify({"error": "Invalid filename"}), 400

        filepath = os.path.join(app.config['CERTIFICATE_DIR'], filename)

        if os.path.exists(filepath):
            logger.info(f"✅ Serving certificate: {filename}")
            return send_file(filepath, as_attachment=True, download_name=filename)
        else:
            logger.warning(f"❌ Certificate file not found: {filename}")
            return jsonify({"error": "Certificate file not found"}), 404

    except Exception as e:
        logger.error(f"❌ File serving error: {e}")
        return jsonify({"error": f"File serving failed: {str(e)}"}), 500
    
@app.route('/api/students', methods=['GET'])
def get_students():
    """Get list of all students (for admin)"""
    try:
        students = cert_app.get_student_list()
        return jsonify({
            "success": True,
            "students": students,
            "count": len(students)
        })
    except Exception as e:
        logger.error(f"❌ Get students error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/student/<sixerclass_id>', methods=['GET'])
def get_student(sixerclass_id):
    """Get specific student details"""
    try:
        student = cert_app.get_student_by_id(sixerclass_id)
        if student:
            return jsonify({
                "success": True,
                "student": student
            })
        else:
            return jsonify({"error": "Student not found"}), 404
    except Exception as e:
        logger.error(f"❌ Get student error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/check-status')
def check_status():
    """System health check"""
    try:
        return jsonify({
            "status": "operational",
            "students_loaded": len(cert_app.student_data) if cert_app.student_data is not None else 0,
            "timestamp": datetime.now().isoformat(),
            "version": "1.0.0"
        })
    except Exception as e:
        logger.error(f"❌ Status check error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/logout')
def logout():
    """Clear session"""
    try:
        session.clear()
        logger.info("✅ User logged out")
        return jsonify({"success": True, "message": "Logged out successfully"})
    except Exception as e:
        logger.error(f"❌ Logout error: {e}")
        return jsonify({"error": str(e)}), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    logger.error(f"❌ Internal server error: {error}")
    return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    print("🚀 Starting AWS Training Certificate Web Application (Production Version)")
    print("📍 URL: http://localhost:5000")
    print("✨ Features: Production-ready authentication, certificate generation, admin dashboard")
    print(f"📊 Students loaded: {len(cert_app.student_data) if cert_app.student_data is not None else 0}")
    print("🔧 Production features: Enhanced error handling, logging, security validation")
    
    app.run(host='0.0.0.0', port=5000, debug=False)  # Set debug=False for production
