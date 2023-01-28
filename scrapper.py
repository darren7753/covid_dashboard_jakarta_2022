from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
import gdown

browser = webdriver.Chrome()
browser.get("https://riwayat-file-covid-19-dki-jakarta-jakartagis.hub.arcgis.com/")

wait = WebDriverWait(browser,10)
wait.until(EC.presence_of_element_located((By.XPATH,"//a[contains(@href,'drive.google.com')]")))

links = browser.find_elements(By.XPATH,"//a[contains(@href,'drive.google.com')]")
gdrives_links = [link.get_attribute("href") for link in links]

browser.quit()

for link in gdrives_links:
    file_id = re.search("d\/(.+)\/edit",link).group(1)
    download_link = f"https://drive.google.com/uc?id={file_id}"
    gdown.download(download_link,quiet=False)