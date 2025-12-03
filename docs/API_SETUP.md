# API Setup Guide - RapidAPI Configuration

This guide explains how to set up RapidAPI to use **live Instagram data** instead of demo mode.

> **Note:** The app works perfectly in demo mode with no API setup required! Only follow this guide if you want real Instagram data.

## Why RapidAPI?

Instagram's official Graph API does not support searching all users by filters. RapidAPI provides access to third-party Instagram data providers that offer search capabilities compliant with Instagram's terms.

## Step 1: Create a RapidAPI Account

1. **Go to [RapidAPI.com](https://rapidapi.com)**

2. **Click "Sign Up" (top right)**
   - Sign up with email or Google account
   - **No credit card required** for free tier

3. **Verify your email address**

4. **You're now registered!**

## Step 2: Find an Instagram API

1. **In the RapidAPI Hub, search for "Instagram"**
   - Use the search bar at the top

2. **Choose an API** that offers user/profile search

   Recommended options (check current availability):
   
   - **Instagram Bulk Profile Scrapper**
     - Good for profile data and posts
     - Free tier: varies by API
   
   - **Instagram API**
     - Various providers offer different endpoints
     - Check pricing and free tier limits
   
   - **Social Media API**
     - May include Instagram among other platforms

3. **Click on the API** to view details

## Step 3: Subscribe to Free Tier

1. **On the API page, click "Pricing"**

2. **Select the FREE plan**
   - Look for "Basic," "Free," or "Freemium" tier
   - Check the quota (e.g., 100-500 requests/month)

3. **Click "Subscribe"**
   - You may need to add a card for verification, but won't be charged
   - Or select "Subscribe without card" if available

4. **Confirm subscription**

## Step 4: Get Your API Credentials

1. **After subscribing, go to the API's main page**

2. **Click "Endpoints" tab**

3. **Look for the sidebar showing:**
   ```
   X-RapidAPI-Key: xxxxxxxxxxxxxxxxxxxxxxxxxx
   X-RapidAPI-Host: api-name.p.rapidapi.com
   ```

4. **Copy these values** - you'll need them next

## Step 5: Configure the Backend

1. **Navigate to the `backend/` folder**

2. **Create a `.env` file** (copy from `.env.example`)
   ```bash
   cp .env.example .env
   ```

3. **Edit `.env` file** with your text editor:
   ```env
   # Server Configuration
   PORT=3000

   # API Mode: 'demo' or 'live'
   MODE=live

   # RapidAPI Configuration
   RAPIDAPI_KEY=your_actual_key_here_replace_this
   RAPIDAPI_HOST=instagram-bulk-profile-scrapper.p.rapidapi.com

   # Rate Limiting
   RATE_LIMIT_MAX=100
   RATE_LIMIT_WINDOW_MS=900000
   ```

4. **Replace the placeholder values:**
   - `RAPIDAPI_KEY`: Paste your actual API key
   - `RAPIDAPI_HOST`: Paste the API host (without `https://`)
   - `MODE`: Change from `demo` to `live`

5. **Save the file**

## Step 6: Restart the Backend Server

1. **Stop the current server** (if running)
   - Press `Ctrl+C` in the terminal

2. **Start the server again:**
   ```bash
   node server.js
   ```

3. **You should see:**
   ```
   ============================================================
   Instagram Influencer Finder - Backend Server
   ============================================================
   Server running on port 3000
   Mode: LIVE
   ...
   ✓ Running in LIVE mode with RapidAPI
     API Host: instagram-bulk-profile-scrapper.p.rapidapi.com
   ============================================================
   ```

## Step 7: Test Live Mode

1. **Open the frontend** (`http://localhost:8000` or `index.html`)

2. **Fill in the filter form** and search

3. **Check the results:**
   - Look for "🔴 Live Mode" badge in results
   - Data should come from real Instagram (subject to API availability)

4. **Check backend terminal:**
   - You should see API calls being made
   - Watch for any error messages

## Understanding Free Tier Limits

### Typical Free Tier Quotas

Most Instagram APIs on RapidAPI offer:
- **100-500 requests per month**
- **5-10 requests per second** rate limit
- **Basic endpoints** (profile, posts, hashtags)

### Managing Your Quota

**Track usage:**
1. Go to [RapidAPI Dashboard](https://rapidapi.com/developer/billing)
2. Check "API Usage" section
3. Monitor remaining quota

**Optimize requests:**
- Use filters wisely to reduce API calls
- Cache results when possible
- Don't make unnecessary duplicate searches

**When you hit the limit:**
- Wait for monthly reset
- Upgrade to paid tier (optional)
- Switch back to demo mode temporarily

## Troubleshooting

### Error: "RapidAPI credentials not configured"

**Cause:** `.env` file missing or incorrect

**Solution:**
1. Ensure `.env` file exists in `backend/` folder
2. Check that `RAPIDAPI_KEY` and `RAPIDAPI_HOST` are set
3. Verify no extra spaces or quotes around values

### Error: "Failed to fetch data from Instagram API"

**Cause:** Invalid API key or exceeded quota

**Solution:**
1. **Verify API key is correct** - copy again from RapidAPI
2. **Check subscription status** - ensure you're subscribed
3. **Check quota** - you may have hit the free tier limit
4. **Try a different API** - some RapidAPI providers may be down

### Error: "Forbidden" or "401 Unauthorized"

**Cause:** API key invalid or expired

**Solution:**
1. Re-generate API key on RapidAPI
2. Check if subscription is active
3. Ensure you're using the correct API host

### No results returned

**Cause:** API limitations or restrictive filters

**Solution:**
1. **Try broader filters** - larger follower range, common industries
2. **Check API documentation** - some APIs have specific requirements
3. **Review backend logs** - look for API error messages
4. **Test the API directly** on RapidAPI website using their testing tool

### Rate limit errors

**Cause:** Too many requests in short time

**Solution:**
1. Wait a few minutes before trying again
2. Reduce search frequency
3. Check `RATE_LIMIT_MAX` in `.env` (default: 100)

## Important Notes

### API Endpoint Differences

**Different RapidAPI providers have different endpoints!**

The current code template assumes basic endpoints like:
- `/profile/{username}`
- `/posts/{username}`
- `/hashtag/{tag}`

**If your API has different endpoints**, you'll need to modify:
`backend/services/instagramService.js`

Example modifications needed:
```javascript
// Change endpoint URLs to match your API
const response = await axios.get(
  `https://${apiHost}/your-actual-endpoint`, // Update this
  {
    headers: {
      'X-RapidAPI-Key': apiKey,
      'X-RapidAPI-Host': apiHost
    }
  }
);
```

### Data Format Variations

Different APIs return data in different formats. You may need to adjust the normalization functions in `instagramService.js` to match your API's response structure.

### Instagram's Terms of Service

- Only use APIs that comply with Instagram's terms
- Don't exceed rate limits
- Respect user privacy
- Don't scrape or store data long-term without permission

## Alternative: Use Official Instagram Graph API

For production use, consider Instagram's official Graph API:

**Pros:**
- Official and compliant
- No third-party dependency
- More reliable

**Cons:**
- Only works with your own Instagram Business account
- Cannot search arbitrary users
- Requires Facebook App setup
- More complex to configure

**Setup:**
1. Create a Facebook Developer account
2. Create a Facebook App
3. Get Instagram Business account access token
4. Use Business Discovery endpoint (limited to businesses you manage)

## Switching Back to Demo Mode

To go back to demo mode:

1. **Edit `.env` file:**
   ```env
   MODE=demo
   ```

2. **Restart server:**
   ```bash
   node server.js
   ```

That's it! The app will use mock data again.

---

## Summary Checklist

- [ ] Created RapidAPI account
- [ ] Subscribed to free tier of an Instagram API
- [ ] Copied API key and host
- [ ] Created `.env` file in backend folder
- [ ] Set `MODE=live`
- [ ] Added `RAPIDAPI_KEY` and `RAPIDAPI_HOST`
- [ ] Restarted backend server
- [ ] Tested search with live mode enabled
- [ ] Verified "🔴 Live Mode" appears in results

**Need help?** Check the [Limitations](LIMITATIONS.md) document for known constraints.
