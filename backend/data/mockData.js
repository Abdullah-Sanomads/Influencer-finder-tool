/**
 * Mock influencer data for demo mode
 * This provides realistic sample data when no API key is configured
 */

const mockInfluencers = [
  {
    id: '1',
    username: 'fitness_emma_fit',
    full_name: 'Emma Rodriguez',
    profile_pic_url: 'https://i.pravatar.cc/150?img=1',
    biography: 'Fitness coach & nutrition expert 💪 Helping you achieve your goals #FitnessMotivation',
    followers: 4500,
    following: 850,
    posts_count: 342,
    is_verified: false,
    country: 'United States',
    category: 'fitness',
    gender: 'female',
    recent_posts: [
      { likes: 520, comments: 45 },
      { likes: 485, comments: 38 },
      { likes: 610, comments: 52 },
      { likes: 545, comments: 41 },
      { likes: 590, comments: 48 },
      { likes: 510, comments: 39 },
      { likes: 625, comments: 54 },
      { likes: 580, comments: 47 },
      { likes: 555, comments: 43 },
      { likes: 600, comments: 50 },
      { likes: 575, comments: 46 },
      { likes: 595, comments: 49 }
    ]
  },
  {
    id: '2',
    username: 'sarah_beauty_glow',
    full_name: 'Sarah Johnson',
    profile_pic_url: 'https://i.pravatar.cc/150?img=5',
    biography: 'Beauty & skincare enthusiast ✨ Natural makeup lover | LA based',
    followers: 3200,
    following: 720,
    posts_count: 256,
    is_verified: false,
    country: 'United States',
    category: 'beauty',
    gender: 'female',
    recent_posts: [
      { likes: 380, comments: 32 },
      { likes: 420, comments: 38 },
      { likes: 395, comments: 35 },
      { likes: 410, comments: 36 },
      { likes: 405, comments: 37 },
      { likes: 390, comments: 33 },
      { likes: 425, comments: 39 },
      { likes: 415, comments: 38 },
      { likes: 400, comments: 34 },
      { likes: 430, comments: 40 },
      { likes: 385, comments: 31 },
      { likes: 395, comments: 35 }
    ]
  },
  {
    id: '3',
    username: 'mike_gym_warrior',
    full_name: 'Michael Chen',
    profile_pic_url: 'https://i.pravatar.cc/150?img=12',
    biography: 'Personal trainer | Bodybuilding enthusiast 🏋️ #GymLife #FitnessJourney',
    followers: 2800,
    following: 650,
    posts_count: 198,
    is_verified: false,
    country: 'Canada',
    category: 'fitness',
    gender: 'male',
    recent_posts: [
      { likes: 310, comments: 28 },
      { likes: 295, comments: 25 },
      { likes: 325, comments: 30 },
      { likes: 300, comments: 27 },
      { likes: 315, comments: 29 },
      { likes: 305, comments: 26 },
      { likes: 320, comments: 31 },
      { likes: 310, comments: 28 },
      { likes: 290, comments: 24 },
      { likes: 330, comments: 32 },
      { likes: 300, comments: 27 },
      { likes: 315, comments: 29 }
    ]
  },
  {
    id: '4',
    username: 'jessica_fashion_style',
    full_name: 'Jessica Martinez',
    profile_pic_url: 'https://i.pravatar.cc/150?img=9',
    biography: 'Fashion blogger | Style inspiration 👗 NYC | Sustainable fashion advocate',
    followers: 4200,
    following: 890,
    posts_count: 425,
    is_verified: false,
    country: 'United States',
    category: 'fashion',
    gender: 'female',
    recent_posts: [
      { likes: 580, comments: 48 },
      { likes: 620, comments: 52 },
      { likes: 595, comments: 50 },
      { likes: 610, comments: 51 },
      { likes: 605, comments: 49 },
      { likes: 590, comments: 47 },
      { likes: 625, comments: 53 },
      { likes: 600, comments: 50 },
      { likes: 615, comments: 52 },
      { likes: 630, comments: 54 },
      { likes: 585, comments: 46 },
      { likes: 595, comments: 50 }
    ]
  },
  {
    id: '5',
    username: 'alex_foodie_adventures',
    full_name: 'Alex Thompson',
    profile_pic_url: 'https://i.pravatar.cc/150?img=14',
    biography: 'Food blogger 🍕 Restaurant reviews | Cooking tutorials | Toronto',
    followers: 3600,
    following: 780,
    posts_count: 312,
    is_verified: false,
    country: 'Canada',
    category: 'food',
    gender: 'male',
    recent_posts: [
      { likes: 450, comments: 40 },
      { likes: 475, comments: 42 },
      { likes: 460, comments: 39 },
      { likes: 490, comments: 44 },
      { likes: 465, comments: 41 },
      { likes: 480, comments: 43 },
      { likes: 470, comments: 40 },
      { likes: 455, comments: 38 },
      { likes: 485, comments: 45 },
      { likes: 495, comments: 46 },
      { likes: 460, comments: 39 },
      { likes: 475, comments: 42 }
    ]
  },
  {
    id: '6',
    username: 'amanda_yoga_peace',
    full_name: 'Amanda Williams',
    profile_pic_url: 'https://i.pravatar.cc/150?img=24',
    biography: 'Yoga instructor 🧘‍♀️ Mindfulness & wellness | Online classes available',
    followers: 2500,
    following: 550,
    posts_count: 178,
    is_verified: false,
    country: 'United States',
    category: 'fitness',
    gender: 'female',
    recent_posts: [
      { likes: 280, comments: 24 },
      { likes: 295, comments: 26 },
      { likes: 270, comments: 22 },
      { likes: 305, comments: 28 },
      { likes: 285, comments: 25 },
      { likes: 290, comments: 24 },
      { likes: 300, comments: 27 },
      { likes: 275, comments: 23 },
      { likes: 310, comments: 29 },
      { likes: 295, comments: 26 },
      { likes: 280, comments: 24 },
      { likes: 290, comments: 25 }
    ]
  },
  {
    id: '7',
    username: 'david_travel_explorer',
    full_name: 'David Brown',
    profile_pic_url: 'https://i.pravatar.cc/150?img=15',
    biography: 'Travel photographer 📸 Adventure seeker | 50+ countries explored',
    followers: 4800,
    following: 920,
    posts_count: 502,
    is_verified: false,
    country: 'United Kingdom',
    category: 'travel',
    gender: 'male',
    recent_posts: [
      { likes: 680, comments: 58 },
      { likes: 720, comments: 62 },
      { likes: 695, comments: 60 },
      { likes: 710, comments: 61 },
      { likes: 700, comments: 59 },
      { likes: 690, comments: 58 },
      { likes: 725, comments: 63 },
      { likes: 705, comments: 60 },
      { likes: 715, comments: 62 },
      { likes: 730, comments: 64 },
      { likes: 685, comments: 57 },
      { likes: 695, comments: 60 }
    ]
  },
  {
    id: '8',
    username: 'lisa_home_decor',
    full_name: 'Lisa Anderson',
    profile_pic_url: 'https://i.pravatar.cc/150?img=20',
    biography: 'Interior designer | Home decor inspiration 🏡 Making spaces beautiful',
    followers: 3100,
    following: 680,
    posts_count: 245,
    is_verified: false,
    country: 'United States',
    category: 'lifestyle',
    gender: 'female',
    recent_posts: [
      { likes: 420, comments: 36 },
      { likes: 445, comments: 39 },
      { likes: 430, comments: 37 },
      { likes: 455, comments: 40 },
      { likes: 440, comments: 38 },
      { likes: 435, comments: 37 },
      { likes: 460, comments: 41 },
      { likes: 450, comments: 39 },
      { likes: 425, comments: 36 },
      { likes: 465, comments: 42 },
      { likes: 415, comments: 35 },
      { likes: 430, comments: 37 }
    ]
  },
  {
    id: '9',
    username: 'chris_tech_geek',
    full_name: 'Christopher Lee',
    profile_pic_url: 'https://i.pravatar.cc/150?img=33',
    biography: 'Tech reviewer 💻 Gadgets & software | YouTube: ChrisTechGeek',
    followers: 4100,
    following: 820,
    posts_count: 367,
    is_verified: false,
    country: 'United States',
    category: 'technology',
    gender: 'male',
    recent_posts: [
      { likes: 570, comments: 50 },
      { likes: 595, comments: 53 },
      { likes: 580, comments: 51 },
      { likes: 610, comments: 54 },
      { likes: 585, comments: 52 },
      { likes: 600, comments: 53 },
      { likes: 590, comments: 52 },
      { likes: 575, comments: 50 },
      { likes: 605, comments: 54 },
      { likes: 615, comments: 55 },
      { likes: 580, comments: 51 },
      { likes: 595, comments: 53 }
    ]
  },
  {
    id: '10',
    username: 'nicole_makeup_pro',
    full_name: 'Nicole Davis',
    profile_pic_url: 'https://i.pravatar.cc/150?img=27',
    biography: 'Professional makeup artist 💄 Beauty tutorials | LA based | DM for bookings',
    followers: 3800,
    following: 790,
    posts_count: 289,
    is_verified: false,
    country: 'United States',
    category: 'beauty',
    gender: 'female',
    recent_posts: [
      { likes: 525, comments: 46 },
      { likes: 550, comments: 49 },
      { likes: 535, comments: 47 },
      { likes: 565, comments: 50 },
      { likes: 540, comments: 48 },
      { likes: 555, comments: 49 },
      { likes: 545, comments: 48 },
      { likes: 530, comments: 46 },
      { likes: 560, comments: 50 },
      { likes: 570, comments: 51 },
      { likes: 535, comments: 47 },
      { likes: 550, comments: 49 }
    ]
  },
  {
    id: '11',
    username: 'james_fitness_coach',
    full_name: 'James Wilson',
    profile_pic_url: 'https://i.pravatar.cc/150?img=52',
    biography: 'Certified personal trainer | Transformation coach 💪 Building better versions',
    followers: 3400,
    following: 710,
    posts_count: 267,
    is_verified: false,
    country: 'United Kingdom',
    category: 'fitness',
    gender: 'male',
    recent_posts: [
      { likes: 475, comments: 42 },
      { likes: 490, comments: 44 },
      { likes: 480, comments: 43 },
      { likes: 505, comments: 45 },
      { likes: 485, comments: 43 },
      { likes: 495, comments: 44 },
      { likes: 500, comments: 45 },
      { likes: 470, comments: 41 },
      { likes: 510, comments: 46 },
      { likes: 515, comments: 47 },
      { likes: 480, comments: 43 },
      { likes: 490, comments: 44 }
    ]
  },
  {
    id: '12',
    username: 'rachel_vegan_life',
    full_name: 'Rachel Green',
    profile_pic_url: 'https://i.pravatar.cc/150?img=47',
    biography: 'Vegan lifestyle blogger 🌱 Plant-based recipes | Ethical living',
    followers: 2900,
    following: 630,
    posts_count: 213,
    is_verified: false,
    country: 'Canada',
    category: 'food',
    gender: 'female',
    recent_posts: [
      { likes: 350, comments: 30 },
      { likes: 375, comments: 33 },
      { likes: 360, comments: 31 },
      { likes: 390, comments: 35 },
      { likes: 365, comments: 32 },
      { likes: 380, comments: 34 },
      { likes: 370, comments: 32 },
      { likes: 355, comments: 30 },
      { likes: 385, comments: 34 },
      { likes: 395, comments: 36 },
      { likes: 360, comments: 31 },
      { likes: 375, comments: 33 }
    ]
  },
  {
    id: '13',
    username: 'kevin_sports_fan',
    full_name: 'Kevin Miller',
    profile_pic_url: 'https://i.pravatar.cc/150?img=56',
    biography: 'Sports journalist ⚽ Game analysis | Fantasy sports tips',
    followers: 4300,
    following: 860,
    posts_count: 398,
    is_verified: false,
    country: 'United States',
    category: 'sports',
    gender: 'male',
    recent_posts: [
      { likes: 595, comments: 52 },
      { likes: 620, comments: 55 },
      { likes: 605, comments: 53 },
      { likes: 635, comments: 56 },
      { likes: 610, comments: 54 },
      { likes: 625, comments: 55 },
      { likes: 615, comments: 54 },
      { likes: 600, comments: 52 },
      { likes: 630, comments: 56 },
      { likes: 640, comments: 57 },
      { likes: 605, comments: 53 },
      { likes: 620, comments: 55 }
    ]
  },
  {
    id: '14',
    username: 'sophia_fashion_trends',
    full_name: 'Sophia Taylor',
    profile_pic_url: 'https://i.pravatar.cc/150?img=45',
    biography: 'Fashion influencer 👠 Trend spotter | Sustainable style advocate',
    followers: 4600,
    following: 910,
    posts_count: 456,
    is_verified: false,
    country: 'United Kingdom',
    category: 'fashion',
    gender: 'female',
    recent_posts: [
      { likes: 650, comments: 56 },
      { likes: 680, comments: 59 },
      { likes: 665, comments: 57 },
      { likes: 695, comments: 60 },
      { likes: 670, comments: 58 },
      { likes: 685, comments: 59 },
      { likes: 675, comments: 58 },
      { likes: 660, comments: 57 },
      { likes: 690, comments: 60 },
      { likes: 700, comments: 61 },
      { likes: 665, comments: 57 },
      { likes: 680, comments: 59 }
    ]
  },
  {
    id: '15',
    username: 'ryan_car_enthusiast',
    full_name: 'Ryan Moore',
    profile_pic_url: 'https://i.pravatar.cc/150?img=60',
    biography: 'Automotive blogger 🚗 Car reviews | Track days | Gear head',
    followers: 3700,
    following: 770,
    posts_count: 301,
    is_verified: false,
    country: 'United States',
    category: 'automotive',
    gender: 'male',
    recent_posts: [
      { likes: 515, comments: 45 },
      { likes: 540, comments: 48 },
      { likes: 525, comments: 46 },
      { likes: 555, comments: 49 },
      { likes: 530, comments: 47 },
      { likes: 545, comments: 48 },
      { likes: 535, comments: 47 },
      { likes: 520, comments: 46 },
      { likes: 550, comments: 49 },
      { likes: 560, comments: 50 },
      { likes: 525, comments: 46 },
      { likes: 540, comments: 48 }
    ]
  }
];

/**
 * Filter influencers based on provided criteria
 * @param {Object} filters - Filter criteria
 * @returns {Array} Filtered influencers
 */
function filterInfluencers(filters) {
  let results = [...mockInfluencers];

  // Filter by gender
  if (filters.gender && filters.gender !== 'both') {
    results = results.filter(inf => inf.gender === filters.gender.toLowerCase());
  }

  // Filter by country
  if (filters.country) {
    results = results.filter(inf => 
      inf.country.toLowerCase().includes(filters.country.toLowerCase())
    );
  }

  // Filter by industry/niche
  if (filters.industry) {
    results = results.filter(inf =>
      inf.category.toLowerCase().includes(filters.industry.toLowerCase()) ||
      inf.biography.toLowerCase().includes(filters.industry.toLowerCase())
    );
  }

  // Filter by follower range
  if (filters.min_followers) {
    results = results.filter(inf => inf.followers >= parseInt(filters.min_followers));
  }
  if (filters.max_followers) {
    results = results.filter(inf => inf.followers <= parseInt(filters.max_followers));
  }

  return results;
}

module.exports = {
  mockInfluencers,
  filterInfluencers
};
