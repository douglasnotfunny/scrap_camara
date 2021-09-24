from selenium import webdriver
import chromedriver_binary  # Adds chromedriver binary to path
import time
import datetime
from datetime import date

options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--disable-gpu")


def get_timestamp():
    today = date.today()
    timestamp_now = time.mktime(datetime.datetime.strptime(today.strftime("%d/%m/%Y"), "%d/%m/%Y").timetuple())

    return timestamp_now

def get_date(type):
    driver = webdriver.Chrome(chrome_options=options)
    driver.get(f'''https://www.camara.leg.br/busca-portal?contextoBusca=BuscaProposicoes&pagina=1&order=data&abaEspecifica=true&filtros=%5B%7B"ano"%3A"2021"%7D%5D&tipos={type}''')

    all_dates = driver.find_elements_by_xpath("//p[@class='busca-resultados__info']")

    all_propositions = driver.find_elements_by_xpath("//h6//a")

    all_link = []
    for a in all_propositions:
        all_link = driver.find_element_by_link_text(a.text)
        print(all_link.get_attribute("href"))

    driver.close()
    return [all_dates,all_propositions,all_link]


def open(type):
    time_now = get_timestamp()
    datas_type = get_date(type)
    print(f"{time_now}\n\n")
    print(f"{datas_type}\n\n")
    
    '''for p in datas_type[1]:
        print(p.find_element_by_link_text("value"))'''

    

if __name__ == '__main__':
    # PUT TYPE PROPOSITION -> ['PL','PEC','PLP']
    open('PL')


