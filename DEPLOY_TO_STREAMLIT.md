# Deploy to Streamlit Cloud - Step by Step Guide

## Prerequisites
✅ Code is ready
✅ Model files are included
✅ Requirements.txt is updated

## Step 1: Create GitHub Repository

1. Go to [GitHub.com](https://github.com) and log in
2. Click the **"+"** icon in the top right → **"New repository"**
3. Repository settings:
   - **Name**: `handwritten-equation-solver` (or your preferred name)
   - **Description**: "CNN-based handwritten math equation solver"
   - **Visibility**: ✅ **Public** (required for free Streamlit Cloud)
   - **Initialize**: ❌ Don't initialize with README (we already have files)
4. Click **"Create repository"**

## Step 2: Push Code to GitHub

After creating the repository, GitHub will show you commands. Use these:

```bash
cd /Users/happy/Documents/Code/Handwritten

# Add remote (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/handwritten-equation-solver.git

# Or if you prefer SSH:
# git remote add origin git@github.com:YOUR_USERNAME/handwritten-equation-solver.git

# Push code
git branch -M main
git push -u origin main
```

**Or use the commands I'll provide below after you tell me your GitHub username.**

## Step 3: Deploy to Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with your **GitHub account**
3. Click **"New app"**
4. Fill in:
   - **Repository**: Select `your-username/handwritten-equation-solver`
   - **Branch**: `main`
   - **Main file path**: `streamlit_app.py`
   - **App URL**: (auto-generated, or choose custom)
5. Click **"Deploy"**

Streamlit will automatically:
- Install dependencies from `requirements.txt`
- Run your app
- Give you a public URL!

## Important Files Included

✅ `streamlit_app.py` - Main app
✅ `inference_utils.py` - Recognition logic
✅ `model.h5` - Trained model (1.9 MB)
✅ `label_encoder.pkl` - Label encoder
✅ `requirements.txt` - Dependencies
✅ `README.md` - Documentation

## After Deployment

1. Your app will be live at: `https://your-app-name.streamlit.app`
2. Share the URL with anyone!
3. Streamlit will auto-update when you push to GitHub

## Troubleshooting

If deployment fails:
- Check that `requirements.txt` has all dependencies
- Verify `model.h5` and `label_encoder.pkl` are in the repo
- Check Streamlit Cloud logs for errors

## Need Help?

Just tell me your GitHub username and I'll give you the exact commands to run!

