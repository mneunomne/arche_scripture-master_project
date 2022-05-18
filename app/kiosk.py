
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

def run_kiosk(path):
  options = Options()
  options.add_argument("--kiosk")
  options.add_argument("--autoplay-policy=no-user-gesture-required")
  options.add_experimental_option("detach", True)
  options.add_experimental_option("useAutomationExtension", False)
  options.add_experimental_option("excludeSwitches",["enable-automation"])
  driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
  driver.get(path)