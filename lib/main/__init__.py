# from ..data import db
from pathlib import Path
import json

from time import sleep
import random

from selenium import webdriver
from selenium.webdriver.common.by import By

class LoginPage:
  def __init__(self, browser):
      self.browser = browser

  def login(self, username, password):
      username_input = self.browser.find_element(By.CSS_SELECTOR, "input[name='username']")
      password_input = self.browser.find_element(By.CSS_SELECTOR, "input[name='password']")
      username_input.send_keys(username)
      password_input.send_keys(password)
      login_button = self.browser.find_element(By.XPATH, "//button[@type='submit']")
      login_button.click()
      sleep(random.randint(3, 6))

class HomePage: # NOTE: MAKE SURE TO ADD TRY AND EXCEPTION CASES (error handling) 
  def __init__(self, browser):
      self.browser = browser
      self.browser.get('https://www.instagram.com/')

  def go_to_login_page(self):
      return LoginPage(self.browser)

  def skip_reminders(self):
      self.browser.find_element(By.XPATH, "//button[text()='Not Now']").click()
      self.browser.find_element(By.XPATH, "//button[text()='Not Now']").click()
      sleep(random.randint(2, 4))

  def go_to_profile_page(self, username):
      self.browser.find_element(By.XPATH, f"//a[@href='/{username}/']").click()
      sleep(random.randint(2, 4))

def read_config():
  print("Reading Config...")
  dir = Path(__file__).parents[2]
  filename = dir / 'config.json'
  f = open(filename)
  
  config = json.load(f)

  return config
  f.close()


def run(version):
  print(f"Running v{version}")
  config = read_config()
  print(config["account_info"])
  credentials = config["account_info"]
  # db.setup()

  username = credentials["Username"]
  password = credentials["Password"]

  options = webdriver.FirefoxOptions()
  options.headless = False

  browser = webdriver.Firefox(options=options)
  browser.implicitly_wait(5)

  browser.get('https://www.instagram.com/')

  home_page = HomePage(browser)
  login_page = home_page.go_to_login_page()
  login_page.login(username, password)
  home_page.skip_reminders()
  home_page.go_to_profile_page(username)

  # browser.close()

    