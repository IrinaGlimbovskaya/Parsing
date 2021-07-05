
#== подключить библиотеки ===
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains


#== открыть файл и ссылку для первой лекции
print("программа для закачки курса INTUIT")
url = input("Введите ссылку на первую лекцию:")
file_name = input("Введите имя файла:")
##-- url = "https://www.intuit.ru/studies/courses/3734/976/lecture/27458"
##-- file_name = "exper.htm"
fhd = open( file_name, "w")
fhd.write("<html><head>\n")
fhd.write('<meta http-equiv="Content-Type" content="text/html; charset=cp1251">\n')
fhd.write('<link type="text/css" rel="stylesheet" href="ab.css">')
fhd.write("</head><body>\n")

driver = webdriver.Firefox('C://Users//Irina//AppData//Local//Programs//Python//Python36')

#== загрузить первую страницу
driver.get( url )
while True:
    doc_state = driver.execute_script("return document.readyState")
    if doc_state == 'complete':
        break

##-- извлечь и вывести все заголовки
text_header = ""
lect_headers  = driver.find_elements_by_css_selector('div.title span.zag')
for lect_header in lect_headers:
    text_header = lect_header.text
    html_header = '<div class = "zag"> '+ text_header + ' </div>'
    print( text_header)
    fhd.write( html_header)

##-- запомнить заголовок лекции
prev_header = text_header   

##-- извлечь содержимое лекции
contents = driver.find_elements_by_css_selector('div.spelling-content-entity')
content = contents[-1]
html_content = content.get_attribute("outerHTML")

##-- поправить ссылки на рисунки
html_content = html_content.replace('"/EDI', '"http://www.intuit.ru/EDI')

##-- записать результат в файл
fhd.write( html_content + "\n")


#== главный цикл подкачки страниц
##-- num = 3 для тестового прогона
while True:
    
    try:
       browser.find_element_by_class('div.next-button-wrapper').click()    
    except:
        break

    ##-- дождаться загрузки страницы сайта
    while True:
        doc_state = driver.execute_script("return document.readyState")
        if doc_state == 'complete':
            break

    ##-- извлечь заголовок лекции
    lect_headers  = driver.find_elements_by_css_selector('div.title span.zag')
    if len( lect_headers) < 1:    #-- защита на последнюю страницу
        break
    text_header = lect_headers[-1].text
    print( text_header)
    html_header = '<div class = "abzag"> '+ text_header + ' </div>'
    if prev_header != text_header:
        fhd.write( html_header + "\n")
        prev_header = text_header

    ##-- извлечь аннотацию лекции
    annotations = driver.find_elements_by_css_selector('div.annotation')
    if len( annotations ) > 0:
        annotation = annotations[0]
        print( annotation.text )
        html_annotation = annotation.get_attribute("outerHTML")
        fhd.write( html_annotation + "\n")
        
    ##-- извлечь содержимое лекции
    contents = driver.find_elements_by_css_selector('div.spelling-content-entity')
    content = contents[-1]
    html_content = content.get_attribute("outerHTML")

    ##-- поправить ссылки на рисунки
    html_content = html_content.replace('"/EDI', '"http://www.intuit.ru/EDI')

    ##-- записать результат в файл
    fhd.write( html_content + "\n")
        
#== закрыть файл и драйвер
fhd.write("</body></html>\n")
fhd.close()
driver.close()
        
