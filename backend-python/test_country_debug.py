"""
Debug test script to verify the country extraction with detailed logging
"""

import os
import sys
import time

# Fix Unicode encoding for Windows console
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

from instagram_scraper import InstagramScraper
from selenium.webdriver.common.by import By

def debug_country_extraction():
    """Test the country extraction functionality with detailed debugging"""
    
    print("=" * 60)
    print("DEBUG: Country Extraction from 'About this account' Modal")
    print("=" * 60)
    
    # Initialize scraper
    scraper = InstagramScraper(headless=False)
    
    try:
        # Start browser
        print("\n[1/5] Starting browser...")
        if not scraper.start_browser():
            print("[X] Failed to start browser")
            return False
        print("[OK] Browser started successfully")
        
        # Login using cookies
        print("\n[2/5] Logging in using cookies...")
        if not scraper.login():
            print("[X] Failed to login")
            return False
        print("[OK] Logged in successfully")
        
        # Test profile - using the username from the uploaded image
        test_username = "deeafitness_"
        
        print(f"\n[3/5] Navigating to test profile: @{test_username}...")
        scraper.driver.get(f'https://www.instagram.com/{test_username}/')
        time.sleep(5)
        print("[OK] Profile loaded")
        
        # Debug: Check what buttons are available
        print(f"\n[4/5] Debugging available buttons...")
        print("-" * 60)
        
        # Check for ellipsis buttons
        print("\n[DEBUG] Looking for ellipsis buttons...")
        
        # Try selector 1
        try:
            buttons = scraper.driver.find_elements(By.XPATH, "//button[contains(., '...')]")
            print(f"  Selector 1 (text '...'): Found {len(buttons)} buttons")
            for i, btn in enumerate(buttons[:3]):
                print(f"    Button {i+1}: text='{btn.text}', visible={btn.is_displayed()}")
        except Exception as e:
            print(f"  Selector 1 failed: {e}")
        
        # Try selector 2
        try:
            buttons = scraper.driver.find_elements(By.XPATH, "//button[.//*[name()='svg' and (@aria-label='Options' or @aria-label='More options')]]")
            print(f"  Selector 2 (SVG aria-label): Found {len(buttons)} buttons")
        except Exception as e:
            print(f"  Selector 2 failed: {e}")
        
        # Try selector 3
        try:
            buttons = scraper.driver.find_elements(By.XPATH, "//button[contains(@aria-label, 'Options') or contains(@aria-label, 'More options')]")
            print(f"  Selector 3 (button aria-label): Found {len(buttons)} buttons")
        except Exception as e:
            print(f"  Selector 3 failed: {e}")
        
        # Try to find ANY button in the header
        try:
            header_buttons = scraper.driver.find_elements(By.XPATH, "//header//button")
            print(f"\n[DEBUG] Total buttons in header: {len(header_buttons)}")
            for i, btn in enumerate(header_buttons[:5]):
                aria_label = btn.get_attribute('aria-label') or 'None'
                text = btn.text or 'None'
                print(f"  Button {i+1}: aria-label='{aria_label}', text='{text}'")
        except Exception as e:
            print(f"  Failed to get header buttons: {e}")
        
        # Extract country using the method
        print(f"\n[5/5] Attempting to extract country...")
        print("-" * 60)
        country = scraper._get_address()
        print("-" * 60)
        
        if country:
            print(f"\n[OK] SUCCESS! Country extracted: '{country}'")
            return True
        else:
            print("\n[X] FAILED! No country information extracted")
            
            # Take a screenshot for debugging
            screenshot_path = os.path.join(os.path.dirname(__file__), "debug_screenshot.png")
            scraper.driver.save_screenshot(screenshot_path)
            print(f"\n[DEBUG] Screenshot saved to: {screenshot_path}")
            
            return False
            
    except Exception as e:
        print(f"\n[X] Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        # Keep browser open for 10 seconds to review
        print("\n" + "=" * 60)
        print("Keeping browser open for 10 seconds for manual review...")
        print("=" * 60)
        time.sleep(10)
        scraper.close()

if __name__ == "__main__":
    success = debug_country_extraction()
    
    print("\n" + "=" * 60)
    if success:
        print("[OK] TEST PASSED")
    else:
        print("[X] TEST FAILED")
    print("=" * 60)
    
    sys.exit(0 if success else 1)
