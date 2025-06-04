import json  # Importing the json module to work with JSON data
import time  # Importing the time module to add delays
import pandas as pd  # Importing pandas for data manipulation and analysis
import os  # Importing os module to interact with the operating system
import random  # Importing random module to generate random numbers
from packages.extension import add_proxy  # Importing add_proxy function from extension_pkg
import undetected_chromedriver as uc  # Importing undetected_chromedriver to avoid detection by websites
from selenium.webdriver.common.by import By  # Importing By class to locate elements
from selenium.common.exceptions import NoSuchElementException, TimeoutException, NoSuchWindowException  # Importing exceptions from selenium
from selenium.webdriver.support.ui import WebDriverWait  # Importing WebDriverWait to wait for elements
from selenium.webdriver.support import expected_conditions as EC  # Importing expected_conditions to use with WebDriverWait
from packages.gls import GeolocationSpoofer  # Importing GeolocationSpoofer class from check.gls
import pdb
import math
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.common.keys import Keys
import selenium
from PIL import Image
from io import BytesIO
from datetime import datetime
def check_xpath_exists(driver, xpath, timeout=10): 
    try: 
        WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((By.XPATH, xpath)))  # Wait until the element is located
        return True 
    except (NoSuchElementException, TimeoutException):  # Handle exceptions if element is not found
        return False

