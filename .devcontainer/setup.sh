#!/bin/bash
echo "🚀 Setting up AWS Training Certificate System environment..."

# Install AWS CLI v2
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install

# Install Python packages for certificate generation
pip install boto3 pillow weasyprint pandas openpyxl

# Install Node.js packages for frontend
npm install -g http-server

# Create project structure
mkdir -p infrastructure/terraform
mkdir -p backend/{certificate-generator,student-auth,excel-importer}
mkdir -p frontend/{static,css,js}
mkdir -p data/{excel-samples,certificate-templates}
mkdir -p docs

echo "✅ Environment setup complete!"
echo "📁 Project structure created"
echo "🎯 Ready to start development!"