from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from lib.locator import WhatapLocators
from lib.stats import Stat

import datetime
import pyotp
import time

today = datetime.date.today()

class Whatap:
    def __init__(self, chrome):
        self.chrome = chrome
        self.whatap_url = "" ## 모니터링 콘솔 URL
        self.whatap_id = "" ## 모니터링 계정
        self.whatap_pw = "" ## 모니터링 계정 비밀번호
        self.otp = "" ## 모니터링 계정 otp key
        
        
    def wait(self, element, locator, waiting=15):
        if element == "ID":
            WebDriverWait(self.chrome, waiting).until(
                expected_conditions.visibility_of_all_elements_located(
                (By.ID, locator)))
        elif element == "CLASS":
            WebDriverWait(self.chrome, waiting).until(
                expected_conditions.visibility_of_all_elements_located(
                (By.CLASS_NAME, locator)))
        
    def click(self, html, second=0.6):
        html.click()
        time.sleep(second)
        return html
    
    def login(self):
        self.chrome.get(self.whatap_url)
        
        id = self.chrome.find_element(By.CSS_SELECTOR, WhatapLocators.ID)
        id.send_keys(self.whatap_id)

        pw = self.chrome.find_element(By.CSS_SELECTOR, WhatapLocators.PW)
        pw.send_keys(self.whatap_pw)
        
        self.click(self.chrome.find_element(By.CSS_SELECTOR, WhatapLocators.LOGIN))
        
        self.wait("ID", "validate_otp_token")

        totp = pyotp.TOTP(self.otp)
        google_otp = totp.now()

        otp = self.chrome.find_element(By.CSS_SELECTOR, WhatapLocators.OTP)
        otp.send_keys(google_otp)

        self.click(self.chrome.find_element(By.CSS_SELECTOR, WhatapLocators.LOGIN2))

        self.wait("CLASS", "wdc_fulldom")
    
    def active_user(self, start_time, end_time):
        self.click(self.chrome.find_element(By.XPATH, WhatapLocators.KERIS_APM))
        self.wait("CLASS", "wdc_fulldom")

        self.click(self.chrome.find_element(By.XPATH, WhatapLocators.APM_ANALYTICS))
        self.click(self.chrome.find_element(By.XPATH, WhatapLocators.APM_METRICS),2)

        self.click(self.chrome.find_element(By.XPATH, WhatapLocators.APM_AGENT),1)
        self.click(self.chrome.find_element(By.XPATH, WhatapLocators.APM_SELECT_AGENT))
        self.click(self.chrome.find_element(By.XPATH, WhatapLocators.APM_ALL_AGENT))
        self.click(self.chrome.find_element(By.XPATH, WhatapLocators.APM_CLOSE_AGENT))
      

        input_stime = self.click(self.chrome.find_element(By.XPATH, WhatapLocators.APM_STIME))
        input_stime.send_keys(f'{start_time}00{"".join(str(today).split("-"))}{end_time}00')
        input_stime.send_keys(Keys.ENTER)

        self.click(self.chrome.find_element(By.XPATH, WhatapLocators.APM_INTERVAL))
        self.click(self.chrome.find_element(By.XPATH, WhatapLocators.APM_COMMON_INTERVAL))

        self.click(self.chrome.find_element(By.XPATH, WhatapLocators.APM_USER))
        self.click(self.chrome.find_element(By.XPATH, WhatapLocators.APM_ACTIVE_USER))

        self.wait("CLASS", "wdc_fulldom")

        max_user = self.click(self.chrome.find_element(By.CSS_SELECTOR, WhatapLocators.APM_MAX_USER)).text
        sync_user = max_user.split()
        max_time = self.chrome.find_elements(By.CSS_SELECTOR, WhatapLocators.APM_MAX_TIME)
       
        return int(sync_user[1]), max_time[1].text
    
    def resource(self, end_time):
        self.click(self.chrome.find_element(By.XPATH, WhatapLocators.KERIS_INFRA))
        self.wait("CLASS", "wdc_fulldom")
        self.click(self.chrome.find_element(By.LINK_TEXT, WhatapLocators.INFRA_REPORT), 2)

        self.click(self.chrome.find_element(By.CSS_SELECTOR, WhatapLocators.INFRA_DROPBOX), 1)
        self.click(self.chrome.find_element(By.XPATH, WhatapLocators.INFRA_DAILY_REPORT), 1)
        self.click(self.chrome.find_element(By.XPATH, WhatapLocators.INFRA_DATE))
        self.click(self.chrome.find_element(By.XPATH, WhatapLocators.INFRA_DATE_SELECT))
        self.click(self.chrome.find_element(By.XPATH, WhatapLocators.INFRA_STIME))
        self.click(self.chrome.find_element(By.XPATH, WhatapLocators.INFRA_STIME_SELECT))
        self.click(self.chrome.find_element(By.XPATH, WhatapLocators.INFRA_STIME_SELECT2))
        self.click(self.chrome.find_element(By.XPATH, WhatapLocators.INFRA_ETIME))
        
        infra_etime = self.chrome.find_element(By.XPATH, WhatapLocators.INFRA_ETIME_CLEAR)
        infra_etime.clear()
        infra_etime.send_keys(end_time)
 
        self.click(self.chrome.find_element(By.XPATH, WhatapLocators.INFRA_ETIME_ENTER))
        self.click(self.chrome.find_element(By.CSS_SELECTOR, WhatapLocators.INFRA_SEARCH))

        WebDriverWait(self.chrome, 10).until(
            expected_conditions.visibility_of_all_elements_located(
            (By.TAG_NAME, "td")))
        
        server_lists = [x.text.strip() for x in self.chrome.find_elements(By.XPATH, WhatapLocators.INFRA_LISTS)]
        server_list = Stat(server_lists)
        server_list.arrange()
        
        return server_list
    
    def network(self, start_time, end_time):
        self.click(self.chrome.find_element(By.XPATH, WhatapLocators.NETWORK_ANALYTICS))
        self.click(self.chrome.find_element(By.XPATH, WhatapLocators.NETWORK_METRICS), 2)

        n_stime = self.click(self.chrome.find_element(By.XPATH, WhatapLocators.NETWORK_STIME))
        n_stime.send_keys(f'{start_time}00{"".join(str(today).split("-"))}{end_time}00')
        n_stime.send_keys(Keys.ENTER)

        self.click(self.chrome.find_element(By.XPATH, WhatapLocators.NETWORK_INTERVAL))
        self.click(self.chrome.find_element(By.XPATH, WhatapLocators.NETWORK_COMMON_INTERVAL))
        self.click(self.chrome.find_element(By.XPATH, WhatapLocators.NETWORK_NETWORK))
        self.click(self.chrome.find_element(By.XPATH, WhatapLocators.NETWORK_IN))
        self.wait("CLASS", "wdc_fulldom", 300)

        n_network_in_max = self.chrome.find_element(By.CSS_SELECTOR, WhatapLocators.NETWORK_IN_MAX).text
        inbound = n_network_in_max.split()

        self.click(self.chrome.find_element(By.CSS_SELECTOR, WhatapLocators.NETWORK_IN_CLOSE), 1)
        self.click(self.chrome.find_element(By.CSS_SELECTOR, WhatapLocators.NETWORK_IN_CLOSE2))
        self.click(self.chrome.find_element(By.XPATH, WhatapLocators.NETWORK_OUT))
        self.wait("CLASS", "wdc_fulldom", 300)

        n_network_out_max = self.chrome.find_element(By.CSS_SELECTOR, WhatapLocators.NETWORK_OUT_MAX).text
        outbound = n_network_out_max.split()
        
        return float(inbound[1])/1000000000, float(outbound[1])/1000000000