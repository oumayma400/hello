from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import sys,os
from pathlib import Path
path = Path(os.path.abspath(__file__))
parrent_path = path.parent.absolute()

Locators = os.path.dirname(parrent_path) + os.path.sep + "Locators";
Locators2 = Locators.replace('\\', '/')
sys.path.append(Locators2)
from Locators import Locator
import time
class ExpertCampaignPage(object):
    def __init__(self):
    	print("hello")
    	#self.driver = driver
    	#driver.find_element(By.ID, Locator.CreateCampaign_button).click()
        #self.search_text = driver.find_element(By.XPATH, Locator.search_text)
        #self.submit = driver.find_element(By.XPATH, Locator.submit)
    def Cc(self, aa, driver):
        print(aa)

        print(os.getcwd())
        time.sleep(5)
        #driver.refresh()
        #driver.find_element_by_link_text('Campaigns').click()
        #driver.find_element(By.LINK_TEXT,Locator.link_campaign).click()
        try:
            myElem = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.LINK_TEXT, Locator.link_campaign)))
            myElem.click()
            time.sleep(2)

        except Exception as e:
            print(e)
        try:
            myElem = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, Locator.CreateCampaign_button)))
            myElem.click()
            myElem = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH , Locator.button_expert_camp)))
            myElem.click()
            # driver.find_element(By.ID, Locator.CreateCampaign_button).click()
            # driver.find_element(By.XPATH , Locator.button_expert_camp).click()
            return True
        except Exception as es:
            print(es)
            return False
