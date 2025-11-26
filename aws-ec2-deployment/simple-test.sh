#!/bin/bash
# Simple Direct Test

echo "🔍 Simple direct application test..."

# Kill any existing processes
pkill -f "python app_aws.py" 2>/dev/null

# Test import directly
echo "📦 Testing Python imports..."
python3 -c "
import sys
sys.path.append('.')
try:
    from app_aws import application
    print('✅ Import successful')
    print(f'App name: {application.name}')
    print(f'Templates folder: {application.template_folder}')
    print(f'Static folder: {application.static_folder}')
except Exception as e:
    print(f'❌ Import error: {e}')
    import traceback
    traceback.print_exc()
"

# Test basic Flask functionality
echo "🌐 Testing basic Flask functionality..."
python3 -c "
from app_aws import application
import tempfile
import os

# Test basic app creation
app = application
print(f'✅ Flask app created successfully')
print(f'   - Secret key: {bool(app.config.get(\"SECRET_KEY\"))}')
print(f'   - Certificate dir: {app.config.get(\"CERTIFICATE_DIR\")}')
print(f'   - Excel dir: {app.config.get(\"EXCEL_DIR\")}')
"
