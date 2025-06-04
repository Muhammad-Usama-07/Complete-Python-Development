import json  # For working with JSON data
import time  # For adding delays
import os  # For interacting with the operating system
import random  # For generating random numbers
import undetected_chromedriver as uc  # For using undetected ChromeDriver to avoid detection by websites
from selenium.webdriver.common.by import By  # For locating elements in Selenium
from selenium.common.exceptions import NoSuchElementException, TimeoutException  # For handling Selenium exceptions
from selenium.webdriver.support.ui import WebDriverWait  # For waiting for elements in Selenium
from selenium.webdriver.support import expected_conditions as EC  # For using expected conditions with WebDriverWait
from packages.gls import GeolocationSpoofer  # For spoofing geolocation
from packages.extension import add_proxy  # For adding proxy configurations
import tempfile  # For creating temporary directories
import shutil  # For file and directory operations
import re  # For regular expressions
import subprocess  # For running shell commands
from datetime import datetime  # For working with date and time
from PIL import Image  # For handling images
from io import BytesIO  # For handling byte streams
import pdb
import logging
import psutil
logger = logging.getLogger(__name__)  # Gets the same config

# Configure logging at the start of your application
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        # logging.FileHandler("application.log"),
        logging.StreamHandler()
    ]
)

# Suppress logging for these libraries (add PIL to the list)
noisy_libraries = [
    'selenium',
    'urllib3', 
    'PIL',                # Main PIL logger
    'PIL.PngImagePlugin', # Specifically for PNG debug messages
    'PIL.Image',           # General image processing
    'undetected_chromedriver.patcher',
    'root'
]

for lib in noisy_libraries:
    logging.getLogger(lib).setLevel(logging.WARNING)

