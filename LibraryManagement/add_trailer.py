import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Load config from file
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
        options.headless = False  # Set to True if you want to run headless
        self.driver = webdriver.Chrome(options=options)
        self.driver.maximize_window()
        self.config = load_config(r"C:\Users\Picnexs\Desktop\ruban\config\config.txt")
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

    def add_trailer(self):
        # Define XPaths
        library_section = "//div[@data-bs-target='#Library-Management']"
        add_library_element = "//span[text()='Add Video Or Audio']"
        trailer_button = "//button[@id='trailerButton']"  # Based on your earlier message
        trailer_input_xpath = "//input[@type='file' and @id='fileInput']"
        register_button = "(//button[text()='Register'])[2]"
        trailer_file = r"C:\Users\Picnexs\Desktop\ruban\OLED .mp4"

        # Navigate through UI
        self.wait.until(EC.element_to_be_clickable((By.XPATH, library_section))).click()
        time.sleep(2)

        self.wait.until(EC.element_to_be_clickable((By.XPATH, add_library_element))).click()
        time.sleep(2)

        self.wait.until(EC.element_to_be_clickable((By.XPATH, trailer_button))).click()
        time.sleep(2)

        # Upload trailer file
        trailer_input = self.wait.until(EC.presence_of_element_located((By.XPATH, trailer_input_xpath)))
        trailer_input.send_keys(trailer_file)
        time.sleep(3)

        # Submit the form
        self.wait.until(EC.element_to_be_clickable((By.XPATH, register_button))).click()
        print("✅ Trailer uploaded and registered successfully.")
        time.sleep(5)

    def close(self):
        self.driver.quit()

# Run script
if __name__ == "__main__":
    test = WebTest()
    test.login()
    test.add_trailer()
    test.close()

    
#2mail.com