/**
 * Instagram Service
 * Handles Instagram API integration (RapidAPI) and data fetching
 */

const axios = require('axios');

/**
 * Search Instagram profiles using RapidAPI
 * This is a placeholder for actual RapidAPI integration
 * Different APIs have different endpoints and structures
 * 
 * @param {Object} filters - Search filters
 * @param {String} apiKey - RapidAPI key
 * @param {String} apiHost - RapidAPI host
 * @returns {Promise<Array>} Array of influencer profiles
 */
async function searchInfluencers(filters, apiKey, apiHost) {
    try {
        console.log(`Attempting to search Instagram with API host: ${apiHost}`);

        // IMPORTANT: Most free Instagram APIs on RapidAPI don't support direct search
        // They typically only support username lookup
        // This is a limitation of Instagram's policies

        // For demonstration, we'll try a few common endpoints
        // In production, you would need to:
        // 1. Use Instagram Graph API (requires business account)
        // 2. Use a paid RapidAPI service with search capabilities
        // 3. Or stick with demo mode

        // Try to search by hashtag (if the API supports it)
        const hashtags = generateHashtagsFromIndustry(filters.industry);
        const results = [];

        // Attempt different endpoint patterns based on common RapidAPI Instagram APIs
        const endpointPatterns = [
            `/hashtag/${hashtags[0]}`,
            `/tag/${hashtags[0]}`,
            `/search?query=${hashtags[0]}`,
            `/v1/hashtag/${hashtags[0]}/posts`
        ];

        let lastError = null;

        for (const endpoint of endpointPatterns) {
            try {
                console.log(`Trying endpoint: https://${apiHost}${endpoint}`);

                const response = await axios.get(
                    `https://${apiHost}${endpoint}`,
                    {
                        headers: {
                            'X-RapidAPI-Key': apiKey,
                            'X-RapidAPI-Host': apiHost
                        },
                        timeout: 10000
                    }
                );

                console.log('API Response received:', response.status);

                // Check if we got valid data
                if (response.data) {
                    // Different APIs return data in different formats
                    const users = response.data.users ||
                        response.data.data ||
                        response.data.items ||
                        (Array.isArray(response.data) ? response.data : null);

                    if (users && users.length > 0) {
                        console.log(`Found ${users.length} results from API`);
                        results.push(...users);
                        break; // Success! Stop trying other endpoints
                    }
                }
            } catch (err) {
                lastError = err;
                console.log(`Endpoint ${endpoint} failed: ${err.message}`);
                continue; // Try next endpoint
            }
        }

        if (results.length === 0) {
            console.warn('⚠️  No results from any API endpoint');
            console.warn('⚠️  This is likely because:');
            console.warn('    1. The API doesn\'t support hashtag/search endpoints');
            console.warn('    2. The API requires different parameters');
            console.warn('    3. You\'ve exceeded your API quota');
            console.warn('    4. The API key is invalid');
            console.warn('');
            console.warn('💡 Recommendation: Switch to MODE=demo in .env file');
            console.warn('   Demo mode works perfectly without any API limitations!');

            throw new Error('API search not supported. Please use demo mode or upgrade to a paid API with search capabilities.');
        }

        // Filter results based on criteria
        const filtered = filterAPIResults(results, filters);

        return filtered;

    } catch (error) {
        console.error('RapidAPI Error:', error.message);
        throw error; // Propagate error so server can inform user
    }
}

/**
 * Fetch user profile details from Instagram API
 * @param {String} username - Instagram username
 * @param {String} apiKey - RapidAPI key
 * @param {String} apiHost - RapidAPI host
 * @returns {Promise<Object>} User profile data
 */
async function getUserProfile(username, apiKey, apiHost) {
    try {
        const response = await axios.get(
            `https://${apiHost}/profile/${username}`,
            {
                headers: {
                    'X-RapidAPI-Key': apiKey,
                    'X-RapidAPI-Host': apiHost
                },
                timeout: 10000
            }
        );

        return normalizeProfileData(response.data);

    } catch (error) {
        console.error(`Error fetching profile ${username}:`, error.message);
        return null;
    }
}

/**
 * Fetch recent posts for engagement calculation
 * @param {String} username - Instagram username
 * @param {String} apiKey - RapidAPI key
 * @param {String} apiHost - RapidAPI host
 * @returns {Promise<Array>} Recent posts
 */
async function getRecentPosts(username, apiKey, apiHost) {
    try {
        const response = await axios.get(
            `https://${apiHost}/posts/${username}`,
            {
                headers: {
                    'X-RapidAPI-Key': apiKey,
                    'X-RapidAPI-Host': apiHost
                },
                params: {
                    count: 12 // Get last 12 posts
                },
                timeout: 10000
            }
        );

        return normalizePosts(response.data);

    } catch (error) {
        console.error(`Error fetching posts for ${username}:`, error.message);
        return [];
    }
}

/**
 * Generate relevant hashtags based on industry/niche
 * @param {String} industry - Industry keyword
 * @returns {Array} Array of hashtags
 */
