# AWS Deployment Guide
# AWS Training Certificate System

## 🚀 Deployment Options

### Option 1: AWS Elastic Beanstalk (Recommended)

1. **Prepare the application:**
   ```bash
   ./deploy.sh
   ```

2. **Create deployment package:**
   ```bash
   zip -r certificate-system.zip . -x "*.git*" "__pycache__/*" "*.pyc"
   ```

3. **Deploy to Elastic Beanstalk:**
   - Go to AWS Elastic Beanstalk console
   - Create new application
   - Choose Python 3.9 platform
   - Upload certificate-system.zip
   - Configure environment variables in EB console

### Option 2: AWS EC2 with Docker

1. **Launch EC2 instance:**
   - Choose Amazon Linux 2 AMI
   - Install Docker: `sudo yum install docker -y`
   - Start Docker: `sudo service docker start`

2. **Deploy application:**
   ```bash
   # Copy files to EC2
   scp -r . ec2-user@your-instance:/home/ec2-user/certificate-system/
   
   # SSH to instance
   ssh ec2-user@your-instance
   
   # Build and run
   cd certificate-system
   sudo docker build -t certificate-system .
   sudo docker run -d -p 80:5000 --name cert-app certificate-system
   ```

### Option 3: AWS ECS with Fargate

1. **Build and push Docker image:**
   ```bash
   # Build image
   docker build -t certificate-system .
   
   # Tag for ECR
   docker tag certificate-system:latest your-account.dkr.ecr.region.amazonaws.com/certificate-system:latest
   
   # Push to ECR
   docker push your-account.dkr.ecr.region.amazonaws.com/certificate-system:latest
   ```

2. **Create ECS service using the pushed image**

## 🔧 Environment Variables

Set these in your AWS deployment:

```bash
SECRET_KEY=your-super-secret-key-change-this-in-production
ADMIN_USERNAME=admin
ADMIN_PASSWORD=secure-password-here
FLASK_ENV=production
FLASK_DEBUG=False
```

## 📁 Required Files Structure

```
/
├── src/
│   ├── app.py
│   └── certificate_generator.py
├── data/
│   ├── templates/
│   │   └── certificate-template.png
│   ├── excel/
│   │   └── student-data.xlsx
│   ├── certificates/
│   └── uploads/
├── assets/
│   ├── Magicbus_logo.png
│   └── bus.png
├── application.py (for Elastic Beanstalk)
├── requirements.txt
└── .env (environment variables)
```

## 🔒 Security Checklist

- [ ] Change default admin credentials
- [ ] Set strong SECRET_KEY
- [ ] Configure HTTPS/SSL
- [ ] Set up proper security groups
- [ ] Enable CloudWatch logging
- [ ] Configure backup for data directory

## 🌐 Domain & SSL

1. **Route 53 for domain:**
   - Register domain or transfer existing
   - Create hosted zone
   - Point to your deployment

2. **SSL Certificate:**
   - Use AWS Certificate Manager
   - Request certificate for your domain
   - Configure in Load Balancer or CloudFront

## 📊 Monitoring

- Enable CloudWatch logs
- Set up health checks
- Configure alarms for errors
- Monitor disk usage for data directory

## 🔄 Backup Strategy

- Regular backup of data/excel/ directory
- Database backup if migrating from Excel
- Code repository backup

## 🚨 Troubleshooting

**Common Issues:**

1. **Template not found:**
   - Ensure certificate-template.png is in data/templates/
   - Check file permissions

2. **Static files not loading:**
   - Verify assets/ directory structure
   - Check file paths in logs

3. **Excel file errors:**
   - Ensure data/excel/ directory exists
   - Check file permissions for write access

4. **Environment variables:**
   - Verify all required env vars are set
   - Check AWS console configuration

## 📞 Support

For deployment issues:
1. Check application logs
2. Verify all files are present
3. Test locally with Docker first
4. Check AWS service limits and permissions