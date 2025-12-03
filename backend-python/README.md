# Python Backend for Instagram Influencer Finder

This is a **Python + Selenium** backend that scrapes Instagram data in real-time.

## ⚠️ IMPORTANT WARNINGS

> **This backend uses web scraping which:**
> - ❌ Violates Instagram's Terms of Service
> - ❌ May result in permanent account bans
> - ❌ Requires significant delays (very slow)
> - ❌ Has no guarantee of working
> - ❌ May have legal implications

**Use at your own risk!**

## 📋 Prerequisites

- Python 3.8 or higher
- Chrome browser installed
- Instagram account (use a dedicated account, NOT your personal one)
- (Recommended) Rotating proxy service

## 🚀 Setup

### 1. Install Python Dependencies

```bash
cd backend-python
pip install -r requirements.txt
```

### 2. Configure Environment

Copy `.env.example` to `.env`:

```bash
copy .env.example .env
```

Edit `.env` and add your Instagram credentials:

```env
INSTAGRAM_USERNAME=your_test_account
INSTAGRAM_PASSWORD=your_password
```

**CRITICAL:** Use a throwaway Instagram account that you don't mind getting banned!

### 3. (Optional but Recommended) Configure Proxy

To reduce ban risk, use a rotating proxy service:

- [Bright Data](https://brightdata.com/) - $20-50/month
- [Smartproxy](https://smartproxy.com/) - $20-40/month
- [Oxylabs](https://oxylabs.io/) - $30-60/month

Add proxy to `.env`:

```env
PROXY_URL=http://username:password@proxy-host:port
```

## 🎯 Running the Server

```bash
python server.py
```

The server will start on `http://localhost:5000`

## 🔌 Connecting to Frontend

Update the frontend API URL to point to the Python backend:

1. Open `frontend/js/app.js`
2. Change line 7:
   ```javascript
   const API_URL = 'http://localhost:5000/api';
   ```

## 📊 How It Works

1. **Login**: Scraper logs into Instagram using your credentials
2. **Search**: Navigates to hashtag pages based on industry filter
3. **Extract**: Clicks on posts and extracts profile information
4. **Calculate**: Computes engagement rates from recent posts
5. **Filter**: Applies your filters (followers, country, etc.)
6. **Return**: Sends data back to frontend

## ⏱️ Performance

- **Search time**: 2-5 minutes per search
- **Results**: 10-15 profiles per search (limited to avoid bans)
- **Rate limit**: 30 seconds minimum between searches
- **Success rate**: 40-60% (may fail due to Instagram blocking)

## 🛡️ Anti-Detection Measures

The scraper includes:

- ✅ `undetected-chromedriver` to bypass bot detection
- ✅ Random delays (2-8 seconds) between actions
- ✅ Human-like scrolling behavior
- ✅ Random user agents
- ✅ Proxy support for IP rotation
- ✅ Session reuse to avoid repeated logins

## 🐛 Troubleshooting

**Login fails:**
- Check Instagram credentials in `.env`
- Try logging in manually first to verify account works
- Instagram may require 2FA verification

**Getting blocked/banned:**
- Use a proxy service
- Increase delays in `.env` (DELAY_MIN_SECONDS, DELAY_MAX_SECONDS)
- Reduce MAX_PROFILES_PER_SEARCH
- Wait longer between searches

**No results found:**
- Instagram may be blocking the scraper
- Try a different hashtag
- Check if your account is shadowbanned
- Consider switching back to demo mode

**Browser doesn't start:**
- Make sure Chrome is installed
- Try setting `HEADLESS=false` in `.env` to see what's happening
- Check Chrome version compatibility

## 🔄 Switching Back to Demo Mode

If scraping doesn't work or you get banned:

1. Stop the Python server
2. Start the Node.js backend:
   ```bash
   cd ../backend
   node server.js
   ```
3. Update frontend API URL back to `http://localhost:3000/api`

Demo mode works perfectly with zero risk!

## 📝 API Endpoints

Same as Node.js backend:

- `GET /api/health` - Health check
- `POST /api/search` - Search influencers
- `POST /api/engagement` - Get engagement rate for username

## ⚖️ Legal Notice

This tool is for educational purposes only. Web scraping Instagram violates their Terms of Service. The developers are not responsible for any account bans, legal issues, or other consequences resulting from using this tool.

**Recommended:** Use demo mode or official Instagram Graph API instead.
