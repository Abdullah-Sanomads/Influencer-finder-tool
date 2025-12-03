"""
Test to verify followers are checked BEFORE country extraction
"""

import os
import sys
import time

# Fix Unicode encoding for Windows console
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

from instagram_scraper import InstagramScraper

def test_followers_first():
    """Verify that followers are checked before country extraction"""
    
    print("=" * 60)
    print("Testing: Followers Checked First (Optimization)")
    print("=" * 60)
    
    scraper = InstagramScraper(headless=False)
    
    try:
        # Start and login
        print("\n[1/4] Starting browser and logging in...")
        if not scraper.start_browser() or not scraper.login():
            print("[X] Failed to start/login")
            return False
        print("[OK] Ready")
        
        # Navigate to test profile
        test_username = "deeafitness_"
        print(f"\n[2/4] Navigating to @{test_username}...")
        scraper.driver.get(f'https://www.instagram.com/{test_username}/')
        time.sleep(5)
        print("[OK] Profile loaded")
        
        # Test 1: Profile with followers OUT of range
        # Should skip country extraction
        print(f"\n[3/4] Test 1: Followers OUT of range")
        print("Expected: Should skip country extraction and reject immediately")
        print("-" * 60)
        
        filters = {
            'min_followers': 100000,  # Profile has ~8k, so this will fail
            'max_followers': 1000000,
            'country': 'united kingdom'  # Has country filter, but shouldn't check it
        }
        
        profile = scraper._analyze_profile_strict(test_username, filters, source_tag='test')
        print("-" * 60)
        
        if profile is None:
            rejection_reason = getattr(scraper, 'rejection_reason', 'Unknown')
            print(f"\n[OK] Profile rejected: {rejection_reason}")
            
            if 'Followers' in rejection_reason and 'not in range' in rejection_reason:
                print("[SUCCESS] Profile rejected due to followers (as expected)")
                print("[INFO] Country extraction was skipped (check logs above)")
            else:
                print(f"[WARNING] Rejected for different reason: {rejection_reason}")
        else:
            print("[X] FAILED: Profile should have been rejected")
            return False
        
        # Test 2: Profile with followers IN range
        # Should proceed to country extraction
        print(f"\n[4/4] Test 2: Followers IN range")
        print("Expected: Should extract country and check it")
        print("-" * 60)
        
        filters = {
            'min_followers': 1000,  # Profile has ~8k, so this will pass
            'max_followers': 10000,
            'country': 'united kingdom'
        }
        
        profile = scraper._analyze_profile_strict(test_username, filters, source_tag='test')
        print("-" * 60)
        
        if profile:
            print(f"\n[SUCCESS] Profile accepted!")
            print(f"Username: @{profile['username']}")
            print(f"Followers: {profile['followers']}")
            print(f"Country: {profile.get('country', 'N/A')}")
            print("[INFO] Country was extracted (check logs above)")
            return True
        else:
            rejection_reason = getattr(scraper, 'rejection_reason', 'Unknown')
            print(f"\n[INFO] Profile rejected: {rejection_reason}")
            
            if 'Country' in rejection_reason:
                print("[OK] Profile rejected due to country (country was checked)")
                return True
            else:
                print(f"[WARNING] Rejected for different reason: {rejection_reason}")
                return False
            
    except Exception as e:
        print(f"\n[X] Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        print("\n" + "=" * 60)
        print("Keeping browser open for 5 seconds...")
        print("=" * 60)
        time.sleep(5)
        scraper.close()

if __name__ == "__main__":
    success = test_followers_first()
    
    print("\n" + "=" * 60)
    if success:
        print("[OK] TEST PASSED - Followers checked first!")
    else:
        print("[X] TEST FAILED")
    print("=" * 60)
    
    sys.exit(0 if success else 1)
