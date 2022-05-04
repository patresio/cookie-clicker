from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time


class CookieClicker:
    def __init__(self):
        self.SITE_LINK = "https://orteil.dashnet.org/cookieclicker/"
        self.SITE_MAP = {
            "buttons": {
                "biscoito": {
                    "xpath": "/html/body/div[2]/div[2]/div[15]/div[8]/div[1]"
                },
                "upgrade-build": {
                    "xpath": "/html/body/div[2]/div[2]/div[19]/div[3]/div[6]/div[$$NUMBER$$]"
                },
                "upgrade": {
                    "xpath": "/html/body/div[2]/div[2]/div[19]/div[3]/div[5]/div[$$NUMBERUP$$]"
                             # /html/body/div[2]/div[2]/div[19]/div[3]/div[5]/div[4]
                }
            }
        }
        self.servico = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=self.servico)
        self.driver.maximize_window()

    def abrir_site(self):
        time.sleep(2)
        self.driver.get(self.SITE_LINK)
        time.sleep(10)

    def clicar_no_cookie(self):
        self.driver.find_element(
            By.XPATH, self.SITE_MAP['buttons']['biscoito']['xpath']).click()

    def pega_melhor_building(self):
        encontrei = False
        elemento_atual = 2

        while not encontrei:
            objeto = self.SITE_MAP["buttons"]["upgrade-build"]["xpath"].replace(
                "$$NUMBER$$", str(elemento_atual))
            classes_objeto = self.driver.find_element(By.XPATH,
                                                      objeto).get_attribute("class")
            if not "enabled" in classes_objeto:
                encontrei = True
            else:
                elemento_atual += 1

        return elemento_atual - 1

    def comprar_building(self):
        objeto = self.SITE_MAP["buttons"]["upgrade-build"]["xpath"].replace(
            "$$NUMBER$$", str(self.pega_melhor_building()))
        self.driver.find_element(By.XPATH, objeto).click()

    def pega_melhor_upgrade(self):
        encontrei = False
        elemento_atual = 1

        while not encontrei:
            objeto = self.SITE_MAP["buttons"]["upgrade"]["xpath"].replace(
                "$$NUMBERUP$$", str(elemento_atual))
            classes_objeto = self.driver.find_element(By.XPATH,
                                                      objeto).get_attribute("class")
            if not "enabled" in classes_objeto:
                encontrei = True
            else:
                elemento_atual += 1

        return elemento_atual - 1

    def comprar_upgrade(self):
        try:
            objeto = self.SITE_MAP["buttons"]["upgrade"]["xpath"].replace(
                "$$NUMBERUP$$", str(self.pega_melhor_building()))
            self.driver.find_element(By.XPATH, objeto).click()
        except NoSuchElementException:
            pass


biscoito = CookieClicker()
biscoito.abrir_site()

i = 0

while True:
    if i % 500 == 0 and i != 0:
        time.sleep(1)
        biscoito.comprar_building()
        time.sleep(1)
        #biscoito.comprar_upgrade()
        #time.sleep(1)
    biscoito.clicar_no_cookie()
    i += 1
