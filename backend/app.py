#!/usr/bin/env python3
"""
ResumeRefiner Backend Application
Entry point for deployment
"""

import sys
import os

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from main import app

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)

