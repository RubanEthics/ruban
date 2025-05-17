import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def load_config(file_path):
    config = {}
    with open(file_path, 'r') as file:
        for line in file:
            if "=" in line:
                key, value = line.strip().split("=", 1)
                config[key.strip()] = value.strip()
    return config

class WebTest:
    def __init__(self):
        options = Options()
        options.headless = False
        self.driver = webdriver.Chrome(options=options)
        self.driver.maximize_window()
        self.config = load_config(r"C:\Users\Picnexs\Desktop\ruban\config\config.txt")  # Update as needed
        self.wait = WebDriverWait(self.driver, 20)

    def login(self):
        self.driver.get(self.config["URL"])
        try:
            email_field = self.wait.until(EC.presence_of_element_located((By.XPATH, "(//input[@name='email'])[2]")))
        except:
            email_field = self.wait.until(EC.presence_of_element_located((By.XPATH, "(//input[@name='email'])[1]")))

        email_field.send_keys(self.config["USERNAME"])
        time.sleep(1)

        password_field = self.wait.until(EC.presence_of_element_located((By.XPATH, "(//input[@name='password'])")))
        password_field.send_keys(self.config["PASSWORD"])
        time.sleep(1)

        login_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, "(//button[@id='signin-submit'])")))
        login_button.click()
        print("✅ Login successful")
        time.sleep(10)

    def delete_video_or_audio(self):
        library_management_xpath = "//div[@id='libraryManagement']"
        add_library_xpath ="//span[text()='All Library']"
        edit_library_element_xpath = "//span[@class='editdropdown-button']"
        delete_element_xpath = "(//span[text()='Delete'])[1]"
        confirm_delete_xpath = "(//span[text()='Delete'])[1]"  # Assuming confirmation uses the same text/span

        # Click Library Management
        self.wait.until(EC.element_to_be_clickable((By.XPATH, library_management_xpath))).click()
        time.sleep(2)

        # Click Add Video Or Audio
        self.wait.until(EC.element_to_be_clickable((By.XPATH, add_library_xpath))).click()
        time.sleep(3)

        # Click Edit dropdown/button for the first library item
        self.wait.until(EC.element_to_be_clickable((By.XPATH, edit_library_element_xpath))).click()
        time.sleep(2)

        # Click Delete from dropdown
        self.wait.until(EC.element_to_be_clickable((By.XPATH, delete_element_xpath))).click()
        time.sleep(2)

        # Confirm Delete (usually a popup/modal)
        self.wait.until(EC.element_to_be_clickable((By.XPATH, confirm_delete_xpath))).click()
        print("✅ Item deleted successfully.")
        time.sleep(5)

    def close(self):
        self.driver.quit()

if __name__ == "__main__":
    test = WebTest()
    test.login()
    test.delete_video_or_audio()
    test.close()
