#!/usr/bin/env python3
"""
Main entry point to start both Flask backend and Streamlit frontend
Run: python run_app.py
"""

import subprocess
import time
import os
import sys
import signal

def run_app():
    # Get the directory of this script
    project_dir = os.path.dirname(os.path.abspath(__file__))
    backend_dir = os.path.join(project_dir, "backend")
    frontend_dir = os.path.join(project_dir, "frontend")
    
    print("=" * 60)
    print("🎬 YouTube Thumbnail Board - Starting")
    print("=" * 60)
    
    # Start Flask backend
    print("\n📌 Starting Flask Backend...")
    backend_process = subprocess.Popen(
        [sys.executable, "app.py"],
        cwd=backend_dir,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    print(f"✅ Flask Backend started (PID: {backend_process.pid})")
    
    # Wait for Flask to start
    time.sleep(3)
    
    # Start Streamlit frontend
    print("\n🎬 Starting Streamlit Frontend...")
    frontend_process = subprocess.Popen(
        [sys.executable, "-m", "streamlit", "run", "streamlit_app.py"],
        cwd=frontend_dir,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    print(f"✅ Streamlit Frontend started (PID: {frontend_process.pid})")
    
    print("\n" + "=" * 60)
    print("🚀 Application Ready!")
    print("=" * 60)
    print("📺 Frontend: http://localhost:8501")
    print("📌 Backend:  http://localhost:5000")
    print("\nPress Ctrl+C to stop both services")
    print("=" * 60 + "\n")
    
    def signal_handler(sig, frame):
        print("\n\n🛑 Shutting down...")
        backend_process.terminate()
        frontend_process.terminate()
        try:
            backend_process.wait(timeout=5)
            frontend_process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            backend_process.kill()
            frontend_process.kill()
        print("✅ All services stopped")
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Keep the processes running
    try:
        while True:
            # Check if processes are still running
            if backend_process.poll() is not None:
                print("⚠️  Backend process ended unexpectedly")
                frontend_process.terminate()
                sys.exit(1)
            if frontend_process.poll() is not None:
                print("⚠️  Frontend process ended unexpectedly")
                backend_process.terminate()
                sys.exit(1)
            time.sleep(1)
    except KeyboardInterrupt:
        signal_handler(None, None)

if __name__ == "__main__":
    run_app()