class DriverConfig:
    def __init__(self, json_data):
        self.token_id = json_data['token_id']
        self.user_agent = json_data['browser_details']['user_agent']
        self.lang = json_data['browser_details']['language']
        self.geo_loc = json_data['browser_details']['geo_location']
        self.timezone = json_data['browser_details']['timezone']
        self.profile_name = json_data['profile_details']['profile_name']
        self.email = json_data['profile_details']['account_details']['login']['mail']
        self.password = json_data['profile_details']['account_details']['login']['password']
        self.recov_email = json_data['profile_details']['account_details']['password_recovery']['recovery_mailbox']
        self.proxy_ip = json_data['proxy_details']['ip']
        self.proxy_port = json_data['proxy_details']['port']
        self.proxy_username = json_data['proxy_details']['username']
        self.proxy_password = json_data['proxy_details']['password']
        self.device_matrix = json_data['device_matrix']

    def match_profile(self, usr_data_dir, prof_name, mail):
        profile_path = os.path.join(usr_data_dir, prof_name)
        prefs_path = os.path.join(profile_path, "Preferences")
        try:
            with open(prefs_path, 'r', encoding='utf-8') as file:  # Open file with UTF-8 encoding
                prof_pref_data = json.load(file)
            profile_email = prof_pref_data['account_info'][0]['email']
            if os.path.isdir(profile_path) and profile_email == mail:
                return profile_path
        except FileNotFoundError:
            # print(f"{e} not exists")
            pass
        except (json.JSONDecodeError, KeyError, IndexError) as e:
            return None


    def create_chrome_profile(self, user_data_dir, profile_name):
        profile_path = os.path.join(user_data_dir, profile_name)  # Create profile path
        if not os.path.exists(profile_path):  # Check if profile path exists
            os.makedirs(profile_path)  # Create profile path if it does not exist
        subdirs = ["Default", "Extension State", "IndexedDB", "Local Storage", "Sessions", "blob_storage"]  # List of subdirectories to create
        for subdir in subdirs:
            os.makedirs(os.path.join(profile_path, subdir), exist_ok=True)  # Create subdirectories
        preferences_file = os.path.join(profile_path, "Default", "Preferences")  # Path to preferences file
        with open(preferences_file, "w") as f:  # Open preferences file in write mode
            f.write('{"profile":{"exit_type":"Normal"}}')  # Write default preferences

    def check_xpath_exists(self, driver, xpath, timeout=60): 
        try: 
            WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((By.XPATH, xpath)))  # Wait until the element is located
            return True 
        except (NoSuchElementException, TimeoutException):  # Handle exceptions if element is not found
            return False
        
    def save_screenshot(self, image, token_id, image_name):

        img_file_path = f"{token_id}/screenshots/{image_name}.png"

        # Save the image to a file
        image.save(img_file_path)

    def sign_in_working(self, driver, mail, pas, recovery_email):
        log_message = f"TOKEN_ID {self.token_id}: signing mail"
        logger.info(log_message)
        try:
            
            if self.check_xpath_exists(driver, '//input[@type="email"] | //input[@aria-label="Email or phone"]', timeout=60):  # Check if email input field exists
                

                sign_in = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//input[@type="email"]')))  # Wait for email input field
                for char in mail:  # Type email character by character
                    time.sleep(random.uniform(0.1, 0.5))  # Add random delay between keystrokes
                    sign_in.send_keys(char)
                time.sleep(random.uniform(0.1, 0.5))  # Add random delay
                screenshot = driver.get_screenshot_as_png()
                screenshot_img = Image.open(BytesIO(screenshot))
                date_time_prog = datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
                log_message = f"TOKEN_ID {self.token_id}: email written"
                logger.info(log_message)
                filename = f"{log_message.split(': ')[-1]}_{date_time_prog}"
                self.save_screenshot(screenshot_img, self.token_id, filename)

                driver.find_element(By.XPATH, "//*[@type='button']/span[text()='Next']").click()  # Click Next button
                screenshot = driver.get_screenshot_as_png()
                screenshot_img = Image.open(BytesIO(screenshot))
                date_time_prog = datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
                log_message = f"TOKEN_ID {self.token_id}: clicked on next button"
                logger.info(log_message)
                filename = f"{log_message.split(': ')[-1]}_{date_time_prog}"
                self.save_screenshot(screenshot_img, self.token_id, filename)


                WebDriverWait(driver, 20).until(
                    lambda d: d.execute_script("return document.readyState") == "complete"
                ) # Wait for the page to load completely
                if self.check_xpath_exists(driver, '//input[@type="password"] | //input[@aria-label="Enter your password"]', timeout=60):
                    WebDriverWait(driver, 20).until(
                    lambda d: d.execute_script("return document.readyState") == "complete"
                ) # Wait for the page to load completely
                    pass_btn = WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, '//input[@type="password"] | //input[@aria-label="Enter your password"]')))  # Wait for password input field
                    for char in pas:  # Type password character by character
                        time.sleep(random.uniform(0.1, 0.5))  # Add random delay between keystrokes
                        pass_btn.send_keys(char)
                    time.sleep(random.uniform(0.1, 0.5))  # Add random delay
                    WebDriverWait(driver, 60).until(
                        lambda d: d.execute_script("return document.readyState") == "complete"
                    ) # Wait for the page to load completely

                    screenshot = driver.get_screenshot_as_png()
                    screenshot_img = Image.open(BytesIO(screenshot))
                    date_time_prog = datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
                    log_message = f"TOKEN_ID {self.token_id}: password written"
                    logger.info(log_message)
                    filename = f"{log_message.split(': ')[-1]}_{date_time_prog}"
                    self.save_screenshot(screenshot_img, self.token_id, filename)

                    driver.find_element(By.XPATH, "//*[@type='button']/span[text()='Next']").click()  # Click Next button
                    WebDriverWait(driver, 20).until(
                        lambda d: d.execute_script("return document.readyState") == "complete"
                    ) # Wait for the page to load completely

                    screenshot = driver.get_screenshot_as_png()
                    screenshot_img = Image.open(BytesIO(screenshot))
                    date_time_prog = datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
                    log_message = f"TOKEN_ID {self.token_id}: clicked on next button"
                    logger.info(log_message)
                    filename = f"{log_message.split(': ')[-1]}_{date_time_prog}"
                    self.save_screenshot(screenshot_img, self.token_id, filename)

                    if self.check_xpath_exists(driver, "//a[text()='Inbox']", timeout=60):  # Check if email input field exists
                        WebDriverWait(driver, 20).until(
                            lambda d: d.execute_script("return document.readyState") == "complete"
                        ) # Wait for the page to load completely
                        screenshot = driver.get_screenshot_as_png()
                        screenshot_img = Image.open(BytesIO(screenshot))
                        date_time_prog = datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
                        log_message = f"TOKEN_ID {self.token_id}: logged in successfully"
                        logger.info(log_message)
                        filename = f"{log_message.split(': ')[-1]}_{date_time_prog}"

                        self.save_screenshot(screenshot_img, self.token_id, filename)

                    ##### check recovery email
                    elif self.check_xpath_exists(driver, "//span[text()='Verify it’s you']", timeout=60):
                        screenshot = driver.get_screenshot_as_png()
                        screenshot_img = Image.open(BytesIO(screenshot))
                        date_time_prog = datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
                        log_message = f"TOKEN_ID {self.token_id}: verify window detected"
                        logger.info(log_message)
                        filename = f"{log_message.split(': ')[-1]}_{date_time_prog}"
                        self.save_screenshot(screenshot_img, self.token_id, filename)


                        time.sleep(random.uniform(1, 5))  # Add random delay
                        WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, "//div[text()='Confirm your recovery email']"))).click()
                        WebDriverWait(driver, 20).until(
                            lambda d: d.execute_script("return document.readyState") == "complete"
                        ) # Wait for the page to load completely
                        screenshot = driver.get_screenshot_as_png()
                        screenshot_img = Image.open(BytesIO(screenshot))
                        date_time_prog = datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
                        log_message = f"TOKEN_ID {self.token_id}: confirm your recovery email"
                        logger.info(log_message)
                        filename = f"{log_message.split(': ')[-1]}_{date_time_prog}"
                        self.save_screenshot(screenshot_img, self.token_id, filename)

                        time.sleep(random.uniform(0.1, 3))  # Add random delay
                        recov_input = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//input[@aria-label='Enter recovery email address']")))  # Wait for email input field
                        for char in recovery_email:  # Type email character by character
                            time.sleep(random.uniform(0.1, 1))  # Add random delay between keystrokes
                            recov_input.send_keys(char)
                        time.sleep(random.uniform(0.1, 0.5))  # Add random delay
                        WebDriverWait(driver, 20).until(
                            lambda d: d.execute_script("return document.readyState") == "complete"
                        ) # Wait for the page to load completely
                        screenshot = driver.get_screenshot_as_png()
                        screenshot_img = Image.open(BytesIO(screenshot))
                        date_time_prog = datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
                        log_message = f"TOKEN_ID {self.token_id}: recovery mail entered"
                        logger.info(log_message)
                        filename = f"{log_message.split(': ')[-1]}_{date_time_prog}"
                        self.save_screenshot(screenshot_img, self.token_id, filename)
                        driver.find_element(By.XPATH, "//*[@type='button']/span[text()='Next']").click()  # Click Next button

                    else:
                        screenshot = driver.get_screenshot_as_png()
                        screenshot_img = Image.open(BytesIO(screenshot))
                        date_time_prog = datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
                        log_message = f"TOKEN_ID {self.token_id}: unable to open mailbox"
                        logger.error(log_message)
                        filename = f"{log_message.split(': ')[-1]}_{date_time_prog}"
                        self.save_screenshot(screenshot_img, self.token_id, filename)
                else:
                    screenshot = driver.get_screenshot_as_png()
                    screenshot_img = Image.open(BytesIO(screenshot))
                    date_time_prog = datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
                    log_message = f"TOKEN_ID {self.token_id}: unable to find password input field"
                    logger.error(log_message)
                    filename = f"{log_message.split(': ')[-1]}_{date_time_prog}"
                    self.save_screenshot(screenshot_img, self.token_id, filename)
            else:
                screenshot = driver.get_screenshot_as_png()
                screenshot_img = Image.open(BytesIO(screenshot))
                date_time_prog = datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
                log_message = f"TOKEN_ID {self.token_id}: unable to find input field"
                logger.error(log_message)
                filename = f"{log_message.split(': ')[-1]}_{date_time_prog}"
                self.save_screenshot(screenshot_img, self.token_id, filename)
                
        except Exception as e:  # Handle any other exceptions
            screenshot = driver.get_screenshot_as_png()
            screenshot_img = Image.open(BytesIO(screenshot))
            date_time_prog = datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
            log_message = f"DRIVER CONFIG - TOKEN_ID: {self.token_id}: error occurred {e}"
            logger.error(log_message)
            filename = f"{log_message.split(': ')[-1]}_{date_time_prog}"
            self.save_screenshot(screenshot_img, self.token_id, filename)
            driver.quit()

    def configure_driver(self):
        logs_ss = {'logs': [], 'ss': {}}
        log_message = f"TOKEN_ID {self.token_id}: configuring driver"
        logger.info(log_message)
        def get_chrome_version():
            """Detect installed Chrome version (Windows)"""
            try:
                # Method 1: Read from registry (most reliable)
                cmd = r'reg query "HKEY_CURRENT_USER\Software\Google\Chrome\BLBeacon" /v version'
                output = subprocess.check_output(cmd, shell=True, stderr=subprocess.DEVNULL).decode()
                version = re.search(r"\d+\.\d+\.\d+", output).group()
                return version.split(".")[0]  # Return major version (e.g., "134")
            except subprocess.CalledProcessError:
                try:
                    # Method 2: Check default install path
                    chrome_path = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
                    version_str = subprocess.check_output(
                        f'wmic datafile where name="{chrome_path}" get Version /value',
                        shell=True
                    ).decode().strip()
                    return version_str.split("=")[1].split(".")[0]  # return version value
                except (subprocess.CalledProcessError, IndexError, AttributeError):
                    return None

        chrome_major_version = get_chrome_version()
        
        chrome_options = uc.ChromeOptions()  # Create ChromeOptions object
        chrome_options.add_argument(f"--user-agent={self.user_agent}")  # Include user agent
        chrome_options.add_argument("--disable-gpu")  # Disable GPU
        chrome_options.add_argument("--no-sandbox")  # Disable sandbox
        chrome_options.add_argument("--disable-infobars")  # Disable infobars
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")  # Disable automation controlled features
        chrome_options.add_argument('--disable-webrtc')  # Disable WebRTC


        base_dir = os.path.join(os.getcwd(), "chrome_profiles")  # Store profiles in a 'chrome_profiles' folder

        profile_name = self.profile_name
        user_data_dir = os.path.join(base_dir, profile_name)
        os.makedirs(user_data_dir, exist_ok=True)  # Ensure unique directory exists
        
        chrome_options.add_argument(f"--user-data-dir={user_data_dir}")  # Add user data directory to Chrome options

        matched_profile = self.match_profile(user_data_dir, profile_name, self.email)  # Check if profile exists
        if matched_profile:
            log_message = f"TOKEN_ID {self.token_id}: profile exists"
            logger.info(log_message)
            chrome_options.add_argument(f"--profile-directory={profile_name}")  # Add profile directory to Chrome options
            
        else:
            time.sleep(3)  # Wait for 3 seconds
            log_message = f"TOKEN_ID {self.token_id}: profile not exists!"
            logger.info(log_message)
            time.sleep(1)  # Wait for 1 second
            log_message = f"TOKEN_ID {self.token_id}: creating profile"
            logger.info(log_message)


            self.create_chrome_profile(user_data_dir, profile_name)  # Create profile
            chrome_options.add_argument(f"--profile-directory={profile_name}")  # Add profile directory to Chrome options
            log_message = f"TOKEN_ID {self.token_id}: profile created!"
            logger.info(log_message)


        if os.path.isdir(os.path.join('proxies', self.proxy_username)):  # Check if proxy username is a directory
            proxies_extension = os.path.join(os.getcwd(), 'proxies', self.proxy_username)  # Set proxies extension path dynamically
            # print(f"------ proxies_extension path: {proxies_extension}")

        else:
            proxies_extension = add_proxy(self.proxy_ip, self.proxy_port, self.proxy_username, self.proxy_password)  # Add proxy

        chrome_options.add_argument("--disable-extensions-except=" + proxies_extension)
        chrome_options.add_argument(f"--load-extension={proxies_extension}")
                
        # Rest of your driver configuration...
        try:
            # pdb.set_trace()
            driver = uc.Chrome(
                options=chrome_options,
                version_main=int(chrome_major_version),
                use_subprocess=True,
                timeout=120
            )
            driver.execute_cdp_cmd('Emulation.setTimezoneOverride', self.timezone)
            spoofer = GeolocationSpoofer(latitude=self.geo_loc['latitude'], 
                                        longitude=self.geo_loc['longitude'])
            driver = spoofer.spoof_geolocation(driver)
            driver.get('about:blank')

            time.sleep(5)
            
            ########## validate ip code 
            current_browser_ip = driver.execute_script("""
                return new Promise((resolve, reject) => {
                    var xhr = new XMLHttpRequest();
                    xhr.open('GET', 'https://api.ipify.org?format=json');
                    xhr.onload = function() {
                        if (xhr.status === 200) {
                            resolve(JSON.parse(xhr.responseText).ip);
                        } else {
                            reject(new Error('Request failed'));
                        }
                    };
                    xhr.onerror = function() {
                        reject(new Error('Request error'));
                    };
                    xhr.send();
                });
            """)

            if current_browser_ip == self.proxy_ip:
                log_message = f"TOKEN_ID {self.token_id}: IP validated on browser"
                logger.info(log_message)
                ##### opening mailbox
                time.sleep(3)
                driver.get("https://mail.google.com")
                time.sleep(2)
                driver.maximize_window()

                
                try:
                    sign_in_path = "(//*[@class='button__label' and text()='Sign in'])"
                    WebDriverWait(driver, 20).until(
                        lambda d: d.execute_script("return document.readyState") == "complete"
                    ) # Wait for the page to load completely
                    if self.check_xpath_exists(driver, "//a[text()='Inbox']", timeout=5):  # Check if already in inbox
                        screenshot = driver.get_screenshot_as_png()
                        screenshot_img = Image.open(BytesIO(screenshot))
                        date_time_prog = datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
                        log_message = f"TOKEN_ID {self.token_id}: mailbox opened successfully"
                        logger.info(log_message)
                        filename = f"{log_message.split(': ')[-1]}_{date_time_prog}"
                        self.save_screenshot(screenshot_img, self.token_id, filename)
                        
                    elif self.check_xpath_exists(driver, '//input[@type="email"] | //input[@aria-label="Email or phone"]', timeout=60):  # Check if email input field exists
                        log_message = f"TOKEN_ID {self.token_id}: found input email field"
                        logger.info(log_message)
                        self.sign_in_working(driver, self.email, self.password, self.recov_email)  # Enter email and password

                    elif WebDriverWait(driver, 60).until(EC.presence_of_all_elements_located((By.XPATH, sign_in_path))):  # Check if sign in button exists
                        sign_in_buttons = WebDriverWait(driver, 60).until(EC.presence_of_all_elements_located((By.XPATH, sign_in_path)))
                        if len(sign_in_buttons) > 1:
                            sign_in_path = sign_in_path + "[2]"
                        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, sign_in_path))).click()
                        self.sign_in_working(driver, self.email, self.password, self.recov_email)  # Enter email and password
                
                    elif self.check_xpath_exists(driver, '//*[@id="password"]/div[1]/div/div[1]//input', timeout=5):  # Check if password input field exists
                        pass_btn = WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, '//*[@id="password"]/div[1]/div/div[1]//input')))  # Wait for password input field
                        for char in self.password:  # Type password character by character
                            time.sleep(random.uniform(0.1, 0.5))  # Add random delay between keystrokes
                            pass_btn.send_keys(char)
                        time.sleep(random.uniform(0.1, 0.5))  # Add random delay
                        driver.find_element(By.XPATH, "//*[@type='button']/span[text()='Next']").click()  # Click Next button
                    
                    else:
                        screenshot = driver.get_screenshot_as_png()
                        screenshot_img = Image.open(BytesIO(screenshot))
                        date_time_prog = datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
                        log_message = f"TOKEN_ID {self.token_id}: Unable to sign in ---> {self.token_id}"
                        logger.error(log_message)
                        filename = f"{log_message.split(': ')[-1]}_{date_time_prog}"
                        self.save_screenshot(screenshot_img, self.token_id, filename)
                        driver.quit()
                        return f"unable to sign in: {str(e)} ---> {self.token_id}", logs_ss
                    # print('logs_ss_sign_in', logs_ss_sign_in)
                    
                    time.sleep(10)  # Wait for 10 seconds
                    return driver

                except Exception as e:  # Handle any other exceptions
                    # print(f"An unexpected error occurred on {self.token_id}: {e}")
                    screenshot = driver.get_screenshot_as_png()
                    screenshot_img = Image.open(BytesIO(screenshot))
                    date_time_prog = datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
                    log_message = f"TOKEN_ID {self.token_id}: An unexpected error occurred {e} ---> {self.token_id}"
                    logger.error(log_message)
                    filename = f"{log_message.split(': ')[-1]}_{date_time_prog}"
                    self.save_screenshot(screenshot_img, self.token_id, filename)
                    driver.quit()
                    return log_message
            else:
                log_message = f"TOKEN_ID {self.token_id}: unable to apply ip on the browser ---> {self.token_id}"
                logger.error(log_message)
                return log_message
            
        except Exception as e:
            screenshot = driver.get_screenshot_as_png()
            screenshot_img = Image.open(BytesIO(screenshot))
            date_time_prog = datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
            filename = f"{log_message.split(': ')[-1]}_{date_time_prog}"
            self.save_screenshot(screenshot_img, self.token_id, filename)
            driver.quit()
            log_message = f"TOKEN_ID {self.token_id}: Error in post-init configuration ---> {self.token_id}: {str(e)} "
            logger.error(log_message)
            return log_message


