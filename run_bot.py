#!/usr/bin/env python3
"""
Startup script for Kirloskar RAG Bot
"""

import subprocess
import sys
import os

def check_dependencies():
    """Check if required packages are installed"""
    required_packages = [
        'streamlit',
        'chromadb', 
        'openai',
        'pandas'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"❌ Missing required packages: {', '.join(missing_packages)}")
        print("Please install them using: pip install -r requirements.txt")
        return False
    
    print("✅ All required packages are installed!")
    return True

def main():
    print("🤖 Starting Kirloskar RAG Bot...")
    print("=" * 50)
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Get the directory of this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    streamlit_app = os.path.join(script_dir, "streamlit_ragbot.py")
    
    # Start Streamlit app
    try:
        print("🚀 Launching Streamlit application...")
        print("The app will open in your default browser at http://localhost:8501")
        print("\nTo stop the application, press Ctrl+C")
        print("=" * 50)
        
        subprocess.run([sys.executable, "-m", "streamlit", "run", streamlit_app])
        
    except KeyboardInterrupt:
        print("\n👋 Shutting down RAG Bot. Goodbye!")
    except Exception as e:
        print(f"❌ Error starting application: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
