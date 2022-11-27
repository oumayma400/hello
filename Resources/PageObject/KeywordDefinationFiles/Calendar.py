import sys
from datetime import datetime
import random
import time
#print(os.getcwd())
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sys,os
from pathlib import Path
path = Path(os.path.abspath(__file__))
parrent_path = path.parent.absolute()

Locators = os.path.dirname(parrent_path.parent.absolute()) + os.path.sep + "Locators";
Locators2 = Locators.replace('\\', '/')
sys.path.append(Locators2)


from selenium.webdriver.common.by import By
import Locator


def singel_calendar_start(driver, dateinput):
    step1 = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, Locator.collect_calendar_id_startdate)))
    step1.send_keys(dateinput)
    # step1.click()
    datetime_splited=dateinput.split(' ')
    datetab=datetime_splited[0]
    datetab=datetab.split('/')
    timeinput = datetime_splited[1]
    timeinput=timeinput.split(':')
    print("timeinput", timeinput)



    start=WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, Locator.collect_calendar_start_YM)))
    start.click()
    time.sleep(1)
    # /html/body/div[2]/div[2]/div/owl-date-time-container/div[2]/owl-date-time-calendar/div[1]/div/button/span
    # /html/body/div[2]/div[2]/div/owl-date-time-container/div[2]/owl-date-time-calendar/div[2]/owl-date-time-multi-year-view
    #/html/body/div[2]/div[2]/div/owl-date-time-container/div[2]/owl-date-time-calendar/div[2]/owl-date-time-multi-year-view/table/tbody/tr[2]/td[3]/span
    year_month= Locator.start +"/owl-date-time-calendar/div[2]/owl-date-time-multi-year-view"
    #Y_M_widget = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, year_month)))



    # Y_M_widget=driver.find_element_by_xpath(year_month)
    xpathyear= "/*[contains(text(),'"+ str(datetab[0])+"')]"
    print(xpathyear)
    print(1)

    # table = driver.find_elements_by_xpath ("//*[@class= 'owl-dt-calendar-table owl-dt-calendar-multi-year-table']/tbody")
    #
    # for i in range(len(table)):
    #     print(table[i])
    #     table2 = driver.find_elements_by_xpath ("//*[@class= 'owl-dt-calendar-table owl-dt-calendar-multi-year-table']/tbody/tr["+str(i)+"]")
    #     for j in range(len(table2)):
    #
    #         check= table2[j].find_element_by_xpath(".//td["+str(j)+ "]/span")
    #         print(check)
    #         if check==str(datetab[0]):
    #             check.click()

    # year = Y_M_widget.find_element_by_xpath(xpathyear)
    # year.click()
    xpathmonth= "//*[contains(text(),'"+ str(datetab[1])+"')]"
    print(2)
    month= WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, xpathmonth)))
    month.click()

    #"//span[@class='owl-dt-calendar-cell-content'][text()='28']"
    if(int(datetab[2]) <10):
        daynumber=int(datetab[2])%10
    else:
        daynumber=datetab[2]
    xpathday=  "//span[@class='owl-dt-calendar-cell-content'][text()="+"'" +str(daynumber)+"']"
    print(xpathday)
    print(3)
    day= WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH,xpathday)))
    # day= start.find_element_by_xpath("//*[contains(text(), '2022')]").click()
    day.click()
    print(4)
    hour= WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//owl-date-time-timer/owl-date-time-timer-box[1]/label/input")))
    hour.clear()
    hour.send_keys(str(timeinput[0]))
    print(5)
    minute= WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//owl-date-time-timer/owl-date-time-timer-box[2]/label/input")))
    minute.clear()
    minute.send_keys(str(timeinput[1]))
    second= WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//owl-date-time-timer/owl-date-time-timer-box[3]/label/input")))
    second.clear()
    second.send_keys(str(timeinput[2]))
    time.sleep(2)
    set= WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'Set')]")))
    set.click()
    #start.find_element_by_xpath("//*[contains(text(),'2020')]").click()












def singel_calendar_stop(driver, dateinput):
    step1 = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, Locator.collect_calendar_id_stopdate)))
    step1.click()
    datetime_splited=dateinput.split(' ')
    datetab=datetime_splited[0]
    datetab=datetab.split('/')
    timeinput = datetime_splited[1]
    timeinput=timeinput.split(':')
    print("timeinput", timeinput)



    start=WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, Locator.collect_calendar_stop_YM)))
    start.click()
    time.sleep(1)
    xpathyear= "//*[contains(text(),'"+ str(datetab[0])+"')]"
    year= WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, xpathyear)))
    year.click()
    xpathmonth= "//*[contains(text(),'"+ str(datetab[1])+"')]"
    month= WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, xpathmonth)))
    month.click()

    #"//span[@class='owl-dt-calendar-cell-content'][text()='28']"
    if(int(datetab[2]) <10):
        daynumber=int(datetab[2])%10
    else:
        daynumber=datetab[2]
    xpathday=  "//span[@class='owl-dt-calendar-cell-content'][text()="+"'" +str(daynumber)+"']"
    print(xpathday)
    day= WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH,xpathday)))
    day.click()
    hour= WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//owl-date-time-timer/owl-date-time-timer-box[1]/label/input")))
    hour.clear()
    hour.send_keys(str(timeinput[0]))
    minute= WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//owl-date-time-timer/owl-date-time-timer-box[2]/label/input")))
    minute.clear()
    minute.send_keys(str(timeinput[1]))
    second= WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//owl-date-time-timer/owl-date-time-timer-box[3]/label/input")))
    second.clear()
    second.send_keys(str(timeinput[2]))
    time.sleep(2)
    set= WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'Set')]")))
    set.click()
