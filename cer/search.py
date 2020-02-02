from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


driver = webdriver.Chrome()
driver.get('https://carfromjapan.com/')

assert 'CAR FROM JAPAN' in driver.title

make = driver.find_element_by_xpath(
        "//*[@id='__next']/div/section/header/div[2]/div[2]/div/form/div/div[2]/div[1]/select")
all_options = make.find_elements_by_tag_name("option")
for option in all_options:
    if 'Mercedes' in option.text:
        option.click()
        break

try:
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, "option[value='54317ca841472697138cfcc5']"))
    )
    print('Element found')
except Exception as e:
    print('Element not found: {}'.format(str(e.args[0])))

model = driver.find_element_by_xpath(
         "//*[@id='__next']/div/section/header/div[2]/div[2]/div/form/div/div[2]/div[2]/select")
all_models = model.find_elements_by_tag_name("option")
for model_option in all_models:
    if 'C-Class' in model_option.text:
        model_option.click()
        break

#driver.quit()
