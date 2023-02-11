import os
import time
from time import sleep

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import LiveServerTestCase, TestCase
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait


class FunctionalTest(TestCase, LiveServerTestCase):
   def test_user_show_login_page(self):
      browser = webdriver.Chrome()
      browser.get("http://127.0.0.1:8000/auth/login?next=/")
      wait = WebDriverWait(browser, 5)
      sleep(2)
      browser.quit()

   def test_user_login_page(self):
      browser = webdriver.Chrome()
      browser.get("http://127.0.0.1:8000/auth/login?next=/")
      wait = WebDriverWait(browser, 5)

      username = browser.find_element(By.NAME,"username")
      username.clear()
      username.send_keys("Emanuelle")
      password = browser.find_element(By.NAME, "password")
      password.send_keys("fms12345")
      password.send_keys(Keys.RETURN)
      sleep(5)
        
      browser.quit()

   def test_user_register_page(self):
      browser = webdriver.Chrome()
      browser.get("http://127.0.0.1:8000/auth/cadastro")
      wait = WebDriverWait(browser, 15)

      username = browser.find_element(By.NAME, "username")
      username.send_keys("TantoFaz2023")
      sleep(1)
      email = browser.find_element(By.NAME, "email")
      email.send_keys("TantoFaz2023@gmail.com")
      sleep(1)
      password = browser.find_element(By.NAME,"password")
      password.send_keys("fms45645")
      sleep(1)
      BtnRequest = wait.until(EC.presence_of_element_located((By.ID, 'btn-submit')))
      BtnRequest.click()
      sleep(5)
        
      browser.quit()

   def test_nao_registrar_usuario_ja_cadastrado(self):
      browser = webdriver.Chrome()
      browser.get("http://127.0.0.1:8000/auth/cadastro")
      wait = WebDriverWait(browser, 15)

      username = browser.find_element(By.NAME, "username")
      username.send_keys("Emanuelle")
      sleep(1)
      email = browser.find_element(By.NAME, "email")
      email.send_keys("emanuele@gmail.com")
      sleep(1)
      password = browser.find_element(By.NAME,"password")
      password.send_keys("fms45645")
      sleep(1)
      BtnRequest = wait.until(EC.presence_of_element_located((By.ID, 'btn-submit')))
      BtnRequest.click()
      sleep(5)
        
      browser.quit()


   def test_list_minhas_despesas(self):
      browser = webdriver.Chrome()
      browser.get("http://127.0.0.1:8000/auth/login?next=/")
      wait = WebDriverWait(browser, 5)

      username = browser.find_element(By.NAME,"username")
      username.clear()
      username.send_keys("Emanuelle")
      password = browser.find_element(By.NAME, "password")
      password.send_keys("fms12345")
      password.send_keys(Keys.RETURN)
      despesas = wait.until(EC.presence_of_element_located((By.ID, 'minhas_despesas')))
      despesas.click()
      sleep(5)
        
      browser.quit()

   def test_list_estatistica_despesas(self):
      browser = webdriver.Chrome()
      browser.get("http://127.0.0.1:8000/auth/login?next=/")
      wait = WebDriverWait(browser, 5)

      username = browser.find_element(By.NAME,"username")
      username.clear()
      username.send_keys("Emanuelle")
      password = browser.find_element(By.NAME, "password")
      password.send_keys("fms12345")
      password.send_keys(Keys.RETURN)
      despesas = wait.until(EC.presence_of_element_located((By.ID, 'estatistica_renda')))
      despesas.click()
      sleep(5)
        
      browser.quit()

   def test_listagem_renda(self):
      browser = webdriver.Chrome()
      browser.get("http://127.0.0.1:8000/auth/login?next=/")
      wait = WebDriverWait(browser, 5)

      username = browser.find_element(By.NAME,"username")
      username.clear()
      username.send_keys("Emanuelle")
      password = browser.find_element(By.NAME, "password")
      password.send_keys("fms12345")
      password.send_keys(Keys.RETURN)
      renda = wait.until(EC.presence_of_element_located((By.ID, 'listagem_renda')))
      renda.click()
      sleep(2)
        
      browser.quit()


   def test_create_renda(self):
      browser = webdriver.Chrome()
      browser.get("http://127.0.0.1:8000/auth/login?next=/")
      wait = WebDriverWait(browser, 5)

      username = browser.find_element(By.NAME,"username")
      username.clear()
      username.send_keys("Emanuelle")
      password = browser.find_element(By.NAME, "password")
      password.send_keys("fms12345")
      password.send_keys(Keys.RETURN)
      renda = wait.until(EC.presence_of_element_located((By.ID, 'listagem_renda')))
      renda.click()
      sleep(2)
      despesas = wait.until(EC.presence_of_element_located((By.ID, 'add_renda')))
      despesas.click()
      descricao = browser.find_element(By.NAME, "descricao")
      descricao.send_keys("Teste")
      sleep(1)
      valor = browser.find_element(By.NAME, "valor")
      valor.send_keys(50)
      sleep(1)
      data = browser.find_element(By.NAME, "data")
      data.send_keys("11/02/2023")
      sleep(4)
      BtnRequest = wait.until(EC.presence_of_element_located((By.ID, 'submit')))
      BtnRequest.click()
      sleep(5)
        
      browser.quit()


   def test_create_categoria(self):
      browser = webdriver.Chrome()
      browser.get("http://127.0.0.1:8000/auth/login?next=/")
      wait = WebDriverWait(browser, 5)

      username = browser.find_element(By.NAME,"username")
      username.clear()
      username.send_keys("Emanuelle")
      password = browser.find_element(By.NAME, "password")
      password.send_keys("fms12345")
      password.send_keys(Keys.RETURN)
      categoria = wait.until(EC.presence_of_element_located((By.ID, 'listagem_categorias')))
      categoria.click()
      sleep(2)
      categoria = wait.until(EC.presence_of_element_located((By.ID, 'add_categoria')))
      categoria.click()
      nome = browser.find_element(By.NAME, "nome")
      nome.send_keys("Curso")
      sleep(2)
      BtnRequest = wait.until(EC.presence_of_element_located((By.ID, 'submit')))
      BtnRequest.click()
      sleep(5)
        
      browser.quit()


   def test_create_despesa(self):
      browser = webdriver.Chrome()
      browser.get("http://127.0.0.1:8000/auth/login?next=/")
      wait = WebDriverWait(browser, 5)

      username = browser.find_element(By.NAME,"username")
      username.clear()
      username.send_keys("Emanuelle")
      password = browser.find_element(By.NAME, "password")
      password.send_keys("fms12345")
      password.send_keys(Keys.RETURN)
      categoria = wait.until(EC.presence_of_element_located((By.ID, 'minhas_despesas')))
      categoria.click()
      sleep(2)
      categoria = wait.until(EC.presence_of_element_located((By.ID, 'add_despesa')))
      categoria.click()
      descricao = browser.find_element(By.NAME, "descricao")
      descricao.send_keys("Django")
      sleep(2)
      categoria = browser.find_element(By.NAME, "categoria")
      select = Select(categoria)
      select.select_by_visible_text("Curso")
      sleep(2)
      valor = browser.find_element(By.NAME, "valor")
      valor.send_keys(50)
      sleep(1)
      data = browser.find_element(By.NAME, "data")
      data.send_keys("11/02/2023")
      sleep(4)

      BtnRequest = wait.until(EC.presence_of_element_located((By.ID, 'submit')))
      BtnRequest.click()
      sleep(5)
        
      browser.quit()