#!/bin/bash

# AWS Training Certificate System - Deployment Script
# This script helps deploy the application to AWS

echo "🚀 AWS Training Certificate System - Deployment Script"
echo "=================================================="

# Check if required files exist
if [ ! -f "src/app.py" ]; then
    echo "❌ Error: src/app.py not found!"
    exit 1
fi

if [ ! -f "requirements.txt" ]; then
    echo "❌ Error: requirements.txt not found!"
    exit 1
fi

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p data/certificates
mkdir -p data/excel
mkdir -p data/uploads
mkdir -p data/templates

# Copy certificate template if it exists
if [ -f "data/templates/certificate-template.png" ]; then
    echo "✅ Certificate template found"
else
    echo "⚠️  Warning: Certificate template not found at data/templates/certificate-template.png"
    echo "   Please ensure you have the certificate template in the correct location"
fi

# Check if assets exist
if [ -f "assets/Magicbus_logo.png" ] && [ -f "assets/bus.png" ]; then
    echo "✅ Assets found"
else
    echo "❌ Error: Required assets not found in assets/ directory"
    exit 1
fi

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Set environment variables for production
export FLASK_ENV=production
export FLASK_DEBUG=False

# Check if .env file exists
if [ -f ".env" ]; then
    echo "✅ Environment file found"
    source .env
else
    echo "⚠️  Warning: .env file not found. Using default values."
    echo "   Copy .env.example to .env and update values for production"
fi

echo ""
echo "🎯 Deployment Checklist:"
echo "========================"
echo "✅ Application structure verified"
echo "✅ Dependencies installed"
echo "✅ Directories created"

if [ -f ".env" ]; then
    echo "✅ Environment variables configured"
else
    echo "⚠️  Environment variables need configuration"
fi

if [ -f "data/templates/certificate-template.png" ]; then
    echo "✅ Certificate template available"
else
    echo "⚠️  Certificate template needs to be added"
fi

echo ""
echo "🚀 Ready to deploy!"
echo ""
echo "For AWS EC2 deployment:"
echo "1. Upload this entire directory to your EC2 instance"
echo "2. Run this script on the server"
echo "3. Configure nginx/apache to proxy to port 5000"
echo "4. Set up SSL certificate"
echo "5. Configure environment variables in .env file"
echo ""
echo "For AWS Elastic Beanstalk:"
echo "1. Create application.py that imports from src/app.py"
echo "2. Zip the entire project"
echo "3. Deploy to Elastic Beanstalk"
echo ""
echo "To start the application:"
echo "python src/app.py"