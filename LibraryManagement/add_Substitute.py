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

    def add_substitution(self):
        # Your new XPaths for substitution
        library_management_xpath = "//div[@id='libraryManagement']"
        add_library_xpath = "//a[@id='addLibrary']"
        substitute_button_xpath = "//button[@id='substituteButton']"
        file_input_xpath = "//input[@type='file' and @id='fileInput']"
        register_button_xpath = "(//button[text()='Register'])[2]"

        substitution_file = r"C:\Users\Picnexs\Desktop\ruban\OLED .mp4"  # Update file path here

        # Open Library Management section
        self.wait.until(EC.element_to_be_clickable((By.XPATH, library_management_xpath))).click()
        time.sleep(2)

        # Click Add Video Or Audio
        self.wait.until(EC.element_to_be_clickable((By.XPATH, add_library_xpath))).click()
        time.sleep(3)

        # Click Substitute button
        self.wait.until(EC.element_to_be_clickable((By.XPATH, substitute_button_xpath))).click()
        time.sleep(2)

        # Upload substitution video
        file_input = self.wait.until(EC.presence_of_element_located((By.XPATH, file_input_xpath)))
        file_input.send_keys(substitution_file)
        time.sleep(5)  # Wait for upload

        # Click Register button
        self.wait.until(EC.element_to_be_clickable((By.XPATH, register_button_xpath))).click()
        print("✅ Substitution video uploaded and registered successfully.")
        time.sleep(5)

    def close(self):
        self.driver.quit()

if __name__ == "__main__":
    test = WebTest()
    test.login()
    test.add_substitution()
    test.close()

#ruban