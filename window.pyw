import PySimpleGUI as sg
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from tqdm import tqdm
sg.theme('TealMono')
layout =[ [sg.Image(r'C:\Users\Irina\Desktop\practice\Intuit.png', justification='center')],
    [sg.Text('Программа для закачки курса INTUIT', justification='center')],
    [ sg.Text('введите ссылку на 1 лекцию: ', size=(20,1)), sg.Input(k = '-IN-'), sg.Button('Парсинг')],
    [ sg.Text('введите имя файла: ', size=(20,1)), sg.Input(k ='-OUT-') ],
    [ sg.Text('Лекция: ', size=(20,1)), sg.Input(k = 'lecture')],
    [ sg.ProgressBar(1, orientation='h', size=(45, 20), key='progress')]]
window = sg.Window('Парсинг лекций с сайта Интуит', layout)
progress_bar = window.FindElement('progress')
while True:
    event,values = window.read()
    print(event)
    if event == 'Парсинг':
        file_name= values['-OUT-']
        fhd = open( file_name, "w")
        fhd.write("<html><head>\n")
        fhd.write('<meta http-equiv="Content-Type" content="text/html; charset=cp1251">\n')
        fhd.write('<link type="text/css" rel="stylesheet" href="ab.css">')
        fhd.write("</head><body>\n")

        driver = webdriver.Firefox('C://Users//Irina//AppData//Local//Programs//Python//Python36')
        url = values['-IN-']
        driver.get( url )
        
        progress_bar.UpdateBar(0, 5)
        time.sleep(.5)
        
        while True:
            doc_state = driver.execute_script("return document.readyState")
            if doc_state == 'complete':
                break

        text_header = ""
        lect_headers  = driver.find_elements_by_css_selector('div.title span.zag')
        
        progress_bar.UpdateBar(1, 5)
        time.sleep(.5)
        
        for lect_header in lect_headers:
            text_header = lect_header.text
            html_header = '<div class = "abzag"> '+ text_header + ' </div>'
            print( text_header)
            window['lecture'].update(text_header)
            fhd.write( html_header)

        prev_header = text_header   

        contents = driver.find_elements_by_css_selector('div.spelling-content-entity')
        content = contents[-1]
        html_content = content.get_attribute("outerHTML")

        html_content = html_content.replace('"/EDI', '"http://www.intuit.ru/EDI')

        fhd.write( html_content + "\n")
        
        progress_bar.UpdateBar(2, 5)
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

            progress_bar.UpdateBar(3, 5)
            time.sleep(.5)

            lect_headers  = driver.find_elements_by_css_selector('div.title span.zag')
            if len( lect_headers) < 1:    
                break

            text_header = lect_headers[-1].text
            print( text_header)
            window['lecture'].update(text_header)
            html_header = '<div class = "abzag"> '+ text_header + ' </div>'
            if prev_header != text_header:
                fhd.write( html_header + "\n")
                prev_header = text_header

            progress_bar.UpdateBar(4, 5)
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

        progress_bar.UpdateBar(5, 5)
        time.sleep(.5)
    
        fhd.write("</body></html>\n")
        fhd.close()
        driver.close()
        
time.sleep(3)

window.close()

