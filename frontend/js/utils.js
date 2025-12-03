/**
 * Utility Functions
 * Helper functions for formatting, validation, and CSV generation
 */

/**
 * Format number with commas (e.g., 1000 -> 1,000)
 * @param {number} num - Number to format
 * @returns {string} Formatted number
 */
function formatNumber(num) {
    return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',');
}

/**
 * Format engagement rate as percentage
 * @param {number} rate - Engagement rate
 * @returns {string} Formatted percentage
 */
function formatPercentage(rate) {
    return `${rate.toFixed(2)}%`;
}

/**
 * Validate filter form data
 * @param {Object} filters - Filter object
 * @returns {Object} { valid: boolean, errors: array }
 */
function validateFilters(filters) {
    const errors = [];

    if (!filters.industry || filters.industry.trim() === '') {
        errors.push('Industry/niche is required');
    }

    if (!filters.country || filters.country.trim() === '') {
        errors.push('Country is required');
    }

    const minFollowers = parseInt(filters.min_followers);
    const maxFollowers = parseInt(filters.max_followers);

    if (isNaN(minFollowers) || minFollowers < 0) {
        errors.push('Min followers must be a valid positive number');
    }

    if (isNaN(maxFollowers) || maxFollowers < 0) {
        errors.push('Max followers must be a valid positive number');
    }

    if (minFollowers > maxFollowers) {
        errors.push('Min followers cannot be greater than max followers');
    }

    return {
        valid: errors.length === 0,
        errors
    };
}

/**
 * Convert array of objects to CSV string
 * @param {Array} data - Array of influencer objects
 * @returns {string} CSV string
 */
function convertToCSV(data) {
    if (!data || data.length === 0) {
        return '';
    }

    // Define CSV headers
    const headers = [
        'Username',
        'Full Name',
        'Followers',
        'Engagement Rate (%)',
        'Avg Likes',
        'Avg Comments',
        'Country',
        'Category',
        'Instagram URL',
        'Bio'
    ];

    // Create CSV rows
    const rows = data.map(influencer => {
        return [
            influencer.username || '',
            influencer.full_name || '',
            influencer.followers || 0,
            influencer.engagement_rate || 0,
            influencer.avg_likes || 0,
            influencer.avg_comments || 0,
            influencer.country || '',
            influencer.category || '',
            `https://instagram.com/${influencer.username}`,
            (influencer.biography || '').replace(/"/g, '""') // Escape quotes
        ];
    });

    // Combine headers and rows
    const csvContent = [
        headers.map(h => `"${h}"`).join(','),
        ...rows.map(row => row.map(cell => `"${cell}"`).join(','))
    ].join('\n');

    return csvContent;
}

/**
 * Download CSV file
 * @param {string} csvContent - CSV string
 * @param {string} filename - File name
 */
function downloadCSV(csvContent, filename = 'influencers.csv') {
    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    const link = document.createElement('a');

    if (navigator.msSaveBlob) { // IE 10+
        navigator.msSaveBlob(blob, filename);
    } else {
        const url = URL.createObjectURL(blob);
        link.href = url;
        link.download = filename;
        link.style.display = 'none';
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        URL.revokeObjectURL(url);
    }
}

/**
 * Debounce function to limit function calls
 * @param {Function} func - Function to debounce
 * @param {number} wait - Wait time in ms
 * @returns {Function} Debounced function
 */
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

/**
 * Show notification toast (optional enhancement)
 * @param {string} message - Message to show
 * @param {string} type - 'success' | 'error' | 'info'
 */
function showNotification(message, type = 'info') {
    console.log(`[${type.toUpperCase()}] ${message}`);
    // Could be enhanced with a toast notification library
}
