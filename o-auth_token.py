#!/usr/bin/env python3
"""
create_instagram_cookies.py
Manual login to Instagram and save cookies for automation
"""

import pickle
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

COOKIES_FILE = "selenium_cookies.pkl"

def create_cookies():
    print("🔐 Instagram Cookie Generator")
    print("=" * 50)
    
    # Start browser
    opts = webdriver.ChromeOptions()
    opts.add_argument("--start-maximized")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=opts)
    
    try:
        # Open Instagram
        print("\n📱 Opening Instagram...")
        driver.get("https://www.instagram.com/")
        time.sleep(3)
        
        print("\n⚠️  MANUAL STEP REQUIRED:")
        print("=" * 50)
        print("1. Log in to Instagram in the browser window")
        print("2. Complete any 2FA if required")
        print("3. Wait until you see your Instagram feed/home page")
        print("4. Then come back here and press ENTER")
        print("=" * 50)
        
        input("\n👉 Press ENTER after you've logged in and see your feed...")
        
        # Verify login by checking for profile elements
        print("\n🔍 Verifying login status...")
        time.sleep(2)
        
        # Check if we're logged in
        try:
            # Look for profile icon or home elements (indicates logged in)
            profile_elements = driver.find_elements(By.XPATH, 
                "//a[contains(@href, '/accounts/')] | //svg[@aria-label='Home'] | //a[@aria-label='Profile']")
            
            if not profile_elements:
                print("❌ Login verification failed. You might not be logged in properly.")
                print("   Please make sure you're on the Instagram home/feed page.")
                retry = input("\n   Retry verification? (y/n): ")
                if retry.lower() == 'y':
                    time.sleep(3)
                    profile_elements = driver.find_elements(By.XPATH, 
                        "//a[contains(@href, '/accounts/')] | //svg[@aria-label='Home']")
            
            if profile_elements:
                print("✅ Login verified!")
            else:
                print("⚠️  Could not verify login, but continuing anyway...")
        except Exception as e:
            print(f"⚠️  Verification check failed: {e}")
            print("   Continuing anyway...")
        
        # Get cookies
        print("\n💾 Extracting cookies...")
        cookies = driver.get_cookies()
        
        # Save cookies
        with open(COOKIES_FILE, "wb") as f:
            pickle.dump(cookies, f)
        
        print(f"\n✅ SUCCESS! Cookies saved to: {COOKIES_FILE}")
        print(f"   Total cookies saved: {len(cookies)}")
        
        # Show important cookies (without values for security)
        important_cookies = ['sessionid', 'csrftoken', 'ds_user_id']
        found_cookies = [c['name'] for c in cookies if c['name'] in important_cookies]
        print(f"   Important cookies found: {', '.join(found_cookies)}")
        
        if 'sessionid' not in found_cookies:
            print("\n⚠️  WARNING: 'sessionid' cookie not found!")
            print("   The cookies might not work properly.")
            print("   Make sure you're fully logged in before saving cookies.")
        
        print("\n✅ You can now run the main scraper script!")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
    
    finally:
        print("\n🔒 Closing browser in 5 seconds...")
        time.sleep(5)
        driver.quit()

if __name__ == "__main__":
    create_cookies()