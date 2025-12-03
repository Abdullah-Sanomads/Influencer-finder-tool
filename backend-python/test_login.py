"""
Manual Login Test
Run this to see what's happening during login
"""

import os
import time
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager

load_dotenv()

username = os.getenv('INSTAGRAM_USERNAME')
password = os.getenv('INSTAGRAM_PASSWORD')

print("="*60)
print("Instagram Login Test")
print("="*60)
print(f"Username: {username}")
print(f"Password: {'*' * len(password)}")
print()
print("Starting browser (visible mode)...")
print()

# Start browser
options = webdriver.ChromeOptions()
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

try:
    # Go to Instagram
    print("1. Navigating to Instagram login page...")
    driver.get('https://www.instagram.com/accounts/login/')
    time.sleep(5)
    
    print("2. Looking for username field...")
    username_input = driver.find_element(By.NAME, 'username')
    
    print("3. Typing username...")
    username_input.clear()
    username_input.send_keys(username)
    time.sleep(2)
    
    print("4. Looking for password field...")
    password_input = driver.find_element(By.NAME, 'password')
    
    print("5. Typing password...")
    password_input.clear()
    password_input.send_keys(password)
    time.sleep(2)
    
    print("6. Pressing Enter to login...")
    password_input.send_keys(Keys.RETURN)
    
    print()
    print("="*60)
    print("WAITING 15 SECONDS - WATCH THE BROWSER!")
    print("="*60)
    print()
    print("Check if:")
    print("  - Login successful → You'll see Instagram feed")
    print("  - CAPTCHA appears → Instagram detected automation")
    print("  - Error message → Wrong credentials or account issue")
    print("  - Still on login page → Login failed")
    print()
    
    time.sleep(15)
    
    # Check result
    current_url = driver.current_url
    print(f"Current URL: {current_url}")
    print()
    
    if 'accounts/login' in current_url:
        print("❌ STILL ON LOGIN PAGE - Login failed!")
        print()
        print("Possible reasons:")
        print("  1. Wrong username or password")
        print("  2. Instagram requires verification (check email/phone)")
        print("  3. Account is locked or banned")
        print("  4. CAPTCHA or challenge required")
        print()
        print("Try logging in manually in the browser to verify credentials work.")
    elif 'challenge' in current_url:
        print("⚠️  CHALLENGE REQUIRED")
        print("Instagram is asking for verification.")
        print("This is common for automated logins.")
    else:
        print("✅ LOGIN SUCCESSFUL!")
        print("The credentials work!")
        
    print()
    print("Press Ctrl+C to close browser...")
    
    # Keep browser open
    while True:
        time.sleep(1)
        
except KeyboardInterrupt:
    print("\nClosing browser...")
except Exception as e:
    print(f"\n❌ ERROR: {e}")
finally:
    driver.quit()
    print("Done!")
