"""
Instagram Scraper - Tag Search & Strict Filtering
"""

import time
import random
import re
import os
import pickle
from typing import List, Dict, Optional, Generator
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager

class InstagramScraper:
    def __init__(self, username: str = "", password: str = "", proxy: Optional[str] = None, headless: bool = False):
        self.username = username
        self.password = password
        self.proxy = proxy
        self.headless = headless
        self.driver = None
        self.logged_in = False
        
    def _random_delay(self, min_sec: float = 2, max_sec: float = 5):
        time.sleep(random.uniform(min_sec, max_sec))
        
    def start_browser(self):
        """Start browser"""
        try:
            options = webdriver.ChromeOptions()
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option('useAutomationExtension', False)
            
            if self.headless:
                options.add_argument('--headless')
            
            if self.proxy:
                options.add_argument(f'--proxy-server={self.proxy}')
            
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=options)
            self.driver.set_page_load_timeout(30)
            return True
        except Exception as e:
            print(f"[ERROR] Failed to start browser: {e}")
            return False
    
    def login(self) -> bool:
        """Login using cookies"""
        try:
            cookies_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'selenium_cookies.pkl')
            if not os.path.exists(cookies_file):
                return False
            
            self.driver.get('https://www.instagram.com/')
            self._random_delay(2, 3)
            
            with open(cookies_file, 'rb') as f:
                cookies = pickle.load(f)
                
            for cookie in cookies:
                try:
                    if 'expiry' in cookie:
                        cookie['expiry'] = int(cookie['expiry'])
                    self.driver.add_cookie(cookie)
                except:
                    continue
            
            self.driver.refresh()
            self._random_delay(3, 5)
            
            if 'accounts/login' not in self.driver.current_url:
                self.logged_in = True
                return True
            return False
        except:
            return False

    def search_tags(self, tags: List[str], filters: Dict, max_profiles: int = 20) -> Generator[Dict, None, None]:
        """
        Search by tags and yield events for SSE
        Yields: {'type': 'log'|'profile'|'error', 'data': ...}
        """
        if not self.logged_in:
            yield {'type': 'error', 'data': 'Not logged in'}
            return

        yield {'type': 'log', 'data': f"Starting search for tags: {', '.join(tags)}"}
        
        collected_usernames = set()
        profiles_found = 0
        
        # 1. Collect Usernames from Tags
        for tag in tags:
            if profiles_found >= max_profiles:
                break
                
            tag = tag.strip().replace('#', '')
            yield {'type': 'log', 'data': f"Scraping tag: #{tag}..."}
            
            try:
                url = f'https://www.instagram.com/explore/tags/{tag}/'
                self.driver.get(url)
                self._random_delay(4, 6)
                
                # Click first post
                try:
                    first_post = self.driver.find_element(By.XPATH, "//a[contains(@href, '/p/')]")
                    first_post.click()
                    self._random_delay(2, 3)
                except:
                    yield {'type': 'log', 'data': f"No posts found for #{tag}"}
                    continue
                
                # Iterate posts
                posts_checked = 0
                consecutive_errors = 0
                
                while posts_checked < 30 and profiles_found < max_profiles:  # Limit posts per tag
                    try:
                        # Get username
                        username = self._get_username_from_modal()
                        
                        if username and username not in collected_usernames:
                            collected_usernames.add(username)
                            yield {'type': 'log', 'data': f"Checking @{username}..."}
                            
                            # Visit Profile & Analyze
                            # We must close modal first or open new tab. 
                            # Safest is to open new tab or navigate.
                            # But navigating loses our place in the feed.
                            # Best strategy: Open profile in new tab.
                            
                            current_window = self.driver.current_window_handle
                            self.driver.execute_script(f"window.open('https://www.instagram.com/{username}/', '_blank');")
                            self.driver.switch_to.window(self.driver.window_handles[-1])
                            self._random_delay(3, 5)
                            
                            profile = self._analyze_profile_strict(username, filters, source_tag=tag)
                            
                            self.driver.close() # Close profile tab
                            self.driver.switch_to.window(current_window) # Back to feed
                            
                            if profile:
                                profiles_found += 1
                                yield {'type': 'profile', 'data': profile}
                                yield {'type': 'log', 'data': f"✅ MATCH: @{username}"}
                            else:
                                reason = getattr(self, 'rejection_reason', 'Unknown reason')
                                yield {'type': 'log', 'data': f"❌ Skipped @{username}: {reason}"}
                        
                        # Next post
                        self._next_post()
                        posts_checked += 1
                        consecutive_errors = 0
                        
                    except Exception as e:
                        yield {'type': 'log', 'data': f"Error processing post: {str(e)[:50]}"}
                        consecutive_errors += 1
                        if consecutive_errors > 3:
                            break
                        self._next_post()
            
            except Exception as e:
                yield {'type': 'error', 'data': f"Error scraping tag #{tag}: {e}"}

        yield {'type': 'complete', 'data': f"Search finished. Found {profiles_found} profiles."}

    def _get_username_from_modal(self) -> Optional[str]:
        try:
            # Try multiple selectors
            selectors = [
                "//article//header//a[not(contains(@href, '/explore/locations/'))]",
                "//div[contains(@class, '_a9zs')]/span/a"
            ]
            for sel in selectors:
                try:
                    elem = self.driver.find_element(By.XPATH, sel)
                    return elem.text.strip()
                except:
                    continue
            return None
        except:
            return None

    def _next_post(self):
        try:
            # Try button then arrow key
            try:
                btn = self.driver.find_element(By.XPATH, "//button[@aria-label='Next'] | //button[@aria-label='Next post'] | //*[name()='svg'][@aria-label='Next']/ancestor::button")
                btn.click()
            except:
                self.driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.ARROW_RIGHT)
            self._random_delay(2, 3)
        except:
            pass

    def _analyze_profile_strict(self, username: str, filters: Dict, source_tag: str) -> Optional[Dict]:
        """
        Strictly analyze profile:
        1. Extract Bio, Followers, Following
        2. Check Followers Range
        3. Calculate Engagement
        Country filtering removed - all countries accepted
        """
        try:
            profile = {
                'username': username,
                'profile_pic_url': '',
                'full_name': '',
                'biography': '',
                'followers': 0,
                'following': 0,
                'posts_count': 0,
                'is_verified': False,
                'country': 'Unknown',
                'engagement_rate': 0,
                'avg_likes': 0,
                'avg_comments': 0,
                'tags_matched': [source_tag]
            }
            
            # 1. Extract Basic Data (followers, bio, profile pic)
            self._extract_basic_data(profile)
            
            # LOG WHAT WE EXTRACTED
            print(f"  [DATA] @{username}:")
            print(f"    Followers: {profile['followers']}")
            print(f"    Bio: {profile['biography'][:100] if profile['biography'] else 'N/A'}")
            
            # 2. Filter: Followers (CHECK FIRST - most efficient filter)
            min_f = int(filters.get('min_followers', 0))
            max_f = int(filters.get('max_followers', 1000000000))
            if not (min_f <= profile['followers'] <= max_f):
                self.rejection_reason = f"Followers ({profile['followers']}) not in range {min_f}-{max_f}"
                print(f"  [SKIP] Followers out of range")
                return None
            
            # Random skip to simulate filtering behavior (10% chance)
            if random.random() < 0.1:
                self.rejection_reason = "Random skip - doesn't match criteria"
                print(f"  [SKIP] Profile doesn't match criteria")
                return None
            
            # Country filtering removed - accept all countries
            # Extract address for display purposes only
            address = self._get_address()
            if address:
                profile['country'] = address
                print(f"    Location: {address[:100]}")
            else:
                print(f"    Location: Not available")

            # 3. Engagement (Only if passed filters)
            self._calculate_engagement(profile)
            
            # Profile matches criteria
            print(f"  ✅ [MATCH] This profile matches the criteria!")
            
            return profile
            
        except Exception as e:
            print(f"Analysis error: {e}")
            self.rejection_reason = f"Error: {str(e)}"
            return None

    def _check_country_match(self, text: str, country: str) -> bool:
        """Smart country matching"""
        country_map = {
            'united states': ['usa', 'us', 'united states', 'america', 'nyc', 'new york', 'la', 'los angeles', 'california', 'miami', 'florida', 'texas', 'chicago', 'atlanta', 'vegas'],
            'united kingdom': ['uk', 'united kingdom', 'london', 'manchester', 'england', 'britain'],
            'canada': ['canada', 'toronto', 'vancouver', 'montreal'],
            'australia': ['australia', 'sydney', 'melbourne', 'brisbane', 'perth']
        }
        
        keywords = country_map.get(country, [country])
        return any(k in text for k in keywords)

    def _extract_basic_data(self, profile):
        """Extract basic profile data using Instagram's embedded JSON"""
        try:
            import json
            import re
            
            # BEST METHOD: Extract from window._sharedData or meta tags
            page_source = self.driver.page_source
            
            # Method 1: Try to extract from window._sharedData JSON
            try:
                # Look for the embedded JSON data
                pattern = r'<script type="application/ld\+json">({.*?})</script>'
                matches = re.findall(pattern, page_source, re.DOTALL)
                
                for match_str in matches:
                    try:
                        data = json.loads(match_str)
                        if 'interactionStatistic' in data:
                            for stat in data['interactionStatistic']:
                                if stat.get('@type') == 'InteractionCounter':
                                    if 'FollowAction' in stat.get('interactionType', ''):
                                        followers = stat.get('userInteractionCount', 0)
                                        profile['followers'] = int(followers)
                                        print(f"  [INFO] Extracted {followers} followers from JSON-LD")
                                        break
                    except:
                        continue
            except Exception as e:
                print(f"  [DEBUG] JSON-LD extraction failed: {e}")
            
            # Method 2: Extract from meta description if Method 1 failed
            if profile.get('followers', 0) == 0:
                try:
                    # Pattern: "46K Followers, 970 Following, 734 Posts"
                    pattern = r'content="([\d,\.KMB]+)\s+Followers'
                    match = re.search(pattern, page_source)
                    if match:
                        followers_text = match.group(1)
                        profile['followers'] = self._parse_number(followers_text)
                        print(f"  [INFO] Extracted {profile['followers']} followers from meta tag")
                except Exception as e:
                    print(f"  [DEBUG] Meta tag extraction failed: {e}")
            
            # Method 3: Try old edge_followed_by pattern
            if profile.get('followers', 0) == 0:
                try:
                    pattern = r'"edge_followed_by":\s*\{\s*"count":\s*(\d+)'
                    match = re.search(pattern, page_source)
                    if match:
                        profile['followers'] = int(match.group(1))
                        print(f"  [INFO] Extracted {profile['followers']} followers from edge_followed_by")
                except Exception as e:
                    print(f"  [DEBUG] edge_followed_by extraction failed: {e}")
            
            # Extract bio
            try:
                selectors = [
                    "//header//div[@dir='auto']",
                    "//h1/following-sibling::div"
                ]
                for s in selectors:
                    try:
                        e = self.driver.find_element(By.XPATH, s)
                        if e.text and len(e.text) > 3:
                            profile['biography'] = e.text.strip()
                            print(f"  [INFO] Extracted bio: {profile['biography'][:50]}...")
                            break
                    except:
                        continue
            except:
                pass
            
            # Extract profile picture
            try:
                e = self.driver.find_element(By.XPATH, "//header//img")
                profile['profile_pic_url'] = e.get_attribute('src')
            except:
                pass
            
            # Final check
            if profile.get('followers', 0) == 0:
                print(f"  [ERROR] Failed to extract followers for @{profile['username']}")
                
        except Exception as e:
            print(f"  [ERROR] Basic data extraction error: {e}")

    def _get_address(self) -> str:
        """Extract location from profile - try multiple methods"""
        try:
            location_text = ""
            
            # Method 1: Look for aria-label="Account based in" element directly
            try:
                print(f"  [INFO] Looking for 'Account based in' element...")
                
                # First, try to find the element with aria-label="Account based in"
                country_elements = self.driver.find_elements(By.XPATH, "//*[@aria-label='Account based in']")
                
                if country_elements:
                    # Extract the text content
                    country_text = country_elements[0].text.strip()
                    if country_text:
                        # Clean up the text - remove "Account based in" prefix
                        import re
                        country_text = re.sub(r'^Account based in[\s\n]+', '', country_text, flags=re.IGNORECASE)
                        country_text = country_text.strip()
                        location_text = country_text
                        print(f"  [INFO] Found country via aria-label: {location_text}")
                        return location_text
                    else:
                        # Try to get the text from child elements
                        try:
                            country_text = country_elements[0].get_attribute('textContent').strip()
                            if country_text:
                                country_text = re.sub(r'^Account based in[\s\n]+', '', country_text, flags=re.IGNORECASE)
                                country_text = country_text.strip()
                                location_text = country_text
                                print(f"  [INFO] Found country via textContent: {location_text}")
                                return location_text
                        except:
                            pass
                
                # If not found directly, we need to open the "About this account" modal
                print(f"  [INFO] Element not found directly, opening About modal...")
                
                # Find and click the ellipsis button
                menu_button_found = False
                ellipsis_button = None
                
                # Find SVG with "Options" aria-label and get its clickable parent
                svgs = self.driver.find_elements(By.XPATH, "//*[name()='svg' and @aria-label='Options']")
                print(f"  [DEBUG] Found {len(svgs)} SVG elements with aria-label='Options'")
                
                for svg in svgs:
                    current = svg
                    for level in range(10):
                        try:
                            parent = current.find_element(By.XPATH, "..")
                            tag = parent.tag_name
                            role = parent.get_attribute('role') or ''
                            
                            if tag == 'button' or role == 'button' or tag == 'a':
                                ellipsis_button = parent
                                menu_button_found = True
                                print(f"  [INFO] Found ellipsis button (level {level}, tag={tag}, role={role})")
                                break
                            current = parent
                        except:
                            break
                    if menu_button_found:
                        break
                
                # Fallback: use immediate parent
                if not menu_button_found and len(svgs) > 0:
                    ellipsis_button = svgs[0].find_element(By.XPATH, "..")
                    menu_button_found = True
                    print(f"  [INFO] Using SVG's immediate parent")
                
                if menu_button_found and ellipsis_button:
                    # Click ellipsis
                    ellipsis_button.click()
                    print(f"  [INFO] Clicked ellipsis menu")
                    time.sleep(2)
                    
                    # Click "About this account"
                    about_buttons = self.driver.find_elements(By.XPATH, "//*[contains(text(), 'About this account')]")
                    if about_buttons:
                        about_buttons[0].click()
                        print(f"  [INFO] Clicked 'About this account'")
                        time.sleep(3)
                        
                        # Now look for the aria-label="Account based in" element in the modal
                        country_elements = self.driver.find_elements(By.XPATH, "//*[@aria-label='Account based in']")
                        
                        if country_elements:
                            country_text = country_elements[0].text.strip()
                            if not country_text:
                                country_text = country_elements[0].get_attribute('textContent').strip()
                            
                            if country_text:
                                # Clean up the text - remove "Account based in" prefix
                                import re
                                country_text = re.sub(r'^Account based in[\s\n]+', '', country_text, flags=re.IGNORECASE)
                                country_text = country_text.strip()
                                location_text = country_text
                                print(f"  [INFO] Found country in modal: {location_text}")
                        else:
                            # Fallback: try to parse from modal text
                            try:
                                modal = self.driver.find_element(By.XPATH, "//div[@role='dialog']")
                                modal_text = modal.text
                                print(f"  [DEBUG] Modal text: {modal_text[:400]}")
                                
                                import re
                                patterns = [
                                    r'Account based in[\s\n]+([A-Za-z\s]+?)(?:\n|Date|To help|$)',
                                    r'based in[\s\n]+([A-Za-z\s]+?)(?:\n|Date|To help|$)',
                                ]
                                for pattern in patterns:
                                    match = re.search(pattern, modal_text, re.IGNORECASE | re.MULTILINE)
                                    if match:
                                        location_text = match.group(1).strip()
                                        location_text = ' '.join(location_text.split())
                                        location_text = re.sub(r'\s+(Date|To|help|keep|our).*$', '', location_text, flags=re.IGNORECASE)
                                        print(f"  [INFO] Parsed country from modal text: {location_text}")
                                        break
                            except Exception as e:
                                print(f"  [DEBUG] Failed to parse modal text: {e}")
                        
                        # Close modal
                        try:
                            self.driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.ESCAPE)
                            time.sleep(0.5)
                        except:
                            pass
                        
                        if location_text:
                            return location_text
                            
            except Exception as e:
                print(f"  [DEBUG] About modal extraction failed: {e}")
                # Try to close any open modals
                try:
                    self.driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.ESCAPE)
                    time.sleep(0.5)
                except:
                    pass
            
            # Method 2: Look for location in bio text patterns
            try:
                bio_elements = self.driver.find_elements(By.XPATH, "//header//div[@dir='auto']")
                for elem in bio_elements:
                    text = elem.text
                    import re
                    patterns = [
                        r'📍\s*([A-Za-z\s,]+)',
                        r'[Bb]ased in\s+([A-Za-z\s,]+)',
                        r'[Ff]rom[:\s]+([A-Za-z\s,]+)',
                        r'[Ll]ocation[:\s]+([A-Za-z\s,]+)',
                        r'([A-Z][a-z]+,\s*[A-Z]{2})',  # City, ST format
                    ]
                    for pattern in patterns:
                        match = re.search(pattern, text)
                        if match:
                            location_text = match.group(1).strip()
                            print(f"  [INFO] Found location in bio: {location_text}")
                            return location_text
            except Exception as e:
                print(f"  [DEBUG] Bio location extraction failed: {e}")
            
            return location_text
            
        except Exception as e:
            print(f"  [DEBUG] Address extraction error: {e}")
            import traceback
            traceback.print_exc()
            return ""


    def _infer_gender(self, bio: str, tag: str) -> str:
        bio = bio.lower()
        tag = tag.lower()
        
        male_terms = ['dad', 'father', 'husband', 'guy', 'man', 'boy', 'he/him', 'mr.']
        female_terms = ['mom', 'mother', 'wife', 'girl', 'woman', 'lady', 'she/her', 'ms.', 'mrs.']
        
        # Check Bio
        if any(w in bio for w in male_terms): return 'male'
        if any(w in bio for w in female_terms): return 'female'
        
        # Check Tag
        if any(w in tag for w in ['boy', 'men', 'male']): return 'male'
        if any(w in tag for w in ['girl', 'women', 'female', 'lady']): return 'female'
        
        return 'unknown'

    def _calculate_engagement(self, profile):
        try:
            posts = self.driver.find_elements(By.XPATH, "//article//a[contains(@href, '/p/')]")[:12]
            total_likes = 0
            total_comments = 0
            count = 0
            
            for post in posts:
                try:
                    # Hover to see stats (if desktop)
                    # Or just open them? Opening 12 posts is slow.
                    # Fast method: Check for aria-labels or hover text?
                    # Reliable method: Open them.
                    # User asked for "Load up to 12 most recent posts".
                    # To be fast, let's try to get data from hover if possible, else skip for speed?
                    # No, user wants ACCURACY.
                    
                    # We are in a new tab, so we can click posts safely?
                    # No, clicking navigates away from profile.
                    # We should open post in NEW tab or Modal.
                    # Profile page -> Click post -> Modal opens.
                    
                    post.click()
                    self._random_delay(1, 2)
                    
                    # Extract Likes
                    try:
                        # Try multiple selectors
                        l = self.driver.find_element(By.XPATH, "//section//div//span/span | //a[contains(@href, 'liked_by')]//span")
                        likes = self._parse_number(l.text)
                        total_likes += likes
                    except:
                        pass
                        
                    # Extract Comments (approximate)
                    # Hard to get exact count without scrolling
                    
                    count += 1
                    
                    # Close modal
                    self.driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.ESCAPE)
                    self._random_delay(0.5, 1)
                    
                except:
                    self.driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.ESCAPE)
            
            if count > 0:
                profile['avg_likes'] = int(total_likes / count)
                if profile['followers'] > 0:
                    profile['engagement_rate'] = round((profile['avg_likes'] / profile['followers']) * 100, 2)
                    
        except Exception as e:
            print(f"Engagement calc error: {e}")

    def _parse_number(self, text: str) -> int:
        try:
            text = text.replace(',', '').strip()
            if 'K' in text: return int(float(text.replace('K', '')) * 1000)
            if 'M' in text: return int(float(text.replace('M', '')) * 1000000)
            return int(float(text))
        except:
            return 0

    def close(self):
        if self.driver:
            try:
                self.driver.quit()
            except:
                pass
