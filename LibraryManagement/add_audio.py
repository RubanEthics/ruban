import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Load config values
def load_config(file_path):
    config = {}
    with open(file_path, 'r') as file:
        for line in file:
            if "=" in line:
                key, value = line.strip().split("=", 1)
                config[key.strip()] = value.strip()
    return config

class AddAudioTest:
    def __init__(self):
        options = Options()
        options.headless = False
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

        print("✅ Login completed.")
        time.sleep(10)

    def add_audio(self):
        # Define all XPaths
        Library_element = "//div[@data-bs-target='#Library-Management']"
        add_library_element = "//span[text()='Add Video Or Audio']"
        audio_button = "//button[text()=' Audio']"
        audio_element = "//input[@type='file' and @accept='audio/mp3']"
        Register_element = "(//button[text()='Register'])[2]"

        # Your audio file path (use raw string or double backslashes to avoid unicode errors)
        audio_file = r"C:\Users\Picnexs\Desktop\ruban\Kannadi Poove.mp3"

        # Navigate through the UI
        self.wait.until(EC.element_to_be_clickable((By.XPATH, Library_element))).click()
        time.sleep(2)

        self.wait.until(EC.element_to_be_clickable((By.XPATH, add_library_element))).click()
        time.sleep(2)

        self.wait.until(EC.element_to_be_clickable((By.XPATH, audio_button))).click()
        time.sleep(2)

        audio_input = self.wait.until(EC.presence_of_element_located((By.XPATH, audio_element)))
        audio_input.send_keys(audio_file)
        time.sleep(2)

        self.wait.until(EC.element_to_be_clickable((By.XPATH, Register_element))).click()
        print("✅ Audio uploaded and registered successfully.")

    def close(self):
        self.driver.quit()

# Run the test
if __name__ == "__main__":
    test = AddAudioTest()
    test.login()
    test.add_audio()
    test.close()


#hi ruban how