class GmailServices:
    def __init__(self, mail, pas, driver):
        self.mail = mail
        self.pas = pas
        self.driver = driver

    ##### ====================== inbox working start ====================== #####
    
    ##### go to inbox
    def go_to_inbox(self):
        logs_ss = {'logs': [], 'ss': {}}
        inbox_xpath = "//a[contains(@href, '#inbox') and @tabindex='-1']"

        if check_xpath_exists(self.driver, inbox_xpath):
            date_time_prog = datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
            log_message = f"\n\n\t{'*' * 2} navigating to Inbox. {'*' * 2} at {date_time_prog} {'*' * 2}\n"
            print(log_message)
            logs_ss['logs'].append(log_message)

            WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, inbox_xpath))).click()
            date_time_prog = datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
            log_message = f"\n\n\t{'*' * 2} successfully arrived in inbox. {'*' * 2} at {date_time_prog} {'*' * 2}\n"
            logs_ss['logs'].append(log_message)
            print(log_message)

        else:
            date_time_prog = datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
            log_message = f"\n\n\t{'*' * 2} already in inbox. {'*' * 2}  at {date_time_prog} {'*' * 2}\n"
            print(log_message)
            logs_ss['logs'].append(log_message)

        screenshot = self.driver.get_screenshot_as_png()
        inbox_screenshot = Image.open(BytesIO(screenshot))
        
        filename = log_message.replace('*', '').strip().replace(' ', '_')
        logs_ss['ss'][f"{filename}_{date_time_prog}"] = inbox_screenshot
        return self.driver, logs_ss
     
    ##### go to promotions
    def go_to_promotion(self):
        logs_ss = {'logs': [], 'ss': {}}
        time.sleep(random.uniform(5, 8))
        if not check_xpath_exists(self.driver, "//a[contains(@href, '#inbox') and @tabindex='0']"):  # Check if not in inbox
            date_time_prog = datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
            log_message = f"\n\n\t{'*' * 2} clicking inbox {'*' * 2} at {date_time_prog} {'*' * 2}\n"
            print(log_message)
            logs_ss['logs'].append(log_message)
            WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, "//a[text()='Inbox']"))).click()  # Click Inbox link
            screenshot = self.driver.get_screenshot_as_png()
            inbox_click_screenshot = Image.open(BytesIO(screenshot))
            date_time_prog = datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
            log_message = f"\n\n\t{'*' * 2} arrived in inbox {'*' * 2} at {date_time_prog} {'*' * 2}\n"
            print(log_message)
            logs_ss['logs'].append(log_message)
            filename = log_message.replace('*', '').strip().replace(' ', '_')
            logs_ss['ss'][f"{filename}_{datetime.now().strftime('%Y-%m-%d_%H_%M_%S')}"] = inbox_click_screenshot
        else:
            screenshot = self.driver.get_screenshot_as_png()
            inbox_screenshot = Image.open(BytesIO(screenshot))
            date_time_prog = datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
            log_message = f"\n\n\t{'*' * 2} already in inbox {'*' * 2} at {date_time_prog} {'*' * 2}\n"
            print(log_message)
            filename = log_message.replace('*', '').strip().replace(' ', '_')
            logs_ss['ss'][f"{filename}_{datetime.now().strftime('%Y-%m-%d_%H_%M_%S')}"] = inbox_screenshot

        time.sleep(3)
        WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, "//div[text()='Promotions']"))).click()  # Click More button
        screenshot = self.driver.get_screenshot_as_png()
        date_time_prog = datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
        log_message = f"\n\n\t{'*' * 2} arrived in promotions {'*' * 2} at {date_time_prog} {'*' * 2}\n"
        print(log_message)
        promotion_screenshot = Image.open(BytesIO(screenshot))
        filename = log_message.replace('*', '').strip().replace(' ', '_')
        logs_ss['ss'][f"{filename}_{datetime.now().strftime('%Y-%m-%d_%H_%M_%S')}"] = promotion_screenshot


        return self.driver, logs_ss

    ##### ====================== inbox working end ====================== #####

    ##### ====================== general working start ====================== #####

    ##### select all
    # ########### logs and screenshot reamininig 
    def select_all(self):
        time.sleep(random.uniform(1, 5))
        logs_ss = {'logs': [], 'ss': {}}
        select_all = "(//span[@role='checkbox'])"
        select_buttons = WebDriverWait(self.driver, 60).until(
                EC.presence_of_all_elements_located((By.XPATH, select_all))
            )
        if len(select_buttons) > 1:
            select_all = select_all + "[2]"
        
        if check_xpath_exists(self.driver, select_all):
            WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, select_all))).click()
            time.sleep(3)
            screenshot = self.driver.get_screenshot_as_png()
            screenshot_img = Image.open(BytesIO(screenshot))
            date_time_prog = datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
            log_message = f"\n\n\t{'*' * 2} all selected. {'*' * 2} at {date_time_prog} {'*' * 2}\n"
            filename = log_message.replace('*', '').strip().replace(' ', '_')
            logs_ss['ss'][f"{filename}_{date_time_prog}"] = screenshot_img
            logs_ss['logs'].append(log_message)
            print(log_message)

        else:
            screenshot = self.driver.get_screenshot_as_png()
            screenshot_img = Image.open(BytesIO(screenshot))
            date_time_prog = datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
            log_message = f"\n\n\t{'*' * 2} error in selecting all. {'*' * 2} at {date_time_prog} {'*' * 2}\n"
            filename = log_message.replace('*', '').strip().replace(' ', '_')
            logs_ss['ss'][f"{filename}_{date_time_prog}"] = screenshot_img
            logs_ss['logs'].append(log_message)
            print(log_message)
        
        time.sleep(random.uniform(1, 5))
        return self.driver, logs_ss


    ##### select message
    def select_message(self, numb_mess):
        time.sleep(random.uniform(5, 10))
        logs_ss = {'logs': [], 'ss': {}}
        log_message = f"\n\n\t{'*' * 2} selecting message. {'*' * 2}\n"
        print(log_message)
        logs_ss['logs'].append(log_message)
        

        
        
        table_grid = "(//table[@role='grid'])"
        len_of_messages = WebDriverWait(self.driver, 60).until(EC.presence_of_all_elements_located((By.XPATH, table_grid)))
        if len(len_of_messages) > 1:
            
            if check_xpath_exists(self.driver, table_grid + "[2]/tbody/tr"):
                table_grid = table_grid + "[2]"
                table_grid_clickable = "("+table_grid+"/tbody/tr)"+ "[{}]".format(numb_mess) + "/td[@data-tooltip='Select']/div[@role='checkbox']"
                WebDriverWait(self.driver, 60).until(EC.presence_of_element_located((By.XPATH, table_grid_clickable))).click()
                log_message = f"\n\n\t{'*' * 2} message selected. {'*' * 2}\n"
                screenshot = self.driver.get_screenshot_as_png()
                print(log_message)

            elif check_xpath_exists(self.driver, table_grid + "[1]/tbody/tr"):
                
                table_grid = table_grid + "[1]"
                table_grid_clickable = "("+table_grid+"/tbody/tr)"+ "[{}]".format(numb_mess) + "/td[@data-tooltip='Select']/div[@role='checkbox']"
                WebDriverWait(self.driver, 60).until(EC.presence_of_element_located((By.XPATH, table_grid_clickable))).click()
                log_message = f"\n\n\t{'*' * 2} message selected. {'*' * 2}\n"
                screenshot = self.driver.get_screenshot_as_png()
                print(log_message)
                
            else:
                log_message = f"\n{'-' * 5} error in selecting message {'-' * 5}\n"
                screenshot = self.driver.get_screenshot_as_png()
                print(log_message)  # Print error message
            
            

        elif len(len_of_messages) < 2:

            table_grid_clickable = "("+table_grid+"/tbody/tr)" + "[{}]".format(numb_mess) + "/td[@data-tooltip='Select']/div[@role='checkbox']"
            WebDriverWait(self.driver, 60).until(EC.presence_of_element_located((By.XPATH, table_grid_clickable))).click()
            log_message = f"\n\n\t{'*' * 2} message selected. {'*' * 2}\n"
            screenshot = self.driver.get_screenshot_as_png()
             
        else:
            log_message = f"\n{'-' * 5} error in selecting message {'-' * 5}\n"
            screenshot = self.driver.get_screenshot_as_png()
        logs_ss['logs'].append(log_message)
        selected_screenshot = Image.open(BytesIO(screenshot))
        filename = log_message.replace('*', '').strip().replace(' ', '_')
        logs_ss['ss'][f"{filename}_{datetime.now().strftime('%Y-%m-%d_%H_%M_%S')}"] = selected_screenshot
        return self.driver, logs_ss

    ##### search working
    def search(self, search_query):
        time.sleep(random.uniform(5, 10))
        logs_ss = {'logs': [], 'ss': {}}
        date_time_prog = datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
        log_message = f"\n\n\t{'*' * 2} searching message {'*' * 2} at {date_time_prog} {'*' * 2}\n"
        print(log_message)
        logs_ss['logs'].append(log_message)
        # Click the search button
        if WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, "//input[@aria-label='Search mail' and @placeholder='Search mail' and @type='text']"))):
            WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, "//input[@aria-label='Search mail' and @placeholder='Search mail' and @type='text']"))).click()
            screenshot = self.driver.get_screenshot_as_png()
            log_message = f"\n\n\t{'*' * 2} clicked on search field {'*' * 2} at {date_time_prog} {'*' * 2}\n"
            search_clicked_screenshot = Image.open(BytesIO(screenshot))
            filename = log_message.replace('*', '').strip().replace(' at ', '').replace(' ', '_')
            date_time_prog = datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
            logs_ss['ss'][f"{filename}_{date_time_prog}"] = search_clicked_screenshot    
            logs_ss['logs'].append(log_message)
            print(log_message)

            # Use a single XPath expression to find the input field directly from the label 
            input_field = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, "//input[@aria-label='Search mail' and @placeholder='Search mail' and @type='text']")))
            # input_field.click()
            for char in search_query:  # Type email character by character
                time.sleep(random.uniform(0.1, 1))  # Add random delay between keystrokes
                input_field.send_keys(char)
            # time.sleep(random.uniform(5, 10))
            time.sleep(random.uniform(0.5, 1))  # Optional sleep before hitting Enter
            input_field.send_keys(Keys.RETURN)
            # WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, "//div[text()='Search'  and @role='button']"))).click()
            
            screenshot = self.driver.get_screenshot_as_png()
            text_searched_screenshot = Image.open(BytesIO(screenshot))
            date_time_prog = datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
            log_message = f"\n\n\t{'*' * 2} text searched {'*' * 2} at {date_time_prog} {'*' * 2}\n"
            filename = log_message.replace('*', '').strip().replace(' at ', '').replace(' ', '_')
            logs_ss['ss'][f"{filename}_{date_time_prog}"] = text_searched_screenshot    
            logs_ss['logs'].append(log_message)
            print(log_message)

            time.sleep(5)
            screenshot = self.driver.get_screenshot_as_png()
            text_searched_screenshot = Image.open(BytesIO(screenshot))
            date_time_prog = datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
            log_message = f"\n\n\t{'*' * 2} search result {'*' * 2} at {date_time_prog} {'*' * 2} \n"
            filename = log_message.replace('*', '').strip().replace(' at ', '').replace(' ', '_')
            logs_ss['ss'][f"{filename}_{date_time_prog}"] = text_searched_screenshot    
            logs_ss['logs'].append(log_message)
            print(log_message)


        else:
            print(f"\n{'-' * 5} error in searching {'-' * 5}\n")
        time.sleep(random.uniform(5, 10))
        return self.driver, logs_ss


    ##### search by from
    def search_by_from(self, search_query):
        time.sleep(random.uniform(5, 10))
        logs_ss = {'logs': [], 'ss': {}}
        date_time_prog = datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
        log_message = f"\n\n\t{'*' * 2} searching message {'*' * 2} at {date_time_prog} {'*' * 2}\n"
        print(log_message)
        logs_ss['logs'].append(log_message)

        search_xpath = "//button[@data-tooltip='Show search options']"
        if check_xpath_exists(self.driver, search_xpath):
            time.sleep(random.uniform(5, 10))
            WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, "//button[@data-tooltip='Show search options']"))).click()
            screenshot = self.driver.get_screenshot_as_png()
            show_search_screenshot = Image.open(BytesIO(screenshot))
            log_message = f"\n\n\t{'*' * 2} clicked on show search options {'*' * 2} at {date_time_prog} {'*' * 2}\n"
            filename = log_message.replace('*', '').strip().replace(' at ', '').replace(' ', '_')
            date_time_prog = datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
            logs_ss['ss'][f"{filename}_{date_time_prog}"] = show_search_screenshot    
            logs_ss['logs'].append(log_message)
            print(log_message)
            
            # Use a single XPath expression to find the input field directly from the label 
            input_field = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, "//label[text()='From']/following::input[@type='text']")))
            # input_field.click()
            for char in search_query:  # Type email character by character
                time.sleep(random.uniform(0.1, 1))  # Add random delay between keystrokes
                input_field.send_keys(char)

            screenshot = self.driver.get_screenshot_as_png()
            text_written_screenshot = Image.open(BytesIO(screenshot))
            date_time_prog = datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
            log_message = f"\n\n\t{'*' * 2} text written {'*' * 2} at {date_time_prog} {'*' * 2}\n"
            filename = log_message.replace('*', '').strip().replace(' at ', '').replace(' ', '_')
            logs_ss['ss'][f"{filename}_{date_time_prog}"] = text_written_screenshot    
            logs_ss['logs'].append(log_message)
            print(log_message)


            time.sleep(random.uniform(1, 5))
            WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, "//div[text()='Search'  and @role='button']"))).click()
            screenshot = self.driver.get_screenshot_as_png()
            search_result_screenshot = Image.open(BytesIO(screenshot))
            date_time_prog = datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
            log_message = f"\n\n\t{'*' * 2} search result {'*' * 2} at {date_time_prog} {'*' * 2}\n"
            filename = log_message.replace('*', '').strip().replace(' at ', '').replace(' ', '_')
            logs_ss['ss'][f"{filename}_{date_time_prog}"] = search_result_screenshot    
            logs_ss['logs'].append(log_message)
            print(log_message)

        else:
            screenshot = self.driver.get_screenshot_as_png()
            error_screenshot = Image.open(BytesIO(screenshot))
            date_time_prog = datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
            log_message = f"\n\n\t{'*' * 2} error in searching using from {'*' * 2} at {date_time_prog} {'*' * 2}\n"
            filename = log_message.replace('*', '').strip().replace(' at ', '').replace(' ', '_')
            logs_ss['ss'][f"{filename}_{date_time_prog}"] = error_screenshot    
            logs_ss['logs'].append(log_message)
            print(log_message)

        return self.driver, logs_ss
    
    ##### search by to
    def search_by_to(self, search_query):
        time.sleep(random.uniform(5, 10))
        logs_ss = {'logs': [], 'ss': {}}
        date_time_prog = datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
        log_message = f"\n\n\t{'*' * 2} searching message {'*' * 2} at {date_time_prog} {'*' * 2}\n"
        print(log_message)
        logs_ss['logs'].append(log_message)

        search_xpath = "//button[@data-tooltip='Show search options']"
        # if WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, "//button[@data-tooltip='Show search options']"))):
        if check_xpath_exists(self.driver, search_xpath):
            time.sleep(random.uniform(5, 10))
            WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, "//button[@data-tooltip='Show search options']"))).click()
            screenshot = self.driver.get_screenshot_as_png()
            show_search_screenshot = Image.open(BytesIO(screenshot))
            log_message = f"\n\n\t{'*' * 2} clicked on show search options {'*' * 2} at {date_time_prog} {'*' * 2}\n"
            filename = log_message.replace('*', '').strip().replace(' at ', '').replace(' ', '_')
            date_time_prog = datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
            logs_ss['ss'][f"{filename}_{date_time_prog}"] = show_search_screenshot    
            logs_ss['logs'].append(log_message)
            print(log_message)


            # Use a single XPath expression to find the input field directly from the label 
            input_field = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, "//label[text()='To']/following::input[@type='text']")))
            # input_field.click()
            for char in search_query:  # Type email character by character
                time.sleep(random.uniform(0.1, 1))  # Add random delay between keystrokes
                input_field.send_keys(char)

            screenshot = self.driver.get_screenshot_as_png()
            text_written_screenshot = Image.open(BytesIO(screenshot))
            date_time_prog = datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
            log_message = f"\n\n\t{'*' * 2} text written {'*' * 2} at {date_time_prog} {'*' * 2}\n"
            filename = log_message.replace('*', '').strip().replace(' at ', '').replace(' ', '_')
            logs_ss['ss'][f"{filename}_{date_time_prog}"] = text_written_screenshot    
            logs_ss['logs'].append(log_message)
            print(log_message)


            time.sleep(random.uniform(1, 5))
            WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, "//div[text()='Search'  and @role='button']"))).click()
            screenshot = self.driver.get_screenshot_as_png()
            search_result_screenshot = Image.open(BytesIO(screenshot))
            date_time_prog = datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
            log_message = f"\n\n\t{'*' * 2} search result {'*' * 2} at {date_time_prog} {'*' * 2}\n"
            filename = log_message.replace('*', '').strip().replace(' at ', '').replace(' ', '_')
            logs_ss['ss'][f"{filename}_{date_time_prog}"] = search_result_screenshot    
            logs_ss['logs'].append(log_message)
            print(log_message)
        else:
            screenshot = self.driver.get_screenshot_as_png()
            error_screenshot = Image.open(BytesIO(screenshot))
            date_time_prog = datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
            log_message = f"\n\n\t{'*' * 2} error in searching using to {'*' * 2} at {date_time_prog} {'*' * 2}\n"
            filename = log_message.replace('*', '').strip().replace(' at ', '').replace(' ', '_')
            logs_ss['ss'][f"{filename}_{date_time_prog}"] = error_screenshot    
            logs_ss['logs'].append(log_message)
            print(log_message)

        return self.driver, logs_ss

    ##### search by subject
    def search_by_subject(self, search_query):
        time.sleep(random.uniform(5, 10))
        logs_ss = {'logs': [], 'ss': {}}
        date_time_prog = datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
        log_message = f"\n\n\t{'*' * 2} searching message {'*' * 2} at {date_time_prog} {'*' * 2}\n"
        print(log_message)
        logs_ss['logs'].append(log_message)
        search_xpath = "//button[@data-tooltip='Show search options']"
        if check_xpath_exists(self.driver, search_xpath):
            time.sleep(random.uniform(5, 10))
            WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, "//button[@data-tooltip='Show search options']"))).click()
            screenshot = self.driver.get_screenshot_as_png()
            show_search_screenshot = Image.open(BytesIO(screenshot))
            log_message = f"\n\n\t{'*' * 2} clicked on show search options {'*' * 2} at {date_time_prog} {'*' * 2}\n"
            filename = log_message.replace('*', '').strip().replace(' at ', '').replace(' ', '_')
            date_time_prog = datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
            logs_ss['ss'][f"{filename}_{date_time_prog}"] = show_search_screenshot    
            logs_ss['logs'].append(log_message)
            print(log_message)

            # Use a single XPath expression to find the input field directly from the label 
            input_field = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, "//label[text()='Subject']/following::input[@type='text']")))
            for char in search_query:
                time.sleep(random.uniform(0.1, 1))
                input_field.send_keys(char)
            screenshot = self.driver.get_screenshot_as_png()
            text_written_screenshot = Image.open(BytesIO(screenshot))
            date_time_prog = datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
            log_message = f"\n\n\t{'*' * 2} text written {'*' * 2} at {date_time_prog} {'*' * 2}\n"
            filename = log_message.replace('*', '').strip().replace(' at ', '').replace(' ', '_')
            logs_ss['ss'][f"{filename}_{date_time_prog}"] = text_written_screenshot    
            logs_ss['logs'].append(log_message)
            print(log_message)

            time.sleep(random.uniform(1, 5))
            
            WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, "//div[text()='Search'  and @role='button']"))).click()
            screenshot = self.driver.get_screenshot_as_png()
            search_result_screenshot = Image.open(BytesIO(screenshot))
            date_time_prog = datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
            log_message = f"\n\n\t{'*' * 2} search result {'*' * 2} at {date_time_prog} {'*' * 2}\n"
            filename = log_message.replace('*', '').strip().replace(' at ', '').replace(' ', '_')
            logs_ss['ss'][f"{filename}_{date_time_prog}"] = search_result_screenshot    
            logs_ss['logs'].append(log_message)
            print(log_message)
        else:
            screenshot = self.driver.get_screenshot_as_png()
            error_screenshot = Image.open(BytesIO(screenshot))
            date_time_prog = datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
            log_message = f"\n\n\t{'*' * 2} error in searching using subject {'*' * 2} at {date_time_prog} {'*' * 2}\n"
            filename = log_message.replace('*', '').strip().replace(' at ', '').replace(' ', '_')
            logs_ss['ss'][f"{filename}_{date_time_prog}"] = error_screenshot    
            logs_ss['logs'].append(log_message)
            print(log_message)
        return self.driver, logs_ss

    ##### open message working
    def open_message(self, msg_no=None):
        time.sleep(random.uniform(5, 10))
        logs_ss = {'logs': [], 'ss': {}}
        date_time_prog = datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
        log_message = f"\n\n\t{'*' * 2} opening message {msg_no } {'*' * 2} at {date_time_prog} {'*' * 2}\n"
        print(log_message)
        logs_ss['logs'].append(log_message)

        if msg_no is not None:
            table_xpath = "((//table[@role='grid']))"

            # Wait for the table to be present
            table = WebDriverWait(self.driver, 60).until(
                EC.presence_of_all_elements_located((By.XPATH, table_xpath))
            )
            if len(table) > 1:

                if check_xpath_exists(self.driver, table_xpath + "[2]/tbody/tr"):
                    table_xpath = table_xpath + "[2]"
                    WebDriverWait(self.driver, 60).until(
                        EC.presence_of_element_located((By.XPATH, "("+ table_xpath + f"//tr)[{msg_no}]"))
                    ).click()
                    date_time_prog = datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
                    log_message = f"\n\n\t{'*' * 2} message {msg_no } opened successfully {'*' * 2} at {date_time_prog} {'*' * 2}\n"
                    logs_ss['logs'].append(log_message)
                    screenshot = self.driver.get_screenshot_as_png()
                    filename = log_message.replace('*', '').strip().replace(' at ', '').replace(' ', '_')
                    print(log_message)

                elif check_xpath_exists(self.driver, table_xpath + "[1]/tbody/tr"):
                    
                    table_xpath = table_xpath + "[1]"
                    WebDriverWait(self.driver, 60).until(
                        EC.presence_of_element_located((By.XPATH, "("+ table_xpath + f"//tr)[{msg_no}]"))
                    ).click()
                    date_time_prog = datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
                    log_message = f"\n\n\t{'*' * 2} message {msg_no } opened successfully {'*' * 2} at {date_time_prog} {'*' * 2}\n"
                    logs_ss['logs'].append(log_message)
                    screenshot = self.driver.get_screenshot_as_png()
                    filename = log_message.replace('*', '').strip().replace(' at ', '').replace(' ', '_')
                    print(log_message)

                else:
                    date_time_prog = datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
                    log_message = f"\n\n\t{'-' * 5} error in opening message {'-' * 5} at {date_time_prog} {'-' * 5}\n"
                    logs_ss['logs'].append(log_message)
                    screenshot = self.driver.get_screenshot_as_png()
                    filename = log_message.replace('*', '').strip().replace(' at ', '').replace(' ', '_')
                    print(log_message)


            elif len(table) < 2:
                WebDriverWait(self.driver, 60).until(
                    EC.presence_of_element_located((By.XPATH, "("+ table_xpath + f"//tr)[{msg_no}]"))
                ).click()
                date_time_prog = datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
                log_message = f"\n\n\t{'*' * 2} message {msg_no } opened successfully {'*' * 2} at {date_time_prog} {'*' * 2}\n"
                logs_ss['logs'].append(log_message)
                screenshot = self.driver.get_screenshot_as_png()
                filename = log_message.replace('*', '').strip().replace(' at ', '').replace(' ', '_')
                print(log_message)

            else:
                date_time_prog = datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
                log_message = f"\n\n\t{'-' * 5} error in opening message {'-' * 5} at {date_time_prog} {'-' * 5}\n"
                logs_ss['logs'].append(log_message)
                filename = log_message.replace('*', '').strip().replace(' at ', '').replace(' ', '_')
                screenshot = self.driver.get_screenshot_as_png()
                print(log_message)
            

        else:
            date_time_prog = datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
            log_message = f"\n\n\t{'-' * 5} no message selected {'-' * 5} at {date_time_prog} {'-' * 5}\n"
            logs_ss['logs'].append(log_message)
            screenshot = self.driver.get_screenshot_as_png()
            filename = log_message.replace('*', '').strip().replace(' at ', '').replace(' ', '_')
            print(log_message)
        show_search_screenshot = Image.open(BytesIO(screenshot))
        logs_ss['ss'][f"{filename}_{date_time_prog}"] = show_search_screenshot 
        return self.driver, logs_ss
    
    ##### archive 
    # def archive_message(self):

    
    #     time.sleep(random.uniform(5, 10))
    #     archive = "//div[@title='Archive' and @role='button'] | //div[@aria-label='Archive' and @role='button']"
    #     if check_xpath_exists(self.driver, archive):
    #         WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, archive))).click()
    #         print(f"\n\n\t{'*' * 2} archived message{'*' * 2}\n")
    #         time.sleep(3)
    #     else:  # Print error message
    #         print(f"\n{'-' * 5} error in archiving {'-' * 5}\n")
    #         time.sleep(3)
    #     return self.driver

    ##### add to contacts 
    def add_to_contacts(self):
        # time.sleep(11111)
        time.sleep(random.uniform(3, 6))  # Reduced sleep time for better performance
        logs_ss = {'logs': [], 'ss': {}}
        try:
            # Wait for the icon to become visible and click it
            # icon_img = WebDriverWait(self.driver, 15).until(
            #     EC.visibility_of_element_located((By.XPATH, "//div[@class='aCi']/img | //div[@class='aCi']"))
            # )
            # icon_img.click()
            
            icon_img_path = "(//div[@class='aCi']/img | //div[@class='aCi'])"
            icon_img = WebDriverWait(self.driver, 60).until(
                    EC.presence_of_all_elements_located((By.XPATH, icon_img_path))
                )
            if len(icon_img) > 1:
                icon_img_path = icon_img_path + "[1]"

            WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, icon_img_path))).click()
            
            date_time_prog = datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
            log_message = f"\n\n\t{'*' * 2} clicked on message icon. {'*' * 2} at {date_time_prog} {'*' * 2}\n"
            logs_ss['logs'].append(log_message)
            screenshot = self.driver.get_screenshot_as_png()
            screenshot_image = Image.open(BytesIO(screenshot))
            filename = log_message.replace('*', '').strip().replace(' ', '_')
            logs_ss['ss'][f"{filename}_{date_time_prog}"] = screenshot_image
            print(log_message)

            # Switch to the iframe (ensure it exists before switching)
            iframe = WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.XPATH, "//iframe[contains(@name,'__HC_94253229') or contains(@name,'I__HC_94253229')]"))
            )
            self.driver.switch_to.frame(iframe)
            time.sleep(random.uniform(1, 5))  # Reduced sleep time for better performance
            date_time_prog = datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
            log_message = f"\n\n\t{'*' * 2} switch to frame. {'*' * 2} at {date_time_prog} {'*' * 2}\n"
            logs_ss['logs'].append(log_message)
            screenshot = self.driver.get_screenshot_as_png()
            screenshot_image = Image.open(BytesIO(screenshot))
            filename = log_message.replace('*', '').strip().replace(' ', '_')
            logs_ss['ss'][f"{filename}_{date_time_prog}"] = screenshot_image
            print(log_message)

            time.sleep(random.uniform(3, 6))
            try:
                # Wait for 'Add to contacts' button to be clickable and click it
                add_to_contacts_button = WebDriverWait(self.driver, 60).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Add to contacts']"))
                )
                add_to_contacts_button.click()
                date_time_prog = datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
                log_message = f"\n\n\t{'*' * 2} added to contacts. {'*' * 2} at {date_time_prog} {'*' * 2}\n"
                logs_ss['logs'].append(log_message)
                screenshot = self.driver.get_screenshot_as_png()
                screenshot_image = Image.open(BytesIO(screenshot))
                filename = log_message.replace('*', '').strip().replace(' ', '_')
                logs_ss['ss'][f"{filename}_{date_time_prog}"] = screenshot_image
                print(log_message)

            except TimeoutException:
                # If 'Add to contacts' isn't found, check for 'Edit contact' or 'Edit your info'
                try:
                    time.sleep(random.uniform(3, 6))

                    # edit_contact_button = WebDriverWait(self.driver, 60).until(
                    #     EC.element_to_be_clickable(
                    #         (By.XPATH, "//button[@aria-label='Edit contact' or @aria-label='Edit your info']")
                    #     )
                    # )
                    if check_xpath_exists(self.driver, "//button[@aria-label='Edit contact' or @aria-label='Edit your info']"):
                        date_time_prog = datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
                        log_message = f"\n\n\t{'*' * 2} contact already added. {'*' * 2} at {date_time_prog} {'*' * 2}\n"
                        logs_ss['logs'].append(log_message)
                        screenshot = self.driver.get_screenshot_as_png()
                        screenshot_image = Image.open(BytesIO(screenshot))
                        filename = log_message.replace('*', '').strip().replace(' ', '_')
                        logs_ss['ss'][f"{filename}_{date_time_prog}"] = screenshot_image
                        print(log_message)
                    else:
                        # time.sleep(1111111)
                        date_time_prog = datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
                        log_message = f"\n\n\t{'*' * 2} error in adding the contact. {'*' * 2} at {date_time_prog} {'*' * 2}\n"
                        logs_ss['logs'].append(log_message)
                        screenshot = self.driver.get_screenshot_as_png()
                        screenshot_image = Image.open(BytesIO(screenshot))
                        filename = log_message.replace('*', '').strip().replace(' ', '_')
                        logs_ss['ss'][f"{filename}_{date_time_prog}"] = screenshot_image
                        print(log_message)

                except TimeoutException:
                    date_time_prog = datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
                    log_message = f"\n\n\t{'*' * 2} error in adding the contact. {'*' * 2} at {date_time_prog} {'*' * 2}\n"
                    logs_ss['logs'].append(log_message)
                    screenshot = self.driver.get_screenshot_as_png()
                    screenshot_image = Image.open(BytesIO(screenshot))
                    filename = log_message.replace('*', '').strip().replace(' ', '_')
                    logs_ss['ss'][f"{filename}_{date_time_prog}"] = screenshot_image
                    print(log_message)

            # Switch back to the default content (main page)
            self.driver.switch_to.default_content()

            # Wait for 'Back to Inbox' button and click it
            back_to_inbox_button = WebDriverWait(self.driver, 60).until(EC.presence_of_element_located((By.XPATH, "//div[(@title='Back to Inbox' or @title='Back to Spam') and @role='button'] "))).click()
    
            # back_to_inbox_button.click()

            return self.driver, logs_ss

        except TimeoutException:
            date_time_prog = datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
            log_message = f"\n\n\t{'*' * 2} TimeoutException: Link not available. {'*' * 2} at {date_time_prog} {'*' * 2}\n"
            logs_ss['logs'].append(log_message)
            screenshot = self.driver.get_screenshot_as_png()
            screenshot_image = Image.open(BytesIO(screenshot))
            filename = log_message.replace('*', '').strip().replace(' ', '_')
            logs_ss['ss'][f"{filename}_{date_time_prog}"] = screenshot_image
            print(log_message)
            return self.driver, logs_ss
        
    ##### show image 
    def show_image(self):
        time.sleep(random.uniform(5, 10))
        try:
            if WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, "//button[text()='Show images']"))):
                WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, "//button[text()='Show images']"))).click()
                print(f"\n\n\t{'*' * 2} images shown {'*' * 2}\n")
                time.sleep(3)
            else:
                print(f"\n{'-' * 5} image not available{'-' * 5}\n")
        except TimeoutException:
            print(f"\n{'-' * 5} TimeoutException: image not available {'-' * 5}\n")
        WebDriverWait(self.driver, 60).until(EC.presence_of_element_located((By.XPATH, "//div[@title='Back to Inbox' and @role='button']"))).click()
        return self.driver

    ##### first link click
    def first_link_click(self):
        time.sleep(random.uniform(5, 10))
        logs_ss = {'logs': [], 'ss': {}}
        try:
            xpath = "//center/a/img | ((//td[@align='center'])[1]//a)"
            check_xpath = WebDriverWait(self.driver, 60).until(
                EC.presence_of_all_elements_located((By.XPATH, xpath))
            )
            if len(check_xpath) > 1:
                print(f"\n\n\t{'*' * 2} greater then 1 {'*' * 2}\n")
                xpath = xpath.split('| ')[1] + '[1]'
                if check_xpath_exists(self.driver, xpath+'/img'):
                    xpath = xpath + '/img'
                else:
                    xpath = xpath
            else:
                print(f"\n\n\t{'*' * 2} less then 1 {'*' * 2}\n")
                # print('')
            WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, xpath))).click()
            screenshot = self.driver.get_screenshot_as_png()
            screenshot_img = Image.open(BytesIO(screenshot))
            date_time_prog = datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
            log_message = f"\n\n\t{'*' * 2} clicked on first link. {'*' * 2} at {date_time_prog} {'*' * 2}\n"
            filename = log_message.replace('*', '').strip().replace(' ', '_')
            logs_ss['ss'][f"{filename}_{date_time_prog}"] = screenshot_img
            print(log_message)
            logs_ss['logs'].append(log_message)

            time.sleep(random.uniform(1, 5))
            self.driver.switch_to.window(self.driver.window_handles[1])
            screenshot = self.driver.get_screenshot_as_png()
            screenshot_img = Image.open(BytesIO(screenshot))
            date_time_prog = datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
            log_message = f"\n\n\t{'*' * 2} switched to second window. {'*' * 2} at {date_time_prog} {'*' * 2}\n"
            filename = log_message.replace('*', '').strip().replace(' ', '_')
            logs_ss['ss'][f"{filename}_{date_time_prog}"] = screenshot_img
            print(log_message)
            logs_ss['logs'].append(log_message)

            # time.sleep(100)
            # print(f"\n\n\t{'*' * 2} second command {'*' * 2}\n")

            time.sleep(random.uniform(1, 5))
            self.driver.switch_to.window(self.driver.window_handles[0])
            screenshot = self.driver.get_screenshot_as_png()
            screenshot_img = Image.open(BytesIO(screenshot))
            date_time_prog = datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
            log_message = f"\n\n\t{'*' * 2} switched to main window. {'*' * 2} at {date_time_prog} {'*' * 2}\n"
            filename = log_message.replace('*', '').strip().replace(' ', '_')
            logs_ss['ss'][f"{filename}_{date_time_prog}"] = screenshot_img
            print(log_message)
            logs_ss['logs'].append(log_message)
            # # self.driver.execute_script("window.close();")
            # # self.driver.close()
            # self.driver.switch_to.window(self.driver.window_handles[1])
        except TimeoutException:
            screenshot = self.driver.get_screenshot_as_png()
            screenshot_img = Image.open(BytesIO(screenshot))
            date_time_prog = datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
            # log_message = f"\n\n\t{'*' * 2} clicked on first link. {'*' * 2} at {date_time_prog} {'*' * 2}\n"
            log_message = f"\n\n\t{'*' * 2} TimeoutException: link not available. {'*' * 2} at {date_time_prog} {'*' * 2}\n"
            filename = log_message.replace('*', '').strip().replace(' ', '_')
            logs_ss['ss'][f"{filename}_{date_time_prog}"] = screenshot_img
            print(log_message)
            logs_ss['logs'].append(log_message)
        # WebDriverWait(self.driver, 60).until(EC.presence_of_element_located((By.XPATH, "//div[@title='Back to Inbox' and @role='button']"))).click()
        return self.driver, logs_ss

    ##### reply message
    def reply(self, message):
        time.sleep(random.uniform(5, 10))
        logs_ss = {'logs': [], 'ss': {}}
        try:
            if WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, "//span[text()='Reply' and @role='link']"))):
                WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, "//span[text()='Reply' and @role='link']"))).click()
                screenshot = self.driver.get_screenshot_as_png()
                screenshot_img = Image.open(BytesIO(screenshot))
                date_time_prog = datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
                log_message = f"\n\n\t{'*' * 2} clicked on reply button. {'*' * 2} at {date_time_prog} {'*' * 2}\n"
                filename = log_message.replace('*', '').strip().replace(' ', '_')
                logs_ss['ss'][f"{filename}_{date_time_prog}"] = screenshot_img
                print(log_message)
                logs_ss['logs'].append(log_message)

                time.sleep(random.uniform(1, 5))    
                input_field = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, "//div[@aria-label='Message Body']")))
                for char in message:
                    time.sleep(random.uniform(0.1, 1))
                    input_field.send_keys(char)

                screenshot = self.driver.get_screenshot_as_png()
                screenshot_img = Image.open(BytesIO(screenshot))
                date_time_prog = datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
                log_message = f"\n\n\t{'*' * 2} message written on text body. {'*' * 2} at {date_time_prog} {'*' * 2}\n"
                filename = log_message.replace('*', '').strip().replace(' ', '_')
                logs_ss['ss'][f"{filename}_{date_time_prog}"] = screenshot_img
                print(log_message)
                logs_ss['logs'].append(log_message)


                time.sleep(random.uniform(1, 5))
                WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, "//div[text()='Send']"))).click()    
                screenshot = self.driver.get_screenshot_as_png()
                screenshot_img = Image.open(BytesIO(screenshot))
                date_time_prog = datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
                log_message = f"\n\n\t{'*' * 2} replied. {'*' * 2} at {date_time_prog} {'*' * 2}\n"
                filename = log_message.replace('*', '').strip().replace(' ', '_')
                logs_ss['ss'][f"{filename}_{date_time_prog}"] = screenshot_img
                print(log_message)
                logs_ss['logs'].append(log_message)
                time.sleep(3)
            else:
                screenshot = self.driver.get_screenshot_as_png()
                screenshot_img = Image.open(BytesIO(screenshot))
                date_time_prog = datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
                log_message = f"\n\n\t{'*' * 2} reply not available. {'*' * 2} at {date_time_prog} {'*' * 2}\n"
                filename = log_message.replace('*', '').strip().replace(' ', '_')
                logs_ss['ss'][f"{filename}_{date_time_prog}"] = screenshot_img
                print(log_message)
                logs_ss['logs'].append(log_message)

        except TimeoutException:
            screenshot = self.driver.get_screenshot_as_png()
            screenshot_img = Image.open(BytesIO(screenshot))
            date_time_prog = datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
            log_message = f"\n\n\t{'*' * 2} TimeoutException: reply not available. {'*' * 2} at {date_time_prog} {'*' * 2}\n"
            filename = log_message.replace('*', '').strip().replace(' ', '_')
            logs_ss['ss'][f"{filename}_{date_time_prog}"] = screenshot_img
            print(log_message)
            logs_ss['logs'].append(log_message)
        return self.driver, logs_ss

    

    ##### mark as read working
    def mark_as_read(self):
        time.sleep(random.uniform(5, 10))

        if WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, "//div[@title='Mark as unread' and @role='button']"))):
            print(f"\n\n\t{'*' * 2} marked as read {'*' * 2}\n")
            time.sleep(3)
        # elif WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, "//div[@title='Mark as unread' and @role='button']"))):
        #     WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, "//div[@title='Mark as unread' and @role='button']"))).click()
        #     print(f"\n\n\t{'*' * 2} marked as read {'*' * 2}\n")
        #     time.sleep(3)
            
        else:
            print(f"\n{'-' * 5} error in making read {'-' * 5}\n")  # Print error message
            time.sleep(3)
        # WebDriverWait(self.driver, 60).until(EC.presence_of_element_located((By.XPATH, "//div[@title='Back to Inbox' and @role='button'] | //div[@title='Back to Spam']"))).click()
        return self.driver
    
    ##### mark as unread working
    def mark_as_unread(self):
        time.sleep(random.uniform(5, 10))
        logs_ss = {'logs': [], 'ss': {}}
        mark_as_unread = "//div[@title='Mark as unread' and @role='button']"
        if check_xpath_exists(self.driver, mark_as_unread):
            time.sleep(random.uniform(5, 10))
            WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, mark_as_unread))).click()
            screenshot = self.driver.get_screenshot_as_png()
            screenshot_img = Image.open(BytesIO(screenshot))
            date_time_prog = datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
            log_message = f"\n\n\t{'*' * 2} marked as unread. {'*' * 2} at {date_time_prog} {'*' * 2}\n"
            filename = log_message.replace('*', '').strip().replace(' ', '_')
            logs_ss['ss'][f"{filename}_{date_time_prog}"] = screenshot_img
            print(log_message)
            logs_ss['logs'].append(log_message)

        else:
            screenshot = self.driver.get_screenshot_as_png()
            screenshot_img = Image.open(BytesIO(screenshot))
            date_time_prog = datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
            log_message = f"\n\n\t{'*' * 2} error in making read. {'*' * 2} at {date_time_prog} {'*' * 2}\n"
            filename = log_message.replace('*', '').strip().replace(' ', '_')
            logs_ss['ss'][f"{filename}_{date_time_prog}"] = screenshot_img
            print(log_message)
            logs_ss['logs'].append(log_message)
        time.sleep(random.uniform(1, 5))
        # WebDriverWait(self.driver, 60).until(EC.presence_of_element_located((By.XPATH, "//div[@title='Back to Inbox' and @role='button'] | //div[@title='Back to Spam']"))).click()
        return self.driver, logs_ss
    
    
    ##### mark as important working
    def mark_as_important(self):
        # Reduced sleep time (if you really need random delay, this is a smaller range)
        time.sleep(random.uniform(3, 6))
        logs_ss = {'logs': [], 'ss': {}}
        more_options = "//div[@aria-label='More email options' and @aria-haspopup='true']"
        advance_toolbar = "//div[text()='Switch to advanced toolbar']"
        # simple_toolbar = "//div[text()='Switch to simple toolbar']"
        mark_important = "//div[text() = 'Mark as important']"
        not_important = "//div[text() = 'Mark as not important']"
        if check_xpath_exists(self.driver, more_options):

            date_time_prog = datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
            log_message = f"\n\n\t{'*' * 2} going to more options. {'*' * 2} at {date_time_prog} {'*' * 2}\n"
            logs_ss['logs'].append(log_message)
            print(log_message)

            WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, more_options))).click()
            screenshot = self.driver.get_screenshot_as_png()
            screenshot_img = Image.open(BytesIO(screenshot))
            date_time_prog = datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
            log_message = f"\n\n\t{'*' * 2} clicked on more options. {'*' * 2} at {date_time_prog} {'*' * 2}\n"
            filename = log_message.replace('*', '').strip().replace(' ', '_')
            logs_ss['ss'][f"{filename}_{date_time_prog}"] = screenshot_img
            print(log_message)
            logs_ss['logs'].append(log_message)
            time.sleep(3)

            if check_xpath_exists(self.driver, not_important):
                screenshot = self.driver.get_screenshot_as_png()
                screenshot_img = Image.open(BytesIO(screenshot))
                date_time_prog = datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
                log_message = f"\n\n\t{'*' * 2} already marked as important. {'*' * 2} at {date_time_prog} {'*' * 2}\n"
                filename = log_message.replace('*', '').strip().replace(' ', '_')
                logs_ss['ss'][f"{filename}_{date_time_prog}"] = screenshot_img
                print(log_message)
                logs_ss['logs'].append(log_message)
                
            elif check_xpath_exists(self.driver, advance_toolbar):
                # print(f"\n\n\t{'*' * 2} going to advance toolbar {'*' * 2}\n")
                WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, advance_toolbar))).click()
                screenshot = self.driver.get_screenshot_as_png()
                screenshot_img = Image.open(BytesIO(screenshot))
                date_time_prog = datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
                log_message = f"\n\n\t{'*' * 2} clicked on advance toolbar. {'*' * 2} at {date_time_prog} {'*' * 2}\n"
                filename = log_message.replace('*', '').strip().replace(' ', '_')
                logs_ss['ss'][f"{filename}_{date_time_prog}"] = screenshot_img
                print(log_message)
                logs_ss['logs'].append(log_message)

                time.sleep(3)
                if check_xpath_exists(self.driver, more_options):
                    WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, advance_toolbar))).click()
                    screenshot = self.driver.get_screenshot_as_png()
                    screenshot_img = Image.open(BytesIO(screenshot))
                    date_time_prog = datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
                    log_message = f"\n\n\t{'*' * 2} clicked on more options again. {'*' * 2} at {date_time_prog} {'*' * 2}\n"
                    filename = log_message.replace('*', '').strip().replace(' ', '_')
                    logs_ss['ss'][f"{filename}_{date_time_prog}"] = screenshot_img
                    print(log_message)
                    logs_ss['logs'].append(log_message)
                    
                    time.sleep(3)
            elif check_xpath_exists(self.driver, mark_important):
                WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, "//div[text()='Mark as important']"))).click()
                screenshot = self.driver.get_screenshot_as_png()
                screenshot_img = Image.open(BytesIO(screenshot))
                date_time_prog = datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
                log_message = f"\n\n\t{'*' * 2} marked as important. {'*' * 2} at {date_time_prog} {'*' * 2}\n"
                filename = log_message.replace('*', '').strip().replace(' ', '_')
                logs_ss['ss'][f"{filename}_{date_time_prog}"] = screenshot_img
                print(log_message)
                logs_ss['logs'].append(log_message)
                time.sleep(3)
            else:
                screenshot = self.driver.get_screenshot_as_png()
                screenshot_img = Image.open(BytesIO(screenshot))
                date_time_prog = datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
                log_message = f"\n\n\t{'*' * 2} unable to find advance toolbar. {'*' * 2} at {date_time_prog} {'*' * 2}\n"
                filename = log_message.replace('*', '').strip().replace(' ', '_')
                logs_ss['ss'][f"{filename}_{date_time_prog}"] = screenshot_img
                logs_ss['logs'].append(log_message)
                print(log_message)
                
            
            time.sleep(random.uniform(1, 5))
            return self.driver, logs_ss

    ##### mark as not important
    def mark_as_not_important(self):
        time.sleep(random.uniform(3, 6))
        logs_ss = {'logs': [], 'ss': {}}
        more_options = "//div[@aria-label='More email options' and @aria-haspopup='true']"
        advance_toolbar = "//div[text()='Switch to advanced toolbar']"
        simple_toolbar = "//div[text()='Switch to simple toolbar']"
        mark_important = "//div[text() = 'Mark as important']"
        not_important = "//div[text() = 'Mark as not important']"
        if check_xpath_exists(self.driver, more_options):
            # print(f"\n\n\t{'*' * 2} going to more options {'*' * 2}\n")
            date_time_prog = datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
            log_message = f"\n\n\t{'*' * 2} going to more options. {'*' * 2} at {date_time_prog} {'*' * 2}\n"
            logs_ss['logs'].append(log_message)
            print(log_message)


            WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, more_options))).click()
            screenshot = self.driver.get_screenshot_as_png()
            screenshot_img = Image.open(BytesIO(screenshot))
            date_time_prog = datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
            log_message = f"\n\n\t{'*' * 2} clicked on more options. {'*' * 2} at {date_time_prog} {'*' * 2}\n"
            filename = log_message.replace('*', '').strip().replace(' ', '_')
            logs_ss['ss'][f"{filename}_{date_time_prog}"] = screenshot_img
            logs_ss['logs'].append(log_message)
            print(log_message)

            if check_xpath_exists(self.driver, advance_toolbar):
                WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, advance_toolbar))).click()
                time.sleep(3)
                screenshot = self.driver.get_screenshot_as_png()
                screenshot_img = Image.open(BytesIO(screenshot))
                date_time_prog = datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
                log_message = f"\n\n\t{'*' * 2} clicked on advance toolbar. {'*' * 2} at {date_time_prog} {'*' * 2}\n"
                filename = log_message.replace('*', '').strip().replace(' ', '_')
                logs_ss['ss'][f"{filename}_{date_time_prog}"] = screenshot_img
                logs_ss['logs'].append(log_message)
                print(log_message)

                if check_xpath_exists(self.driver, more_options):
                    WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, advance_toolbar))).click()
                    time.sleep(3)
                    screenshot = self.driver.get_screenshot_as_png()
                    screenshot_img = Image.open(BytesIO(screenshot))
                    date_time_prog = datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
                    log_message = f"\n\n\t{'*' * 2} clicked on more options again. {'*' * 2} at {date_time_prog} {'*' * 2}\n"
                    filename = log_message.replace('*', '').strip().replace(' ', '_')
                    logs_ss['ss'][f"{filename}_{date_time_prog}"] = screenshot_img
                    logs_ss['logs'].append(log_message)
                    print(log_message)

            elif check_xpath_exists(self.driver, not_important):
                WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, not_important))).click()
                time.sleep(3)
                screenshot = self.driver.get_screenshot_as_png()
                screenshot_img = Image.open(BytesIO(screenshot))
                date_time_prog = datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
                log_message = f"\n\n\t{'*' * 2} marked as not important. {'*' * 2} at {date_time_prog} {'*' * 2}\n"
                filename = log_message.replace('*', '').strip().replace(' ', '_')
                logs_ss['ss'][f"{filename}_{date_time_prog}"] = screenshot_img
                logs_ss['logs'].append(log_message)
                print(log_message)

            elif check_xpath_exists(self.driver, mark_important):
                time.sleep(3)
                screenshot = self.driver.get_screenshot_as_png()
                screenshot_img = Image.open(BytesIO(screenshot))
                date_time_prog = datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
                log_message = f"\n\n\t{'*' * 2} already marked as important. {'*' * 2} at {date_time_prog} {'*' * 2}\n"
                filename = log_message.replace('*', '').strip().replace(' ', '_')
                logs_ss['ss'][f"{filename}_{date_time_prog}"] = screenshot_img
                logs_ss['logs'].append(log_message)
                print(log_message)

            else:
                screenshot = self.driver.get_screenshot_as_png()
                screenshot_img = Image.open(BytesIO(screenshot))
                date_time_prog = datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
                log_message = f"\n\n\t{'*' * 2} unable to find advance toolbar. {'*' * 2} at {date_time_prog} {'*' * 2}\n"
                filename = log_message.replace('*', '').strip().replace(' ', '_')
                logs_ss['ss'][f"{filename}_{date_time_prog}"] = screenshot_img
                logs_ss['logs'].append(log_message)
                print(log_message)
            
        time.sleep(random.uniform(1, 5))            
        return self.driver, logs_ss
    
    ##### add star 
    def star_message(self):
        time.sleep(random.uniform(5, 8))
        logs_ss = {'logs': [], 'ss': {}}
        # time.sleep(1000)
        try:
            if WebDriverWait(self.driver, 60).until(EC.presence_of_element_located((By.XPATH, "//div[@aria-label='Starred' and @role='checkbox']"))):
                screenshot = self.driver.get_screenshot_as_png()
                screenshot_img = Image.open(BytesIO(screenshot))
                date_time_prog = datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
                log_message = f"\n\n\t{'*' * 2} message is already starred. {'*' * 2} at {date_time_prog} {'*' * 2}\n"
                filename = log_message.replace('*', '').strip().replace(' ', '_')
                logs_ss['ss'][f"{filename}_{date_time_prog}"] = screenshot_img
                logs_ss['logs'].append(log_message)
                print(log_message)

            elif WebDriverWait(self.driver, 60).until(EC.presence_of_element_located((By.XPATH, "//div[@aria-label='Not starred' and @role='checkbox'] | //div[@aria-label='Not starred' and @role='checkbox']/span"))):
                WebDriverWait(self.driver, 60).until(EC.presence_of_element_located((By.XPATH, "//div[@aria-label='Not starred' and @role='checkbox'] | //div[@aria-label='Not starred' and @role='checkbox']/span']"))).click()
                screenshot = self.driver.get_screenshot_as_png()
                screenshot_img = Image.open(BytesIO(screenshot))
                date_time_prog = datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
                log_message = f"\n\n\t{'*' * 2} message starred. {'*' * 2} at {date_time_prog} {'*' * 2}\n"
                filename = log_message.replace('*', '').strip().replace(' ', '_')
                logs_ss['ss'][f"{filename}_{date_time_prog}"] = screenshot_img
                logs_ss['logs'].append(log_message)
                print(log_message)
            
            else:
                screenshot = self.driver.get_screenshot_as_png()
                screenshot_img = Image.open(BytesIO(screenshot))
                date_time_prog = datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
                log_message = f"\n\n\t{'*' * 2} error in starring message. {'*' * 2} at {date_time_prog} {'*' * 2}\n"
                filename = log_message.replace('*', '').strip().replace(' ', '_')
                logs_ss['ss'][f"{filename}_{date_time_prog}"] = screenshot_img
                logs_ss['logs'].append(log_message)
                print(log_message)
            
        except TimeoutException:
            WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, "//div[@aria-label='Not starred' and @role='checkbox']"))).click()
            screenshot = self.driver.get_screenshot_as_png()
            screenshot_img = Image.open(BytesIO(screenshot))
            date_time_prog = datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
            log_message = f"\n\n\t{'*' * 2} message starred. {'*' * 2} at {date_time_prog} {'*' * 2}\n"
            filename = log_message.replace('*', '').strip().replace(' ', '_')
            logs_ss['ss'][f"{filename}_{date_time_prog}"] = screenshot_img
            logs_ss['logs'].append(log_message)
            print(log_message)
            # print(f"\n{'-' * 5} TimeoutException: error in starring message {'-' * 5}\n")   
        time.sleep(random.uniform(1, 5))
        # WebDriverWait(self.driver, 60).until(EC.presence_of_element_located((By.XPATH, "//div[(@title='Back to Inbox' or @aria-label='Back to Inbox' or @title='Back to Spam' or @aria-label='Back to Spam') and @role='button']"))).click()
        return self.driver, logs_ss
    
    
    ##### remove star 
    def remove_star(self):
        time.sleep(random.uniform(5, 8))
        logs_ss = {'logs': [], 'ss': {}}
        # time.sleep(1000)
        star_mess_xpath = "//div[@aria-label='Starred' and @role='checkbox']"
        not_star_mess_xpath = "//div[@aria-label='Not starred' and @role='checkbox'] | //div[@aria-label='Not starred' and @role='checkbox']/span"
        try:
            if check_xpath_exists(self.driver, not_star_mess_xpath):
                screenshot = self.driver.get_screenshot_as_png()
                screenshot_img = Image.open(BytesIO(screenshot))
                date_time_prog = datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
                log_message = f"\n\n\t{'*' * 2} message is already not starred. {'*' * 2} at {date_time_prog} {'*' * 2}\n"
                filename = log_message.replace('*', '').strip().replace(' ', '_')
                logs_ss['ss'][f"{filename}_{date_time_prog}"] = screenshot_img
                logs_ss['logs'].append(log_message)
                print(log_message)

            elif check_xpath_exists(self.driver, star_mess_xpath):
                WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, star_mess_xpath))).click()
                screenshot = self.driver.get_screenshot_as_png()
                screenshot_img = Image.open(BytesIO(screenshot))
                date_time_prog = datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
                log_message = f"\n\n\t{'*' * 2} message not starred successfully. {'*' * 2} at {date_time_prog} {'*' * 2}\n"
                filename = log_message.replace('*', '').strip().replace(' ', '_')
                logs_ss['ss'][f"{filename}_{date_time_prog}"] = screenshot_img
                logs_ss['logs'].append(log_message)
                print(log_message)
            
            else:
                screenshot = self.driver.get_screenshot_as_png()
                screenshot_img = Image.open(BytesIO(screenshot))
                date_time_prog = datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
                log_message = f"\n\n\t{'*' * 2} error in starring message. {'*' * 2} at {date_time_prog} {'*' * 2}\n"
                filename = log_message.replace('*', '').strip().replace(' ', '_')
                logs_ss['ss'][f"{filename}_{date_time_prog}"] = screenshot_img
                logs_ss['logs'].append(log_message)
                print(log_message)
                
            
        except TimeoutException:
            WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, "//div[@aria-label='Not starred' and @role='checkbox']"))).click()
            screenshot = self.driver.get_screenshot_as_png()
            screenshot_img = Image.open(BytesIO(screenshot))
            date_time_prog = datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
            log_message = f"\n\n\t{'*' * 2} message starred. {'*' * 2} at {date_time_prog} {'*' * 2}\n"
            filename = log_message.replace('*', '').strip().replace(' ', '_')
            logs_ss['ss'][f"{filename}_{date_time_prog}"] = screenshot_img
            logs_ss['logs'].append(log_message)
            print(log_message)
            # print(f"\n{'-' * 5} TimeoutException: error in starring message {'-' * 5}\n")   
        time.sleep(random.uniform(1, 5))
        # WebDriverWait(self.driver, 60).until(EC.presence_of_element_located((By.XPATH, "//div[(@title='Back to Inbox' or @aria-label='Back to Inbox' or @title='Back to Spam' or @aria-label='Back to Spam') and @role='button']"))).click()
        return self.driver, logs_ss

    #### move to inbox
    def move_to(self, location):
        time.sleep(random.uniform(1, 5))
        logs_ss = {'logs': [], 'ss': {}}
        move_to_path = "(//div[@role='button' and (@aria-label='Move to' or @title='Move to')])"
        move_button = WebDriverWait(self.driver, 60).until(
                EC.presence_of_all_elements_located((By.XPATH, move_to_path))
            )
        if len(move_button) > 1:
            move_to_path = move_to_path + "[2]"
        try:
            if not WebDriverWait(self.driver, 20).until(EC.presence_of_all_elements_located((By.XPATH, "//table[@role='grid']/tbody/tr"))):
                screenshot = self.driver.get_screenshot_as_png()
                screenshot_img = Image.open(BytesIO(screenshot))
                date_time_prog = datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
                log_message = f"\n\n\t{'*' * 2} no messages available. {'*' * 2} at {date_time_prog} {'*' * 2}\n"
                filename = log_message.replace('*', '').strip().replace(' ', '_')
                logs_ss['ss'][f"{filename}_{date_time_prog}"] = screenshot_img
                logs_ss['logs'].append(log_message)
                print(log_message)
            if check_xpath_exists(self.driver, move_to_path):
                WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, move_to_path))).click()
                time.sleep(2)
                screenshot = self.driver.get_screenshot_as_png()
                screenshot_img = Image.open(BytesIO(screenshot))
                date_time_prog = datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
                log_message = f"\n\n\t{'*' * 2} open moved to menu. {'*' * 2} at {date_time_prog} {'*' * 2}\n"
                filename = log_message.replace('*', '').strip().replace(' ', '_')
                logs_ss['ss'][f"{filename}_{date_time_prog}"] = screenshot_img
                logs_ss['logs'].append(log_message)
                print(log_message)
                
                WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, f"//div[@role='menuitem' and @aria-hidden='false']/div[text()='{location}']"))).click()
                time.sleep(2)
                screenshot = self.driver.get_screenshot_as_png()
                screenshot_img = Image.open(BytesIO(screenshot))
                date_time_prog = datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
                log_message = f"\n\n\t{'*' * 2} moved to {location}. {'*' * 2} at {date_time_prog} {'*' * 2}\n"
                filename = log_message.replace('*', '').strip().replace(' ', '_')
                logs_ss['ss'][f"{filename}_{date_time_prog}"] = screenshot_img
                logs_ss['logs'].append(log_message)
                print(log_message)
            else:
                screenshot = self.driver.get_screenshot_as_png()
                screenshot_img = Image.open(BytesIO(screenshot))
                date_time_prog = datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
                log_message = f"\n\n\t{'*' * 2} unable to find move to button. {'*' * 2} at {date_time_prog} {'*' * 2}\n"
                filename = log_message.replace('*', '').strip().replace(' ', '_')
                logs_ss['ss'][f"{filename}_{date_time_prog}"] = screenshot_img
                logs_ss['logs'].append(log_message)
                print(log_message)
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(1111111)
                

        time.sleep(random.uniform(1, 5))
        return self.driver, logs_ss

    #### switch to page 
    def switch_to_next_page(self, page_no):
        '''Switch to next page '''
        time.sleep(random.uniform(5, 8))
        logs_ss = {'logs': [], 'ss': {}}
        if check_xpath_exists(self.driver, "//div[@role='button' and @aria-label='Older' and @aria-disabled='true']"):
            screenshot = self.driver.get_screenshot_as_png()
            screenshot_img = Image.open(BytesIO(screenshot))
            date_time_prog = datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
            log_message = f"\n\n\t{'*' * 2} no pages available. {'*' * 2} at {date_time_prog} {'*' * 2}\n"
            filename = log_message.replace('*', '').strip().replace(' ', '_')
            logs_ss['ss'][f"{filename}_{date_time_prog}"] = screenshot_img
            logs_ss['logs'].append(log_message)
            print(log_message)
        elif check_xpath_exists(self.driver, "//div[@role='button' and @aria-label='Older']"):
            if page_no > 1:
                for i in range(page_no):
                    if check_xpath_exists(self.driver, "//div[@role='button' and @aria-label='Older']"):
                        WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, "//div[@role='button' and @aria-label='Older']"))).click()
                        time.sleep(random.uniform(1, 5))
                        # print(f"\n\n\t{'*' * 2} switched to next page {i+1}{'*' * 2}\n")
                        screenshot = self.driver.get_screenshot_as_png()
                        screenshot_img = Image.open(BytesIO(screenshot))
                        date_time_prog = datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
                        log_message = f"\n\n\t{'*' * 2} switched to next page {i+1}. {'*' * 2} at {date_time_prog} {'*' * 2}\n"
                        filename = log_message.replace('*', '').strip().replace(' ', '_')
                        logs_ss['ss'][f"{filename}_{date_time_prog}"] = screenshot_img
                        logs_ss['logs'].append(log_message)
                        print(log_message)
                        
                    else:
                        screenshot = self.driver.get_screenshot_as_png()
                        screenshot_img = Image.open(BytesIO(screenshot))
                        date_time_prog = datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
                        log_message = f"\n\n\t{'*' * 2} no pages available. {'*' * 2} at {date_time_prog} {'*' * 2}\n"
                        filename = log_message.replace('*', '').strip().replace(' ', '_')
                        logs_ss['ss'][f"{filename}_{date_time_prog}"] = screenshot_img
                        logs_ss['logs'].append(log_message)
                        print(log_message)
                        break
            elif page_no == 1:
                WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, "//div[@role='button' and @aria-label='Older']"))).click()
                screenshot = self.driver.get_screenshot_as_png()
                screenshot_img = Image.open(BytesIO(screenshot))
                date_time_prog = datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
                log_message = f"\n\n\t{'*' * 2} switched to next page. {'*' * 2} at {date_time_prog} {'*' * 2}\n"
                filename = log_message.replace('*', '').strip().replace(' ', '_')
                logs_ss['ss'][f"{filename}_{date_time_prog}"] = screenshot_img
                logs_ss['logs'].append(log_message)
                print(log_message)
            else:
                screenshot = self.driver.get_screenshot_as_png()
                screenshot_img = Image.open(BytesIO(screenshot))
                date_time_prog = datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
                log_message = f"\n\n\t{'*' * 2} no more pages available. {'*' * 2} at {date_time_prog} {'*' * 2}\n"
                filename = log_message.replace('*', '').strip().replace(' ', '_')
                logs_ss['ss'][f"{filename}_{date_time_prog}"] = screenshot_img
                logs_ss['logs'].append(log_message)
                print(log_message)
        else:
            screenshot = self.driver.get_screenshot_as_png()
            screenshot_img = Image.open(BytesIO(screenshot))
            date_time_prog = datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
            log_message = f"\n\n\t{'*' * 2} unable to switch to next page. {'*' * 2} at {date_time_prog} {'*' * 2}\n"
            filename = log_message.replace('*', '').strip().replace(' ', '_')
            logs_ss['ss'][f"{filename}_{date_time_prog}"] = screenshot_img
            logs_ss['logs'].append(log_message)
            print(log_message)
        time.sleep(random.uniform(1, 5))
        return self.driver, logs_ss

    #### delete working
    def delete_message(self):
        time.sleep(random.uniform(1, 5))
        logs_ss = {'logs': [], 'ss': {}}
        if check_xpath_exists(self.driver, "//div[@role='button' and (@aria-label='Delete' or @title='Delete')]"):
            WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, "//div[@role='button' and (@aria-label='Delete' or @title='Delete')]"))).click()
            time.sleep(2)
            screenshot = self.driver.get_screenshot_as_png()
            screenshot_img = Image.open(BytesIO(screenshot))
            date_time_prog = datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
            log_message = f"\n\n\t{'*' * 2} deleted. {'*' * 2} at {date_time_prog} {'*' * 2}\n"
            filename = log_message.replace('*', '').strip().replace(' ', '_')
            logs_ss['ss'][f"{filename}_{date_time_prog}"] = screenshot_img
            logs_ss['logs'].append(log_message)
            print(log_message)
        else:
            time.sleep(111111)
            screenshot = self.driver.get_screenshot_as_png()
            screenshot_img = Image.open(BytesIO(screenshot))
            date_time_prog = datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
            log_message = f"\n\n\t{'*' * 2} error in deleting message. {'*' * 2} at {date_time_prog} {'*' * 2}\n"
            filename = log_message.replace('*', '').strip().replace(' ', '_')
            logs_ss['ss'][f"{filename}_{date_time_prog}"] = screenshot_img
            logs_ss['logs'].append(log_message)
            print(log_message)
        return self.driver, logs_ss

    ##### delete forever 
    def delete_forever(self):
        time.sleep(random.uniform(1, 5))
        logs_ss = {'logs': [], 'ss': {}}
        if not WebDriverWait(self.driver, 20).until(EC.presence_of_all_elements_located((By.XPATH, "//table[@role='grid']/tbody/tr"))):
            screenshot = self.driver.get_screenshot_as_png()
            screenshot_img = Image.open(BytesIO(screenshot))
            date_time_prog = datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
            log_message = f"\n\n\t{'*' * 2} no message available to delete. {'*' * 2} at {date_time_prog} {'*' * 2}\n"
            filename = log_message.replace('*', '').strip().replace(' ', '_')
            logs_ss['ss'][f"{filename}_{date_time_prog}"] = screenshot_img
            logs_ss['logs'].append(log_message)
            print(log_message)
        else:
            delete_forever1 = "(//div[text()='Delete forever'])"
            delete_forever2 = "(//div[@role='button']/div[text()='Delete forever'])"
            df_buttons = WebDriverWait(self.driver, 60).until(
                    EC.presence_of_all_elements_located((By.XPATH, delete_forever2 + ' | '+delete_forever1))
                )
            # print(f"\n\n\t{'*' * 2} len delete forever buttons: {len(df_buttons)} {'*' * 2}\n")
            if len(df_buttons) > 1:
                # print(f"\n\n\t{'*' * 2} delete forever buttons: {df_buttons} {'*' * 2}\n")
                delete_forever2 = delete_forever2 + "[2]"
            if check_xpath_exists(self.driver, delete_forever2):
                WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, delete_forever2))).click()
                screenshot = self.driver.get_screenshot_as_png()
                screenshot_img = Image.open(BytesIO(screenshot))
                date_time_prog = datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
                log_message = f"\n\n\t{'*' * 2} message deleted permanently. {'*' * 2} at {date_time_prog} {'*' * 2}\n"
                filename = log_message.replace('*', '').strip().replace(' ', '_')
                logs_ss['ss'][f"{filename}_{date_time_prog}"] = screenshot_img
                logs_ss['logs'].append(log_message)
                print(log_message)
                
            else:
                screenshot = self.driver.get_screenshot_as_png()
                screenshot_img = Image.open(BytesIO(screenshot))
                date_time_prog = datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
                log_message = f"\n\n\t{'*' * 2} delete button not exist. {'*' * 2} at {date_time_prog} {'*' * 2}\n"
                filename = log_message.replace('*', '').strip().replace(' ', '_')
                logs_ss['ss'][f"{filename}_{date_time_prog}"] = screenshot_img
                logs_ss['logs'].append(log_message)
                print(log_message)
        
        time.sleep(random.uniform(1, 5))
        return self.driver, logs_ss

    ##### disable promotions
    def disable_promotions(self):
        time.sleep(random.uniform(5, 10))
        logs_ss = {'logs': [], 'ss': {}}

        if check_xpath_exists(self.driver, "//a[@role='button' and @aria-label='Settings']"):  # Check if already in inbox
            WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, "//a[@role='button' and @aria-label='Settings']"))).click()
            screenshot = self.driver.get_screenshot_as_png()
            screenshot_img = Image.open(BytesIO(screenshot))
            date_time_prog = datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
            log_message = f"\n\n\t{'*' * 2} clicked on setting. {'*' * 2} at {date_time_prog} {'*' * 2}\n"
            filename = log_message.replace('*', '').strip().replace(' ', '_')
            logs_ss['ss'][f"{filename}_{date_time_prog}"] = screenshot_img
            logs_ss['logs'].append(log_message)
            print(log_message)

            time.sleep(5)
            WebDriverWait(self.driver, 60).until(EC.presence_of_element_located((By.XPATH, "//button[@aria-label='See all settings' and text()='See all settings']"))).click()
            screenshot = self.driver.get_screenshot_as_png()
            screenshot_img = Image.open(BytesIO(screenshot))
            date_time_prog = datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
            log_message = f"\n\n\t{'*' * 2} clicked on all setting. {'*' * 2} at {date_time_prog} {'*' * 2}\n"
            filename = log_message.replace('*', '').strip().replace(' ', '_')
            logs_ss['ss'][f"{filename}_{date_time_prog}"] = screenshot_img
            logs_ss['logs'].append(log_message)
            print(log_message)
            time.sleep(5)
            
            WebDriverWait(self.driver, 60).until(EC.presence_of_element_located((By.XPATH, "//a[@role='tab' and text()='Inbox']"))).click()
            screenshot = self.driver.get_screenshot_as_png()
            screenshot_img = Image.open(BytesIO(screenshot))
            date_time_prog = datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
            log_message = f"\n\n\t{'*' * 2} clicked on inbox tab. {'*' * 2} at {date_time_prog} {'*' * 2}\n"
            filename = log_message.replace('*', '').strip().replace(' ', '_')
            logs_ss['ss'][f"{filename}_{date_time_prog}"] = screenshot_img
            logs_ss['logs'].append(log_message)
            print(log_message)

            checkbox = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, "//td[label[text()='Promotions']]/preceding-sibling::td[1]/input[@type='checkbox']")))
            

            # Check if the checkbox is selected
            if not checkbox.is_selected():
                screenshot = self.driver.get_screenshot_as_png()
                screenshot_img = Image.open(BytesIO(screenshot))
                date_time_prog = datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
                log_message = f"\n\n\t{'*' * 2} promotion is already disabled. {'*' * 2} at {date_time_prog} {'*' * 2}\n"
                filename = log_message.replace('*', '').strip().replace(' ', '_')
                logs_ss['ss'][f"{filename}_{date_time_prog}"] = screenshot_img
                logs_ss['logs'].append(log_message)
                print(log_message)


            # Verify if the checkbox is now checked
            elif checkbox.is_selected():
                checkbox.click()  # Click the checkbox if it is not selected
                screenshot = self.driver.get_screenshot_as_png()
                screenshot_img = Image.open(BytesIO(screenshot))
                date_time_prog = datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
                log_message = f"\n\n\t{'*' * 2} clicked on checkbox. {'*' * 2} at {date_time_prog} {'*' * 2}\n"
                filename = log_message.replace('*', '').strip().replace(' ', '_')
                logs_ss['ss'][f"{filename}_{date_time_prog}"] = screenshot_img
                logs_ss['logs'].append(log_message)
                print(log_message)


                time.sleep(random.uniform(1, 5))
                save_change_path = "(//button[text()='Save Changes'])"
                save_button = WebDriverWait(self.driver, 60).until(EC.presence_of_all_elements_located((By.XPATH, save_change_path)))
                if len(save_button) > 1:
                    save_change_path = save_change_path + "[2]"
                save_button = WebDriverWait(self.driver, 60).until(EC.presence_of_element_located((By.XPATH, save_change_path)))

                self.driver.execute_script("arguments[0].scrollIntoView();", save_button)
                screenshot = self.driver.get_screenshot_as_png()
                screenshot_img = Image.open(BytesIO(screenshot))
                date_time_prog = datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
                log_message = f"\n\n\t{'*' * 2} scrolled to save button. {'*' * 2} at {date_time_prog} {'*' * 2}\n"
                filename = log_message.replace('*', '').strip().replace(' ', '_')
                logs_ss['ss'][f"{filename}_{date_time_prog}"] = screenshot_img
                logs_ss['logs'].append(log_message)
                print(log_message)
                is_disabled = save_button.get_attribute('disabled') is not None
                if is_disabled:

                    screenshot = self.driver.get_screenshot_as_png()
                    screenshot_img = Image.open(BytesIO(screenshot))
                    date_time_prog = datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
                    log_message = f"\n\n\t{'*' * 2} promotion is already disabled. {'*' * 2} at {date_time_prog} {'*' * 2}\n"
                    filename = log_message.replace('*', '').strip().replace(' ', '_')
                    logs_ss['ss'][f"{filename}_{date_time_prog}"] = screenshot_img
                    logs_ss['logs'].append(log_message)
                    print(log_message)
                else:
                    save_button.click()
                    print(f"\n\n\t{'*' * 2} changes saved {'*' * 2}\n")
                    screenshot = self.driver.get_screenshot_as_png()
                    screenshot_img = Image.open(BytesIO(screenshot))
                    date_time_prog = datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
                    log_message = f"\n\n\t{'*' * 2} promotion disabled successfully, changes saved. {'*' * 2} at {date_time_prog} {'*' * 2}\n"
                    filename = log_message.replace('*', '').strip().replace(' ', '_')
                    logs_ss['ss'][f"{filename}_{date_time_prog}"] = screenshot_img
                    logs_ss['logs'].append(log_message)
                    print(log_message)

                

            else:
                screenshot = self.driver.get_screenshot_as_png()
                screenshot_img = Image.open(BytesIO(screenshot))
                date_time_prog = datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
                log_message = f"\n\n\t{'*' * 2} error. {'*' * 2} at {date_time_prog} {'*' * 2}\n"
                filename = log_message.replace('*', '').strip().replace(' ', '_')
                logs_ss['ss'][f"{filename}_{date_time_prog}"] = screenshot_img
                logs_ss['logs'].append(log_message)
                print(log_message)

        else:
            screenshot = self.driver.get_screenshot_as_png()
            screenshot_img = Image.open(BytesIO(screenshot))
            date_time_prog = datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
            log_message = f"\n\n\t{'*' * 2} no xpath available. {'*' * 2} at {date_time_prog} {'*' * 2}\n"
            filename = log_message.replace('*', '').strip().replace(' ', '_')
            logs_ss['ss'][f"{filename}_{date_time_prog}"] = screenshot_img
            logs_ss['logs'].append(log_message)
            print(log_message)

            
        time.sleep(random.uniform(1, 5))
        return self.driver, logs_ss
    

    ##### disable social
    def disable_social(self):
        time.sleep(random.uniform(5, 10))
        logs_ss = {'logs': [], 'ss': {}}
        # if WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, "//a[@role='tab' and text()='Inbox']"))):  # Check if already in inbox
        #     pass
        # else:
        if check_xpath_exists(self.driver, "//a[@role='button' and @aria-label='Settings']"):  # Check if already in inbox
            WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, "//a[@role='button' and @aria-label='Settings']"))).click()
            time.sleep(5)
            WebDriverWait(self.driver, 60).until(EC.presence_of_element_located((By.XPATH, "//button[@aria-label='See all settings' and text()='See all settings']"))).click()
            time.sleep(5)
            
            WebDriverWait(self.driver, 60).until(EC.presence_of_element_located((By.XPATH, "//a[@role='tab' and text()='Inbox']"))).click()
            
            # checkbox = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, "//td//input[@type='checkbox']/following::td/label[text()='Social']")))
            checkbox = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, "//td[label[text()='Social']]/preceding-sibling::td[1]/input[@type='checkbox']")))


            # Check if the checkbox is selected
            if not checkbox.is_selected():
                # print("clicking on checkbox") 
                # checkbox.click()  # Click the checkbox if it is not selected
                screenshot = self.driver.get_screenshot_as_png()
                screenshot_img = Image.open(BytesIO(screenshot))
                date_time_prog = datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
                log_message = f"\n\n\t{'*' * 2} social is already disabled. {'*' * 2} at {date_time_prog} {'*' * 2}\n"
                filename = log_message.replace('*', '').strip().replace(' ', '_')
                logs_ss['ss'][f"{filename}_{date_time_prog}"] = screenshot_img
                logs_ss['logs'].append(log_message)
                print(log_message)

            # Verify if the checkbox is now checked
            elif checkbox.is_selected():
                checkbox.click()  # Click the checkbox if it is not selected
                screenshot = self.driver.get_screenshot_as_png()
                screenshot_img = Image.open(BytesIO(screenshot))
                date_time_prog = datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
                log_message = f"\n\n\t{'*' * 2} clicked on checkbox. {'*' * 2} at {date_time_prog} {'*' * 2}\n"
                filename = log_message.replace('*', '').strip().replace(' ', '_')
                logs_ss['ss'][f"{filename}_{date_time_prog}"] = screenshot_img
                logs_ss['logs'].append(log_message)
                print(log_message)

                time.sleep(random.uniform(1, 5))
                save_change_path = "(//button[text()='Save Changes'])"
                save_button = WebDriverWait(self.driver, 60).until(EC.presence_of_all_elements_located((By.XPATH, save_change_path)))
                if len(save_button) > 1:
                    save_change_path = save_change_path + "[2]"
                save_button = WebDriverWait(self.driver, 60).until(EC.presence_of_element_located((By.XPATH, save_change_path)))

                self.driver.execute_script("arguments[0].scrollIntoView();", save_button)
                screenshot = self.driver.get_screenshot_as_png()
                screenshot_img = Image.open(BytesIO(screenshot))
                date_time_prog = datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
                log_message = f"\n\n\t{'*' * 2} scrolled to save button. {'*' * 2} at {date_time_prog} {'*' * 2}\n"
                filename = log_message.replace('*', '').strip().replace(' ', '_')
                logs_ss['ss'][f"{filename}_{date_time_prog}"] = screenshot_img
                logs_ss['logs'].append(log_message)
                print(log_message)
                is_disabled = save_button.get_attribute('disabled') is not None
                if is_disabled:

                    screenshot = self.driver.get_screenshot_as_png()
                    screenshot_img = Image.open(BytesIO(screenshot))
                    date_time_prog = datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
                    log_message = f"\n\n\t{'*' * 2} social is already disabled. {'*' * 2} at {date_time_prog} {'*' * 2}\n"
                    filename = log_message.replace('*', '').strip().replace(' ', '_')
                    logs_ss['ss'][f"{filename}_{date_time_prog}"] = screenshot_img
                    logs_ss['logs'].append(log_message)
                    print(log_message)
                else:
                    save_button.click()
                    print(f"\n\n\t{'*' * 2} changes saved {'*' * 2}\n")
                    screenshot = self.driver.get_screenshot_as_png()
                    screenshot_img = Image.open(BytesIO(screenshot))
                    date_time_prog = datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
                    log_message = f"\n\n\t{'*' * 2} social disabled successfully, changes saved. {'*' * 2} at {date_time_prog} {'*' * 2}\n"
                    filename = log_message.replace('*', '').strip().replace(' ', '_')
                    logs_ss['ss'][f"{filename}_{date_time_prog}"] = screenshot_img
                    logs_ss['logs'].append(log_message)
                    print(log_message)
            else:
                screenshot = self.driver.get_screenshot_as_png()
                screenshot_img = Image.open(BytesIO(screenshot))
                date_time_prog = datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
                log_message = f"\n\n\t{'*' * 2} error. {'*' * 2} at {date_time_prog} {'*' * 2}\n"
                filename = log_message.replace('*', '').strip().replace(' ', '_')
                logs_ss['ss'][f"{filename}_{date_time_prog}"] = screenshot_img
                logs_ss['logs'].append(log_message)
                print(log_message)
        else:
            screenshot = self.driver.get_screenshot_as_png()
            screenshot_img = Image.open(BytesIO(screenshot))
            date_time_prog = datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
            log_message = f"\n\n\t{'*' * 2} no xpath available. {'*' * 2} at {date_time_prog} {'*' * 2}\n"
            filename = log_message.replace('*', '').strip().replace(' ', '_')
            logs_ss['ss'][f"{filename}_{date_time_prog}"] = screenshot_img
            logs_ss['logs'].append(log_message)
            print(log_message)

        time.sleep(random.uniform(1, 5))
        return self.driver,logs_ss

    ##### send message
    def compose_message(self, recipients_mail, subject_text):
        time.sleep(random.uniform(5, 10))
        logs_ss = {'logs': [], 'ss': {}}
        WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, "//div[text()='Compose']"))).click()
        screenshot = self.driver.get_screenshot_as_png()
        screenshot_img = Image.open(BytesIO(screenshot))
        date_time_prog = datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
        log_message = f"\n\n\t{'*' * 2} clicked in compose. {'*' * 2} at {date_time_prog} {'*' * 2}\n"
        filename = log_message.replace('*', '').strip().replace(' ', '_')
        logs_ss['ss'][f"{filename}_{date_time_prog}"] = screenshot_img
        logs_ss['logs'].append(log_message)
        print(log_message)

        recipients = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, "//input[@aria-label='To recipients']")))
        # recipients.send_keys("TLDR")
        for char in recipients_mail:  # Type email character by character
            time.sleep(random.uniform(0.1, 0.5))  # Add random delay between keystrokes
            recipients.send_keys(char)
        time.sleep(random.uniform(1, 5))
        screenshot = self.driver.get_screenshot_as_png()
        screenshot_img = Image.open(BytesIO(screenshot))
        date_time_prog = datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
        log_message = f"\n\n\t{'*' * 2} recipients written. {'*' * 2} at {date_time_prog} {'*' * 2}\n"
        filename = log_message.replace('*', '').strip().replace(' ', '_')
        logs_ss['ss'][f"{filename}_{date_time_prog}"] = screenshot_img
        logs_ss['logs'].append(log_message)
        print(log_message)

        subject = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, "//input[@aria-label='Subject']")))

        for char in subject_text:  # Type email character by character
            time.sleep(random.uniform(0.1, 0.5))  # Add random delay between keystrokes
            subject.send_keys(char)
        time.sleep(random.uniform(1, 5))
        screenshot = self.driver.get_screenshot_as_png()
        screenshot_img = Image.open(BytesIO(screenshot))
        date_time_prog = datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
        log_message = f"\n\n\t{'*' * 2} subject written. {'*' * 2} at {date_time_prog} {'*' * 2}\n"
        filename = log_message.replace('*', '').strip().replace(' ', '_')
        logs_ss['ss'][f"{filename}_{date_time_prog}"] = screenshot_img
        logs_ss['logs'].append(log_message)
        print(log_message)

        WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, "//div[@role='button' and text()='Send']"))).click()
        time.sleep(random.uniform(1, 3))
        screenshot = self.driver.get_screenshot_as_png()
        screenshot_img = Image.open(BytesIO(screenshot))
        date_time_prog = datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
        log_message = f"\n\n\t{'*' * 2} message sent. {'*' * 2} at {date_time_prog} {'*' * 2}\n"
        filename = log_message.replace('*', '').strip().replace(' ', '_')
        logs_ss['ss'][f"{filename}_{date_time_prog}"] = screenshot_img
        logs_ss['logs'].append(log_message)
        print(log_message)


        return self.driver, logs_ss

    ##### ====================== general working end ====================== #####
    

    ##### ====================== Trash working start ====================== #####
    def goto_trash(self):
        time.sleep(random.uniform(5, 10))
        logs_ss = {'logs': [], 'ss': {}}
        if check_xpath_exists(self.driver, "//a[text()='Trash']"):  # Check if already in Spam
            screenshot = self.driver.get_screenshot_as_png()
            screenshot_img = Image.open(BytesIO(screenshot))
            date_time_prog = datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
            log_message = f"\n\n\t{'*' * 2} already in trash! {'*' * 2} at {date_time_prog} {'*' * 2}\n"
            filename = log_message.replace('*', '').strip().replace(' ', '_')
            logs_ss['ss'][f"{filename}_{date_time_prog}"] = screenshot_img
            logs_ss['logs'].append(log_message)
            print(log_message)
        else:
            date_time_prog = datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
            log_message = f"\n\n\t{'*' * 2} going to trash. {'*' * 2} at {date_time_prog} {'*' * 2}\n"
            logs_ss['logs'].append(log_message)
            print(log_message)

            time.sleep(3)
            WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, "(//span[@role='button']/span[text()='More'])[1]"))).click()  # Click More button
            screenshot = self.driver.get_screenshot_as_png()
            screenshot_img = Image.open(BytesIO(screenshot))
            date_time_prog = datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
            log_message = f"\n\n\t{'*' * 2} clicked on more. {'*' * 2} at {date_time_prog} {'*' * 2}\n"
            filename = log_message.replace('*', '').strip().replace(' ', '_')
            logs_ss['ss'][f"{filename}_{date_time_prog}"] = screenshot_img
            logs_ss['logs'].append(log_message)
            print(log_message)

            WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, "//a[text()='Trash']"))).click()  # Click Spam link
            screenshot = self.driver.get_screenshot_as_png()
            screenshot_img = Image.open(BytesIO(screenshot))
            date_time_prog = datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
            log_message = f"\n\n\t{'*' * 2} arrived in trash. {'*' * 2} at {date_time_prog} {'*' * 2}\n"
            filename = log_message.replace('*', '').strip().replace(' ', '_')
            logs_ss['ss'][f"{filename}_{date_time_prog}"] = screenshot_img
            logs_ss['logs'].append(log_message)
            print(log_message)
        
        return self.driver, logs_ss
    
    def empty_trash(self): 
        time.sleep(random.uniform(5, 10))
        logs_ss = {'logs': [], 'ss': {}}
        empty_trash = "(//span[text()='Empty Trash now'])"
        # if check_xpath_exists(self.driver, "//table[@role='grid']/tbody/tr") == False:
        if not WebDriverWait(self.driver, 20).until(EC.presence_of_all_elements_located((By.XPATH, "//table[@role='grid']/tbody/tr"))):
            screenshot = self.driver.get_screenshot_as_png()
            screenshot_img = Image.open(BytesIO(screenshot))
            date_time_prog = datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
            log_message = f"\n\n\t{'*' * 2} trash is already empty! {'*' * 2} at {date_time_prog} {'*' * 2}\n"
            filename = log_message.replace('*', '').strip().replace(' ', '_')
            logs_ss['ss'][f"{filename}_{date_time_prog}"] = screenshot_img
            logs_ss['logs'].append(log_message)
            print(log_message)
            
        elif check_xpath_exists(self.driver, empty_trash):
            WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, empty_trash))).click()
            time.sleep(3)
            screenshot = self.driver.get_screenshot_as_png()
            screenshot_img = Image.open(BytesIO(screenshot))
            date_time_prog = datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
            log_message = f"\n\n\t{'*' * 2} clicked empty trash now. {'*' * 2} at {date_time_prog} {'*' * 2}\n"
            filename = log_message.replace('*', '').strip().replace(' ', '_')
            logs_ss['ss'][f"{filename}_{date_time_prog}"] = screenshot_img
            logs_ss['logs'].append(log_message)
            print(log_message)

            if check_xpath_exists(self.driver, "//span[text()='OK']"):
                WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, "//span[text()='OK']"))).click()
                time.sleep(3)
                screenshot = self.driver.get_screenshot_as_png()
                screenshot_img = Image.open(BytesIO(screenshot))
                date_time_prog = datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
                log_message = f"\n\n\t{'*' * 2} trash emptied successfully. {'*' * 2} at {date_time_prog} {'*' * 2}\n"
                filename = log_message.replace('*', '').strip().replace(' ', '_')
                logs_ss['ss'][f"{filename}_{date_time_prog}"] = screenshot_img
                logs_ss['logs'].append(log_message)
                print(log_message)
            else:
                screenshot = self.driver.get_screenshot_as_png()
                screenshot_img = Image.open(BytesIO(screenshot))
                date_time_prog = datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
                log_message = f"\n\n\t{'*' * 2} error in emptying trash. {'*' * 2} at {date_time_prog} {'*' * 2}\n"
                filename = log_message.replace('*', '').strip().replace(' ', '_')
                logs_ss['ss'][f"{filename}_{date_time_prog}"] = screenshot_img
                logs_ss['logs'].append(log_message)
                print(log_message)
        else:
            screenshot = self.driver.get_screenshot_as_png()
            screenshot_img = Image.open(BytesIO(screenshot))
            date_time_prog = datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
            log_message = f"\n\n\t{'*' * 2} error in emptying trash. {'*' * 2} at {date_time_prog} {'*' * 2}\n"
            filename = log_message.replace('*', '').strip().replace(' ', '_')
            logs_ss['ss'][f"{filename}_{date_time_prog}"] = screenshot_img
            logs_ss['logs'].append(log_message)
            print(log_message)
        
        time.sleep(random.uniform(1, 5))
        return self.driver, logs_ss
    ##### ====================== Trash working end ====================== #####

    ##### ====================== setting work start ====================== #####

    def always_show_message(self):
        time.sleep(random.uniform(5, 10))
        logs_ss = {'logs': [], 'ss': {}}
        setting_icon_xpath = "//a[@role='button' and @aria-label='Settings']"
        if check_xpath_exists(self.driver, "//h2[@tabindex='-1' and text()='Settings']"):
            date_time_prog = datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
            log_message = f"\n\n\t{'*' * 2} already in settings! {'*' * 2} at {date_time_prog} {'*' * 2}\n"
            logs_ss['logs'].append(log_message)
            print(log_message)

            general_set_path = "//a[@aria-selected='false' and text()='General']"
            if check_xpath_exists(self.driver, general_set_path):
                WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, general_set_path))).click()
                screenshot = self.driver.get_screenshot_as_png()
                screenshot_img = Image.open(BytesIO(screenshot))
                date_time_prog = datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
                log_message = f"\n\n\t{'*' * 2} arrived in general settings. {'*' * 2} at {date_time_prog} {'*' * 2}\n"
                filename = log_message.replace('*', '').strip().replace(' ', '_')
                logs_ss['ss'][f"{filename}_{date_time_prog}"] = screenshot_img
                logs_ss['logs'].append(log_message)
                print(log_message)
                time.sleep(random.uniform(1, 5))

        elif check_xpath_exists(self.driver, setting_icon_xpath):
            WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, setting_icon_xpath))).click()
            screenshot = self.driver.get_screenshot_as_png()
            screenshot_img = Image.open(BytesIO(screenshot))
            date_time_prog = datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
            log_message = f"\n\n\t{'*' * 2} clicked on setting icon. {'*' * 2} at {date_time_prog} {'*' * 2}\n"
            filename = log_message.replace('*', '').strip().replace(' ', '_')
            logs_ss['ss'][f"{filename}_{date_time_prog}"] = screenshot_img
            logs_ss['logs'].append(log_message)
            print(log_message)
            time.sleep(random.uniform(1, 5))
            # print(f"\n\n\t{'*' * 2} clicked on setting icon {'*' * 2}\n")
            WebDriverWait(self.driver, 60).until(EC.presence_of_element_located((By.XPATH, "//button[@aria-label='See all settings' and text()='See all settings']"))).click()
            screenshot = self.driver.get_screenshot_as_png()
            screenshot_img = Image.open(BytesIO(screenshot))
            date_time_prog = datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
            log_message = f"\n\n\t{'*' * 2} clicked on see all settings. {'*' * 2} at {date_time_prog} {'*' * 2}\n"
            filename = log_message.replace('*', '').strip().replace(' ', '_')
            logs_ss['ss'][f"{filename}_{date_time_prog}"] = screenshot_img
            logs_ss['logs'].append(log_message)
            print(log_message)
            time.sleep(random.uniform(1, 5))
        else:
            screenshot = self.driver.get_screenshot_as_png()
            screenshot_img = Image.open(BytesIO(screenshot))
            date_time_prog = datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
            log_message = f"\n\n\t{'*' * 2} unable to find setting path. {'*' * 2} at {date_time_prog} {'*' * 2}\n"
            filename = log_message.replace('*', '').strip().replace(' ', '_')
            logs_ss['ss'][f"{filename}_{date_time_prog}"] = screenshot_img
            logs_ss['logs'].append(log_message)
            print(log_message)

        pathh = "//span[text()='Images:']"
        try:
            time.sleep(random.uniform(1, 5))
            element = WebDriverWait(self.driver, 60).until(EC.presence_of_element_located((By.XPATH, pathh)))
            if element:
                time.sleep(random.uniform(1, 5))
                self.driver.execute_script("arguments[0].scrollIntoView();", element)
                screenshot = self.driver.get_screenshot_as_png()
                screenshot_img = Image.open(BytesIO(screenshot))
                date_time_prog = datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
                log_message = f"\n\n\t{'*' * 2} scrolled to images tag. {'*' * 2} at {date_time_prog} {'*' * 2}\n"
                filename = log_message.replace('*', '').strip().replace(' ', '_')
                logs_ss['ss'][f"{filename}_{date_time_prog}"] = screenshot_img
                logs_ss['logs'].append(log_message)
                print(log_message)
                time.sleep(random.uniform(1, 5))
                
                radio_button_path = "(//tr[.//span[text()='Images:']]//input[@type='radio'])[1]"
                WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, radio_button_path))).click()
                time.sleep(random.uniform(1, 5))
                screenshot = self.driver.get_screenshot_as_png()
                screenshot_img = Image.open(BytesIO(screenshot))
                date_time_prog = datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
                log_message = f"\n\n\t{'*' * 2} clicked on checkbox. {'*' * 2} at {date_time_prog} {'*' * 2}\n"
                filename = log_message.replace('*', '').strip().replace(' ', '_')
                logs_ss['ss'][f"{filename}_{date_time_prog}"] = screenshot_img
                logs_ss['logs'].append(log_message)
                print(log_message)

                save_button = WebDriverWait(self.driver, 60).until(EC.presence_of_element_located((By.XPATH, "//button[text()='Save Changes']")))
                self.driver.execute_script("arguments[0].scrollIntoView();", save_button)
                time.sleep(random.uniform(1, 5))
                screenshot = self.driver.get_screenshot_as_png()
                screenshot_img = Image.open(BytesIO(screenshot))
                date_time_prog = datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
                log_message = f"\n\n\t{'*' * 2} scrolled to save button. {'*' * 2} at {date_time_prog} {'*' * 2}\n"
                filename = log_message.replace('*', '').strip().replace(' ', '_')
                logs_ss['ss'][f"{filename}_{date_time_prog}"] = screenshot_img
                logs_ss['logs'].append(log_message)
                print(log_message)

                is_disabled = save_button.get_attribute('disabled') is not None
                if is_disabled:
                    screenshot = self.driver.get_screenshot_as_png()
                    screenshot_img = Image.open(BytesIO(screenshot))
                    date_time_prog = datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
                    log_message = f"\n\n\t{'*' * 2} button is already disabled. {'*' * 2} at {date_time_prog} {'*' * 2}\n"
                    filename = log_message.replace('*', '').strip().replace(' ', '_')
                    logs_ss['ss'][f"{filename}_{date_time_prog}"] = screenshot_img
                    logs_ss['logs'].append(log_message)
                    print(log_message)
                else:
                    save_button.click()
                    time.sleep(random.uniform(1, 5))
                    screenshot = self.driver.get_screenshot_as_png()
                    screenshot_img = Image.open(BytesIO(screenshot))
                    date_time_prog = datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
                    log_message = f"\n\n\t{'*' * 2} changes saved successfully. {'*' * 2} at {date_time_prog} {'*' * 2}\n"
                    filename = log_message.replace('*', '').strip().replace(' ', '_')
                    logs_ss['ss'][f"{filename}_{date_time_prog}"] = screenshot_img
                    logs_ss['logs'].append(log_message)
                    print(log_message)
                    
        except selenium.common.exceptions.TimeoutException:
            screenshot = self.driver.get_screenshot_as_png()
            screenshot_img = Image.open(BytesIO(screenshot))
            date_time_prog = datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
            log_message = f"\n\n\t{'*' * 2} element not found within the timeout period. {'*' * 2} at {date_time_prog} {'*' * 2}\n"
            filename = log_message.replace('*', '').strip().replace(' ', '_')
            logs_ss['ss'][f"{filename}_{date_time_prog}"] = screenshot_img
            logs_ss['logs'].append(log_message)
            print(log_message)

        except selenium.common.exceptions.JavascriptException as e:
            screenshot = self.driver.get_screenshot_as_png()
            screenshot_img = Image.open(BytesIO(screenshot))
            date_time_prog = datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
            log_message = f"\n\n\t{'*' * 2} JavascriptException occurred:. {'*' * 2} at {date_time_prog} {'*' * 2}\n"
            filename = log_message.replace('*', '').strip().replace(' ', '_')
            logs_ss['ss'][f"{filename}_{date_time_prog}"] = screenshot_img
            logs_ss['logs'].append(log_message)
            print(log_message)

        except Exception as e:
            screenshot = self.driver.get_screenshot_as_png()
            screenshot_img = Image.open(BytesIO(screenshot))
            date_time_prog = datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
            log_message = f"\n\n\t{'*' * 2} Exception occurred. {'*' * 2} at {date_time_prog} {'*' * 2}\n"
            filename = log_message.replace('*', '').strip().replace(' ', '_')
            logs_ss['ss'][f"{filename}_{date_time_prog}"] = screenshot_img
            logs_ss['logs'].append(log_message)
            print(log_message)

        time.sleep(random.uniform(1, 5))
        return self.driver, logs_ss
    

    def add_to_safe_sender(self, sender_mail):
        time.sleep(random.uniform(5, 10))
        logs_ss = {'logs': [], 'ss': {}}

        setting_icon_xpath = "//a[@role='button' and @aria-label='Settings']"
        time.sleep(random.uniform(5, 10))
        if check_xpath_exists(self.driver, "//h2[@tabindex='-1' and text()='Settings']"):
            log_message = f"\n\n\t{'*' * 2} already in settings. {'*' * 2} at {date_time_prog} {'*' * 2}\n"
            logs_ss['logs'].append(log_message)
            print(log_message)
            general_set_path = "//a[@aria-selected='false' and text()='General']"
            if check_xpath_exists(self.driver, general_set_path):
                WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, general_set_path))).click()
                screenshot = self.driver.get_screenshot_as_png()
                screenshot_img = Image.open(BytesIO(screenshot))
                date_time_prog = datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
                log_message = f"\n\n\t{'*' * 2} arrived in general settings. {'*' * 2} at {date_time_prog} {'*' * 2}\n"
                filename = log_message.replace('*', '').strip().replace(' ', '_')
                logs_ss['ss'][f"{filename}_{date_time_prog}"] = screenshot_img
                logs_ss['logs'].append(log_message)
                print(log_message)
                time.sleep(random.uniform(1, 5))
        elif check_xpath_exists(self.driver, setting_icon_xpath):
            WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, setting_icon_xpath))).click()
            time.sleep(random.uniform(1, 5))
            screenshot = self.driver.get_screenshot_as_png()
            screenshot_img = Image.open(BytesIO(screenshot))
            date_time_prog = datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
            log_message = f"\n\n\t{'*' * 2} clicked on setting icon. {'*' * 2} at {date_time_prog} {'*' * 2}\n"
            filename = log_message.replace('*', '').strip().replace(' ', '_')
            logs_ss['ss'][f"{filename}_{date_time_prog}"] = screenshot_img
            logs_ss['logs'].append(log_message)
            print(log_message)

            WebDriverWait(self.driver, 60).until(EC.presence_of_element_located((By.XPATH, "//button[@aria-label='See all settings' and text()='See all settings']"))).click()
            time.sleep(random.uniform(1, 5))
            screenshot = self.driver.get_screenshot_as_png()
            screenshot_img = Image.open(BytesIO(screenshot))
            date_time_prog = datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
            log_message = f"\n\n\t{'*' * 2} clicked on see all settings. {'*' * 2} at {date_time_prog} {'*' * 2}\n"
            filename = log_message.replace('*', '').strip().replace(' ', '_')
            logs_ss['ss'][f"{filename}_{date_time_prog}"] = screenshot_img
            logs_ss['logs'].append(log_message)
            print(log_message)
        else:
            screenshot = self.driver.get_screenshot_as_png()
            screenshot_img = Image.open(BytesIO(screenshot))
            date_time_prog = datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
            log_message = f"\n\n\t{'*' * 2} unable to find setting path. {'*' * 2} at {date_time_prog} {'*' * 2}\n"
            filename = log_message.replace('*', '').strip().replace(' ', '_')
            logs_ss['ss'][f"{filename}_{date_time_prog}"] = screenshot_img
            logs_ss['logs'].append(log_message)
            print(log_message)

        try:
            WebDriverWait(self.driver, 60).until(EC.presence_of_element_located((By.XPATH, "//a[text()='Filters and Blocked Addresses']"))).click()
            time.sleep(random.uniform(1, 5))
            screenshot = self.driver.get_screenshot_as_png()
            screenshot_img = Image.open(BytesIO(screenshot))
            date_time_prog = datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
            log_message = f"\n\n\t{'*' * 2} clicked on Filters and Blocked Addresses. {'*' * 2} at {date_time_prog} {'*' * 2}\n"
            filename = log_message.replace('*', '').strip().replace(' ', '_')
            logs_ss['ss'][f"{filename}_{date_time_prog}"] = screenshot_img
            logs_ss['logs'].append(log_message)
            print(log_message)

            WebDriverWait(self.driver, 60).until(EC.presence_of_element_located((By.XPATH, "//span[text()='Create a new filter']"))).click()
            time.sleep(random.uniform(1, 5))
            screenshot = self.driver.get_screenshot_as_png()
            screenshot_img = Image.open(BytesIO(screenshot))
            date_time_prog = datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
            log_message = f"\n\n\t{'*' * 2} clicked on create a new filter. {'*' * 2} at {date_time_prog} {'*' * 2}\n"
            filename = log_message.replace('*', '').strip().replace(' ', '_')
            logs_ss['ss'][f"{filename}_{date_time_prog}"] = screenshot_img
            logs_ss['logs'].append(log_message)
            print(log_message)

            input_field = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, "//label[text()='From']/following::input[@type='text']")))
            for char in sender_mail:  # Type email character by character
                time.sleep(random.uniform(0.1, 1))  # Add random delay between keystrokes
                input_field.send_keys(char)
            time.sleep(random.uniform(1, 5))
            screenshot = self.driver.get_screenshot_as_png()
            screenshot_img = Image.open(BytesIO(screenshot))
            date_time_prog = datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
            log_message = f"\n\n\t{'*' * 2} mail written. {'*' * 2} at {date_time_prog} {'*' * 2}\n"
            filename = log_message.replace('*', '').strip().replace(' ', '_')
            logs_ss['ss'][f"{filename}_{date_time_prog}"] = screenshot_img
            logs_ss['logs'].append(log_message)
            print(log_message)


            create_filter_path = "//div[text()='Create filter' and @tabindex='0']"
            if check_xpath_exists(self.driver, create_filter_path):
                WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, create_filter_path))).click()
                # print(f"\n\n\t{'*' * 2} clicked on Create filter {'*' * 2}\n")
                time.sleep(random.uniform(1, 5))
                screenshot = self.driver.get_screenshot_as_png()
                screenshot_img = Image.open(BytesIO(screenshot))
                date_time_prog = datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
                log_message = f"\n\n\t{'*' * 2} clicked on Create filter. {'*' * 2} at {date_time_prog} {'*' * 2}\n"
                filename = log_message.replace('*', '').strip().replace(' ', '_')
                logs_ss['ss'][f"{filename}_{date_time_prog}"] = screenshot_img
                logs_ss['logs'].append(log_message)
                print(log_message)


                WebDriverWait(self.driver, 60).until(EC.presence_of_element_located((By.XPATH, "//label[text()='Never send it to Spam']"))).click()
                # print(f"\n\n\t{'*' * 2} clicked on Never send it to Spam {'*' * 2}\n")
                time.sleep(random.uniform(1, 5))
                screenshot = self.driver.get_screenshot_as_png()
                screenshot_img = Image.open(BytesIO(screenshot))
                date_time_prog = datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
                log_message = f"\n\n\t{'*' * 2} clicked on Never send it to Spam. {'*' * 2} at {date_time_prog} {'*' * 2}\n"
                filename = log_message.replace('*', '').strip().replace(' ', '_')
                logs_ss['ss'][f"{filename}_{date_time_prog}"] = screenshot_img
                logs_ss['logs'].append(log_message)
                print(log_message)

                WebDriverWait(self.driver, 60).until(EC.presence_of_element_located((By.XPATH, "//div[text()='Create filter' and @role='button']"))).click()
                time.sleep(random.uniform(1, 5))
                screenshot = self.driver.get_screenshot_as_png()
                screenshot_img = Image.open(BytesIO(screenshot))
                date_time_prog = datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
                log_message = f"\n\n\t{'*' * 2} filter created. {'*' * 2} at {date_time_prog} {'*' * 2}\n"
                filename = log_message.replace('*', '').strip().replace(' ', '_')
                logs_ss['ss'][f"{filename}_{date_time_prog}"] = screenshot_img
                logs_ss['logs'].append(log_message)
                print(log_message)

                # //label[text()='Never send it to Spam']/preceding-sibling::input[@type="checkbox"]
            else:
                # print(f"\n{'-' * 5} error in creating filter {'-' * 5}\n")
                screenshot = self.driver.get_screenshot_as_png()
                screenshot_img = Image.open(BytesIO(screenshot))
                date_time_prog = datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
                log_message = f"\n\n\t{'*' * 2} error in creating filter. {'*' * 2} at {date_time_prog} {'*' * 2}\n"
                filename = log_message.replace('*', '').strip().replace(' ', '_')
                logs_ss['ss'][f"{filename}_{date_time_prog}"] = screenshot_img
                logs_ss['logs'].append(log_message)
                print(log_message)
        except Exception as e:
            print(f"\n{'-' * 5} error in changing language: {e} {'-' * 5}\n")
            screenshot = self.driver.get_screenshot_as_png()
            screenshot_img = Image.open(BytesIO(screenshot))
            date_time_prog = datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
            log_message = f"\n\n\t{'*' * 2} error in changing language: {e}. {'*' * 2} at {date_time_prog} {'*' * 2}\n"
            filename = log_message.replace('*', '').strip().replace(' ', '_')
            logs_ss['ss'][f"{filename}_{date_time_prog}"] = screenshot_img
            logs_ss['logs'].append(log_message)
            print(log_message)

        time.sleep(random.uniform(1, 5))
        return self.driver, logs_ss
            
    def change_language(self, lang):
        time.sleep(random.uniform(5, 10))
        logs_ss = {'logs': [], 'ss': {}}
        setting_icon_xpath = "//a[@role='button' and @aria-label='Settings']"
        if check_xpath_exists(self.driver, "//h2[@tabindex='-1' and text()='Settings']"):
            log_message = f"\n\n\t{'*' * 2} already in settings. {'*' * 2} at {date_time_prog} {'*' * 2}\n"
            logs_ss['logs'].append(log_message)
            print(log_message)
            general_set_path = "//a[@aria-selected='false' and text()='General']"
            if check_xpath_exists(self.driver, general_set_path):
                WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, general_set_path))).click()
                screenshot = self.driver.get_screenshot_as_png()
                screenshot_img = Image.open(BytesIO(screenshot))
                date_time_prog = datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
                log_message = f"\n\n\t{'*' * 2} arrived in general settings. {'*' * 2} at {date_time_prog} {'*' * 2}\n"
                filename = log_message.replace('*', '').strip().replace(' ', '_')
                logs_ss['ss'][f"{filename}_{date_time_prog}"] = screenshot_img
                logs_ss['logs'].append(log_message)
                print(log_message)
                time.sleep(random.uniform(1, 5))

        elif check_xpath_exists(self.driver, setting_icon_xpath):
            WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, setting_icon_xpath))).click()
            time.sleep(random.uniform(1, 5))
            screenshot = self.driver.get_screenshot_as_png()
            screenshot_img = Image.open(BytesIO(screenshot))
            date_time_prog = datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
            log_message = f"\n\n\t{'*' * 2} clicked on setting icon. {'*' * 2} at {date_time_prog} {'*' * 2}\n"
            filename = log_message.replace('*', '').strip().replace(' ', '_')
            logs_ss['ss'][f"{filename}_{date_time_prog}"] = screenshot_img
            logs_ss['logs'].append(log_message)
            print(log_message)

            WebDriverWait(self.driver, 60).until(EC.presence_of_element_located((By.XPATH, "//button[@aria-label='See all settings' and text()='See all settings']"))).click()
            time.sleep(random.uniform(1, 5))
            screenshot = self.driver.get_screenshot_as_png()
            screenshot_img = Image.open(BytesIO(screenshot))
            date_time_prog = datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
            log_message = f"\n\n\t{'*' * 2} clicked on see all settings. {'*' * 2} at {date_time_prog} {'*' * 2}\n"
            filename = log_message.replace('*', '').strip().replace(' ', '_')
            logs_ss['ss'][f"{filename}_{date_time_prog}"] = screenshot_img
            logs_ss['logs'].append(log_message)
            print(log_message)
        else:
            screenshot = self.driver.get_screenshot_as_png()
            screenshot_img = Image.open(BytesIO(screenshot))
            date_time_prog = datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
            log_message = f"\n\n\t{'*' * 2} unable to find setting path. {'*' * 2} at {date_time_prog} {'*' * 2}\n"
            filename = log_message.replace('*', '').strip().replace(' ', '_')
            logs_ss['ss'][f"{filename}_{date_time_prog}"] = screenshot_img
            logs_ss['logs'].append(log_message)
            print(log_message)
        try:
            
            WebDriverWait(self.driver, 60).until(EC.presence_of_element_located((By.XPATH, "//a[text()='Change language settings for other Google products']/preceding-sibling::select"))).click()
            screenshot = self.driver.get_screenshot_as_png()
            screenshot_img = Image.open(BytesIO(screenshot))
            date_time_prog = datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
            log_message = f"\n\n\t{'*' * 2} clicked on language size menu. {'*' * 2} at {date_time_prog} {'*' * 2}\n"
            filename = log_message.replace('*', '').strip().replace(' ', '_')
            logs_ss['ss'][f"{filename}_{date_time_prog}"] = screenshot_img
            logs_ss['logs'].append(log_message)
            print(log_message)
            # Extract the text of each option and store them in a list
            options = WebDriverWait(self.driver, 20).until(EC.presence_of_all_elements_located((By.XPATH, "//a[text()='Change language settings for other Google products']/preceding-sibling::select/option")))
            options_values = [option.get_attribute('value') for option in options]

            # Print the list to verify the result
            # print('------------------------- options_text: ', options_text)
            if lang in options_values:
                WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, f"//a[text()='Change language settings for other Google products']/preceding-sibling::select/option[@value='{lang}']"))).click()
                time.sleep(random.uniform(1, 5))
                screenshot = self.driver.get_screenshot_as_png()
                screenshot_img = Image.open(BytesIO(screenshot))
                date_time_prog = datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
                log_message = f"\n\n\t{'*' * 2} clicked on {lang} language. {'*' * 2} at {date_time_prog} {'*' * 2}\n"
                filename = log_message.replace('*', '').strip().replace(' ', '_')
                logs_ss['ss'][f"{filename}_{date_time_prog}"] = screenshot_img
                logs_ss['logs'].append(log_message)
                print(log_message)
                
                WebDriverWait(self.driver, 60).until(EC.presence_of_element_located((By.XPATH, "//a[text()='Change language settings for other Google products']/preceding-sibling::select"))).click()
                time.sleep(random.uniform(1, 5))
                screenshot = self.driver.get_screenshot_as_png()
                screenshot_img = Image.open(BytesIO(screenshot))
                date_time_prog = datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
                log_message = f"\n\n\t{'*' * 2} language selected. {'*' * 2} at {date_time_prog} {'*' * 2}\n"
                filename = log_message.replace('*', '').strip().replace(' ', '_')
                logs_ss['ss'][f"{filename}_{date_time_prog}"] = screenshot_img
                logs_ss['logs'].append(log_message)
                print(log_message)

                save_button = WebDriverWait(self.driver, 60).until(EC.presence_of_element_located((By.XPATH, "//button[text()='Save Changes']")))
                self.driver.execute_script("arguments[0].scrollIntoView();", save_button)
                screenshot = self.driver.get_screenshot_as_png()
                screenshot_img = Image.open(BytesIO(screenshot))
                date_time_prog = datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
                log_message = f"\n\n\t{'*' * 2} scrolled to save button. {'*' * 2} at {date_time_prog} {'*' * 2}\n"
                filename = log_message.replace('*', '').strip().replace(' ', '_')
                logs_ss['ss'][f"{filename}_{date_time_prog}"] = screenshot_img
                logs_ss['logs'].append(log_message)
                print(log_message)


                is_disabled = save_button.get_attribute('disabled') is not None
                if is_disabled:
                    screenshot = self.driver.get_screenshot_as_png()
                    screenshot_img = Image.open(BytesIO(screenshot))
                    date_time_prog = datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
                    log_message = f"\n\n\t{'*' * 2} already selected. {'*' * 2} at {date_time_prog} {'*' * 2}\n"
                    filename = log_message.replace('*', '').strip().replace(' ', '_')
                    logs_ss['ss'][f"{filename}_{date_time_prog}"] = screenshot_img
                    logs_ss['logs'].append(log_message)
                    print(log_message)

                else:
                    save_button.click()
                    time.sleep(random.uniform(1, 5))
                    screenshot = self.driver.get_screenshot_as_png()
                    screenshot_img = Image.open(BytesIO(screenshot))
                    date_time_prog = datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
                    log_message = f"\n\n\t{'*' * 2} changes saved. {'*' * 2} at {date_time_prog} {'*' * 2}\n"
                    filename = log_message.replace('*', '').strip().replace(' ', '_')
                    logs_ss['ss'][f"{filename}_{date_time_prog}"] = screenshot_img
                    logs_ss['logs'].append(log_message)
                    print(log_message)
            else:
                screenshot = self.driver.get_screenshot_as_png()
                screenshot_img = Image.open(BytesIO(screenshot))
                date_time_prog = datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
                log_message = f"\n\n\t{'*' * 2} please give page size among these. {'*' * 2} at {date_time_prog} {'*' * 2}\n"
                filename = log_message.replace('*', '').strip().replace(' ', '_')
                logs_ss['ss'][f"{filename}_{date_time_prog}"] = screenshot_img
                logs_ss['logs'].append(log_message)
                print(log_message)

        except Exception as e:
            screenshot = self.driver.get_screenshot_as_png()
            screenshot_img = Image.open(BytesIO(screenshot))
            date_time_prog = datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
            log_message = f"\n\n\t{'*' * 2} error in changing language. {'*' * 2} at {date_time_prog} {'*' * 2}\n"
            filename = log_message.replace('*', '').strip().replace(' ', '_')
            logs_ss['ss'][f"{filename}_{date_time_prog}"] = screenshot_img
            logs_ss['logs'].append(log_message)
            print(log_message)

        time.sleep(random.uniform(1, 5))
        return self.driver, logs_ss
    
    def change_max_page_size(self, page_size):
        time.sleep(random.uniform(5, 10))
        logs_ss = {'logs': [], 'ss': {}}
        setting_icon_xpath = "//a[@role='button' and @aria-label='Settings']"
        if check_xpath_exists(self.driver, "//h2[@tabindex='-1' and text()='Settings']"):
            log_message = f"\n\n\t{'*' * 2} already in settings. {'*' * 2} at {date_time_prog} {'*' * 2}\n"
            logs_ss['logs'].append(log_message)
            print(log_message)
            general_set_path = "//a[@aria-selected='false' and text()='General']"
            if check_xpath_exists(self.driver, general_set_path):
                WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, general_set_path))).click()
                screenshot = self.driver.get_screenshot_as_png()
                screenshot_img = Image.open(BytesIO(screenshot))
                date_time_prog = datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
                log_message = f"\n\n\t{'*' * 2} arrived in general settings. {'*' * 2} at {date_time_prog} {'*' * 2}\n"
                filename = log_message.replace('*', '').strip().replace(' ', '_')
                logs_ss['ss'][f"{filename}_{date_time_prog}"] = screenshot_img
                logs_ss['logs'].append(log_message)
                print(log_message)
                time.sleep(random.uniform(1, 5))

        elif check_xpath_exists(self.driver, setting_icon_xpath):
            WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, setting_icon_xpath))).click()
            time.sleep(random.uniform(1, 5))
            screenshot = self.driver.get_screenshot_as_png()
            screenshot_img = Image.open(BytesIO(screenshot))
            date_time_prog = datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
            log_message = f"\n\n\t{'*' * 2} clicked on setting icon. {'*' * 2} at {date_time_prog} {'*' * 2}\n"
            filename = log_message.replace('*', '').strip().replace(' ', '_')
            logs_ss['ss'][f"{filename}_{date_time_prog}"] = screenshot_img
            logs_ss['logs'].append(log_message)
            print(log_message)

            WebDriverWait(self.driver, 60).until(EC.presence_of_element_located((By.XPATH, "//button[@aria-label='See all settings' and text()='See all settings']"))).click()
            time.sleep(random.uniform(1, 5))
            screenshot = self.driver.get_screenshot_as_png()
            screenshot_img = Image.open(BytesIO(screenshot))
            date_time_prog = datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
            log_message = f"\n\n\t{'*' * 2} clicked on see all settings. {'*' * 2} at {date_time_prog} {'*' * 2}\n"
            filename = log_message.replace('*', '').strip().replace(' ', '_')
            logs_ss['ss'][f"{filename}_{date_time_prog}"] = screenshot_img
            logs_ss['logs'].append(log_message)
            print(log_message)
        else:
            screenshot = self.driver.get_screenshot_as_png()
            screenshot_img = Image.open(BytesIO(screenshot))
            date_time_prog = datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
            log_message = f"\n\n\t{'*' * 2} unable to find setting path. {'*' * 2} at {date_time_prog} {'*' * 2}\n"
            filename = log_message.replace('*', '').strip().replace(' ', '_')
            logs_ss['ss'][f"{filename}_{date_time_prog}"] = screenshot_img
            logs_ss['logs'].append(log_message)
            print(log_message)

        try:
            WebDriverWait(self.driver, 60).until(EC.presence_of_element_located((By.XPATH, "//td[text()='Show ']/select"))).click()
            screenshot = self.driver.get_screenshot_as_png()
            screenshot_img = Image.open(BytesIO(screenshot))
            date_time_prog = datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
            log_message = f"\n\n\t{'*' * 2} clicked on page size menu. {'*' * 2} at {date_time_prog} {'*' * 2}\n"
            filename = log_message.replace('*', '').strip().replace(' ', '_')
            logs_ss['ss'][f"{filename}_{date_time_prog}"] = screenshot_img
            logs_ss['logs'].append(log_message)
            print(log_message)

            # Extract the text of each option and store them in a list
            options = WebDriverWait(self.driver, 20).until(EC.presence_of_all_elements_located((By.XPATH, "//td[text()='Show ']/select/option")))
            options_text = [option.text for option in options]

            # Print the list to verify the result
            if page_size in options_text:
                    
                WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, f"//td[text()='Show ']/select/option[@value='{page_size}']"))).click()
                time.sleep(random.uniform(1, 5))
                screenshot = self.driver.get_screenshot_as_png()
                screenshot_img = Image.open(BytesIO(screenshot))
                date_time_prog = datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
                log_message = f"\n\n\t{'*' * 2} clicked on {page_size} page size. {'*' * 2} at {date_time_prog} {'*' * 2}\n"
                filename = log_message.replace('*', '').strip().replace(' ', '_')
                logs_ss['ss'][f"{filename}_{date_time_prog}"] = screenshot_img
                logs_ss['logs'].append(log_message)
                print(log_message)

                WebDriverWait(self.driver, 60).until(EC.presence_of_element_located((By.XPATH, "//td[text()='Show ']/select"))).click()
                time.sleep(random.uniform(1, 5))
                screenshot = self.driver.get_screenshot_as_png()
                screenshot_img = Image.open(BytesIO(screenshot))
                date_time_prog = datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
                log_message = f"\n\n\t{'*' * 2} page size selected. {'*' * 2} at {date_time_prog} {'*' * 2}\n"
                filename = log_message.replace('*', '').strip().replace(' ', '_')
                logs_ss['ss'][f"{filename}_{date_time_prog}"] = screenshot_img
                logs_ss['logs'].append(log_message)
                print(log_message)

                save_button = WebDriverWait(self.driver, 60).until(EC.presence_of_element_located((By.XPATH, "//button[text()='Save Changes']")))
                self.driver.execute_script("arguments[0].scrollIntoView();", save_button)
                screenshot = self.driver.get_screenshot_as_png()
                screenshot_img = Image.open(BytesIO(screenshot))
                date_time_prog = datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
                log_message = f"\n\n\t{'*' * 2} scrolled to save button. {'*' * 2} at {date_time_prog} {'*' * 2}\n"
                filename = log_message.replace('*', '').strip().replace(' ', '_')
                logs_ss['ss'][f"{filename}_{date_time_prog}"] = screenshot_img
                logs_ss['logs'].append(log_message)
                print(log_message)

                is_disabled = save_button.get_attribute('disabled') is not None
                if is_disabled:
                    screenshot = self.driver.get_screenshot_as_png()
                    screenshot_img = Image.open(BytesIO(screenshot))
                    date_time_prog = datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
                    log_message = f"\n\n\t{'*' * 2} already selected. {'*' * 2} at {date_time_prog} {'*' * 2}\n"
                    filename = log_message.replace('*', '').strip().replace(' ', '_')
                    logs_ss['ss'][f"{filename}_{date_time_prog}"] = screenshot_img
                    logs_ss['logs'].append(log_message)
                    print(log_message)
                else:
                    save_button.click()
                    # print(f"\n\n\t{'*' * 2} changes saved {'*' * 2}\n")
                    time.sleep(random.uniform(1, 5))
                    screenshot = self.driver.get_screenshot_as_png()
                    screenshot_img = Image.open(BytesIO(screenshot))
                    date_time_prog = datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
                    log_message = f"\n\n\t{'*' * 2} changes saved. {'*' * 2} at {date_time_prog} {'*' * 2}\n"
                    filename = log_message.replace('*', '').strip().replace(' ', '_')
                    logs_ss['ss'][f"{filename}_{date_time_prog}"] = screenshot_img
                    logs_ss['logs'].append(log_message)
                    print(log_message)
            else:
                screenshot = self.driver.get_screenshot_as_png()
                screenshot_img = Image.open(BytesIO(screenshot))
                date_time_prog = datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
                log_message = f"\n\n\t{'*' * 2} please give correct language among these. {'*' * 2} at {date_time_prog} {'*' * 2}\n"
                filename = log_message.replace('*', '').strip().replace(' ', '_')
                logs_ss['ss'][f"{filename}_{date_time_prog}"] = screenshot_img
                logs_ss['logs'].append(log_message)
                print(log_message)

        except Exception as e:
            screenshot = self.driver.get_screenshot_as_png()
            screenshot_img = Image.open(BytesIO(screenshot))
            date_time_prog = datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
            log_message = f"\n\n\t{'*' * 2} error in changing page. {'*' * 2} at {date_time_prog} {'*' * 2}\n"
            filename = log_message.replace('*', '').strip().replace(' ', '_')
            logs_ss['ss'][f"{filename}_{date_time_prog}"] = screenshot_img
            logs_ss['logs'].append(log_message)
            print(log_message)

        time.sleep(random.uniform(1, 5))
        return self.driver, logs_ss
        
    ##### ====================== setting work end ====================== #####

    ##### ====================== spam work start ====================== ##### 
    
    ##### report spam
    def report_spam(self):
        time.sleep(random.uniform(5, 10))
        logs_ss = {'logs': [], 'ss': {}}
        date_time_prog = datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
        log_message = f"\n\n\t{'*' * 2} arrived in reporting spam. {'*' * 2} at {date_time_prog} {'*' * 2}\n"
        print(log_message)
        logs_ss['logs'].append(log_message)
        
        if WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, "//div[@title='Report spam' and @role='button']"))):
            WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, "//div[@title='Report spam' and @role='button']"))).click()
            screenshot = self.driver.get_screenshot_as_png()
            screenshot_img = Image.open(BytesIO(screenshot))
            date_time_prog = datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
            log_message = f"\n\n\t{'*' * 2} reported as spam. {'*' * 2} at {date_time_prog} {'*' * 2}\n"
            filename = log_message.replace('*', '').strip().replace(' ', '_')
            logs_ss['ss'][f"{filename}_{date_time_prog}"] = screenshot_img
            print(log_message)
            logs_ss['logs'].append(log_message)
            time.sleep(random.uniform(1, 5))

            if check_xpath_exists(self.driver, "//button[.//span[text()='Report spam']]"):
                WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, "//button[.//span[text()='Report spam']]"))).click()
                screenshot = self.driver.get_screenshot_as_png()
                screenshot_img = Image.open(BytesIO(screenshot))
                date_time_prog = datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
                log_message = f"\n\n\t{'*' * 2} spam reported successfully. {'*' * 2} at {date_time_prog} {'*' * 2}\n"
                filename = log_message.replace('*', '').strip().replace(' ', '_')
                logs_ss['ss'][f"{filename}_{date_time_prog}"] = screenshot_img
                print(log_message)
                logs_ss['logs'].append(log_message)
            # else:
            #     screenshot = self.driver.get_screenshot_as_png()
            #     screenshot_img = Image.open(BytesIO(screenshot))
            #     date_time_prog = datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
            #     log_message = f"\n\n\t{'*' * 2} error in reporting spam. {'*' * 2} at {date_time_prog} {'*' * 2}\n"
            #     filename = log_message.replace('*', '').strip().replace(' ', '_')
            #     logs_ss['ss'][f"{filename}_{date_time_prog}"] = screenshot_img
            #     print(log_message)
            #     logs_ss['logs'].append(log_message)

        else:
            screenshot = self.driver.get_screenshot_as_png()
            screenshot_img = Image.open(BytesIO(screenshot))
            date_time_prog = datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
            log_message = f"\n\n\t{'*' * 2} error in reporting spam. {'*' * 2} at {date_time_prog} {'*' * 2}\n"
            filename = log_message.replace('*', '').strip().replace(' ', '_')
            logs_ss['ss'][f"{filename}_{date_time_prog}"] = screenshot_img
            print(log_message)
            logs_ss['logs'].append(log_message)
        # WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, "//button[.//span[text()='Report spam']]"))).click()
        # time.sleep(5)
        return self.driver, logs_ss

    ##### go to spam working
    def go_to_spam(self):
        logs_ss = {'logs': [], 'ss': {}}
        if check_xpath_exists(self.driver, "//a[contains(@href, '#spam') and @tabindex='-1']") == False and check_xpath_exists(self.driver,"(//span[@role='button']/span[text()='More'])[1]"):  # Check if not in inbox
            going_to_spam = f"\n\n\t{'*' * 2} going to spam {'*' * 2}\n"
            print(going_to_spam)
            logs_ss['logs'].append(going_to_spam)
            time.sleep(3)

            WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, "(//span[@role='button']/span[text()='More'])[1]"))).click()  # Click More button
            clicked_on_more = f"\n\n\t{'*' * 2} clicked on more {'*' * 2}\n"
            print(clicked_on_more)
            logs_ss['logs'].append(clicked_on_more)
            screenshot = self.driver.get_screenshot_as_png()
            clicked_on_more_ss = Image.open(BytesIO(screenshot))
            filename = clicked_on_more.replace('*', '').strip().replace(' ', '_')
            logs_ss['ss'][f"{filename}_{datetime.now().strftime('%Y-%m-%d_%H_%M_%S')}"] = clicked_on_more_ss



            WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, "//a[text()='Spam']"))).click()  # Click Spam link
            arrived_in_spam = f"\n\n\t{'*' * 2} arrived in spam {'*' * 2}\n"
            print(arrived_in_spam)
            logs_ss['logs'].append(arrived_in_spam)
            screenshot = self.driver.get_screenshot_as_png()
            arrived_in_spam_ss = Image.open(BytesIO(screenshot))
            filename = arrived_in_spam.replace('*', '').strip().replace(' ', '_')
            logs_ss['ss'][f"{filename}_{datetime.now().strftime('%Y-%m-%d_%H_%M_%S')}"] = arrived_in_spam_ss


        else:
            already_in_spam = f"\n\n\t{'*' * 2} already in spam! {'*' * 2}\n"
            logs_ss['logs'].append(already_in_spam)
            screenshot = self.driver.get_screenshot_as_png()
            already_in_spam_ss = Image.open(BytesIO(screenshot))
            filename = already_in_spam.replace('*', '').strip().replace(' ', '_')
            logs_ss['ss'][f"{filename}_{datetime.now().strftime('%Y-%m-%d_%H_%M_%S')}"] = already_in_spam_ss
            print(already_in_spam)



        time.sleep(random.uniform(1, 5))  # Wait for 5-10 seconds
        return self.driver, logs_ss
    
    ##### not spam work
    def report_not_spam(self):
        time.sleep(random.uniform(5, 10))
        logs_ss = {'logs': [], 'ss': {}}
        not_spam = "(//div[@role='button']/div[text()='Not spam'])"
        spam_buttons = WebDriverWait(self.driver, 60).until(
                EC.presence_of_all_elements_located((By.XPATH, not_spam))
            )
        # print(f"\n\n\t{'*' * 2} len delete forever buttons: {len(df_buttons)} {'*' * 2}\n")
        if len(spam_buttons) > 1:
            # print(f"\n\n\t{'*' * 2} delete forever buttons: {df_buttons} {'*' * 2}\n")
            not_spam = not_spam + "[2]"
        if check_xpath_exists(self.driver, not_spam):
            WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, not_spam))).click()
            screenshot = self.driver.get_screenshot_as_png()
            screenshot_img = Image.open(BytesIO(screenshot))
            date_time_prog = datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
            log_message = f"\n\n\t{'*' * 2} not spam successfully. {'*' * 2} at {date_time_prog} {'*' * 2}\n"
            filename = log_message.replace('*', '').strip().replace(' ', '_')
            logs_ss['ss'][f"{filename}_{date_time_prog}"] = screenshot_img
            print(log_message)
            logs_ss['logs'].append(log_message)
        else:
            screenshot = self.driver.get_screenshot_as_png()
            screenshot_img = Image.open(BytesIO(screenshot))
            date_time_prog = datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
            log_message = f"\n\n\t{'*' * 2} not spam button not exist. {'*' * 2} at {date_time_prog} {'*' * 2}\n"
            filename = log_message.replace('*', '').strip().replace(' ', '_')
            logs_ss['ss'][f"{filename}_{date_time_prog}"] = screenshot_img
            print(log_message)
            logs_ss['logs'].append(log_message)
        time.sleep(random.uniform(1, 5))
        return self.driver, logs_ss
    ##### ====================== spam work end ====================== #####

    ##### ====================== general work start ====================== #####

    
        
    def send_message(self, recipients_mail, subject_text):
        WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, "//div[text()='Compose']"))).click()
        recipients = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, "//input[@aria-label='To recipients']")))
        # recipients.send_keys("TLDR")
        for char in recipients_mail:  # Type email character by character
            time.sleep(random.uniform(0.1, 0.5))  # Add random delay between keystrokes
            recipients.send_keys(char)
        time.sleep(2)
        subject = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, "//input[@aria-label='Subject']")))

        for char in subject_text:  # Type email character by character
            time.sleep(random.uniform(0.1, 0.5))  # Add random delay between keystrokes
            subject.send_keys(char)
        time.sleep(2)
        WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, "//div[@role='button' and text()='Send']"))).click()
        
    ##### ====================== general work start ====================== #####
