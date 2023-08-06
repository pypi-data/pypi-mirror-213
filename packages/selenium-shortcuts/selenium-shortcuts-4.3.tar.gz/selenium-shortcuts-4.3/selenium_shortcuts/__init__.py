import os, sys, subprocess, requests
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By

class setup_shortcuts:
    '''Shortcut functions for Selenium'''
    def __init__(self, browser='chrome', port=9222, wait_for=10, executable_path='chromedriver', headless=False, use_uc=False, browser_version=None, driver=None, profile=None, additional_options=[]):
        self.browser_process_id = None

        if not driver:
            try: # Check if Chrome is already started
                requests.get(f'http://localhost:{port}/json')
            except requests.exceptions.ConnectionError: # Otherwise, start Chrome
                self.open_chrome(browser, port, headless, profile, additional_options)
            
            options = webdriver.ChromeOptions()
            options.debugger_address = f'127.0.0.1:{port}' # Must be 127.0.0.1 for undetected-chromedriver, not localhost
            if use_uc:
                import undetected_chromedriver as uc
                driver = uc.Chrome(options=options, use_subprocess=True, driver_executable_path=executable_path, version_main=browser_version)
                os.kill(driver.browser_pid, 15) # undetected-chromedriver connects to the existing browser then starts a browser on a random port, this closes the random browser
            else:
                driver = webdriver.Chrome(options=options, executable_path=executable_path)
                
        driver.implicitly_wait(wait_for) # Wait X seconds for element to load before raising error
        self.driver = driver
        self.wait_for = wait_for
        
    def find(self, css_selector, attribute=None, parent=None):
        if not parent:
            parent = self.driver
        element = parent.find_element(By.CSS_SELECTOR, css_selector)
        if attribute:
            attribute = element.get_attribute(attribute)
            return element, attribute
        return element

    def find_by_text(self, text, attribute=None, parent=None):
        if not parent:
            parent = self.driver
        element = parent.find_element(By.XPATH, f'//*[text()[contains(.,"{text}")]]')
        if attribute:
            attribute = element.get_attribute(attribute)
            return element, attribute
        return element

    def finds(self, css_selector, parent=None, wait_for=None):
        if not parent:
            parent = self.driver
        if wait_for:
            self.driver.implicitly_wait(wait_for)
        elements = parent.find_elements(By.CSS_SELECTOR, css_selector)
        if wait_for:
            self.driver.implicitly_wait(self.wait_for)
        return elements

    def click(self, css_selector, parent=None):
        if not parent:
            parent = self.driver
        element = parent.find_element(By.CSS_SELECTOR, css_selector)
        element.click()

    def click_by_text(self, text, parent=None):
        if not parent:
            parent = self.driver
        element = parent.find_element(By.XPATH, f'//*[text()[contains(.,"{text}")]]')
        element.click()

    def text(self, css_selector, parent=None):
        if not parent:
            parent = self.driver
        element = parent.find_element(By.CSS_SELECTOR, css_selector)
        return element.text

    def send(self, css_selector, text, clear=False, parent=None):
        if not parent:
            parent = self.driver
        element = parent.find_element(By.CSS_SELECTOR, css_selector)
        if clear:
            element.clear()
        element.send_keys(text)
    
    def get(self, url, check_current_url=True, parent=None):
        if not parent:
            parent = self.driver
        if not check_current_url or parent.current_url != url:
            parent.get(url)

    def check(self, css_selector, parent=None, check_visible=True, multiple=False):
        if not parent:
            parent = self.driver
        self.driver.implicitly_wait(1)
        elements = parent.find_elements(By.CSS_SELECTOR, css_selector)
        self.driver.implicitly_wait(self.wait_for)
        if elements:
            if not check_visible or elements[-1].is_displayed():
                if not multiple:
                    return elements[0]
                else:
                    return elements
        return []

    def check_by_text(self, text, parent=None, check_visible=True, multiple=False):
        if not parent:
            parent = self.driver
        self.driver.implicitly_wait(1)
        elements = parent.find_elements(By.XPATH, f'//*[text()[contains(.,"{text}")]]')
        self.driver.implicitly_wait(self.wait_for)
        if elements:
            if not check_visible or elements[-1].is_displayed():
                if not multiple:
                    return elements[0]
                else:
                    return elements
        return []
    
    def find_chrome_location(self, browser):
        if sys.platform == 'win32':
            folders_chrome_could_be_installed_to = [
                os.environ.get('PROGRAMFILES'),
                os.environ.get('PROGRAMFILES(X86)'),
                os.environ.get('LOCALAPPDATA')
                ]
            for folder in folders_chrome_could_be_installed_to:
                if browser == 'chromium':
                    chrome_location = f'{folder}/Chromium/Application/chrome.exe'
                else:
                    chrome_location = f'{folder}/Google/Chrome/Application/chrome.exe'
                if os.path.exists(chrome_location):
                    return chrome_location
        else:
            if browser == 'chromium':
                chrome_location = '/Applications/Chromium.app/Contents/MacOS/Chromium'
            else:
                chrome_location = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
            if os.path.exists(chrome_location):
                return chrome_location
        raise RuntimeError("Couldn't find a Chrome install")
    
    def open_chrome(self, browser, port, headless, profile, additional_options):
        chrome_location = self.find_chrome_location(browser)

        if not profile:
            profile = f'--user-data-dir={os.getcwd()}/profile'
        launch_arguments = [
            f'--remote-debugging-port={port}',
            profile,
            '--no-default-browser-check', # Works
            '--credentials_enable_service=false', '--profile.password_manager_enabled=false', '--disable-save-password-bubble', '--disable-notifications' # Unknown
            ]
        if not os.path.exists(profile) and all('window-size' not in option for option in additional_options):
            launch_arguments.append('--start-maximized')
        if headless:
            launch_arguments += ['--headless', '--window-size=1920,1080', '--no-sandbox']
        if additional_options:
            launch_arguments += additional_options

        self.browser_process_id = subprocess.Popen([chrome_location] + launch_arguments).pid
        sleep(1)
    
    def close(self):
        if self.browser_process_id:
            os.kill(self.browser_process_id, 15)
        else:
            self.driver.quit()