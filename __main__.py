from selenium import webdriver
from selenium.webdriver.chrome.service import Service

from lib.webhook import Messages
from lib.whatap import Whatap
from lib.stats import SpreadSheet

import datetime

monitoring_start_time = '07'
now = datetime.datetime.now()

options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
#options.add_experimental_option('detach', True)
service = Service('chromedriver.exe')
chrome = webdriver.Chrome(service=service, options=options)

if __name__ == '__main__':
    try:
        if now.hour >= 17:
            monitoring_end_time = '17'
            end_time = "17:00"
        else:
            monitoring_end_time = '10'
            end_time = "10:00"
            
        whatap = Whatap(chrome)
        
        whatap.login()
        max_user, max_time = whatap.active_user(monitoring_start_time, monitoring_end_time)
        
        server_list = whatap.resource(end_time)
        #network_in, network_out = 0.475, 1.087
        network_in, network_out = whatap.network(monitoring_start_time, monitoring_end_time)

        avg = server_list.printer(max_user, max_time, network_in, network_out)
        
        google_sheet = SpreadSheet(max_user, max_time, network_in, network_out)
        doc = google_sheet.certify()
        google_sheet.update_sheet(google_sheet.init_sheet(doc), avg, now.hour)
    except Exception as error:
        Messages.errormsg(monitoring_end_time, error)
    else:
        #Messages.successmsg(monitoring_end_time)
        Messages.temp(monitoring_end_time, max_user, max_time, network_in, network_out, avg)