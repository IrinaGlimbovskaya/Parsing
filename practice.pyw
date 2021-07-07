from selenium import webdriver
from selenium.webdriver.common.keys import Keys

print("программа для закачки курса INTUIT")
url = input("Введите ссылку на курс:")

driver = webdriver.Firefox('C://Users//Irina//AppData//Local//Programs//Python//Python36')
driver.get( url )

driver.find_element_by_partial_link_text("Лекция 1").click()
