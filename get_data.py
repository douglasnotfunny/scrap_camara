from selenium import webdriver
import chromedriver_binary  # Adds chromedriver binary to path
import time
import datetime
import requests 
import hashlib



options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--disable-gpu")

def get_timestamp(date):
    timestamp_now = time.mktime(datetime.datetime.strptime(date, "%d/%m/%Y").timetuple())

    return timestamp_now



def get_info_all_propositions(type):
    driver = webdriver.Chrome(chrome_options=options)
    num_page = 1
    all_timestamp = []
    all_link = []
    all_propositions = []

    today = datetime.date.today()
    time_now = get_timestamp(today.strftime("%d/%m/%Y"))
    tree_day_ago = time_now-(24*60*60)

    condition = 0

    while num_page==num_page:
        url = f'''https://www.camara.leg.br/busca-portal?contextoBusca=BuscaProposicoes&pagina={num_page}&order=data&abaEspecifica=true&filtros=%5B%7B"ano"%3A"2021"%7D%5D&tipos={type}'''
        print(f"Variables: {num_page}\n\n\n\n\n\n\n\n\n")
        driver.get(url)

        all_dates = driver.find_elements_by_xpath("//p[@class='busca-resultados__info']")

        for date in all_dates:
            d = (date.text.split('\n')[1].split(" ")[0])
            timestamp = get_timestamp(d)
            if timestamp>=tree_day_ago:
                print(f"oi {d,timestamp,tree_day_ago, condition}")
                all_timestamp.append(timestamp)
            else:
                condition = 1
                print(f"hey {d,timestamp,tree_day_ago, condition}")
                break

        all_propositions = driver.find_elements_by_xpath("//h6//a")

        for a in all_propositions:
            link = driver.find_element_by_link_text(a.text)
            all_link.append(link.get_attribute("href"))

        time.sleep(5)
        if condition == 1: break
        num_page+=1
    return [all_timestamp,all_propositions,all_link]

def get_pdf_proposition(link_proposition):
    driver = webdriver.Chrome(chrome_options=options)
    h1 = []

    for proposition in link_proposition:
        print(proposition)
        driver.get(f'''{proposition}''')

        # intero_teor_text = driver.find_elements_by_xpath("//span[@class='naoVisivelNaImpressao']")

        it_link = driver.find_element_by_link_text("Inteiro teor")
        link = it_link.get_attribute("href")
        print(link)
        download_pdf(link)
        h1.append(pdf_to_hash())
    print(h1)
    return h1


def download_pdf(url):
    filename = url.split('filename=')[1] 
    r = requests.get(url, stream=True)
    with open('metadata.pdf', 'wb') as fd: 
        for chunk in r.iter_content(2000): 
            fd.write(chunk)
    return url.split('filename=')[1]

def pdf_to_hash():
    file = "metadata.pdf"
    BLOCK_SIZE = 65536

    file_hash = hashlib.md5()
    with open(file, 'rb') as f:
        fb = f.read(BLOCK_SIZE)
        while len(fb) > 0:
            file_hash.update(fb) 
            fb = f.read(BLOCK_SIZE)
    print(file_hash.hexdigest())
    return file_hash.hexdigest()


def run(type):
    datas_type = get_info_all_propositions(type)
    list_hash = get_pdf_proposition(datas_type[2])

    return list_hash
    
    
if __name__ == '__main__':
    # PUT TYPE PROPOSITION -> ['PL','PEC','PLP']
    list_hash = run('PL')
    print(list_hash)


