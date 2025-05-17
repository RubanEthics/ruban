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

    def preview_library_item(self):
        # Define your XPaths
        Library_element = "//div[@data-bs-target='#Library-Management']"
        all_library_element = "//span[text()='All Library']"
        edit_library_element = "//span[@class='editdropdown-button']"
        preview_element = "(//a[contains(@href, '/library-preview/') and contains(span, 'Preview')])[1]"
        title_element = "//input[@name='title']"
        link_element = "//input[@type='file' and @accept='video/mp4']"
        update_button_element = "//span[text()='Update']"

        # Navigate to Library Management
        self.wait.until(EC.element_to_be_clickable((By.XPATH, Library_element))).click()
        time.sleep(2)

        # Click "All Library"
        self.wait.until(EC.element_to_be_clickable((By.XPATH, all_library_element))).click()
        time.sleep(3)

        # Click Edit dropdown/button for first item
        self.wait.until(EC.element_to_be_clickable((By.XPATH, edit_library_element))).click()
        time.sleep(2)

        # Click Preview link
        self.wait.until(EC.element_to_be_clickable((By.XPATH, preview_element))).click()
        time.sleep(5)  # wait for preview page or modal to load

        # If you want to edit title or upload new file in preview (optional)
        # Example: change title
        # title_input = self.wait.until(EC.presence_of_element_located((By.XPATH, title_element)))
        # title_input.clear()
        # title_input.send_keys("Updated Title")
        # time.sleep(1)

        # Example: upload new video file
        # video_file_path = r"C:\Users\Picnexs\Desktop\ruban\sample_video.mp4"
        # file_input = self.wait.until(EC.presence_of_element_located((By.XPATH, link_element)))
        # file_input.send_keys(video_file_path)
        # time.sleep(2)

        # Click Update button (if any edits are done)
        # self.wait.until(EC.element_to_be_clickable((By.XPATH, update_button_element))).click()
        # print("✅ Preview updated successfully")
        # time.sleep(5)
        #thank you ruban
        print("✅ Preview page opened successfully.")

    def close(self):
        self.driver.quit()

if __name__ == "__main__":
    test = WebTest()
    test.login()
    test.preview_library_item()
    test.close()
