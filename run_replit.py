#!/usr/bin/env python3
"""
ResumeRefiner Replit Runner
This script starts the ResumeRefiner application on Replit
"""

import os
import sys
import subprocess
from pathlib import Path

def main():
    """Main entry point for running ResumeRefiner on Replit"""
    
    # Get the current directory
    current_dir = Path(__file__).parent
    backend_dir = current_dir / "backend"
    
    print("🚀 Starting ResumeRefiner on Replit...")
    print(f"📁 Working directory: {current_dir}")
    print(f"🔧 Backend directory: {backend_dir}")
    
    # Check if backend directory exists
    if not backend_dir.exists():
        print("❌ Backend directory not found!")
        sys.exit(1)
    
    # Set environment variables
    os.environ["PYTHONPATH"] = str(backend_dir)
    os.environ["FLASK_ENV"] = "production"
    os.environ["FLASK_RUN_HOST"] = "0.0.0.0"
    os.environ["FLASK_RUN_PORT"] = "5000"
    
    # Change to backend directory
    os.chdir(backend_dir)
    
    # Check if main.py exists
    main_py = backend_dir / "src" / "main.py"
    if not main_py.exists():
        print("❌ main.py not found in backend/src/")
        sys.exit(1)
    
    print("✅ Starting Flask application...")
    print("🌐 Application will be available at your Repl URL")
    print("📝 Check the console for any errors")
    print("-" * 50)
    
    # Run the Flask application
    try:
        subprocess.run([sys.executable, "src/main.py"], check=True)
    except KeyboardInterrupt:
        print("\n🛑 Application stopped by user")
    except subprocess.CalledProcessError as e:
        print(f"❌ Application failed to start: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

