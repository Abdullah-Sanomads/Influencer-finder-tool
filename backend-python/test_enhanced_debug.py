"""
Enhanced debug test - try to find the ellipsis menu with scrolling and alternative methods
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
from selenium.webdriver.common.action_chains import ActionChains

def enhanced_debug():
    """Enhanced debugging with more thorough element search"""
    
    print("=" * 60)
    print("ENHANCED DEBUG: Finding Ellipsis Menu")
    print("=" * 60)
    
    # Initialize scraper
    scraper = InstagramScraper(headless=False)
    
    try:
        # Start browser
        print("\n[1/6] Starting browser...")
        if not scraper.start_browser():
            print("[X] Failed to start browser")
            return False
        print("[OK] Browser started")
        
        # Login
        print("\n[2/6] Logging in...")
        if not scraper.login():
            print("[X] Failed to login")
            return False
        print("[OK] Logged in")
        
        # Navigate to profile
        test_username = "deeafitness_"
        print(f"\n[3/6] Navigating to @{test_username}...")
        scraper.driver.get(f'https://www.instagram.com/{test_username}/')
        time.sleep(5)
        print("[OK] Profile loaded")
        
        # Look for ALL buttons on the page
        print(f"\n[4/6] Searching for all buttons on page...")
        all_buttons = scraper.driver.find_elements(By.TAG_NAME, "button")
        print(f"[DEBUG] Total buttons found: {len(all_buttons)}")
        
        ellipsis_button = None
        for i, btn in enumerate(all_buttons):
            try:
                text = btn.text.strip()
                aria_label = btn.get_attribute('aria-label') or ''
                
                # Check if this is the ellipsis button
                if '...' in text or 'more options' in aria_label.lower() or 'options' in aria_label.lower():
                    print(f"\n[FOUND] Potential ellipsis button #{i}:")
                    print(f"  Text: '{text}'")
                    print(f"  Aria-label: '{aria_label}'")
                    print(f"  Visible: {btn.is_displayed()}")
                    print(f"  Location: {btn.location}")
                    
                    if btn.is_displayed():
                        ellipsis_button = btn
                        break
            except:
                continue
        
        if not ellipsis_button:
            print("\n[WARNING] Ellipsis button not found in standard buttons")
            print("[INFO] Trying alternative approach - looking for SVG elements...")
            
            # Try to find SVG with specific characteristics
            svgs = scraper.driver.find_elements(By.TAG_NAME, "svg")
            print(f"[DEBUG] Total SVG elements: {len(svgs)}")
            
            for i, svg in enumerate(svgs[:20]):  # Check first 20 SVGs
                try:
                    aria_label = svg.get_attribute('aria-label') or ''
                    if 'more' in aria_label.lower() or 'option' in aria_label.lower():
                        print(f"\n[FOUND] Potential SVG #{i}:")
                        print(f"  Aria-label: '{aria_label}'")
                        # Get parent button
                        parent = svg.find_element(By.XPATH, "..")
                        if parent.tag_name == 'button':
                            ellipsis_button = parent
                            print(f"  Parent is button - using this!")
                            break
                except:
                    continue
        
        # Try clicking the ellipsis button
        print(f"\n[5/6] Attempting to click ellipsis and extract country...")
        if ellipsis_button:
            try:
                # Scroll to button
                scraper.driver.execute_script("arguments[0].scrollIntoView(true);", ellipsis_button)
                time.sleep(1)
                
                # Click it
                print("[INFO] Clicking ellipsis button...")
                ellipsis_button.click()
                time.sleep(2)
                
                # Look for "About this account" option
                print("[INFO] Looking for 'About this account' option...")
                about_elements = scraper.driver.find_elements(By.XPATH, "//*[contains(text(), 'About this account')]")
                
                if about_elements:
                    print(f"[FOUND] 'About this account' option - clicking...")
                    about_elements[0].click()
                    time.sleep(3)
                    
                    # Extract from modal
                    print("[INFO] Extracting country from modal...")
                    try:
                        modal = scraper.driver.find_element(By.XPATH, "//div[@role='dialog']")
                        modal_text = modal.text
                        print(f"\n[MODAL TEXT]:\n{modal_text}\n")
                        
                        # Parse country
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
                            print(f"\n[OK] TEST PASSED - Country: {country}")
                            return True
                        else:
                            print(f"\n[X] Could not parse country from modal text")
                            return False
                            
                    except Exception as e:
                        print(f"[X] Error extracting from modal: {e}")
                        return False
                else:
                    print("[X] 'About this account' option not found in menu")
                    # Take screenshot of menu
                    scraper.driver.save_screenshot("debug_menu.png")
                    print("[DEBUG] Screenshot of menu saved to debug_menu.png")
                    return False
                    
            except Exception as e:
                print(f"[X] Error clicking ellipsis: {e}")
                import traceback
                traceback.print_exc()
                return False
        else:
            print("[X] Could not find ellipsis button")
            print("[INFO] This might mean:")
            print("  1. You need to be logged in to see the menu")
            print("  2. The profile is private")
            print("  3. Instagram's UI has changed")
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
    success = enhanced_debug()
    
    print("\n" + "=" * 60)
    if success:
        print("[OK] TEST PASSED")
    else:
        print("[X] TEST FAILED")
    print("=" * 60)
    
    sys.exit(0 if success else 1)