function generateHashtagsFromIndustry(industry) {
    const hashtagMap = {
        'fitness': ['fitness', 'fitnessmodel', 'fitnessmotivation', 'gym', 'workout'],
        'beauty': ['beauty', 'makeup', 'skincare', 'beautyblogger', 'makeuptutorial'],
        'fashion': ['fashion', 'style', 'fashionblogger', 'ootd', 'fashionista'],
        'food': ['food', 'foodie', 'foodblogger', 'cooking', 'recipes'],
        'travel': ['travel', 'wanderlust', 'travelphotography', 'adventure', 'explore'],
        'lifestyle': ['lifestyle', 'lifestyleblogger', 'dailylife', 'inspo'],
        'technology': ['tech', 'technology', 'gadgets', 'techreview', 'innovation'],
        'sports': ['sports', 'athlete', 'sportsnews', 'fitness', 'training']
    };

    const lowerIndustry = industry ? industry.toLowerCase() : '';

    // Find matching industry or use the keyword itself
    for (const [key, tags] of Object.entries(hashtagMap)) {
        if (lowerIndustry.includes(key)) {
            return tags;
        }
    }

    // If no match, return the industry keyword itself
    return [lowerIndustry.replace(/\s+/g, '')];
}

/**
 * Filter API results based on criteria
 * @param {Array} results - Raw API results
 * @param {Object} filters - Filter criteria
 * @returns {Array} Filtered results
 */
function filterAPIResults(results, filters) {
    let filtered = [...results];

    // Filter by follower range
    if (filters.min_followers) {
        filtered = filtered.filter(user =>
            (user.followers || user.follower_count || 0) >= parseInt(filters.min_followers)
        );
    }

    if (filters.max_followers) {
        filtered = filtered.filter(user =>
            (user.followers || user.follower_count || 0) <= parseInt(filters.max_followers)
        );
    }

    // Filter by country (if available in bio or location)
    if (filters.country) {
        filtered = filtered.filter(user => {
            const bio = (user.biography || user.bio || '').toLowerCase();
            const location = (user.location || '').toLowerCase();
            const country = filters.country.toLowerCase();

            return bio.includes(country) || location.includes(country);
        });
    }

    // Gender filter would require name-based inference
    if (filters.gender && filters.gender !== 'both') {
        filtered = filtered.filter(user => {
            const inferredGender = inferGenderFromName(user.full_name || user.name || '');
            return inferredGender === filters.gender.toLowerCase();
        });
    }

    return filtered;
}

/**
 * Normalize profile data from different API formats
 * @param {Object} rawData - Raw API response
 * @returns {Object} Normalized profile data
 */
function normalizeProfileData(rawData) {
    return {
        id: rawData.id || rawData.user_id || '',
        username: rawData.username || rawData.handle || '',
        full_name: rawData.full_name || rawData.name || '',
        profile_pic_url: rawData.profile_pic_url || rawData.avatar || '',
        biography: rawData.biography || rawData.bio || '',
        followers: rawData.followers || rawData.follower_count || 0,
        following: rawData.following || rawData.following_count || 0,
        posts_count: rawData.posts_count || rawData.media_count || 0,
        is_verified: rawData.is_verified || false,
        country: extractCountryFromBio(rawData.biography || rawData.bio || ''),
        category: rawData.category || 'general'
    };
}

/**
 * Normalize posts data
 * @param {Array} rawPosts - Raw posts from API
 * @returns {Array} Normalized posts
 */
function normalizePosts(rawPosts) {
    if (!Array.isArray(rawPosts)) {
        return [];
    }

    return rawPosts.map(post => ({
        likes: post.likes || post.like_count || 0,
        comments: post.comments || post.comment_count || 0
    }));
}

/**
 * Infer gender from name (simple heuristic)
 * Note: This is not 100% accurate and should be used with caution
 * @param {String} name - Full name
 * @returns {String} 'male', 'female', or 'unknown'
 */
function inferGenderFromName(name) {
    const femaleNames = ['sarah', 'emma', 'jessica', 'amanda', 'lisa', 'nicole', 'rachel', 'sophia', 'emily', 'olivia', 'ava', 'isabella', 'mia', 'charlotte', 'amelia'];
    const maleNames = ['michael', 'david', 'james', 'chris', 'christopher', 'kevin', 'ryan', 'alex', 'alexander', 'john', 'robert', 'william', 'daniel', 'matthew', 'joseph'];

    const lowerName = name.toLowerCase();

    for (const femaleName of femaleNames) {
        if (lowerName.includes(femaleName)) {
            return 'female';
        }
    }

    for (const maleName of maleNames) {
        if (lowerName.includes(maleName)) {
            return 'male';
        }
    }

    return 'unknown';
}

/**
 * Extract country from bio text
 * @param {String} bio - Biography text
 * @returns {String} Country name or 'Unknown'
 */
function extractCountryFromBio(bio) {
    const countries = ['United States', 'Canada', 'United Kingdom', 'Australia', 'India', 'Germany', 'France', 'Spain', 'Italy', 'Brazil'];
    const cities = {
        'LA': 'United States',
        'NYC': 'United States',
        'New York': 'United States',
        'Los Angeles': 'United States',
        'Toronto': 'Canada',
        'London': 'United Kingdom',
        'Paris': 'France',
        'Berlin': 'Germany'
    };

    const lowerBio = bio.toLowerCase();

    // Check for country names
    for (const country of countries) {
        if (lowerBio.includes(country.toLowerCase())) {
            return country;
        }
    }

    // Check for city names
    for (const [city, country] of Object.entries(cities)) {
        if (lowerBio.includes(city.toLowerCase())) {
            return country;
        }
    }

    return 'Unknown';
}

module.exports = {
    searchInfluencers,
    getUserProfile,
    getRecentPosts,
    generateHashtagsFromIndustry,
    inferGenderFromName,
    extractCountryFromBio
};
