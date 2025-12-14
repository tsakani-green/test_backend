# test_simple.py
import requests
import socket
import sys

def test_connection():
    print("🔍 Testing Backend Connection")
    print("=" * 50)
    
    url = "http://127.0.0.1:3001"
    
    # Test 1: Check port
    print("1. Checking port 3001...")
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(2)
    result = sock.connect_ex(('127.0.0.1', 3001))
    
    if result == 0:
        print("   ✅ Port 3001 is OPEN")
    else:
        print("   ❌ Port 3001 is CLOSED")
        print("   Backend is NOT running!")
        return False
    
    # Test 2: Try to connect
    print("\n2. Trying to connect...")
    try:
        response = requests.get(f"{url}/", timeout=5)
        print(f"   ✅ Connected! HTTP {response.status_code}")
        print(f"   Response: {response.text[:100]}...")
        return True
    except requests.exceptions.ConnectionError:
        print("   ❌ Connection refused")
        print("   Backend might be running but not accessible")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    return False

if __name__ == "__main__":
    if test_connection():
        print("\n✅ Backend is running and accessible")
    else:
        print("\n❌ Backend is NOT accessible")
        print("\n🔧 Try running backend with:")
        print("python -m uvicorn main:app --host 0.0.0.0 --port 3001")