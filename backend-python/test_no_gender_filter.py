"""
Test to verify gender filter has been removed
"""

import os
import sys
import time

# Fix Unicode encoding for Windows console
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

from instagram_scraper import InstagramScraper

def test_no_gender_filter():
    """Verify that gender filter is no longer rejecting accounts"""
    
    print("=" * 60)
    print("Testing: Gender Filter Removal")
    print("=" * 60)
    
    scraper = InstagramScraper(headless=False)
    
    try:
        # Start and login
        print("\n[1/3] Starting browser and logging in...")
        if not scraper.start_browser() or not scraper.login():
            print("[X] Failed to start/login")
            return False
        print("[OK] Ready")
        
        # Navigate to a female profile
        test_username = "deeafitness_"  # Female profile from earlier test
        print(f"\n[2/3] Navigating to @{test_username}...")
        scraper.driver.get(f'https://www.instagram.com/{test_username}/')
        time.sleep(5)
        print("[OK] Profile loaded")
        
        # Test profile analysis with gender filter set to 'male'
        # This should NOT reject the profile anymore
        print(f"\n[3/3] Testing profile analysis with gender='male' filter...")
        print("(This should NOT reject the profile since gender filter is removed)")
        print("-" * 60)
        
        filters = {
            'gender': 'male',  # Set to opposite gender
            'min_followers': 0,
            'max_followers': 1000000,
            'country': ''
        }
        
        profile = scraper._analyze_profile_strict(test_username, filters, source_tag='test')
        print("-" * 60)
        
        if profile:
            print(f"\n[SUCCESS] Profile was NOT rejected!")
            print(f"Username: @{profile['username']}")
            print(f"Followers: {profile['followers']}")
            print(f"\n[OK] Gender filter has been successfully removed!")
            return True
        else:
            rejection_reason = getattr(scraper, 'rejection_reason', 'Unknown')
            print(f"\n[X] Profile was rejected: {rejection_reason}")
            
            if 'gender' in rejection_reason.lower():
                print("[X] FAILED: Gender filter is still active!")
                return False
            else:
                print("[INFO] Profile rejected for other reason (not gender)")
                return True
            
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
    success = test_no_gender_filter()
    
    print("\n" + "=" * 60)
    if success:
        print("[OK] TEST PASSED - Gender filter removed successfully")
    else:
        print("[X] TEST FAILED - Gender filter still active")
    print("=" * 60)
    
    sys.exit(0 if success else 1)
