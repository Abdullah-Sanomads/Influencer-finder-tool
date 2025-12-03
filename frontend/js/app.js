/**
 * Main Application Logic
 * Handles navigation, API calls, and user interactions
 */

// Configuration
const API_URL = 'http://localhost:5000/api';

// State management
let allInfluencers = [];
let selectedInfluencers = [];

/**
 * Navigate to welcome screen
 */
function navigateToWelcome() {
    hideAllScreens();
    document.getElementById('welcome-screen').classList.add('active');
}

/**
 * Navigate to filter screen
 */
function navigateToFilters() {
    hideAllScreens();
    document.getElementById('filter-screen').classList.add('active');
}

/**
 * Navigate to results screen
 */
function navigateToResults() {
    hideAllScreens();
    document.getElementById('results-screen').classList.add('active');
}

/**
 * Hide all screens
 */
function hideAllScreens() {
    document.querySelectorAll('.screen').forEach(screen => {
        screen.classList.remove('active');
    });
}

/**
 * Handle filter form submission
 */
document.addEventListener('DOMContentLoaded', () => {
    const filterForm = document.getElementById('filter-form');

    if (filterForm) {
        filterForm.addEventListener('submit', async (e) => {
            e.preventDefault();

            // Get form data
            const formData = new FormData(filterForm);
            const filters = {
                gender: formData.get('gender'),
                country: formData.get('country'),
                industry: formData.get('industry'),
                min_followers: formData.get('min_followers'),
                max_followers: formData.get('max_followers'),
                sort_by: 'engagement_rate',
                sort_order: 'desc'
            };

            // Validate filters
            const validation = validateFilters(filters);
            if (!validation.valid) {
                alert('Please check your filters:\n' + validation.errors.join('\n'));
                return;
            }

            // Navigate to results and start search
            navigateToResults();
            await searchInfluencers(filters);
        });
    }
});

/**
 * Search for influencers
 * @param {Object} filters - Filter criteria
 */
async function searchInfluencers(filters) {
    const loadingState = document.getElementById('loading-state');
    const errorState = document.getElementById('error-state');
    const resultsGrid = document.getElementById('results-grid');
    const resultsCount = document.getElementById('results-count');
    const modeBadge = document.getElementById('results-mode');

    // Show loading state
    loadingState.style.display = 'flex';
    errorState.style.display = 'none';
    resultsGrid.style.display = 'none';

    try {
        console.log('Searching with filters:', filters);

        const response = await fetch(`${API_URL}/search`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(filters)
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || 'Failed to search influencers');
        }

        const result = await response.json();
        console.log('Search results:', result);

        // Update state
        allInfluencers = result.data || [];
        selectedInfluencers = [];

        // Update UI
        resultsCount.textContent = allInfluencers.length;
        modeBadge.textContent = result.mode === 'demo' ? '🎮 Demo Mode' : '🔴 Live Mode';

        // Hide loading
        loadingState.style.display = 'none';

        // Show results or empty state
        if (allInfluencers.length === 0) {
            resultsGrid.innerHTML = '';
            resultsGrid.appendChild(createEmptyState());
            resultsGrid.style.display = 'block';
        } else {
            displayInfluencers(allInfluencers);
            resultsGrid.style.display = 'grid';
        }

    } catch (error) {
        console.error('Search error:', error);

        // Show error state
        loadingState.style.display = 'none';
        errorState.style.display = 'flex';
        document.getElementById('error-message').textContent = error.message;
    }
}

/**
 * Display influencers in the grid
 * @param {Array} influencers - Array of influencer objects
 */
function displayInfluencers(influencers) {
    const resultsGrid = document.getElementById('results-grid');
    resultsGrid.innerHTML = '';

    influencers.forEach(influencer => {
        const card = createInfluencerCard(influencer);
        resultsGrid.appendChild(card);
    });

    // Update export button state
    updateExportButton();
}

/**
 * Handle sort button click
 * @param {HTMLElement} button - Sort button element
 */
function handleSort(button) {
    const sortBy = button.dataset.sort;
    const sortOrder = button.dataset.order;

    // Update active state
    document.querySelectorAll('.btn-sort').forEach(btn => {
        btn.classList.remove('active');
    });
    button.classList.add('active');

    // Sort influencers
    const sorted = sortInfluencersClient(allInfluencers, sortBy, sortOrder);
    displayInfluencers(sorted);
}

/**
 * Client-side sort function
 * @param {Array} influencers - Array of influencers
 * @param {String} sortBy - Field to sort by
 * @param {String} order - 'asc' or 'desc'
 * @returns {Array} Sorted array
 */
function sortInfluencersClient(influencers, sortBy, order) {
    const sorted = [...influencers].sort((a, b) => {
        const aValue = a[sortBy] || 0;
        const bValue = b[sortBy] || 0;

        return order === 'asc' ? aValue - bValue : bValue - aValue;
    });

    return sorted;
}

/**
 * Handle influencer selection/deselection
 * @param {HTMLInputElement} checkbox - Checkbox element
 * @param {String} username - Influencer username
 */
function handleInfluencerSelection(checkbox, username) {
    const influencer = allInfluencers.find(inf => inf.username === username);

    if (!influencer) return;

    if (checkbox.checked) {
        // Add to selected list
        if (!selectedInfluencers.find(inf => inf.username === username)) {
            selectedInfluencers.push(influencer);
        }
    } else {
        // Remove from selected list
        selectedInfluencers = selectedInfluencers.filter(inf => inf.username !== username);
    }

    console.log(`Selected ${selectedInfluencers.length} influencers`);
    updateExportButton();
}

/**
 * Update export button state
 */
function updateExportButton() {
    const exportBtn = document.getElementById('export-btn');

    if (selectedInfluencers.length > 0) {
        exportBtn.disabled = false;
        exportBtn.textContent = `Export ${selectedInfluencers.length} Shortlisted`;
        // Re-add icon
        exportBtn.innerHTML = `
      <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
        <path d="M10 12V4M10 12L7 9M10 12L13 9" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        <path d="M4 16H16" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
      </svg>
      Export ${selectedInfluencers.length} Shortlisted
    `;
    } else {
        exportBtn.disabled = true;
        exportBtn.innerHTML = `
      <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
        <path d="M10 12V4M10 12L7 9M10 12L13 9" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        <path d="M4 16H16" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
      </svg>
      Export Shortlisted
    `;
    }
}

/**
 * Export shortlisted influencers as CSV
 */
function exportShortlisted() {
    if (selectedInfluencers.length === 0) {
        alert('Please select at least one influencer to export');
        return;
    }

    const csvContent = convertToCSV(selectedInfluencers);
    const timestamp = new Date().toISOString().split('T')[0];
    const filename = `influencers_shortlist_${timestamp}.csv`;

    downloadCSV(csvContent, filename);
    showNotification(`Exported ${selectedInfluencers.length} influencers to ${filename}`, 'success');
}

/**
 * Check API health on load
 */
async function checkAPIHealth() {
    try {
        const response = await fetch(`${API_URL}/health`);
        const data = await response.json();
        console.log('API Health:', data);
    } catch (error) {
        console.warn('API not available:', error.message);
        console.warn('Make sure the backend server is running on http://localhost:3000');
    }
}

// Check API health when page loads
document.addEventListener('DOMContentLoaded', () => {
    checkAPIHealth();
});
