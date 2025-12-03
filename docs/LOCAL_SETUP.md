# Local Setup Guide

This guide will walk you through setting up the Instagram Influencer Finder on your local machine for development.

## Prerequisites

Before you begin, ensure you have the following installed:

- **Node.js** (version 14 or higher)
  - Download from [nodejs.org](https://nodejs.org/)
  - Verify installation: `node --version`
  - Should also install npm: `npm --version`

- **Modern Web Browser**
  - Chrome, Firefox, Edge, or Safari

- **Text Editor** (optional but recommended)
  - VS Code, Sublime Text, or your preferred editor

## Step-by-Step Setup

### 1. Download the Project

Extract the project files to a location on your computer, for example:
```
C:\Users\YourName\Projects\instagram-influencer-finder\
```

Your folder structure should look like:
```
instagram-influencer-finder/
├── backend/
│   ├── data/
│   ├── services/
│   ├── package.json
│   ├── server.js
│   └── .env.example
├── frontend/
│   ├── css/
│   ├── js/
│   └── index.html
├── docs/
└── README.md
```

### 2. Set Up the Backend

#### 2.1 Navigate to the backend folder

```bash
cd backend
```

#### 2.2 Install Node.js dependencies

```bash
npm install
```

This will install:
- express
- axios
- cors
- dotenv
- express-rate-limit

You should see a `node_modules` folder created.

#### 2.3 Configure environment variables (Optional for demo mode)

For **demo mode** (using mock data), no configuration needed! The server runs out-of-the-box.

For **live mode** (RapidAPI), see [API_SETUP.md](API_SETUP.md).

#### 2.4 Start the backend server

```bash
node server.js
```

You should see output like:
```
============================================================
Instagram Influencer Finder - Backend Server
============================================================
Server running on port 3000
Mode: DEMO
API URL: http://localhost:3000

⚠️  Running in DEMO mode with mock data
   To use real Instagram data:
   1. Get a free RapidAPI key from https://rapidapi.com
   2. Set RAPIDAPI_KEY and RAPIDAPI_HOST in .env file
   3. Change MODE=live in .env file

Endpoints:
  GET  /api/health  - Health check
  POST /api/search  - Search influencers
  POST /api/engagement - Get engagement rate
============================================================
```

**Keep this terminal window open**. The server needs to stay running.

### 3. Set Up the Frontend

#### 3.1 Open a new terminal/command prompt

Keep the backend terminal running, and open a new one.

#### 3.2 Navigate to the frontend folder

```bash
cd frontend
```

#### 3.3 Option A: Open directly in browser (Simplest)

Simply locate the `index.html` file in your file explorer and double-click it.

The app should open in your default browser at a file URL like:
```
file:///C:/Users/YourName/Projects/instagram-influencer-finder/frontend/index.html
```

#### 3.4 Option B: Use a local web server (Recommended)

**Using Python (if installed):**

```bash
# Python 3
python -m http.server 8000

# Python 2
python -m SimpleHTTPServer 8000
```

Then visit: `http://localhost:8000`

**Using Node.js http-server:**

```bash
# Install globally (once)
npm install -g http-server

# Run in frontend folder
http-server -p 8000
```

Then visit: `http://localhost:8000`

**Using VS Code Live Server extension:**

1. Install "Live Server" extension in VS Code
2. Right-click `index.html`
3. Select "Open with Live Server"

### 4. Test the Application

#### 4.1 Verify backend is running

Open `http://localhost:3000/api/health` in your browser.

You should see JSON response:
```json
{
  "status": "OK",
  "mode": "demo",
  "timestamp": "2024-12-03T...",
  "message": "Running in DEMO mode with mock data"
}
```

#### 4.2 Test the frontend

1. Open the frontend (e.g., `http://localhost:8000` or `file:///...index.html`)
2. You should see the **Welcome Screen** with the app logo
3. Click "Start Filtering"
4. Fill in the filter form:
   - Gender: **Female**
   - Country: **United States**
   - Industry: **fitness**
   - Min Followers: **1000**
   - Max Followers: **5000**
5. Click "Find Influencers"
6. You should see results with mock influencer data!

#### 4.3 Test CSV export

1. On the results page, check the "Shortlist" checkbox on 2-3 influencers
2. Click "Export Shortlisted" button
3. A CSV file should download to your Downloads folder

## Troubleshooting

### Backend Issues

**Error: "Cannot find module 'express'"**
- Solution: Run `npm install` in the backend folder

**Error: "Port 3000 is already in use"**
- Solution: Kill the process using port 3000 or change the PORT in `.env`
- Windows: `netstat -ano | findstr :3000` then `taskkill /PID <PID> /F`
- Mac/Linux: `lsof -i :3000` then `kill -9 <PID>`
- Or change port: Create `.env` file with `PORT=3001`

**Error: "node: command not found"**
- Solution: Node.js is not installed or not in PATH
- Reinstall Node.js from [nodejs.org](https://nodejs.org/)

### Frontend Issues

**Blank white screen**
- Check browser console (F12) for errors
- Ensure all JavaScript files exist in `js/` folder

**"Failed to fetch" or CORS errors**
- Ensure backend is running on `http://localhost:3000`
- Check that `API_URL` in `frontend/js/app.js` is correct
- Try using a local web server instead of `file://` protocol

**No results showing**
- Open browser console (F12) and check for errors
- Verify backend is responding: visit `http://localhost:3000/api/health`
- Try broader filters (larger follower range, generic industry like "fitness")

### General Tips

- **Always keep the backend server running** while testing the frontend
- **Check the browser console** (F12) for JavaScript errors
- **Check the backend terminal** for API errors and logs
- **Clear browser cache** if styles aren't updating (Ctrl+F5 or Cmd+Shift+R)

## Next Steps

- **Try live mode**: See [API_SETUP.md](API_SETUP.md) to configure RapidAPI
- **Deploy the app**: See [DEPLOYMENT.md](DEPLOYMENT.md) for free hosting options
- **Customize the app**: Edit the code to add your own features!

## Development Tips

### Auto-restart backend on changes

Install nodemon globally:
```bash
npm install -g nodemon
```

Then run:
```bash
nodemon server.js
```

The server will automatically restart when you edit files.

### Frontend development

For frontend development, using a local web server with live reload is recommended:

**VS Code Live Server**: Automatically refreshes on file changes

**Browser DevTools**: Use F12 to inspect and debug

### File watching

To watch for changes across the entire project, you can use tools like:
- **Browsersync**
- **Live Server** (VS Code extension)

## Project Structure

```
backend/
├── data/
│   └── mockData.js          # Sample influencer data
├── services/
│   ├── engagementCalculator.js   # Engagement rate logic
│   └── instagramService.js       # API integration
├── package.json             # Dependencies
├── server.js                # Main Express app
├── .env.example             # Environment template
└── .env                     # Your config (create this)

frontend/
├── css/
│   └── styles.css           # All styles
├── js/
│   ├── app.js               # Main app logic
│   ├── components.js        # UI components
│   └── utils.js             # Helper functions
└── index.html               # Main HTML file
```

## Environment Variables

Create a `.env` file in the `backend/` folder for customization:

```env
# Server port
PORT=3000

# Mode: 'demo' or 'live'
MODE=demo

# RapidAPI credentials (for live mode)
RAPIDAPI_KEY=your_key_here
RAPIDAPI_HOST=api-host-here

# Rate limiting
RATE_LIMIT_MAX=100
RATE_LIMIT_WINDOW_MS=900000
```

Changes to `.env` require restarting the server.

---

**You're all set!** 🎉 Enjoy discovering influencers!
