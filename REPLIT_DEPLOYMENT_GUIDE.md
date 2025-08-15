# 🚀 ResumeRefiner Replit Deployment Guide

This guide provides step-by-step instructions for deploying the ResumeRefiner application on Replit.

## 📋 Prerequisites

Before starting, ensure you have:

1. **Replit Account**: Sign up at [replit.com](https://replit.com)
2. **Gemini API Key**: Get from [Google AI Studio](https://makersuite.google.com/app/apikey)
3. **Project Files**: The complete ResumeRefiner project folder

## 🎯 Step-by-Step Deployment

### Step 1: Create New Repl

1. **Login to Replit**
   - Go to [replit.com](https://replit.com)
   - Sign in to your account

2. **Create New Repl**
   - Click **"Create Repl"** button
   - Choose **"Import from GitHub"** OR **"Upload files"**

3. **Upload Project Files**
   - If using file upload, drag and drop the entire `ResumeRefiner_Replit_Deploy` folder
   - Wait for files to upload completely

### Step 2: Configure Environment Variables

1. **Access Secrets**
   - In your Repl, click on **"Secrets"** (🔒 lock icon) in the left sidebar
   - This is where you'll store sensitive configuration

2. **Add Required Environment Variables**
   
   Add these key-value pairs:

   ```
   Key: GEMINI_API_KEY
   Value: your_actual_gemini_api_key_here
   ```

   ```
   Key: FLASK_ENV
   Value: production
   ```

   ```
   Key: FLASK_RUN_HOST
   Value: 0.0.0.0
   ```

   ```
   Key: FLASK_RUN_PORT
   Value: 5000
   ```

   ```
   Key: PYTHONPATH
   Value: /home/runner/ResumeRefiner/backend
   ```

### Step 3: Install Dependencies

The `.replit` configuration file will automatically handle most installations. If you need to install manually:

1. **Open Shell** (click the Shell tab)

2. **Install Python Dependencies**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

3. **Install Frontend Dependencies**
   ```bash
   cd frontend
   npm install
   ```

### Step 4: Configure Frontend

1. **Update Frontend Configuration**
   - Open `frontend/src/config.js`
   - Update the backend URL to match your Repl URL:

   ```javascript
   const config = {
     BACKEND_URL: 'https://your-repl-name.your-username.repl.co'
   };
   ```

2. **Build Frontend** (if needed)
   ```bash
   cd frontend
   npm run build
   ```

### Step 5: Run the Application

1. **Click the "Run" Button**
   - The green "Run" button at the top of the Repl
   - This will start the Flask backend automatically

2. **Check Console Output**
   - Look for messages like:
   ```
   * Running on all addresses (0.0.0.0)
   * Running on http://127.0.0.1:5000
   * Running on http://0.0.0.0:5000
   ```

3. **Access Your Application**
   - Replit will provide a URL like: `https://your-repl-name.your-username.repl.co`
   - Click on the URL to open your application

## 🔧 Configuration Files Explained

### `.replit` File
```toml
run = "cd backend && python src/main.py"
modules = ["python-3.11", "nodejs-20"]
```
- Defines how to run your application
- Specifies required modules (Python 3.11, Node.js 20)

### `replit.nix` File
```nix
{ pkgs }: {
  deps = [
    pkgs.python311Full
    pkgs.texlive.combined.scheme-full
    # ... other dependencies
  ];
}
```
- Manages system-level dependencies
- Includes LaTeX for PDF generation

### `requirements.txt`
- Lists all Python packages needed
- Automatically installed when Repl starts

## 🧪 Testing Your Deployment

### 1. Health Check
- Visit: `https://your-repl-url/api/resume/health`
- Should return: `{"status": "healthy"}`

### 2. Frontend Test
- Open your main Repl URL
- Should see the ResumeRefiner interface
- Try uploading a test PDF

### 3. Full Workflow Test
1. Upload a resume PDF
2. Add job description
3. Click "Start Optimization"
4. Verify PDF download works

## 🚨 Troubleshooting

### Common Issues and Solutions

#### 1. "Failed to fetch" Error
**Problem**: Frontend can't connect to backend
**Solutions**:
- Check if backend is running (look for Flask startup messages)
- Verify environment variables are set correctly
- Ensure CORS is configured properly

#### 2. LaTeX/PDF Compilation Errors
**Problem**: PDF generation fails
**Solutions**:
- Check if LaTeX is installed (should be automatic with `replit.nix`)
- Verify file permissions
- Check console for LaTeX error messages

#### 3. Gemini API Errors
**Problem**: AI optimization fails
**Solutions**:
- Verify `GEMINI_API_KEY` is correct
- Check API quota and billing status
- Ensure API key has proper permissions

#### 4. File Upload Issues
**Problem**: Can't upload files
**Solutions**:
- Check file size (max 16MB)
- Verify file type (PDF, DOCX supported)
- Check backend logs for errors

### Debug Commands

```bash
# Check Python packages
pip list

# Check environment variables
env | grep GEMINI

# Test backend directly
curl https://your-repl-url/api/resume/health

# Check file permissions
ls -la backend/
```

## 🔒 Security Considerations

### Environment Variables
- ✅ **DO**: Store API keys in Replit Secrets
- ❌ **DON'T**: Put API keys in code files
- ✅ **DO**: Use `.env.example` as a template

### File Handling
- Files are processed in memory when possible
- Temporary files are cleaned up automatically
- Upload size is limited to 16MB

### API Security
- CORS is configured for web access
- Input validation on all endpoints
- LaTeX injection prevention

## 📊 Performance Optimization

### Replit-Specific Tips

1. **Keep Repl Active**
   - Replit may sleep inactive Repls
   - Consider using a uptime monitor service

2. **Memory Management**
   - Large PDF processing uses memory
   - Monitor usage in Repl dashboard

3. **File Storage**
   - Temporary files are cleaned automatically
   - Don't store large files permanently

## 🔄 Updates and Maintenance

### Updating Your Deployment

1. **Update Code**
   - Upload new files to your Repl
   - Or sync with GitHub if using Git integration

2. **Update Dependencies**
   ```bash
   pip install -r requirements.txt --upgrade
   cd frontend && npm update
   ```

3. **Restart Application**
   - Click "Stop" then "Run" in Replit
   - Or use Shell: `pkill python && python backend/src/main.py`

### Monitoring

- Check Repl console for errors
- Monitor API usage in Google Cloud Console
- Watch for memory/CPU usage in Replit dashboard

## 🎉 Success Checklist

After deployment, verify:

- [ ] Repl starts without errors
- [ ] Health endpoint returns 200 OK
- [ ] Frontend loads properly
- [ ] File upload works
- [ ] AI optimization processes
- [ ] PDF generation succeeds
- [ ] Download links work

## 📞 Getting Help

If you encounter issues:

1. **Check Console Logs**
   - Look for error messages in Repl console
   - Check browser developer tools

2. **Verify Configuration**
   - Double-check environment variables
   - Ensure all files uploaded correctly

3. **Test Components**
   - Test backend API endpoints individually
   - Verify frontend can reach backend

4. **Common Solutions**
   - Restart the Repl
   - Clear browser cache
   - Check API key validity

## 🎯 Next Steps

After successful deployment:

1. **Custom Domain** (Repl Pro feature)
   - Configure custom domain if needed
   - Set up SSL certificate

2. **Monitoring**
   - Set up uptime monitoring
   - Monitor API usage and costs

3. **Backup**
   - Export your Repl regularly
   - Keep API keys secure

---

**Congratulations!** 🎉 Your ResumeRefiner application should now be running on Replit!

For additional support, refer to the main README.md file or check the troubleshooting section above.

