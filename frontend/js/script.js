let eventSource = null;
let foundProfiles = [];

function startSearch(event) {
    event.preventDefault();

    // Get form values
    const tags = document.getElementById('tags').value;
    const gender = document.getElementById('gender').value;
    const country = document.getElementById('country').value;
    const minFollowers = document.getElementById('minFollowers').value;
    const maxFollowers = document.getElementById('maxFollowers').value;
    const maxProfiles = document.getElementById('maxProfiles').value;

    // Reset UI
    document.getElementById('resultsGrid').innerHTML = '';
    document.getElementById('resultCount').textContent = '(0)';
    document.getElementById('searchBtn').disabled = true;
    document.getElementById('searchBtn').textContent = 'Searching...';
    document.getElementById('exportBtn').disabled = true;
    foundProfiles = [];

    addLog('Starting search...', 'info');

    // Close existing connection
    if (eventSource) {
        eventSource.close();
    }

    // Construct URL
    const params = new URLSearchParams({
        tags: tags,
        gender: gender,
        country: country,
        min_followers: minFollowers,
        max_followers: maxFollowers,
        max_profiles: maxProfiles
    });

    // Open SSE Connection
    const url = `http://localhost:5000/api/stream?${params.toString()}`;
    eventSource = new EventSource(url);

    eventSource.onmessage = function (event) {
        try {
            const data = JSON.parse(event.data);

            if (data.type === 'log') {
                addLog(data.data, 'info');
            } else if (data.type === 'error') {
                addLog(data.data, 'error');
            } else if (data.type === 'profile') {
                addProfile(data.data);
            } else if (data.type === 'complete') {
                addLog(data.data, 'success');
                stopSearch();
            }
        } catch (e) {
            console.error('Error parsing event:', e);
        }
    };

    eventSource.onerror = function (err) {
        console.error('EventSource failed:', err);
        addLog('Connection lost or search finished.', 'error');
        stopSearch();
    };
}

function stopSearch() {
    if (eventSource) {
        eventSource.close();
        eventSource = null;
    }
    document.getElementById('searchBtn').disabled = false;
    document.getElementById('searchBtn').textContent = 'Start Finding';
    if (foundProfiles.length > 0) {
        document.getElementById('exportBtn').disabled = false;
    }
}

function addLog(message, type) {
    const panel = document.getElementById('logContent');
    const div = document.createElement('div');
    div.className = `log-line log-${type}`;
    div.textContent = `> ${message}`;
    panel.appendChild(div);
    panel.scrollTop = panel.scrollHeight;
}

function addProfile(profile) {
    foundProfiles.push(profile);
    document.getElementById('resultCount').textContent = `(${foundProfiles.length})`;

    const grid = document.getElementById('resultsGrid');
    const card = document.createElement('div');
    card.className = 'profile-card';

    const engagement = profile.engagement_rate ? `${profile.engagement_rate}% ER` : 'N/A';

    card.innerHTML = `
        <div class="profile-header">
            <img src="${profile.profile_pic_url || 'https://via.placeholder.com/50'}" class="profile-pic" onerror="this.src='https://via.placeholder.com/50'">
            <div class="profile-info">
                <h3>@${profile.username}</h3>
                <p>${profile.full_name || ''}</p>
            </div>
        </div>
        
        <div class="profile-stats">
            <div class="stat">
                <span class="stat-value">${formatNumber(profile.followers)}</span>
                <span class="stat-label">Followers</span>
            </div>
            <div class="stat">
                <span class="stat-value">${formatNumber(profile.following)}</span>
                <span class="stat-label">Following</span>
            </div>
            <div class="stat">
                <span class="stat-value">${formatNumber(profile.posts_count)}</span>
                <span class="stat-label">Posts</span>
            </div>
        </div>
        
        <div class="engagement-badge">
            ⚡ ${engagement}
        </div>
        
        <p class="profile-bio">${profile.biography || 'No bio'}</p>
        
        <div class="profile-actions">
            <a href="https://instagram.com/${profile.username}" target="_blank" class="btn-link">Open Profile</a>
        </div>
    `;

    grid.prepend(card);
}

function formatNumber(num) {
    if (num >= 1000000) return (num / 1000000).toFixed(1) + 'M';
    if (num >= 1000) return (num / 1000).toFixed(1) + 'K';
    return num;
}

function clearLogs() {
    document.getElementById('logContent').innerHTML = '';
}

function exportCSV() {
    if (foundProfiles.length === 0) return;

    const headers = ['Username', 'Full Name', 'Followers', 'Following', 'Posts', 'Engagement Rate', 'Avg Likes', 'Avg Comments', 'Bio', 'Profile URL'];
    const csvContent = [
        headers.join(','),
        ...foundProfiles.map(p => [
            p.username,
            `"${(p.full_name || '').replace(/"/g, '""')}"`,
            p.followers,
            p.following,
            p.posts_count,
            p.engagement_rate,
            p.avg_likes,
            p.avg_comments,
            `"${(p.biography || '').replace(/"/g, '""').replace(/\n/g, ' ')}"`,
            `https://instagram.com/${p.username}`
        ].join(','))
    ].join('\n');

    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    const link = document.createElement('a');
    link.href = URL.createObjectURL(blob);
    link.download = `influencers_${new Date().toISOString().slice(0, 10)}.csv`;
    link.click();
}
