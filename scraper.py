from concurrent.futures import ThreadPoolExecutor
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.alert import Alert
import time
from bs4 import BeautifulSoup
import re
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import csv
import os
import requests
from selenium.webdriver.support.ui import Select
import openpyxl
from datetime import datetime
import os
from selenium.webdriver.support.ui import Select
import csv
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.remote.webelement import WebElement
import openpyxl
import pandas as pd
from selenium.common.exceptions import StaleElementReferenceException, NoSuchWindowException


def initilize_driver():
        # options = Options()
        # # options.add_experimental_option('debuggerAddress', '127.0.0.1:9222')
        # options.add_argument('start-maximized')
        # driver = webdriver.Chrome(options=options)
        # action = ActionChains(driver)

        options = Options()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument(f"--log-level=3")
        options.add_argument('start-maximized')
        driver = webdriver.Chrome(service=Service(executable_path="/usr/bin/chromedriver"),options=options)
        action = ActionChains(driver)
            
        driver.get("https://www.flashscore.com/")
        livebutton=WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH,'//div[text()="LIVE"]')))
        livebutton.click()
        
        time.sleep(5)
        
        try:
            WebDriverWait(driver,20).until(EC.presence_of_all_elements_located((By.XPATH,'//div[@class="event__info"]/following-sibling::*')))
            expand_buttons=driver.find_elements(By.XPATH,'//div[@class="event__info"]/following-sibling::*') 
            for button in expand_buttons:
                button.click()
        except:
            pass
        
        return driver,action

def validate(ele):
    text=ele.text if ele is not None else ""
    if "GOAL" in text:
        text=text.replace("GOAL","")
    return text
    

def Scrape(driver,action):
    try:
        # ? clicking on expand buttons if exist
        expand_buttons=driver.find_elements(By.XPATH,'//div[@class="event__info"]/following-sibling::*') 
        for button in expand_buttons:
                driver.execute_script("arguments[0].click();",button)
                # button.click()
                
    except NoSuchWindowException:
        driver,action=initilize_driver()
                
    # ? waiting for live matches to load 
    WebDriverWait(driver,20).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR,"section.event")))
    soup=BeautifulSoup(driver.page_source,"html.parser")
    matches=soup.select('div[title="Click for match detail!"]')  
    headers = soup.select('.event__titleBox')


    
    live_leagues=[
            
    ]
        

    # ? iterating in matches
    for match in matches:
        
        header = match.find_previous(class_='event__titleBox')

        Country = header.select_one(".event__title--type").text.strip().replace(":","")
        League_Name = header.select_one(".event__title--name").text.strip()
        

        
        league=match.find("div",class_="event__titleBox")
        league=validate(league)
        team1=match.select('div.event__participant')[0]
        team1=validate(team1)
        team2=match.select('div.event__participant')[1]
        team2=validate(team2)
        time=match.select_one(".event__stage--block")
        time=validate(time).replace("\xa0","")
        team1_score=match.find("div",class_="event__score event__score--home")
        team1_score=validate(team1_score)
        
        if team1_score=="":
              team1_score=match.find("div",class_="event__score event__score--home highlighted")
              team1_score=validate(team1_score)
              
        team2_score=match.find("div",class_="event__score event__score--away")
        team2_score=validate(team2_score)
        
        if team2_score=="":
            team2_score=match.find("div",class_="event__score event__score--away highlighted")
            team2_score=validate(team2_score)
        
        team1_logo=match.select_one(".event__logo.event__logo--home")["src"]
        team2_logo=match.select_one(".event__logo.event__logo--away")["src"]
        
        
        
        # match_data = {
        # "country":Country,
        # "league": League_Name,
        # "team1": team1,
        # "team2": team2,
        # "time": time,
        # "team1_score": team1_score,
        # "team2_score": team2_score
        # }
        
        
        
        match={
                "league":{
                    "name":League_Name,
                    "country":Country,
                     "time": time,
                },
                "teams":{
                    "team1":{
                    "name":team1,
                    "logo":team1_logo,
                    "score":team1_score
                    },
                    "team2":{
                    "name":team2,
                    "logo":team2_logo,
                    "score":team2_score
                    }
                },
                "goals":{
                    "team1":team1_score,
                    "team2":team2_score,
                     "time": time,
                }
            }
    
        live_leagues.append(match)
    return live_leagues,driver,action
        
        
# while True:
#   Scrape()
#   time.sleep(1)



