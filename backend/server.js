/**
 * Instagram Influencer Finder - Backend Server
 * Express.js API server for influencer discovery
 */

require('dotenv').config();
const express = require('express');
const cors = require('cors');
const rateLimit = require('express-rate-limit');

const { filterInfluencers } = require('./data/mockData');
const { enrichWithEngagement, sortInfluencers } = require('./services/engagementCalculator');
const instagramService = require('./services/instagramService');

const app = express();
const PORT = process.env.PORT || 3000;
const MODE = process.env.MODE || 'demo';

// Middleware
app.use(cors());
app.use(express.json());

// Rate limiting to protect API
const limiter = rateLimit({
    windowMs: parseInt(process.env.RATE_LIMIT_WINDOW_MS) || 15 * 60 * 1000, // 15 minutes
    max: parseInt(process.env.RATE_LIMIT_MAX) || 100, // Limit each IP to 100 requests per windowMs
    message: 'Too many requests from this IP, please try again later.'
});

app.use('/api/', limiter);

// Logging middleware
app.use((req, res, next) => {
    console.log(`[${new Date().toISOString()}] ${req.method} ${req.path}`);
    next();
});

/**
 * Health check endpoint
 */
app.get('/api/health', (req, res) => {
    res.json({
        status: 'OK',
        mode: MODE,
        timestamp: new Date().toISOString(),
        message: MODE === 'demo'
            ? 'Running in DEMO mode with mock data'
            : 'Running in LIVE mode with RapidAPI'
    });
});

/**
 * Search influencers endpoint
 * POST /api/search
 * Body: {
 *   gender: 'male' | 'female' | 'both',
 *   country: string,
 *   industry: string,
 *   min_followers: number,
 *   max_followers: number,
 *   sort_by: 'engagement_rate' | 'followers',
 *   sort_order: 'asc' | 'desc'
 * }
 */
app.post('/api/search', async (req, res) => {
    try {
        const filters = req.body;

        // Validate required fields
        if (!filters.industry) {
            return res.status(400).json({
                error: 'Industry/niche is required'
            });
        }

        console.log('Search filters received:', filters);

        let influencers = [];

        if (MODE === 'demo') {
            // Use mock data in demo mode
            console.log('Using DEMO mode - returning mock data');
            influencers = filterInfluencers(filters);
        } else {
            // Use RapidAPI in live mode
            console.log('Using LIVE mode - calling RapidAPI');

            const apiKey = process.env.RAPIDAPI_KEY;
            const apiHost = process.env.RAPIDAPI_HOST;

            if (!apiKey || !apiHost) {
                return res.status(500).json({
                    error: 'RapidAPI credentials not configured. Please set RAPIDAPI_KEY and RAPIDAPI_HOST in .env file.'
                });
            }

            try {
                const apiResults = await instagramService.searchInfluencers(filters, apiKey, apiHost);

                // Enrich API results with recent posts data
                const enrichedResults = [];

                for (const profile of apiResults.slice(0, 20)) { // Limit to 20 to avoid rate limits
                    try {
                        const recentPosts = await instagramService.getRecentPosts(profile.username, apiKey, apiHost);
                        enrichedResults.push({
                            ...profile,
                            recent_posts: recentPosts
                        });
                    } catch (error) {
                        console.error(`Error fetching posts for ${profile.username}:`, error.message);
                        // Include profile without posts
                        enrichedResults.push({
                            ...profile,
                            recent_posts: []
                        });
                    }
                }

                influencers = enrichedResults;

            } catch (apiError) {
                console.error('RapidAPI error:', apiError.message);
                return res.status(503).json({
                    error: 'Instagram API search is not available',
                    details: apiError.message,
                    suggestion: 'Most free Instagram APIs don\'t support search functionality. Please switch to demo mode by changing MODE=demo in your .env file, or upgrade to a paid API service.',
                    demoModeInstructions: {
                        step1: 'Open backend/.env file',
                        step2: 'Change MODE=live to MODE=demo',
                        step3: 'Restart the server',
                        step4: 'Demo mode provides realistic mock data without API limitations'
                    }
                });
            }
        }

        // Calculate engagement rates for all influencers
        const enrichedInfluencers = influencers.map(inf => enrichWithEngagement(inf));

        // Sort results
        const sortBy = filters.sort_by || 'engagement_rate';
        const sortOrder = filters.sort_order || 'desc';
        const sortedInfluencers = sortInfluencers(enrichedInfluencers, sortBy, sortOrder);

        console.log(`Returning ${sortedInfluencers.length} influencers`);

        res.json({
            success: true,
            count: sortedInfluencers.length,
            mode: MODE,
            filters: filters,
            data: sortedInfluencers
        });

    } catch (error) {
        console.error('Search error:', error);
        res.status(500).json({
            error: 'An error occurred while searching for influencers',
            details: error.message
        });
    }
});

/**
 * Get engagement rate for a specific username
 * POST /api/engagement
 * Body: { username: string }
 */
app.post('/api/engagement', async (req, res) => {
    try {
        const { username } = req.body;

        if (!username) {
            return res.status(400).json({
                error: 'Username is required'
            });
        }

        if (MODE === 'demo') {
            return res.status(400).json({
                error: 'Engagement lookup by username is not available in demo mode'
            });
        }

        const apiKey = process.env.RAPIDAPI_KEY;
        const apiHost = process.env.RAPIDAPI_HOST;

        // Fetch profile and recent posts
        const profile = await instagramService.getUserProfile(username, apiKey, apiHost);

        if (!profile) {
            return res.status(404).json({
                error: 'User not found'
            });
        }

        const recentPosts = await instagramService.getRecentPosts(username, apiKey, apiHost);

        const influencer = {
            ...profile,
            recent_posts: recentPosts
        };

        const enriched = enrichWithEngagement(influencer);

        res.json({
            success: true,
            data: enriched
        });

    } catch (error) {
        console.error('Engagement calculation error:', error);
        res.status(500).json({
            error: 'Failed to calculate engagement rate',
            details: error.message
        });
    }
});

/**
 * 404 handler
 */
app.use((req, res) => {
    res.status(404).json({
        error: 'Endpoint not found'
    });
});

/**
 * Error handler
 */
app.use((error, req, res, next) => {
    console.error('Server error:', error);
    res.status(500).json({
        error: 'Internal server error',
        details: error.message
    });
});

// Start server
app.listen(PORT, () => {
    console.log('='.repeat(60));
    console.log('Instagram Influencer Finder - Backend Server');
    console.log('='.repeat(60));
    console.log(`Server running on port ${PORT}`);
    console.log(`Mode: ${MODE.toUpperCase()}`);
    console.log(`API URL: http://localhost:${PORT}`);

    if (MODE === 'demo') {
        console.log('\n⚠️  Running in DEMO mode with mock data');
        console.log('   To use real Instagram data:');
        console.log('   1. Get a free RapidAPI key from https://rapidapi.com');
        console.log('   2. Set RAPIDAPI_KEY and RAPIDAPI_HOST in .env file');
        console.log('   3. Change MODE=live in .env file');
    } else {
        console.log('\n✓ Running in LIVE mode with RapidAPI');
        console.log(`  API Host: ${process.env.RAPIDAPI_HOST}`);
    }

    console.log('\nEndpoints:');
    console.log(`  GET  /api/health  - Health check`);
    console.log(`  POST /api/search  - Search influencers`);
    console.log(`  POST /api/engagement - Get engagement rate`);
    console.log('='.repeat(60));
});

module.exports = app;
