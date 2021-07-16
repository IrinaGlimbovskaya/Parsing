import PySimpleGUI as sg
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from tqdm import tqdm
sg.theme('TealMono')
layout =[ [sg.Image(r'C:\Users\Irina\Desktop\practice\Intuit.png')],
    [ sg.Text('Программа для закачки курса INTUIT')],
    [ sg.Button('Ввод ссылки и имени файла')],
    [ sg.Text('введите ссылку на курс: ', size=(22,1)), sg.Input(k = '-IN-'), sg.Button('Парсинг')],
    [ sg.Text('введите имя файла: ', size=(22,1)), sg.Input(k ='-OUT-') ],
    [ sg.ProgressBar(10, orientation='h', size=(46, 20), key='progressBar')],
    [ sg.Text('Лекция: ', size=(22,1)), sg.Input(k = 'lecture')],
    [ sg.Text('Номер страницы: ', size=(22,1)), sg.Input(k = 'page', size=(10,1))],      
    [ sg.ProgressBar(10, orientation='h', size=(46, 20), key='progress')]]

window = sg.Window('Парсинг лекций с сайта Интуит', layout)
progress_bar = window.FindElement('progress')
fh = open ("url.txt")
ls = fh.readlines()
for line in ls:
    line = line.strip()
line_num = 0

while True:
    event,values = window.read()
    print(event)
    if event == 'Ввод ссылки и имени файла':
        line = ls[line_num]
        url, file_name = line.split()
        line_num += 1
        if line_num > len(ls):
            url, file_name = '', ''
        window["-IN-"].update(url)
        window["-OUT-"].update(file_name)
        window['page'].update()
        window['lecture'].update()
        
    if event == 'Парсинг':         
        file_name = values['-OUT-']
        fhd = open( file_name, "w")
        fhd.write("<html><head>\n")
        fhd.write('<meta http-equiv="Content-Type" content="text/html; charset=cp1251">\n')
        fhd.write('<link type="text/css" rel="stylesheet" href="ab.css">')
        fhd.write("</head><body>\n")

        driver = webdriver.Firefox('C://Users//Irina//AppData//Local//Programs//Python//Python36')
        url = values['-IN-']
        driver.get( url )

        link = driver.find_element_by_id('non-collapsible-item-1')
        all_links = link.find_elements_by_css_selector('a')
        print(len(all_links))
        test_links = link.find_elements_by_partial_link_text("Тест")
        print(len(test_links))
        exam_links = link.find_elements_by_partial_link_text('Экзамен')
        print(len(exam_links))
        lect_count = len(all_links)-len(test_links)- len(exam_links)
        print(lect_count)
        
        link = driver.find_element_by_link_text('Лекция 1')
        link.send_keys(Keys.RETURN)
        print("лекция 1")

        time.sleep(3)
        
        page_num = 0
        lect_num = 0
        lect_name = ""
        while True:
            doc_state = driver.execute_script("return document.readyState")
            if doc_state == 'complete':
                break

        text_header = ""
        lect_headers  = driver.find_elements_by_css_selector('div.title span.zag')

        time.sleep(.5)
        
        for lect_header in lect_headers:
            text_header = lect_header.text
            html_header = '<div class = "abzag"> '+ text_header + ' </div>'
            #print( text_header)
            window['lecture'].update(text_header)
            #print("Имя лекции:", lect_name )
            print("Имя лекции:", lect_name )
            print("Текст заголовка:", text_header)
            if lect_name != text_header:
                page_num = 1
                lect_name = text_header
                print("Имя лекции if:", lect_name )
                print("Текст заголовка if:", text_header)
            else:
                page_num += 1
            window['page'].update(page_num)
            fhd.write( html_header)

        prev_header = text_header   

        contents = driver.find_elements_by_css_selector('div.spelling-content-entity')
        content = contents[-1]
        html_content = content.get_attribute("outerHTML")

        html_content = html_content.replace('"/EDI', '"http://www.intuit.ru/EDI')

        fhd.write( html_content + "\n")

        time.sleep(.5)

        while True:
            try:
                driver.find_element_by_link_text('Дальше >>').send_keys(Keys.RETURN)
                time.sleep(30)
            except:
                break

            while True:
                doc_state = driver.execute_script("return document.readyState")
                if doc_state == 'complete':
                    break

            time.sleep(.5)

            lect_headers  = driver.find_elements_by_css_selector('div.title span.zag')
            if len( lect_headers) < 1:    
                break

            text_header = lect_headers[-1].text
            print( text_header)
            window['lecture'].update(text_header)

            if lect_name != text_header:
                page_num = 1
                lect_name = text_header
                lect_num += 1
                print (lect_num)
                new_val = lect_num*10//lect_count
                window['progressBar'].update(new_val)
            else:
                page_num += 1
                window['progress'].update(page_num)
            window['page'].update(page_num)
            html_header = '<div class = "abzag"> '+ text_header + ' </div>'
            if prev_header != text_header:
                fhd.write( html_header + "\n")
                prev_header = text_header

            time.sleep(.5)

            annotations = driver.find_elements_by_css_selector('div.annotation')
            if len( annotations ) > 0:
                annotation = annotations[0]
                print( annotation.text )
                html_annotation = annotation.get_attribute("outerHTML")
                fhd.write( html_annotation + "\n")
            
            contents = driver.find_elements_by_css_selector('div.spelling-content-entity')
            content = contents[-1]
            html_content = content.get_attribute("outerHTML")
        
            html_content = html_content.replace('"/EDI', '"http://www.intuit.ru/EDI')

            fhd.write( html_content + "\n")

        fhd.write("</body></html>\n")
        fhd.close()
        driver.close()
        
time.sleep(3)
