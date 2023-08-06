from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import random

class selenium_leo:

    def __init__(self) -> None:
        pass
    
    def send_keys_as_human(locator_variable, text):
        """Se le pasa una cadena de texto y la va escribiendo letra por letra en tiempo random
           entre 0.15 y 0.40 segundos.

        Args:
            locator_variable (variable): La variable del selector obtenido anteriormente
            text (string): El texto que queremos escribir como "Humano"
        """
        lista_letras = list(text)
        for letra in lista_letras:
            locator_variable.send_keys(letra)
            random_sleep = random.uniform(0.15, 0.40)
            sleep(random_sleep)
    
    def doble_selector_xpath(selectorPath1, SelectorPath2, wait_time_in_sec, driver):
        """Se le pasa 2 dirección de selectores y el tiempo de espera, si el primero falla usa el segundo.

        Args:
            selectorPath1 (string): Selector 1 xpath
            SelectorPath2 (string): Selector 2 xpath
            wait_time_in_sec (int): Tiempo de espera en segundos

        Returns:
            _type_: retorna el selector indicado
        """
        wait = WebDriverWait(driver, wait_time_in_sec)
        try:
            selector = wait.until(EC.element_to_be_clickable((By.XPATH, selectorPath1)))
            return selector
        except:
            print("Second selector")
            selector = wait.until(EC.element_to_be_clickable((By.XPATH, SelectorPath2)))
            return selector
    
    def doble_selector_name_xpath(selectorPath1, SelectorPath2, wait_time_in_sec, driver):
        """Se le pasa 2 dirección de selectores y el tiempo de espera, si el primero falla usa el segundo.

        Args:
            selectorPath1 (string): Selector 1 name
            SelectorPath2 (string): Selector 2 xpath
            wait_time_in_sec (int): Tiempo de espera en segundos

        Returns:
            _type_: retorna el selector indicado
        """
        wait = WebDriverWait(driver, wait_time_in_sec)
        try:
            selector = wait.until(EC.element_to_be_clickable((By.NAME, selectorPath1)))
            return selector
        except:
            print("Second selector")
            selector = wait.until(EC.element_to_be_clickable((By.XPATH, SelectorPath2)))
            return selector
    
    def doble_selector_class_xpath(selectorPath1, SelectorPath2, wait_time_in_sec, driver):
        """Se le pasa 2 dirección de selectores y el tiempo de espera, si el primero falla usa el segundo.

        Args:
            selectorPath1 (string): Selector 1 class_name
            SelectorPath2 (string): Selector 2 xpath
            wait_time_in_sec (int): Tiempo de espera en segundos

        Returns:
            _type_: retorna el selector indicado
        """
        wait = WebDriverWait(driver, wait_time_in_sec)
        try:
            selector = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, selectorPath1)))
            return selector
        except:
            print("Second selector")
            selector = wait.until(EC.element_to_be_clickable((By.XPATH, SelectorPath2)))
            return selector
    
    def doble_selector_css_xpath(selectorPath1, SelectorPath2, wait_time_in_sec, driver):
        """Se le pasa 2 dirección de selectores y el tiempo de espera, si el primero falla usa el segundo.

        Args:
            selectorPath1 (string): Selector 1 css
            SelectorPath2 (string): Selector 2 xpath
            wait_time_in_sec (int): Tiempo de espera en segundos

        Returns:
            _type_: retorna el selector indicado
        """
        wait = WebDriverWait(driver, wait_time_in_sec)
        try:
            selector = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, selectorPath1)))
            return selector
        except:
            print("Second selector")
            selector = wait.until(EC.element_to_be_clickable((By.XPATH, SelectorPath2)))
            return selector
        
    def doble_selector_css_name(selectorPath1, SelectorPath2, wait_time_in_sec, driver):
        """Se le pasa 2 dirección de selectores y el tiempo de espera, si el primero falla usa el segundo.

        Args:
            selectorPath1 (string): Selector 1 css
            SelectorPath2 (string): Selector 2 name
            wait_time_in_sec (int): Tiempo de espera en segundos

        Returns:
            _type_: retorna el selector indicado
        """
        wait = WebDriverWait(driver, wait_time_in_sec)
        try:
            selector = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, selectorPath1)))
            return selector
        except:
            print("Second selector")
            selector = wait.until(EC.element_to_be_clickable((By.NAME, SelectorPath2)))
            return selector