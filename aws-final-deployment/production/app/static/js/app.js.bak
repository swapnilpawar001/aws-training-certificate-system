// AWS Training Certificate System - Production JavaScript

class CertificateApp {
    constructor() {
        this.currentStudent = null;
        this.isLoading = false;
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.setupValidation();
        this.setupModalHandlers();
        this.setupKeyboardNavigation();
    }

    setupEventListeners() {
        const form = document.getElementById('certificateForm');
        form.addEventListener('submit', (e) => this.handleSubmit(e));
        
        // Real-time validation
        const inputs = form.querySelectorAll('input');
        inputs.forEach(input => {
            input.addEventListener('blur', () => this.validateField(input));
            input.addEventListener('input', () => this.clearFieldError(input));
        });
    }

    setupValidation() {
        // Batch number format validation
        const batchInput = document.getElementById('batchNumber');
        batchInput.addEventListener('input', (e) => {
            let value = e.target.value.toUpperCase();
            if (value && !value.startsWith('AWS-')) {
                e.target.value = 'AWS-' + value.replace('AWS-', '');
            }
        });

        // SixerClass ID format validation
        const idInput = document.getElementById('sixerclassId');
        idInput.addEventListener('input', (e) => {
            let value = e.target.value.toUpperCase();
            if (value && !value.startsWith('SIX')) {
                e.target.value = 'SIX' + value.replace('SIX', '');
            }
        });
    }

