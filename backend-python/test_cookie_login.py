"""
Test script to verify cookie-based Instagram login
"""

from instagram_scraper import InstagramScraper
import time

def test_cookie_login():
    print("=" * 60)
    print("Testing Instagram Login with Cookies")
    print("=" * 60)
    
    # Create scraper instance
    scraper = InstagramScraper()
    
    # Start browser
    print("\n1. Starting browser...")
    if not scraper.start_browser():
        print("[FAILED] Could not start browser")
        return False
    
    # Login with cookies
    print("\n2. Logging in with cookies...")
    if not scraper.login():
        print("[FAILED] Cookie login failed")
        scraper.close()
        return False
    
    print("\n[SUCCESS] Cookie login worked!")
    print("\nBrowser will stay open for 10 seconds so you can verify...")
    time.sleep(10)
    
    # Close browser
    scraper.close()
    return True

if __name__ == "__main__":
    success = test_cookie_login()
    if success:
        print("\n✓ Cookie-based login is working correctly!")
    else:
        print("\n✗ Cookie-based login failed. Check the errors above.")
