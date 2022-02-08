import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
import pandas as pd
import numpy as np

def temperature_conversion(Fahrenheit):
    temperature_in_celsius = (Fahrenheit - 32) * (5/9)
    return temperature_in_celsius

day_of_the_week = []
low_temperature = []
high_temperature = []
day_description = []
night_description = []

url = 'https://weather.com/weather/tenday/l/San+Francisco+CA?canonicalCityId=dfdaba8cbe3a4d12a8796e1f7b1ccc7174b4b0a2d5ddb1c8566ae9f154fa638c';
pth = 'chromedriver.exe'

driver = webdriver.Chrome(pth)

driver.get(url)

sleep(7)

driver.find_element_by_css_selector('#truste-consent-button').click()
sleep(5)


for i in range(1,11):
    
    sleep(3)
    day_date = driver.find_element_by_xpath(f'/html/body/div[1]/main/div[2]/main/div[1]/section/div[2]/details[{i}]/div/div[1]/h3/span')
    sleep(2)
    day_temperatures = driver.find_element_by_xpath(f'/html/body/div[1]/main/div[2]/main/div[1]/section/div[2]/details[{i}]/div/div[1]/div/div[1]/span')
                                                
    sleep(2)
    night_temperatures = driver.find_element_by_xpath(f'/html/body/div[1]/main/div[2]/main/div[1]/section/div[2]/details[{i}]/div/div[3]/div/div[1]/span')
    sleep(2)
    get_day_description = driver.find_element_by_xpath(f'/html/body/div[1]/main/div[2]/main/div[1]/section/div[2]/details[{i}]/div/div[1]/p')
    sleep(2)
    get_night_description = driver.find_element_by_xpath(f'/html/body/div[1]/main/div[2]/main/div[1]/section/div[2]/details[{i}]/div/div[3]/p')
    sleep(5)

    day, space, date = day_date.text.partition(' ')
    day_of_the_week.append(day)

    day_temperatures = day_temperatures.text
    day_digits,day_symbol,day_space = day_temperatures.partition('°')

    int_day_temperature = int(day_digits)

    day_temperature_in_C = temperature_conversion(int_day_temperature)
    day_temperature_in_C = round(day_temperature_in_C,1)
    high_temperature.append(day_temperature_in_C)

    night_temperatures = night_temperatures.text

    night_digits,night_symbol,night_space = night_temperatures.partition('°')
    int_night_temperature = int(night_digits)

    night_temperature_in_C = temperature_conversion(int_night_temperature)
    night_temperature_in_C = round(night_temperature_in_C,1)
    low_temperature.append(night_temperature_in_C)

    day_description_str = get_day_description.text
    day_first,day_second,day_third = day_description_str.partition('.')
    day_description.append(day_first)
    
    night_description_str = get_night_description.text
    night_first,night_second,night_third = night_description_str.partition('.')
    night_description.append(night_first)

    sleep(5)
    driver.find_element_by_css_selector(f'#detailIndex{i} > summary > div > svg').click()
    sleep(4)


#########################################       SAVING IT INTO PANDAS DATAFRAME        #######################################################################

data = {'Days':day_of_the_week,'Low Temperature in C':low_temperature,'Night Description':night_description,'High Temperature in C':high_temperature,'Day Description':day_description}
dates_from_08 = pd.date_range('2022-02-08',periods=10,freq='D')

df = pd.DataFrame(data,index=dates_from_08)
    
df.index.name = 'Dates'
print(df)