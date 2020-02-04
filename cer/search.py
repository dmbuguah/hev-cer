from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from cer.constants import CAR_MAKE, CAR_MODEL, CAR_YOM, CAR_SORT_BY

driver = webdriver.Chrome()
driver.get('https://carfromjapan.com/')

assert 'CAR FROM JAPAN' in driver.title

make = driver.find_element_by_xpath(CAR_MAKE)
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
except Exception as e:
    print('Element not found: {}'.format(str(e.args[0])))

model = driver.find_element_by_xpath(CAR_MODEL)
all_models = model.find_elements_by_tag_name("option")
for model_option in all_models:
    if 'C-Class' in model_option.text:
        model_option.click()
        break

driver.find_element_by_id("year-control-minYear").click()

yom = driver.find_element_by_xpath(CAR_YOM)
all_yoms = yom.find_elements_by_tag_name("option")
for all_yom in all_yoms:
    if str(all_yom.get_attribute("value")) == '2013':
        all_yom.click()
        break

driver.find_element_by_class_name('btni-search').click()

try:
    element = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, "option[value='priceUSD']"))
    )
except Exception as e:
    print('Element not found: {}'.format(str(e.args[0])))


sort_by = driver.find_element_by_xpath(CAR_SORT_BY)
all_sort_by = sort_by.find_elements_by_tag_name("option")
sort_price = [sb for sb in all_sort_by if sb.get_attribute('value') == 'priceUSD']
if sort_price:
    sort_price[0].click()

try:
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.CLASS_NAME, 'fa-sort-up'))
    )
    print('Element found')
except Exception as e:
    print('Element not found: {}'.format(str(e.args[0])))

dcar_table = driver.find_element_by_class_name('table-car')
dcar_rows = dcar_table.find_elements(By.TAG_NAME, "tr")
next(iter(dcar_rows))
for dcar_row in dcar_rows:
    row_items = dcar_row.find_elements(By.TAG_NAME, "td")
    if row_items:
        for row_item in row_items:
            pass
    print('yer')
driver.quit()
