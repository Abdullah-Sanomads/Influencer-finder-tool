"""
Test script to verify Instagram scraper setup
This will test browser initialization without actually logging in
"""

import sys
import os

# Fix encoding for Windows
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

print("="*60)
print("Instagram Scraper - Setup Test")
print("="*60)
print()

# Test 1: Check Python version
print("1. Checking Python version...")
print(f"   [OK] Python {sys.version.split()[0]}")
print()

# Test 2: Check imports
print("2. Checking required packages...")
try:
    import selenium
    print(f"   [OK] selenium {selenium.__version__}")
except ImportError as e:
    print(f"   [ERROR] selenium not found: {e}")
    sys.exit(1)

try:
    from webdriver_manager.chrome import ChromeDriverManager
    print(f"   [OK] webdriver-manager installed")
except ImportError as e:
    print(f"   [ERROR] webdriver-manager not found: {e}")
    sys.exit(1)

try:
    import flask
    print(f"   [OK] flask {flask.__version__}")
except ImportError as e:
    print(f"   [ERROR] flask not found: {e}")
    sys.exit(1)

try:
    from flask_cors import CORS
    print(f"   [OK] flask-cors installed")
except ImportError as e:
    print(f"   [ERROR] flask-cors not found: {e}")
    sys.exit(1)

try:
    from dotenv import load_dotenv
    print(f"   [OK] python-dotenv installed")
except ImportError as e:
    print(f"   [ERROR] python-dotenv not found: {e}")
    sys.exit(1)

try:
    from fake_useragent import UserAgent
    print(f"   [OK] fake-useragent installed")
except ImportError as e:
    print(f"   [ERROR] fake-useragent not found: {e}")
    sys.exit(1)

print()

# Test 3: Check .env file
print("3. Checking configuration...")
if os.path.exists('.env'):
    print("   [OK] .env file found")
    load_dotenv()
    
    username = os.getenv('INSTAGRAM_USERNAME', '')
    password = os.getenv('INSTAGRAM_PASSWORD', '')
    
    if username and password:
        print(f"   [OK] Instagram credentials configured (@{username})")
    else:
        print("   [WARN]  Instagram credentials not set in .env")
        print("      Please copy .env.example to .env and add your credentials")
else:
    print("   [WARN]  .env file not found")
    print("      Please copy .env.example to .env and configure it")
print()

# Test 4: Test browser initialization
print("4. Testing browser initialization...")
print("   This may take 10-20 seconds on first run...")
try:
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service
    from webdriver_manager.chrome import ChromeDriverManager
    
    options = webdriver.ChromeOptions()
    options.add_argument('--headless=new')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.get('https://www.google.com')
    
    if 'Google' in driver.title:
        print("   [OK] Browser initialized successfully")
        print("   [OK] ChromeDriver auto-installed")
    else:
        print("   [WARN]  Browser opened but unexpected page loaded")
    
    driver.quit()
    print("   [OK] Browser closed successfully")
    
except Exception as e:
    print(f"   [ERROR] Browser initialization failed: {e}")
    print()
    print("   Troubleshooting:")
    print("   - Make sure Chrome browser is installed")
    print("   - Try updating Chrome to the latest version")
    print("   - Check if any antivirus is blocking Chrome")
    sys.exit(1)

print()
print("="*60)
print("[OK] All tests passed!")
print("="*60)
print()
print("Next steps:")
print("1. Configure Instagram credentials in .env file")
print("2. (Optional) Configure proxy in .env for better success rate")
print("3. Run: python server.py")
print()
print("[WARN]  IMPORTANT REMINDERS:")
print("   - Use a throwaway Instagram account (not your personal one)")
print("   - Expect slow performance (2-5 min per search)")
print("   - Account may get banned - this is normal for web scraping")
print("   - Consider using demo mode instead for testing")
print()
