from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException
from sqlalchemy.orm import Session
from models import CarAdverts
from database import get_db
import time
import requests
import os
from urllib.parse import urlparse

class SCRAPER:
    def __init__(self, url):
        self.url = url
        self.manager = ChromeService(ChromeDriverManager().install()) #Chrome manageris
        self.driver = webdriver.Chrome(service=self.manager) #chrome driveris
        self.driver.get(self.url)
        self.db = get_db()

    def measure_time(func):
        def wrapper(*args, **kwargs):
            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time()
            execution_time = end_time - start_time
            print(f"Run time:{execution_time:.1f} seconds")
            return result
        return wrapper

    def click_cookie(self):
        self.driver.implicitly_wait(2)
        try:
            self.driver.find_element('xpath', "//div/button[@id ='onetrust-reject-all-handler']").click()
        except:
            pass

    def list_of_urls(self):
        self.listas = []
        self.idlistas = []
        a = 0
        if a == 0:
            self.click_cookie()
            a+=1
        else:
            pass
        advert_ids_in_database = {str(advert_id[0]) for advert_id in self.db.query(CarAdverts.Skelbimo_id).all()}
        pages = self.driver.find_elements('xpath', "//div[@class='list-items']/a")
        for page in pages:
            advert_id = page.get_attribute('data-id')
            if advert_id not in advert_ids_in_database:
                self.listas.append(page.get_attribute('href') + '#gallery')
        return self.listas

    def pull_car_info_desktop(self):
        setas = {'Kaina':self.driver.find_element('xpath', "//div[@class='price']").text,
                 'Telefono numeris':self.driver.find_element('xpath', "//div[@class='button seller-phone-number js-phone-number']").text,
                 'URL':self.driver.current_url}
        print(setas)

    def pull_car_info_mobile(self):
        marke, modelis = self.driver.find_element('xpath', "//h1").text.split(' ', 1)
        setas = {'Marke':marke,
                 'Modelis':modelis,
                 'Telefono_nr':self.try_finding_element_withoutsplitting("//a[@class = 'contact-button contact-phone js-contact-phone']"),
                 'Kontakto_vardas':self.try_finding_element_withoutsplitting("//div[@class='contact-name']"),
                 'Miestas':self.try_finding_element_withoutsplitting("//div[@class='contact-location']"),
                 'Kaina':''.join(filter(str.isdigit, self.try_finding_element_withoutsplitting("//div[@class='main-price']"))),
                 'Metai':self.try_finding_element("//span[@class='view-field view-i field_make_date']"),
                 'Pirma_registracija': self.try_finding_element("//span[@class='view-field view-i field_origin_country_id']"),
                 'Variklis':self.try_finding_element("//span[@class='view-field view-i field_engine']"),
                 'Kebulas':self.try_finding_element("//span[@class='view-field view-i field_body_type_id']"),
                 'Ratai':self.try_finding_element("//span[@class='view-field view-i field_wheel_drive_id']"),
                 'Klimatas':self.try_finding_element("//span[@class='view-field view-i field_condition_type_id']"),
                 'Defektai':self.try_finding_element("//span[@class='view-field view-i field_has_damaged_id']"),
                 'Rida':''.join(filter(str.isdigit, self.try_finding_element("//span[@class='view-field view-i field_kilometrage']"))),
                 'Kuras':self.try_finding_element("//span[@class='view-field view-i field_fuel_id']"),
                 'Deze':self.try_finding_element("//span[@class='view-field view-i field_gearbox_id']"),
                 'Spalva':self.try_finding_element("//span[@class='view-field view-i field_color_id']"),
                 'Skelbimo_id':self.try_finding_element("//span[@class='view-field view-i field_id']")[1:],
                 'URL': self.driver.current_url
                 }
        with self.db.begin():
            self.db.add(CarAdverts(**setas))
        self.download_photos()
        return setas

    def try_finding_element_withoutsplitting(self, xpathas, defaultas = "none"):
        try:
            return self.driver.find_element('xpath', xpathas).text
        except:
            return defaultas
        
    def try_finding_element(self, xpathas, defaultas = "none"):
        try:
            return self.driver.find_element('xpath', xpathas).text.split(': ', 1)[1]
        except:
            return defaultas

    def find_photos(self):
        piclist = []
        image_urls = [element.get_attribute("src") or element.get_attribute("data-src")
                      for element in
                      self.driver.find_elements('xpath', "//div[@class='photo-list']/div/span/picture/img[contains(@src,"
                                                         " 'https://autoplius-img.dgn.lt/') or contains(@data-src, 'https://autoplius-img.dgn.lt')]")]
        for linkas in image_urls:
            piclist.append(linkas)
        return piclist


    def next_page_desktop_version(self):
        try:
            linkas = self.driver.find_element('xpath', "//li/a[@class='next']").get_attribute('href')
        except NoSuchElementException:
            linkas = None
        return linkas

    def next_page_mobile(self):
        try:
            linkas = self.driver.find_element('xpath',"//a[@class='fr btn button right-nav']").get_attribute('href')
        except NoSuchElementException:
            linkas = None
        return linkas

    @measure_time
    def do_something(self):
        max_iterations = 200
        iteration = 0
        while True:
            self.list_of_urls()
            for link in self.listas:
                self.driver.execute_script("window.open('about:blank', 'newtab')")
                self.driver.switch_to.window(self.driver.window_handles[-1])
                self.driver.get(link)
                self.pull_car_info_mobile()
                self.driver.switch_to.window(self.driver.window_handles[0])
            next_page_url = self.next_page_mobile()
            if not next_page_url:
                break
            self.driver.get(next_page_url)
            iteration += 1
            if iteration >= max_iterations:
                break
        print('Done!')

    def download_photos(self):
        url_parts = urlparse(self.driver.current_url)
        advert_id = os.path.basename(url_parts.path).split('-')[-1].split('.')[0]
        folder_name = 'Skelbimu_Images/' +  advert_id
        os.makedirs(folder_name, exist_ok=True)
        photo_counter = 1
        for link in self.find_photos():
            try:
                r = requests.get(link)
                filename = os.path.join(folder_name, f"{photo_counter}.jpg")  # Use the counter in the filename
                with open(filename, 'wb') as f:
                    f.write(r.content)
                photo_counter += 1  # Increment the counter
            except requests.exceptions.RequestException as e:
                continue


linkas = input('Iveskite URL: ')
scraperis = SCRAPER(linkas)
scraperis.do_something()