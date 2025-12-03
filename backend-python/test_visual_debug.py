"""
Visual debug test - take screenshots at each step
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

def visual_debug():
    """Visual debugging with screenshots"""
    
    print("=" * 60)
    print("VISUAL DEBUG: Taking screenshots at each step")
    print("=" * 60)
    
    scraper = InstagramScraper(headless=False)
    
    try:
        # Start and login
        print("\n[1/7] Starting browser and logging in...")
        if not scraper.start_browser() or not scraper.login():
            print("[X] Failed to start/login")
            return False
        print("[OK] Ready")
        
        # Navigate
        test_username = "deeafitness_"
        print(f"\n[2/7] Navigating to @{test_username}...")
        scraper.driver.get(f'https://www.instagram.com/{test_username}/')
        time.sleep(5)
        scraper.driver.save_screenshot("step1_profile_loaded.png")
        print("[OK] Profile loaded - screenshot saved: step1_profile_loaded.png")
        
        # Find ellipsis button
        print(f"\n[3/7] Finding ellipsis button...")
        svgs = scraper.driver.find_elements(By.XPATH, "//*[name()='svg' and @aria-label='Options']")
        print(f"  Found {len(svgs)} SVG elements")
        
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
                        print(f"  Found button at level {level}, tag={tag}, role={role}")
                        break
                        
                    onclick = parent.get_attribute('onclick')
                    if onclick:
                        ellipsis_button = parent
                        print(f"  Found clickable parent with onclick at level {level}")
                        break
                        
                    current = parent
                except:
                    break
            if ellipsis_button:
                break
        
        # Fallback: use immediate parent
        if not ellipsis_button and len(svgs) > 0:
            try:
                parent = svgs[0].find_element(By.XPATH, "..")
                ellipsis_button = parent
                print(f"  Using SVG's immediate parent as fallback (tag={parent.tag_name})")
            except:
                pass
        
        if not ellipsis_button:
            print("[X] Ellipsis button not found")
            return False
        
        print("[OK] Found ellipsis button")
        
        # Click ellipsis
        print(f"\n[4/7] Clicking ellipsis button...")
        ellipsis_button.click()
        time.sleep(2)
        scraper.driver.save_screenshot("step2_menu_opened.png")
        print("[OK] Menu opened - screenshot saved: step2_menu_opened.png")
        
        # Find and click "About this account"
        print(f"\n[5/7] Looking for 'About this account' option...")
        about_buttons = scraper.driver.find_elements(By.XPATH, "//*[contains(text(), 'About this account')]")
        print(f"  Found {len(about_buttons)} elements with 'About this account' text")
        
        if not about_buttons:
            print("[X] 'About this account' not found")
            return False
        
        print(f"\n[6/7] Clicking 'About this account'...")
        about_buttons[0].click()
        time.sleep(5)  # Wait longer
        scraper.driver.save_screenshot("step3_about_modal.png")
        print("[OK] Clicked - screenshot saved: step3_about_modal.png")
        
        # Extract modal text
        print(f"\n[7/7] Extracting modal text...")
        try:
            modal = scraper.driver.find_element(By.XPATH, "//div[@role='dialog']")
            modal_text = modal.text
            print(f"\n[MODAL TEXT]:\n{'-'*60}\n{modal_text}\n{'-'*60}\n")
            
            # Try to extract country
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
                return True
            else:
                print(f"\n[X] Could not parse country from modal text")
                print(f"\n[INFO] Please check the screenshots to see what happened")
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
        print("Keeping browser open for 20 seconds for review...")
        print("Check the screenshots in the backend-python folder")
        print("=" * 60)
        time.sleep(20)
        scraper.close()

if __name__ == "__main__":
    success = visual_debug()
    
    print("\n" + "=" * 60)
    if success:
        print("[OK] TEST PASSED")
    else:
        print("[X] TEST FAILED - Check screenshots for details")
    print("=" * 60)
    
    sys.exit(0 if success else 1)
