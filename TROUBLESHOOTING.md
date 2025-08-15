# 🔧 ResumeRefiner Troubleshooting Guide

This guide helps you resolve common issues when deploying and running ResumeRefiner on Replit.

## 🚨 Common Issues

### 1. "Failed to fetch" Error

**Symptoms:**
- Frontend shows "Failed to fetch" when trying to upload
- Network errors in browser console
- Can't connect to backend

**Causes & Solutions:**

#### Backend Not Running
```bash
# Check if backend is running
ps aux | grep python

# If not running, start it
cd backend && python src/main.py
```

#### Wrong Backend URL
- Check `frontend/src/config.js`
- Update `BACKEND_URL` to your Repl URL
- Should be: `https://your-repl-name.your-username.repl.co`

#### CORS Issues
- Verify CORS is enabled in backend
- Check browser console for CORS errors
- Restart the Repl if needed

#### Environment Variables Missing
- Go to Secrets (🔒) in Replit
- Verify `GEMINI_API_KEY` is set
- Add missing environment variables

### 2. PDF Compilation Errors

**Symptoms:**
- "Failed to compile PDF" message
- LaTeX errors in console
- PDF download doesn't work

**Solutions:**

#### LaTeX Not Installed
```bash
# Check if LaTeX is available
which pdflatex

# If missing, restart Repl (LaTeX installs automatically)
```

#### Template Syntax Errors
- Check console for LaTeX error messages
- Look for unescaped special characters
- Verify template formatting

#### File Permissions
```bash
# Check backend directory permissions
ls -la backend/

# Fix permissions if needed
chmod +x backend/src/main.py
```

### 3. Gemini API Issues

**Symptoms:**
- "AI optimization failed" message
- API quota exceeded errors
- Invalid API key errors

**Solutions:**

#### Invalid API Key
- Verify API key in [Google AI Studio](https://makersuite.google.com/app/apikey)
- Check for extra spaces or characters
- Regenerate key if needed

#### API Quota Exceeded
- Check usage in Google Cloud Console
- Wait for quota reset
- Upgrade to paid plan if needed

#### Network Issues
```bash
# Test API connectivity
curl -H "Authorization: Bearer $GEMINI_API_KEY" \
  https://generativelanguage.googleapis.com/v1/models
```

### 4. File Upload Problems

**Symptoms:**
- Can't select files
- Upload progress stuck
- File size errors

**Solutions:**

#### File Size Too Large
- Maximum file size: 16MB
- Compress PDF if too large
- Check file size before upload

#### Unsupported File Type
- Supported: PDF, DOCX
- Convert other formats first
- Check file extension

#### Browser Issues
- Clear browser cache
- Try different browser
- Disable ad blockers

### 5. Repl Won't Start

**Symptoms:**
- Run button doesn't work
- Console shows errors
- Application won't load

**Solutions:**

#### Missing Dependencies
```bash
# Install Python dependencies
cd backend && pip install -r requirements.txt

# Install Node dependencies
cd frontend && npm install
```

#### Configuration Issues
- Check `.replit` file exists
- Verify `replit.nix` configuration
- Ensure proper file structure

#### Memory Issues
- Restart the Repl
- Check memory usage in dashboard
- Optimize code if needed

## 🔍 Debugging Commands

### Check System Status
```bash
# Check Python version
python --version

# Check installed packages
pip list

# Check Node version
node --version

# Check LaTeX installation
pdflatex --version
```

### Test Backend Components
```bash
# Test health endpoint
curl https://your-repl-url/api/resume/health

# Test file upload
curl -X POST -F "file=@test.pdf" \
  https://your-repl-url/api/resume/ingest

# Check backend logs
tail -f backend/logs/app.log
```

### Frontend Debugging
```bash
# Build frontend
cd frontend && npm run build

# Check for JavaScript errors
# Open browser console (F12)

# Test API calls
fetch('https://your-repl-url/api/resume/health')
  .then(r => r.json())
  .then(console.log)
```

## 📊 Performance Issues

### Slow Response Times

**Causes:**
- Large file processing
- AI API latency
- LaTeX compilation time

**Solutions:**
- Optimize file sizes
- Add progress indicators
- Implement caching

### Memory Usage

**Monitor:**
```bash
# Check memory usage
free -h

# Check process memory
ps aux --sort=-%mem | head
```

**Optimize:**
- Process files in chunks
- Clean up temporary files
- Restart Repl if needed

## 🔒 Security Issues

### API Key Exposure

**Check:**
- API key not in code files
- Using Replit Secrets properly
- No keys in console logs

**Fix:**
- Move keys to Secrets
- Update code references
- Regenerate exposed keys

### File Upload Security

**Verify:**
- File type validation working
- Size limits enforced
- No executable uploads

## 🛠️ Advanced Troubleshooting

### Enable Debug Mode

Add to Secrets:
```
FLASK_DEBUG=True
FLASK_ENV=development
```

### Detailed Logging

```python
# Add to main.py
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Network Diagnostics

```bash
# Test connectivity
ping google.com

# Check DNS resolution
nslookup generativelanguage.googleapis.com

# Test HTTPS
curl -I https://your-repl-url
```

## 📞 Getting Help

### Before Asking for Help

1. **Check Console Logs**
   - Backend console in Repl
   - Browser developer tools
   - Network tab for API calls

2. **Verify Configuration**
   - Environment variables set
   - Files uploaded correctly
   - Dependencies installed

3. **Test Components**
   - Backend health endpoint
   - Frontend loads
   - API calls work

### Information to Include

When reporting issues, provide:

- **Error Messages**: Exact text from console
- **Steps to Reproduce**: What you did before error
- **Environment**: Browser, OS, Repl URL
- **Configuration**: Environment variables (without API keys)
- **Logs**: Relevant console output

### Self-Help Resources

1. **Replit Documentation**: [docs.replit.com](https://docs.replit.com)
2. **Flask Documentation**: [flask.palletsprojects.com](https://flask.palletsprojects.com)
3. **React Documentation**: [react.dev](https://react.dev)
4. **Google AI Documentation**: [ai.google.dev](https://ai.google.dev)

## 🎯 Prevention Tips

### Regular Maintenance

- **Update Dependencies**: Monthly package updates
- **Monitor Usage**: Check API quotas regularly
- **Backup Configuration**: Export Repl settings
- **Test Functionality**: Regular end-to-end tests

### Best Practices

- **Environment Variables**: Always use Secrets
- **Error Handling**: Implement proper error boundaries
- **Logging**: Add meaningful log messages
- **Testing**: Test after any changes

### Monitoring

- **Uptime**: Use external monitoring service
- **Performance**: Monitor response times
- **Errors**: Track error rates
- **Usage**: Monitor API consumption

---

## 🎉 Quick Recovery Checklist

If everything breaks, try this sequence:

1. ✅ **Stop and Start** the Repl
2. ✅ **Check Secrets** are set correctly
3. ✅ **Verify API Key** is valid
4. ✅ **Test Health Endpoint** works
5. ✅ **Clear Browser Cache** and reload
6. ✅ **Check Console Logs** for errors
7. ✅ **Restart Fresh** if needed

Most issues resolve with a simple restart! 🔄

