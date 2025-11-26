#!/bin/bash
# Local Testing Script - AWS Certificate System

echo "🧪 Testing AWS deployment package locally..."

# Kill any existing processes
pkill -f "gunicorn" 2>/dev/null
pkill -f "python app_aws.py" 2>/dev/null

# Set local environment
export FLASK_ENV=development
export PORT=5001
export CERTIFICATE_DIR=/tmp/certificates
export EXCEL_DIR=/tmp/excel-data

# Create directories
mkdir -p $CERTIFICATE_DIR $EXCEL_DIR

# Test with simple Flask first (not systemd)
echo "📊 Starting Flask application on port $PORT..."
python3 app_aws.py > local_test.log 2>&1 &

# Wait for startup
sleep 3

# Test the application
echo "🧪 Testing local application..."
response=$(curl -s http://localhost:$PORT/api/check-status 2>/dev/null)

if [[ $response == *"operational"* ]]; then
    echo "✅ Local application working on port $PORT"
    echo "🌐 Test URLs:"
    echo "   - Health: http://localhost:$PORT/api/check-status"
    echo "   - Web UI: http://localhost:$PORT"
else
    echo "❌ Local application issues"
    echo "📋 Response: $response"
    echo "📊 Logs:"
    tail -10 local_test.log
fi
