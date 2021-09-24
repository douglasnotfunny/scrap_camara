from selenium import webdriver
import chromedriver_binary  # Adds chromedriver binary to path
import time
import datetime
from datetime import date
import requests 


options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--disable-gpu")


def get_timestamp():
    today = date.today()
    timestamp_now = time.mktime(datetime.datetime.strptime(today.strftime("%d/%m/%Y"), "%d/%m/%Y").timetuple())

    return timestamp_now



def get_info_all_propositions(type):
    driver = webdriver.Chrome(chrome_options=options)
    driver.get(f'''https://www.camara.leg.br/busca-portal?contextoBusca=BuscaProposicoes&pagina=1&order=data&abaEspecifica=true&filtros=%5B%7B"ano"%3A"2021"%7D%5D&tipos={type}''')

    all_dates = driver.find_elements_by_xpath("//p[@class='busca-resultados__info']")

    all_propositions = driver.find_elements_by_xpath("//h6//a")

    all_link = []
    for a in all_propositions:
        link = driver.find_element_by_link_text(a.text)
        all_link.append(link.get_attribute("href"))

    driver.close()
    return [all_dates,all_propositions,all_link]

def get_pdf_proposition(link_proposition):
    driver = webdriver.Chrome(chrome_options=options)
    
    for proposition in link_proposition:
        print(proposition)
        driver.get(f'''{proposition}''')

        # intero_teor_text = driver.find_elements_by_xpath("//span[@class='naoVisivelNaImpressao']")

        it_link = driver.find_element_by_link_text("Inteiro teor")
        link = it_link.get_attribute("href")
        print(link)
        download_pdf(link)
        time.sleep(5)


def download_pdf(url): 
    r = requests.get(url, stream=True)
    with open('metadata.pdf', 'wb') as fd: 
        for chunk in r.iter_content(2000): 
            fd.write(chunk)



def run(type):
    time_now = get_timestamp()
    datas_type = get_info_all_propositions(type)
    print(f"{time_now}\n\n")
    print(f"{datas_type}\n\n")

    get_pdf_proposition(datas_type[2])
    
    

if __name__ == '__main__':
    # PUT TYPE PROPOSITION -> ['PL','PEC','PLP']
    run('PL')


