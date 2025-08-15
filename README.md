# 🎯 ResumeRefiner - Replit Deployment Package

**AI-Powered Resume Optimization Tool** - Ready for instant Replit deployment!

A production-grade, mobile-responsive web application that accepts resumes in various formats, optimizes them using Google Gemini AI, and generates downloadable PDF and LaTeX files with before/after comparison functionality.

## 🚀 Quick Replit Deployment (5 Minutes)

### 1. Upload to Replit
1. Go to [replit.com](https://replit.com) and sign in
2. Click **"Create Repl"** → **"Upload files"**
3. Drag this entire folder to Replit
4. Wait for upload to complete

### 2. Add API Key
1. Click **"Secrets"** (🔒) in Replit sidebar
2. Add: `GEMINI_API_KEY` = `your_api_key_here`
3. Get your API key from [Google AI Studio](https://makersuite.google.com/app/apikey)

### 3. Run Application
1. Click the green **"Run"** button
2. Wait for startup (30-60 seconds)
3. Click your Repl URL when it appears

### 4. Test
1. Upload a resume PDF
2. Add job description
3. Click "Start Optimization"
4. Download optimized resume!

## 📚 Replit Documentation
- **📖 [REPLIT_DEPLOYMENT_GUIDE.md](REPLIT_DEPLOYMENT_GUIDE.md)** - Detailed deployment instructions
- **⚡ [QUICK_START.md](QUICK_START.md)** - 5-minute setup guide
- **🔧 [TROUBLESHOOTING.md](TROUBLESHOOTING.md)** - Common issues and solutions

## 🚀 Features

### Core Functionality
- **Multi-format Resume Input**: Supports DOCX, PDF uploads, and Google Docs links
- **AI-Powered Optimization**: Uses Google Gemini 1.5 Pro for intelligent resume enhancement
- **STAR/C.A.R./XYZ Methodologies**: Applies proven resume writing frameworks
- **ATS-Friendly Output**: Optimizes for Applicant Tracking Systems
- **Before/After Comparison**: Visual diff view for experience bullets
- **Professional PDF Generation**: LaTeX-based PDF compilation
- **Customizable Parameters**: Region, seniority level, and writing tone options

### Technical Features
- **Responsive Design**: Mobile-first, professional UI using Tailwind CSS and shadcn/ui
- **Real-time Progress**: Step-by-step progress indicators
- **Error Handling**: Comprehensive error states and user feedback
- **File Validation**: Secure file upload with type and size validation
- **API Integration**: RESTful backend with proper CORS support

## 🏗️ Architecture

### Backend (Flask)
- **Framework**: Flask with Python 3.11
- **AI Integration**: Google Gemini API for resume optimization
- **Document Processing**: Mammoth (DOCX), PyPDF2 (PDF), Google Docs API
- **PDF Generation**: LaTeX with pdflatex compilation
- **Validation**: JSON Schema validation for structured data

### Frontend (React)
- **Framework**: React 18 with Vite
- **UI Components**: shadcn/ui component library
- **Styling**: Tailwind CSS with custom theme
- **Icons**: Lucide React icons
- **State Management**: React hooks for application state

## 📁 Project Structure

```
ResumeRefiner/
├── backend/
│   ├── src/
│   │   ├── routes/
│   │   │   ├── resume.py          # Main API endpoints
│   │   │   └── user.py            # User management (template)
│   │   ├── services/
│   │   │   ├── resume_parser.py   # Document parsing service
│   │   │   ├── gemini_optimizer.py # AI optimization service
│   │   │   ├── latex_renderer.py  # LaTeX template rendering
│   │   │   └── pdf_compiler.py    # PDF compilation service
│   │   ├── utils/
│   │   │   ├── validation.py      # JSON schema validation
│   │   │   └── file_utils.py      # File handling utilities
│   │   └── main.py               # Flask application entry point
│   ├── venv/                     # Python virtual environment
│   ├── requirements.txt          # Python dependencies
│   └── .env                      # Environment variables
└── frontend/
    ├── src/
    │   ├── components/ui/        # shadcn/ui components
    │   ├── App.jsx              # Main React application
    │   ├── App.css              # Application styles
    │   └── main.jsx             # React entry point
    ├── package.json             # Node.js dependencies
    └── index.html               # HTML template
```

## 🔧 API Endpoints

### POST /api/ingest
Ingests resume from file upload or Google Docs URL
- **Input**: Multipart file or JSON with `googleDocUrl`
- **Output**: Structured resume data with parsing statistics

### POST /api/optimize
Optimizes resume using Gemini AI with STAR/C.A.R./XYZ methodologies
- **Input**: Resume data, job description, region, seniority, tone
- **Output**: Optimized JSON with ATS keywords and validation report

### POST /api/render
Renders optimized JSON to LaTeX format
- **Input**: Optimized resume JSON
- **Output**: LaTeX string ready for compilation

### POST /api/compile
Compiles LaTeX to PDF
- **Input**: LaTeX string
- **Output**: PDF file download

### GET /api/health
Health check endpoint
- **Output**: Service status

## 🛠️ Setup and Installation

### Prerequisites
- Python 3.11+
- Node.js 20+
- LaTeX distribution (texlive)
- Google Gemini API key

### Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Create .env file
echo "GEMINI_API_KEY=your_api_key_here" > .env
echo "MAX_UPLOAD_MB=12" >> .env

# Start the server
python src/main.py
```

### Frontend Setup
```bash
cd frontend
pnpm install  # or npm install
pnpm run dev  # or npm run dev
```

### LaTeX Setup (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install -y texlive-latex-base texlive-latex-extra texlive-fonts-recommended
```

## 🚀 Running the Application

1. **Start Backend**: `cd backend && source venv/bin/activate && python src/main.py`
2. **Start Frontend**: `cd frontend && pnpm run dev`
3. **Access Application**: Open http://localhost:5173 in your browser

The backend runs on port 5001, frontend on port 5173 (or next available port).

## 📋 Usage Workflow

1. **Upload Resume**: Choose file upload or Google Docs URL
2. **Configure Options**: Set region, seniority level, and writing tone
3. **Add Job Description** (Optional): Paste target job description for optimization
4. **Start Optimization**: Click "Start Optimization" to begin processing
5. **Review Results**: View before/after comparison and ATS keywords
6. **Download Files**: Get optimized PDF and LaTeX source files

## 🔒 Security Features

- **File Validation**: Strict file type and size limits
- **Input Sanitization**: LaTeX escaping and validation
- **CORS Configuration**: Proper cross-origin request handling
- **Error Handling**: Secure error messages without sensitive data exposure
- **Rate Limiting**: API quota management for Gemini integration

## 🎨 Design Principles

### Resume Optimization
- **STAR Method**: Situation, Task, Action, Results structure
- **C.A.R. Framework**: Challenge, Action, Results with quantification
- **XYZ Formula**: "Accomplished X as measured by Y by doing Z"
- **ATS Optimization**: Keyword optimization and formatting
- **Regional Conventions**: US/UK/EU spelling and formatting standards

### User Experience
- **Progressive Disclosure**: Step-by-step workflow with clear progress
- **Responsive Design**: Mobile-first approach with touch-friendly interface
- **Error Prevention**: Validation and helpful error messages
- **Performance**: Optimized loading and processing indicators

## 🧪 Testing

### Backend Testing
```bash
# Test file ingestion
curl -X POST -F "file=@sample_resume.docx" http://localhost:5001/api/ingest

# Test health endpoint
curl http://localhost:5001/api/health
```

### Frontend Testing
- Manual testing through browser interface
- File upload validation
- Responsive design verification
- Error state handling

## 📦 Deployment

### Production Considerations
- **Environment Variables**: Secure API key management
- **File Storage**: Temporary file cleanup and storage limits
- **Scaling**: Consider Redis for session management
- **Monitoring**: Add logging and error tracking
- **SSL/HTTPS**: Enable secure connections
- **CDN**: Static asset optimization

### Docker Deployment (Future Enhancement)
```dockerfile
# Dockerfile example for backend
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5001
CMD ["python", "src/main.py"]
```

## 🔧 Configuration

### Environment Variables
- `GEMINI_API_KEY`: Google Gemini API key (required)
- `MAX_UPLOAD_MB`: Maximum file upload size (default: 12)
- `FLASK_ENV`: Flask environment (development/production)
- `FLASK_DEBUG`: Enable debug mode (True/False)

### Customization Options
- **LaTeX Templates**: Modify `latex_renderer.py` for custom layouts
- **Parsing Rules**: Adjust `resume_parser.py` for different formats
- **UI Themes**: Update Tailwind configuration for branding
- **Optimization Prompts**: Customize Gemini prompts in `gemini_optimizer.py`

## 🐛 Troubleshooting

### Common Issues
1. **Gemini API Quota**: Check API usage and billing
2. **LaTeX Compilation**: Ensure all packages are installed
3. **File Upload**: Verify file types and size limits
4. **CORS Errors**: Check backend CORS configuration
5. **Port Conflicts**: Use different ports if 5001/5173 are occupied

### Debug Mode
Enable Flask debug mode for detailed error messages:
```bash
export FLASK_DEBUG=True
python src/main.py
```

## 📄 License

This project is built for demonstration purposes. Please ensure compliance with:
- Google Gemini API Terms of Service
- File processing library licenses
- UI component library licenses

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 📞 Support

For issues and questions:
1. Check the troubleshooting section
2. Review API documentation
3. Check server logs for detailed error messages
4. Verify environment configuration

---

**ResumeRefiner** - Transforming resumes with AI-powered optimization for the modern job market.

