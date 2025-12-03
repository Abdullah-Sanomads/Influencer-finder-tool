/**
 * UI Components
 * Reusable component generators for the application
 */

/**
 * Create an influencer card element
 * @param {Object} influencer - Influencer data
 * @returns {HTMLElement} Card element
 */
function createInfluencerCard(influencer) {
    const card = document.createElement('div');
    card.className = 'influencer-card';
    card.dataset.influencerId = influencer.id || influencer.username;

    const instagramUrl = `https://instagram.com/${influencer.username}`;

    card.innerHTML = `
    <div class="card-header">
      <img 
        src="${influencer.profile_pic_url || 'https://i.pravatar.cc/150'}" 
        alt="${influencer.full_name}"
        class="profile-pic"
        onerror="this.src='https://i.pravatar.cc/150'"
      >
      <div class="profile-info">
        <div class="profile-name">
          ${influencer.full_name || influencer.username}
          ${influencer.is_verified ? '<span class="verified-badge" title="Verified">✓</span>' : ''}
        </div>
        <a 
          href="${instagramUrl}" 
          target="_blank" 
          rel="noopener noreferrer"
          class="profile-username"
        >
          @${influencer.username}
        </a>
      </div>
    </div>
    
    <div class="card-stats">
      <div class="stat">
        <span class="stat-value">${formatNumber(influencer.followers || 0)}</span>
        <span class="stat-label">Followers</span>
      </div>
      <div class="stat">
        <span class="stat-value">${formatNumber(influencer.posts_count || 0)}</span>
        <span class="stat-label">Posts</span>
      </div>
    </div>
    
    ${influencer.biography ? `
      <div class="card-bio">${influencer.biography}</div>
    ` : ''}
    
    <div class="card-meta">
      ${influencer.country ? `<span class="meta-tag">📍 ${influencer.country}</span>` : ''}
      ${influencer.category ? `<span class="meta-tag">#${influencer.category}</span>` : ''}
      ${influencer.gender ? `<span class="meta-tag">${influencer.gender === 'female' ? '♀️' : influencer.gender === 'male' ? '♂️' : '👤'} ${influencer.gender}</span>` : ''}
    </div>
    
    <div class="engagement-section">
      <span class="engagement-rate">${formatPercentage(influencer.engagement_rate || 0)}</span>
      <span class="engagement-label">Engagement Rate</span>
      <div class="engagement-details">
        <span>❤️ ${formatNumber(influencer.avg_likes || 0)} avg likes</span>
        <span>💬 ${formatNumber(influencer.avg_comments || 0)} avg comments</span>
      </div>
      ${influencer.posts_analyzed ? `
        <div class="engagement-details" style="margin-top: 0.5rem;">
          <span style="font-size: 0.8rem; color: var(--text-muted);">Based on ${influencer.posts_analyzed} recent posts</span>
        </div>
      ` : ''}
    </div>
    
    <div class="card-actions">
      <div class="checkbox-wrapper">
        <input 
          type="checkbox" 
          id="select-${influencer.username}"
          onchange="handleInfluencerSelection(this, '${influencer.username}')"
        >
        <label for="select-${influencer.username}">Shortlist</label>
      </div>
    </div>
  `;

    return card;
}

/**
 * Create loading spinner element
 * @returns {HTMLElement} Loading spinner
 */
function createLoadingSpinner() {
    const container = document.createElement('div');
    container.className = 'loading-state';
    container.innerHTML = `
    <div class="spinner"></div>
    <p>Searching Instagram for influencers...</p>
  `;
    return container;
}

/**
 * Create error message element
 * @param {string} message - Error message
 * @returns {HTMLElement} Error element
 */
function createErrorMessage(message) {
    const container = document.createElement('div');
    container.className = 'error-state';
    container.innerHTML = `
    <div class="error-icon">⚠️</div>
    <h3>Something went wrong</h3>
    <p>${message}</p>
    <button class="btn btn-primary" onclick="navigateToFilters()">Try Again</button>
  `;
    return container;
}

/**
 * Create empty state element
 * @returns {HTMLElement} Empty state element
 */
function createEmptyState() {
    const container = document.createElement('div');
    container.className = 'error-state';
    container.innerHTML = `
    <div class="error-icon">🔍</div>
    <h3>No influencers found</h3>
    <p>Try adjusting your filters to get more results</p>
    <button class="btn btn-primary" onclick="navigateToFilters()">Change Filters</button>
  `;
    return container;
}
