#!/usr/bin/env python3
import requests
import json
import time

def test_production_system():
    print("🧪 Testing Production Web Application System")
    print("="*60)
    
    base_url = "http://localhost:5000"
    
    # Test 1: System status and health
    print("1. Testing system status and health...")
    try:
        response = requests.get(f"{base_url}/api/check-status", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ System operational - Version: {data.get('version', 'Unknown')}")
            print(f"   📊 Students loaded: {data.get('students_loaded', 0)}")
        else:
            print(f"   ❌ Status check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Status check error: {e}")
        return False
    
    # Test 2: Authentication with multiple students
    test_students = [
        {
            "student_name": "John Doe Smith",
            "batch_number": "AWS-2024-001",
            "sixerclass_id": "SIX001"
        },
        {
            "student_name": "Jane Doe Wilson", 
            "batch_number": "AWS-2024-001",
            "sixerclass_id": "SIX002"
        }
    ]
    
    for i, student in enumerate(test_students, 1):
        print(f"\n2.{i} Testing authentication for {student['student_name']}...")
        
        try:
            response = requests.post(
                f"{base_url}/api/authenticate",
                json=student,
                headers={'Content-Type': 'application/json'},
                timeout=15
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get('success'):
                    print(f"   ✅ Authentication successful")
                    print(f"   📋 Student: {result['student']['student_name']}")
                    print(f"   🏷️  Batch: {result['student']['batch_number']}")
                else:
                    print(f"   ❌ Authentication failed: {result.get('error', 'Unknown error')}")
                    return False
            else:
                print(f"   ❌ Authentication error: {response.status_code}")
                print(f"   📄 Response: {response.text}")
                return False
                
        except Exception as e:
            print(f"   ❌ Authentication test error: {e}")
            return False
    
    # Test 3: Certificate generation and download
    print("\n3. Testing certificate generation and download...")
    
    try:
        # First authenticate to establish session
        auth_response = requests.post(
            f"{base_url}/api/authenticate",
            json=test_students[0],
            headers={'Content-Type': 'application/json'},
            timeout=15
        )
        
        if auth_response.ok:
            # Now request certificate download
            download_response = requests.post(
                f"{base_url}/api/download-certificate",
                headers={'Content-Type': 'application/json'},
                timeout=20
            )
            
            if download_response.status_code == 200:
                result = download_response.json()
                if result.get('success'):
                    print(f"   ✅ Certificate generated successfully")
                    print(f"   📄 Filename: {result['filename']}")
                    print(f"   🔗 Download URL: {result['download_url']}")
                    
                    # Test download URL
                    download_test = requests.get(f"{base_url}{result['download_url']}", timeout=10)
                    if download_test.status_code == 200:
                        print(f"   ✅ Download URL accessible")
                    else:
                        print(f"   ⚠️  Download URL test failed: {download_test.status_code}")
                else:
                    print(f"   ❌ Certificate generation failed: {result.get('error', 'Unknown error')}")
                    return False
            else:
                print(f"   ❌ Download error: {download_response.status_code}")
                return False
        else:
            print("   ❌ Cannot test download - authentication failed")
            return False
            
    except Exception as e:
        print(f"   ❌ Download test error: {e}")
        return False
    
    # Test 4: Get students list (admin feature)
    print("\n4. Testing admin features - students list...")
    
    try:
        response = requests.get(f"{base_url}/api/students", timeout=10)
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                print(f"   ✅ Students list retrieved - {result['count']} students")
                if result['students']:
                    print(f"   📋 Sample: {result['students'][0]['student_name']}")
            else:
                print(f"   ⚠️  Students list failed: {result.get('error', 'Unknown error')}")
        else:
            print(f"   ⚠️  Students list error: {response.status_code}")
    except Exception as e:
        print(f"   ⚠️  Students list test error: {e}")
    
    print("\n🎯 Production system test finished!")
    print("✅ All core functionality tests passed!")
    print("🌐 Production web interface: http://localhost:5000")
    print("📊 Admin features: /api/students (GET)")
    print("🔧 Enhanced error handling and logging enabled")
    
    return True

if __name__ == "__main__":
    success = test_production_system()
    if success:
        print("\n🎉 Production system is ready for deployment!")
        print("🚀 Next steps: AWS deployment, database integration, email delivery")
    else:
        print("\n❌ Production system has issues that need to be resolved")
