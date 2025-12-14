# test_backend.py (no requests needed)
import socket
import sys

def test_backend():
    print("🔍 Testing Backend Connection")
    print("=" * 50)
    
    # Test if port 3001 is open
    print("1. Checking port 3001...")
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(2)
    
    try:
        result = sock.connect_ex(('127.0.0.1', 3001))
        if result == 0:
            print("   ✅ Port 3001 is OPEN - Backend is running!")
            
            # Try to read a simple response
            sock.send(b"GET / HTTP/1.1\r\nHost: 127.0.0.1\r\n\r\n")
            response = sock.recv(1024)
            if b"HTTP" in response:
                print("   ✅ Backend responding to HTTP requests")
                print(f"   Response preview: {response[:100]}...")
            else:
                print("   ⚠️  Port open but not responding to HTTP")
                
            return True
        else:
            print("   ❌ Port 3001 is CLOSED")
            print("   Backend is NOT running!")
            return False
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False
    finally:
        sock.close()

if __name__ == "__main__":
    if test_backend():
        print("\n✅ Backend is accessible at http://127.0.0.1:3001")
        print("\n📋 Next steps:")
        print("1. Open browser: http://127.0.0.1:3001/docs")
        print("2. Test: curl http://127.0.0.1:3001/health")
    else:
        print("\n❌ Backend is NOT running")
        print("\n🔧 Start it with:")
        print("python -m uvicorn main:app --host 0.0.0.0 --port 3001")