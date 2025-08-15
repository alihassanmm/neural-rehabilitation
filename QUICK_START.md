# ⚡ ResumeRefiner Quick Start Guide

Get your ResumeRefiner application running on Replit in under 10 minutes!

## 🎯 What You Need

1. **Replit account** (free at [replit.com](https://replit.com))
2. **Gemini API key** (free at [Google AI Studio](https://makersuite.google.com/app/apikey))
3. **This project folder** (ResumeRefiner_Replit_Deploy)

## 🚀 5-Minute Setup

### Step 1: Upload to Replit (2 minutes)

1. Go to [replit.com](https://replit.com) and sign in
2. Click **"Create Repl"**
3. Choose **"Upload files"**
4. Drag the entire `ResumeRefiner_Replit_Deploy` folder
5. Wait for upload to complete

### Step 2: Add API Key (1 minute)

1. Click **"Secrets"** (🔒) in the left sidebar
2. Add this secret:
   - **Key**: `GEMINI_API_KEY`
   - **Value**: `your_actual_api_key_here`

### Step 3: Run Application (1 minute)

1. Click the green **"Run"** button
2. Wait for startup messages
3. Click the URL that appears (like `https://your-repl.replit.dev`)

### Step 4: Test (1 minute)

1. Upload a resume PDF
2. Add a job description
3. Click "Start Optimization"
4. Download your optimized resume!

## ✅ Success Indicators

You'll know it's working when you see:

```
* Running on all addresses (0.0.0.0)
* Running on http://127.0.0.1:5000
```

And your URL shows the ResumeRefiner interface.

## 🚨 Quick Fixes

### If the Run button doesn't work:
1. Open **Shell** tab
2. Type: `cd backend && python src/main.py`

### If you get "Failed to fetch":
1. Check your API key in Secrets
2. Click Stop, then Run again

### If PDF generation fails:
1. Wait 30 seconds for LaTeX to install
2. Try again

## 🎉 That's It!

Your ResumeRefiner is now live and ready to optimize resumes!

**Need more help?** Check the detailed `REPLIT_DEPLOYMENT_GUIDE.md` file.

---

**Pro Tip**: Bookmark your Repl URL - it's your permanent link to the application!

