#!/usr/bin/env python3
"""
ResumeRefiner Setup Script
Installs the ResumeRefiner application and its dependencies
"""

from setuptools import setup, find_packages
import os

# Read the README file
def read_readme():
    with open("README.md", "r", encoding="utf-8") as fh:
        return fh.read()

# Read requirements
def read_requirements():
    with open("requirements.txt", "r", encoding="utf-8") as fh:
        return [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="resume-refiner",
    version="1.0.0",
    author="ResumeRefiner Team",
    author_email="support@resumerefiner.com",
    description="AI-powered resume optimization tool with professional PDF generation",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/your-username/resume-refiner",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: JavaScript",
        "Topic :: Office/Business",
        "Topic :: Text Processing :: Markup :: LaTeX",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    python_requires=">=3.11",
    install_requires=read_requirements(),
    extras_require={
        "dev": [
            "pytest>=7.4.3",
            "pytest-flask>=1.3.0",
            "black>=23.11.0",
            "flake8>=6.1.0",
        ],
        "production": [
            "gunicorn>=21.2.0",
            "waitress>=2.1.2",
        ],
    },
    entry_points={
        "console_scripts": [
            "resume-refiner=backend.src.main:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.md", "*.txt", "*.json", "*.js", "*.jsx", "*.css", "*.html"],
    },
    zip_safe=False,
)