    setupModalHandlers() {
        // Modal close buttons
        document.querySelector('.close').addEventListener('click', () => this.closeModal());
        document.getElementById('downloadBtn').addEventListener('click', () => this.handleDownload());
        
        // Close modal when clicking outside
        window.addEventListener('click', (e) => {
            const modal = document.getElementById('successModal');
            if (e.target === modal) {
                this.closeModal();
            }
        });

        // Escape key to close modal
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape') {
                this.closeModal();
            }
        });
    }

    setupKeyboardNavigation() {
        const form = document.getElementById('certificateForm');
        const inputs = form.querySelectorAll('input');
        
        inputs.forEach((input, index) => {
            input.addEventListener('keydown', (e) => {
                if (e.key === 'Enter' && index < inputs.length - 1) {
                    e.preventDefault();
                    inputs[index + 1].focus();
                }
            });
        });
    }

    async handleSubmit(e) {
        e.preventDefault();
        
        if (this.isLoading) return;
        
        const formData = this.getFormData();
        if (!this.validateForm(formData)) return;
        
        this.showLoading(true);
        this.clearError();
        
        try {
            // Step 1: Authenticate student
            const authResult = await this.authenticateStudent(formData);
            
            if (authResult.success) {
                this.currentStudent = authResult.student;
                
                // Step 2: Generate certificate
                const downloadResult = await this.generateCertificate();
                
                if (downloadResult.success) {
                    this.showSuccess(downloadResult);
                    this.triggerDownload(downloadResult.download_url);
                } else {
                    throw new Error(downloadResult.error || 'Certificate generation failed');
                }
            } else {
                throw new Error(authResult.error || 'Authentication failed');
            }
            
        } catch (error) {
            this.showError(error.message);
            logger.error('Certificate generation failed:', error);
        } finally {
            this.showLoading(false);
        }
    }

    getFormData() {
        return {
            student_name: document.getElementById('studentName').value.trim(),
            batch_number: document.getElementById('batchNumber').value.trim(),
            sixerclass_id: document.getElementById('sixerclassId').value.trim()
        };
    }

    validateForm(data) {
        this.clearError();
        
        if (!data.student_name) {
            this.showFieldError('studentName', 'Please enter your full name');
            return false;
        }
        
        if (!data.batch_number) {
            this.showFieldError('batchNumber', 'Please enter your batch number');
            return false;
        }
        
        if (!data.sixerclass_id) {
            this.showFieldError('sixerclassId', 'Please enter your SixerClass ID');
            return false;
        }
        
        // Format validation
        if (!data.batch_number.match(/^AWS-\d{4}-\d{3}$/i)) {
            this.showFieldError('batchNumber', 'Batch number must be in format: AWS-YYYY-NNN');
            return false;
        }
        
        if (!data.sixerclass_id.match(/^SIX\d{3}$/i)) {
            this.showFieldError('sixerclassId', 'SixerClass ID must be in format: SIXNNN');
            return false;
        }
        
        return true;
    }

    validateField(field) {
        const input = document.getElementById(field);
        const value = input.value.trim();
        
        if (!value) {
            this.showFieldError(field, 'This field is required');
            return false;
        }
        
        // Specific validations
        if (field === 'batchNumber' && value && !value.match(/^AWS-\d{4}-\d{3}$/i)) {
            this.showFieldError(field, 'Format: AWS-YYYY-NNN (e.g., AWS-2024-001)');
            return false;
        }
        
        if (field === 'sixerclassId' && value && !value.match(/^SIX\d{3}$/i)) {
            this.showFieldError(field, 'Format: SIXNNN (e.g., SIX001)');
            return false;
        }
        
        this.clearFieldError(field);
        return true;
    }

    showFieldError(fieldId, message) {
        const field = document.getElementById(fieldId);
        const formGroup = field.closest('.form-group');
        
        // Remove existing error
        this.clearFieldError(fieldId);
        
        // Create error element
        const errorElement = document.createElement('div');
        errorElement.className = 'field-error';
        errorElement.textContent = message;
        errorElement.style.cssText = `
            color: #f44336;
            font-size: 0.85rem;
            margin-top: 5px;
            animation: slideIn 0.3s ease-out;
        `;
        
        formGroup.appendChild(errorElement);
        field.classList.add('error');
    }

    clearFieldError(fieldId) {
        const field = document.getElementById(fieldId);
        const formGroup = field.closest('.form-group');
        const existingError = formGroup.querySelector('.field-error');
        
        if (existingError) {
            existingError.remove();
        }
        
        field.classList.remove('error');
    }

    clearError() {
        const errorDiv = document.getElementById('errorMessage');
        errorDiv.style.display = 'none';
    }

    showLoading(show) {
        this.isLoading = show;
        const loadingDiv = document.getElementById('loadingOverlay');
        const submitBtn = document.getElementById('submitBtn');
        
        if (show) {
            loadingDiv.style.display = 'flex';
            submitBtn.disabled = true;
            submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Processing...';
        } else {
            loadingDiv.style.display = 'none';
            submitBtn.disabled = false;
            submitBtn.innerHTML = '<i class="fas fa-download"></i> Download Certificate';
        }
    }

    showError(message) {
        const errorDiv = document.getElementById('errorMessage');
        const errorText = document.getElementById('errorText');
        
        errorText.textContent = message;
        errorDiv.style.display = 'flex';
        
        // Auto-hide after 5 seconds
        setTimeout(() => {
            errorDiv.style.display = 'none';
        }, 5000);
    }

    showSuccess(result) {
        const modal = document.getElementById('successModal');
        const preview = document.getElementById('certificatePreview');
        
        // Update preview content
        preview.innerHTML = `
            <div class="student-info">
                <h4>Certificate for ${result.student_name}</h4>
                <p><strong>Batch:</strong> ${result.batch_number}</p>
                <p><strong>SixerClass ID:</strong> ${result.sixerclass_id}</p>
                <p><strong>Training Period:</strong> ${result.batch_start_date} to ${result.batch_end_date}</p>
            </div>
            <div class="certificate-icon">
                <i class="fas fa-certificate"></i>
            </div>
        `;
        
        // Show modal
        modal.style.display = 'flex';
    }

    closeModal() {
        const modal = document.getElementById('successModal');
        modal.style.display = 'none';
        
        // Clear form after successful download
        if (this.currentStudent) {
            document.getElementById('certificateForm').reset();
            this.currentStudent = null;
        }
    }

    async authenticateStudent(data) {
        try {
            const response = await fetch('/api/authenticate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            });
            
            const result = await response.json();
            
            if (response.ok) {
                return result;
            } else {
                return { success: false, error: result.error || 'Authentication failed' };
            }
        } catch (error) {
            return { success: false, error: 'Network error. Please check your connection.' };
        }
    }

    async generateCertificate() {
        try {
            const response = await fetch('/api/download-certificate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                }
            });
            
            const result = await response.json();
            
            if (response.ok) {
                return result;
            } else {
                return { success: false, error: result.error || 'Certificate generation failed' };
            }
        } catch (error) {
            return { success: false, error: 'Network error during certificate generation.' };
        }
    }

    triggerDownload(url) {
        // Open download in new tab
        window.open(url, '_blank');
        
        // Show success notification
        this.showSuccessNotification();
    }

    showSuccessNotification() {
        const notification = document.createElement('div');
        notification.className = 'success-notification';
        notification.innerHTML = `
            <i class="fas fa-check-circle"></i>
            <span>Certificate downloaded successfully!</span>
        `;
        
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: linear-gradient(135deg, #4caf50 0%, #45a049 100%);
            color: white;
            padding: 15px 20px;
            border-radius: 8px;
            box-shadow: 0 5px 15px rgba(76, 175, 80, 0.3);
            z-index: 3000;
            animation: slideInRight 0.3s ease-out;
        `;
        
        document.body.appendChild(notification);
        
        setTimeout(() => {
            notification.style.animation = 'slideOutRight 0.3s ease-out';
            setTimeout(() => {
                document.body.removeChild(notification);
            }, 300);
        }, 3000);
    }

    showAdminPanel() {
        // Placeholder for admin functionality
        alert('Admin panel coming soon! This will allow batch management and certificate oversight.');
    }
}

// Add dynamic styles
const dynamicStyles = `
<style>
    @keyframes slideInRight {
        from { transform: translateX(100%); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    
    @keyframes slideOutRight {
        from { transform: translateX(0); opacity: 1; }
        to { transform: translateX(100%); opacity: 0; }
    }
    
    .field-error {
        animation: slideIn 0.3s ease-out;
    }
    
    @keyframes slideIn {
        from { transform: translateY(-10px); opacity: 0; }
        to { transform: translateY(0); opacity: 1; }
    }
    
    .form-group input.error {
        border-color: #f44336;
        background: #fff5f5;
    }
    
    .loading .form-group input {
        opacity: 0.6;
        pointer-events: none;
    }
    
    .success-notification {
        font-weight: 500;
        display: flex;
        align-items: center;
        gap: 10px;
    }
</style>
`;

document.head.insertAdjacentHTML('beforeend', dynamicStyles);

// Initialize application
document.addEventListener('DOMContentLoaded', () => {
    const app = new CertificateApp();
    
    console.log('🚀 AWS Training Certificate System initialized');
    console.log('✨ Premium web interface loaded');
    console.log('🎯 Production-ready certificate generation system');
});

// Error logging
const logger = {
    info: (message, ...args) => console.log(`[INFO] ${message}`, ...args),
    error: (message, ...args) => console.error(`[ERROR] ${message}`, ...args),
    warn: (message, ...args) => console.warn(`[WARN] ${message}`, ...args)
};
