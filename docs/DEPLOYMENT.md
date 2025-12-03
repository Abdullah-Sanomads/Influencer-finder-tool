# Deployment Guide - Free Hosting

This guide shows you how to deploy the Instagram Influencer Finder to free hosting platforms so it's accessible online.

## Overview

We'll deploy:
- **Backend** → Render.com (free tier)
- **Frontend** → Netlify (free tier)

Both are 100% free and don't require a credit card.

## Prerequisites

- GitHub account (for code hosting)
- The app working locally (follow [LOCAL_SETUP.md](LOCAL_SETUP.md) first)

## Part 1: Deploy Backend to Render

### Step 1: Push Code to GitHub

1. **Create a new GitHub repository**
   - Go to [github.com/new](https://github.com/new)
   - Name: `instagram-influencer-finder`
   - Make it Public or Private (your choice)
   - Don't initialize with README (we already have code)
   - Click "Create repository"

2. **Push your code to GitHub**

   Open terminal in your project root folder:

   ```bash
   # Initialize git (if not already)
   git init
   
   # Add all files
   git add .
   
   # Commit
   git commit -m "Initial commit - Instagram Influencer Finder"
   
   # Add remote (replace with YOUR repo URL)
   git remote add origin https://github.com/YOUR_USERNAME/instagram-influencer-finder.git
   
   # Push to GitHub
   git branch -M main
   git push -u origin main
   ```

3. **Verify code is on GitHub**
   - Visit your repository URL
   - You should see all project files

### Step 2: Create Render Account

1. **Go to [render.com](https://render.com)**

2. **Click "Get Started"**

3. **Sign up with GitHub** (recommended)
   - This will link your GitHub repositories
   - Authorize Render to access your repos

4. **You're now logged in to Render Dashboard**

### Step 3: Create a New Web Service

1. **Click "New +" button** (top right)

2. **Select "Web Service"**

3. **Connect your GitHub repository:**
   - Find `instagram-influencer-finder`
   - Click "Connect"

4. **Configure the service:**

   **Name:** `influencer-finder-backend` (or your choice)
   
   **Region:** Select closest to you
   
   **Branch:** `main`
   
   **Root Directory:** `backend`
   
   **Runtime:** `Node`
   
   **Build Command:** `npm install`
   
   **Start Command:** `node server.js`
   
   **Instance Type:** `Free`

5. **Add Environment Variables:**

   Click "Advanced" → "Add Environment Variable"

   Add these:
   
   ```
   PORT=3000
   MODE=demo
   RAPIDAPI_KEY=your_key_if_using_live_mode
   RAPIDAPI_HOST=your_host_if_using_live_mode
   RATE_LIMIT_MAX=100
   RATE_LIMIT_WINDOW_MS=900000
   ```

   *For demo mode, only `PORT` and `MODE=demo` are needed.*

6. **Click "Create Web Service"**

7. **Wait for deployment** (2-5 minutes)
   - Watch the logs in the dashboard
   - You'll see npm install and server startup messages

8. **Your backend is live!**
   - Render will give you a URL like:
     `https://influencer-finder-backend.onrender.com`
   - **Save this URL** - you'll need it for the frontend

### Step 4: Test Your Deployed Backend

Visit: `https://your-backend-url.onrender.com/api/health`

You should see:
```json
{
  "status": "OK",
  "mode": "demo",
  "timestamp": "...",
  "message": "Running in DEMO mode with mock data"
}
```

✅ Backend is deployed!

## Part 2: Deploy Frontend to Netlify

### Step 1: Update Frontend API URL

1. **Edit `frontend/js/app.js`**

2. **Find this line:**
   ```javascript
   const API_URL = 'http://localhost:3000/api';
   ```

3. **Change it to your Render backend URL:**
   ```javascript
   const API_URL = 'https://influencer-finder-backend.onrender.com/api';
   ```
   *(Replace with your actual Render URL)*

4. **Save the file**

5. **Commit and push to GitHub:**
   ```bash
   git add frontend/js/app.js
   git commit -m "Update API URL for production"
   git push
   ```

### Step 2: Create Netlify Account

1. **Go to [netlify.com](https://www.netlify.com)**

2. **Click "Sign up"**

3. **Sign up with GitHub** (recommended)
   - Authorize Netlify

4. **You're now in Netlify Dashboard**

### Step 3: Deploy Frontend

**Option A: Deploy from GitHub (Recommended)**

1. **Click "Add new site" → "Import an existing project"**

2. **Click "Deploy with GitHub"**

3. **Select your repository** (`instagram-influencer-finder`)

4. **Configure build settings:**
   
   **Base directory:** `frontend`
   
   **Build command:** *(leave empty)*
   
   **Publish directory:** `frontend`

5. **Click "Deploy site"**

6. **Wait for deployment** (30 seconds - 1 minute)

7. **Your site is live!**
   - Netlify gives you a URL like:
     `https://random-name-12345.netlify.app`

**Option B: Manual deployment (Drag & Drop)**

1. **Click "Add new site" → "Deploy manually"**

2. **Drag the entire `frontend` folder** into the drop zone

3. **Wait for deployment**

4. **Your site is live!**

### Step 4: Customize Your Domain (Optional)

1. **In Netlify dashboard, click "Site settings"**

2. **Click "Change site name"**

3. **Enter a custom name:**
   - Example: `influencer-finder-app`
   - Your URL becomes: `https://influencer-finder-app.netlify.app`

4. **Or connect a custom domain** (if you own one)
   - Follow Netlify's custom domain guide

## Testing the Deployed App

1. **Visit your Netlify URL**
   - Example: `https://influencer-finder-app.netlify.app`

2. **Click "Start Filtering"**

3. **Fill in filters and search**

4. **Verify results appear**

5. **Test CSV export**

6. **Test on mobile device**

✅ **Your app is fully deployed and accessible worldwide!**

## Post-Deployment Notes

### Free Tier Limitations

**Render (Backend):**
- **Sleep after 15 minutes of inactivity**
  - First request after sleep takes 30-60 seconds to wake up
  - Subsequent requests are fast
- **750 hours/month** of uptime (enough for hobby projects)
- **Limited RAM** (512 MB)

**Netlify (Frontend):**
- **100 GB bandwidth/month**
- **Unlimited builds**
- **Custom domain** (free)
- **HTTPS automatically** enabled

### Keeping Your Backend Awake

To prevent Render from sleeping, you can use:

1. **Uptime monitoring services** (ping every 10 minutes)
   - [UptimeRobot](https://uptimerobot.com/) (free)
   - [Cron-Job.org](https://cron-job.org) (free)
   - Configure to ping: `https://your-backend.onrender.com/api/health`

2. **Scheduled task in the backend** (ping itself)
   - Add a cron job to keep the server active

### Updating Your Deployed App

**Backend updates:**
1. Make changes locally
2. Commit and push to GitHub
3. Render auto-deploys from GitHub (if connected)
4. Or manually trigger deploy in Render dashboard

**Frontend updates:**
1. Make changes locally
2. If using GitHub: commit and push → auto-deploys
3. If using manual: drag & drop new `frontend` folder to Netlify

## Alternative Deployment Options

### Backend Alternatives

**Railway.app:**
- Similar to Render
- 500 hours/month free tier
- [railway.app](https://railway.app)

**Fly.io:**
- More technical setup
- Good free tier
- [fly.io](https://fly.io)

**Heroku:**
- No longer offers free tier (as of Nov 2022)

### Frontend Alternatives

**Vercel:**
- Similar to Netlify
- Great for  frontend apps
- [vercel.com](https://vercel.com)

**GitHub Pages:**
- 100% free
- Works with static sites
- [pages.github.com](https://pages.github.com)

**Cloudflare Pages:**
- Unlimited bandwidth
- Fast CDN
- [pages.cloudflare.com](https://pages.cloudflare.com)

## Troubleshooting

### Backend deployment fails

**Check Render logs:**
- Go to Render dashboard → your service → "Logs"
- Look for errors during build or start

**Common issues:**
- Missing `package.json` dependencies
- Wrong Node.js version (ensure you're using 14+)
- Environment variables not set correctly

### Frontend can't connect to backend

**CORS errors:**
- Ensure backend has CORS enabled (it should by default in our code)
- Check backend logs for requests

**Wrong API URL:**
- Verify `API_URL` in `frontend/js/app.js` matches your Render URL
- Include `/api` at the end
- Use `https://` not `http://`

### Backend goes to sleep

**This is normal on free tier.**

Solutions:
- Use an uptime monitor (see above)
- Upgrade to paid tier on Render ($7/month)
- Accept the 30-60 second wake-up time on first request

### Build succeeds but site doesn't load

**Check Netlify deploy logs:**
- Verify all files were uploaded
- Check browser console for errors

**Common issues:**
- Paths are case-sensitive in production (Windows is case-insensitive)
- Missing files (ensure all were pushed to GitHub)

## Security Best Practices

### Environment Variables

**Never commit `.env` file to GitHub.**

Your `.gitignore` should include:
```
.env
node_modules/
```

**Store secrets safely:**
- Use Render's environment variables UI
- Don't hard code API keys in scripts

### API Keys

If using live mode:
- Keep `RAPIDAPI_KEY` in Render environment variables only
- Rotate keys if exposed
- Monitor usage in RapidAPI dashboard

## Monitoring Your App

### Render Monitoring

- Check deployment status in dashboard
- View real-time logs
- Set up alert emails

### Netlify Analytics (Optional Paid Feature)

- Track page views
- Monitor performance
- See visitor locations

### Free Alternatives

- **Google Analytics** - add to `index.html`
- **Plausible** - privacy-friendly alternative
- **Cloudflare Analytics** - if using Cloudflare

---

## Deployment Checklist

### Backend
- [ ] Code pushed to GitHub
- [ ] Render account created
- [ ] Web service created and configured
- [ ] Environment variables set
- [ ] Deployment successful
- [ ] `/api/health` endpoint returns 200 OK
- [ ] Backend URL saved for frontend

### Frontend
- [ ] `API_URL` updated to production backend
- [ ] Code pushed to GitHub (if using GitHub deploy)
- [ ] Netlify account created
- [ ] Site deployed
- [ ] Custom domain configured (optional)
- [ ] App loads and functions correctly
- [ ] Search returns results
- [ ] CSV export works

### Optional
- [ ] Uptime monitor configured
- [ ] Analytics added
- [ ] Custom domain purchased and connected
- [ ] GitHub repository README updated with live URL

---

**Congratulations! Your Instagram Influencer Finder is now live and accessible to everyone!** 🎉

Share your deployed URL with others and start discovering influencers!
