/**
 * Engagement Rate Calculator
 * Calculates engagement metrics for Instagram influencers
 */

/**
 * Calculate engagement rate for an influencer
 * Formula: (average_likes + average_comments) / followers * 100
 * 
 * @param {Object} influencer - Influencer data with recent_posts and followers
 * @returns {Object} Engagement metrics
 */
function calculateEngagementRate(influencer) {
    if (!influencer.recent_posts || influencer.recent_posts.length === 0) {
        return {
            engagement_rate: 0,
            avg_likes: 0,
            avg_comments: 0,
            posts_analyzed: 0
        };
    }

    const posts = influencer.recent_posts;
    const totalLikes = posts.reduce((sum, post) => sum + (post.likes || 0), 0);
    const totalComments = posts.reduce((sum, post) => sum + (post.comments || 0), 0);

    const avgLikes = totalLikes / posts.length;
    const avgComments = totalComments / posts.length;

    // Engagement rate formula
    const engagementRate = ((avgLikes + avgComments) / influencer.followers) * 100;

    return {
        engagement_rate: parseFloat(engagementRate.toFixed(2)),
        avg_likes: Math.round(avgLikes),
        avg_comments: Math.round(avgComments),
        posts_analyzed: posts.length
    };
}

/**
 * Add engagement metrics to influencer object
 * @param {Object} influencer - Influencer data
 * @returns {Object} Influencer with engagement metrics
 */
function enrichWithEngagement(influencer) {
    const engagement = calculateEngagementRate(influencer);

    return {
        ...influencer,
        ...engagement
    };
}

/**
 * Sort influencers by engagement rate or followers
 * @param {Array} influencers - Array of influencers
 * @param {String} sortBy - 'engagement' or 'followers'
 * @param {String} order - 'asc' or 'desc'
 * @returns {Array} Sorted influencers
 */
function sortInfluencers(influencers, sortBy = 'engagement_rate', order = 'desc') {
    const sorted = [...influencers].sort((a, b) => {
        const aValue = a[sortBy] || 0;
        const bValue = b[sortBy] || 0;

        return order === 'asc' ? aValue - bValue : bValue - aValue;
    });

    return sorted;
}

module.exports = {
    calculateEngagementRate,
    enrichWithEngagement,
    sortInfluencers
};
