# Deployment Guide

This project has two parts:
1. **Backend** (Hugging Face Spaces) - ML model API
2. **Frontend** (Vercel) - Web interface

---

## Part 1: Deploy Backend to Hugging Face Spaces

### Step 1: Create a new Space

1. Go to [huggingface.co/spaces](https://huggingface.co/spaces)
2. Click "Create new Space"
3. Fill in:
   - **Name**: `equation-solver` (or any name)
   - **SDK**: Gradio
   - **Hardware**: CPU Basic (free)
   - **Visibility**: Public
4. Click "Create Space"

### Step 2: Upload files

Upload these files to your Space (via the web UI or git):

```
hf-backend/
├── app.py              → Upload as app.py
├── requirements.txt    → Upload as requirements.txt

Root directory/
├── model.h5            → Upload as model.h5
├── label_encoder.pkl   → Upload as label_encoder.pkl
```

You can upload via:
- **Web UI**: Click "Files" tab → "Add file" → "Upload files"
- **Git**: Clone the repo and push

### Step 3: Wait for build

The Space will automatically build and deploy. This takes 2-5 minutes.
Once ready, you'll see the Gradio interface.

### Step 4: Get your API URL

Your API endpoint will be:
```
https://YOUR-USERNAME-equation-solver.hf.space/api/predict
```

Replace `YOUR-USERNAME` with your Hugging Face username.

---

## Part 2: Deploy Frontend to Vercel

### Step 1: Create environment variable

In the `frontend/` directory, create a `.env.local` file:

```bash
cd frontend
echo "NEXT_PUBLIC_API_URL=https://YOUR-USERNAME-equation-solver.hf.space/api/predict" > .env.local
```

Replace `YOUR-USERNAME` with your actual Hugging Face username.

### Step 2: Test locally

```bash
cd frontend
npm run dev
```

Open http://localhost:3000 to verify it works.

### Step 3: Deploy to Vercel

**Option A: Via Vercel CLI**

```bash
npm i -g vercel
cd frontend
vercel
```

**Option B: Via Vercel Dashboard**

1. Go to [vercel.com](https://vercel.com)
2. Click "Add New Project"
3. Import your GitHub repository
4. Set **Root Directory** to `frontend`
5. Add Environment Variable:
   - Name: `NEXT_PUBLIC_API_URL`
   - Value: `https://YOUR-USERNAME-equation-solver.hf.space/api/predict`
6. Click Deploy

---

## Updating the API URL

After deploying the backend, update the frontend:

1. **Local**: Edit `frontend/.env.local`
2. **Vercel**: Go to Project Settings → Environment Variables → Update `NEXT_PUBLIC_API_URL`

---

## Troubleshooting

### "Failed to process image" error
- Ensure your HF Space is running (not sleeping)
- Check the API URL is correct
- Verify the Space finished building

### HF Space keeps sleeping
- Free tier spaces sleep after 48 hours of inactivity
- Visit your Space URL to wake it up
- Consider upgrading to a paid tier for always-on

### CORS errors
- Gradio handles CORS automatically
- If issues persist, check your Space's app.py

---

## Local Development

### Backend
```bash
cd hf-backend
pip install -r requirements.txt
python app.py
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

