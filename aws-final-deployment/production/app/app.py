from flask import Flask, render_template, request, jsonify, send_file, session
from flask_cors import CORS
import pandas as pd
import logging
import os
from werkzeug.utils import secure_filename
from datetime import datetime
from pdf_certificate_generator_final import FinalPDFCertificateGenerator

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['CERTIFICATE_DIR'] = '/tmp/certificates'
app.config['EXCEL_DIR'] = '/tmp/excel-data'

# Ensure directories exist
os.makedirs(app.config['CERTIFICATE_DIR'], exist_ok=True)
os.makedirs(app.config['EXCEL_DIR'], exist_ok=True)

CORS(app)

# Initialize final perfect PDF generator
pdf_generator = FinalPDFCertificateGenerator()

# Load students data
def load_students_data():
    try:
        excel_path = '../data/excel-samples/student-data.xlsx'
        df = pd.read_excel(excel_path)
        logger.info(f"✅ Loaded {len(df)} students from {excel_path}")
        return df.to_dict('records')
    except Exception as e:
        logger.error(f"❌ Error loading students data: {e}")
        return []

students_data = load_students_data()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/check-status')
def check_status():
    return jsonify({
        "status": "operational",
        "students_loaded": len(students_data),
        "timestamp": datetime.now().isoformat(),
        "version": "3.0.0-Perfect-PDF"
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
        
        # Generate final perfect PDF certificate
        safe_name = secure_filename(student['student_name'].replace(' ', '_'))
        filename = f"certificate_{student['sixerclass_id']}_{safe_name}.pdf"
        filepath = os.path.join(app.config['CERTIFICATE_DIR'], filename)
        
        # Create final perfect PDF certificate
        result = pdf_generator.create_final_certificate(student, filepath)
        
        if result:
            logger.info(f"✅ Final perfect PDF certificate generated: {filename}")
            logger.info(f"📍 Perfect positions used: Name(405,400) Dates(345,277)(625,277)")
            return jsonify({
                "success": True,
                "download_url": f"/api/serve-certificate/{filename}",
                "filename": filename,
                "student_name": student['student_name']
            })
        else:
            return jsonify({"error": "Certificate generation failed"}), 500

    except Exception as e:
        logger.error(f"❌ Certificate download error: {e}")
        return jsonify({"error": "Certificate generation failed"}), 500

@app.route('/api/serve-certificate/<filename>')
def serve_certificate(filename):
    try:
        # Security check
        if not filename.startswith('certificate_') or not filename.endswith('.pdf'):
            return jsonify({"error": "Invalid filename"}), 400
            
        filepath = os.path.join(app.config['CERTIFICATE_DIR'], filename)
        
        if os.path.exists(filepath):
            logger.info(f"✅ Serving perfect PDF certificate: {filename}")
            return send_file(filepath, as_attachment=True, download_name=filename)
        else:
            logger.warning(f"❌ Certificate file not found: {filename}")
            return jsonify({"error": "Certificate file not found"}), 404
            
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

if __name__ == '__main__':
    logger.info("🚀 Starting AWS Training Certificate System - Final Perfect PDF Version")
    logger.info("📍 Using perfect coordinates: Name(405,400) Dates(345,277)(625,277)")
    app.run(host='0.0.0.0', port=5000, debug=False)
