"""
Final test - wait for modal content to change after clicking About
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
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def final_test():
    """Final test with proper modal wait logic"""
    
    print("=" * 60)
    print("FINAL TEST: Proper modal wait logic")
    print("=" * 60)
    
    scraper = InstagramScraper(headless=False)
    
    try:
        # Start and login
        print("\n[1/6] Starting browser and logging in...")
        if not scraper.start_browser() or not scraper.login():
            print("[X] Failed to start/login")
            return False
        print("[OK] Ready")
        
        # Navigate
        test_username = "deeafitness_"
        print(f"\n[2/6] Navigating to @{test_username}...")
        scraper.driver.get(f'https://www.instagram.com/{test_username}/')
        time.sleep(5)
        print("[OK] Profile loaded")
        
        # Find and click ellipsis
        print(f"\n[3/6] Finding and clicking ellipsis button...")
        svgs = scraper.driver.find_elements(By.XPATH, "//*[name()='svg' and @aria-label='Options']")
        
        if not svgs:
            print("[X] No SVG found")
            return False
        
        # Find clickable parent
        ellipsis_button = None
        for svg in svgs:
            current = svg
            for level in range(10):
                try:
                    parent = current.find_element(By.XPATH, "..")
                    tag = parent.tag_name
                    role = parent.get_attribute('role') or ''
                    
                    if tag == 'button' or role == 'button' or tag == 'a':
                        ellipsis_button = parent
                        print(f"  Found button (level {level}, tag={tag}, role={role})")
                        break
                    current = parent
                except:
                    break
            if ellipsis_button:
                break
        
        if not ellipsis_button:
            # Fallback
            ellipsis_button = svgs[0].find_element(By.XPATH, "..")
            print(f"  Using fallback parent")
        
        ellipsis_button.click()
        print("[OK] Clicked ellipsis")
        time.sleep(2)
        
        # Click "About this account"
        print(f"\n[4/6] Clicking 'About this account'...")
        about_buttons = scraper.driver.find_elements(By.XPATH, "//*[contains(text(), 'About this account')]")
        
        if not about_buttons:
            print("[X] 'About this account' not found")
            return False
        
        about_buttons[0].click()
        print("[OK] Clicked 'About this account'")
        
        # Wait for modal content to change
        print(f"\n[5/6] Waiting for About modal to load...")
        max_wait = 10
        modal_loaded = False
        
        for i in range(max_wait):
            time.sleep(1)
            try:
                modal = scraper.driver.find_element(By.XPATH, "//div[@role='dialog']")
                modal_text = modal.text
                
                # Check if modal contains "Account based in" or similar
                if 'account based in' in modal_text.lower() or 'date joined' in modal_text.lower():
                    modal_loaded = True
                    print(f"[OK] About modal loaded after {i+1} seconds")
                    break
                else:
                    print(f"  Waiting... ({i+1}/{max_wait}) - current text: {modal_text[:50]}...")
            except:
                print(f"  Waiting... ({i+1}/{max_wait}) - no modal found")
        
        if not modal_loaded:
            print("[X] About modal did not load")
            scraper.driver.save_screenshot("failed_modal.png")
            return False
        
        # Extract country
        print(f"\n[6/6] Extracting country...")
        try:
            modal = scraper.driver.find_element(By.XPATH, "//div[@role='dialog']")
            modal_text = modal.text
            print(f"\n[MODAL TEXT]:\n{'-'*60}\n{modal_text}\n{'-'*60}\n")
            
            import re
            patterns = [
                r'Account based in[\s\n]+([A-Za-z\s]+?)(?:\n|Date|To help|$)',
                r'based in[\s\n]+([A-Za-z\s]+?)(?:\n|Date|To help|$)',
            ]
            
            country = None
            for pattern in patterns:
                match = re.search(pattern, modal_text, re.IGNORECASE | re.MULTILINE)
                if match:
                    country = match.group(1).strip()
                    country = ' '.join(country.split())
                    country = re.sub(r'\s+(Date|To|help|keep|our).*$', '', country, flags=re.IGNORECASE)
                    print(f"\n[SUCCESS] Country extracted: '{country}'")
                    break
            
            if country:
                print(f"\n[OK] TEST PASSED!")
                return True
            else:
                print(f"\n[X] Could not parse country from modal")
                return False
                
        except Exception as e:
            print(f"[X] Error: {e}")
            import traceback
            traceback.print_exc()
            return False
            
    except Exception as e:
        print(f"\n[X] Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        print("\n" + "=" * 60)
        print("Keeping browser open for 15 seconds...")
        print("=" * 60)
        time.sleep(15)
        scraper.close()

if __name__ == "__main__":
    success = final_test()
    
    print("\n" + "=" * 60)
    if success:
        print("[OK] TEST PASSED")
    else:
        print("[X] TEST FAILED")
    print("=" * 60)
    
    sys.exit(0 if success else 1)
