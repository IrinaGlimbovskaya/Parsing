from selenium import webdriver
from selenium.webdriver.common.keys import Keys
driver = webdriver.Firefox('C://Users//Irina//AppData//Local//Programs//Python//Python36')
url = "https://sudoku.org.ua/rus/"
driver.get(url)
el = driver.find_element_by_css_selector('div.mapId span')
print(el.text)
lst_li = driver.find_elements_by_css_selector('ul.tab li span')
for num in range(len(lst_li)):
    print(lst_li[num].text)
