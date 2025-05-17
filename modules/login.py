import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Load key-value pairs from config.txt
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
        # Set Chrome options to make sure the browser window is visible
        options = Options()
        options.headless = False  # Make sure the browser shows (False means visible)
        
        # Initialize the WebDriver with options
        self.driver = webdriver.Chrome(options=options)
        self.driver.maximize_window()  # Open browser maximized
        self.config = load_config(r"C:\Users\Picnexs\Desktop\ruban\config\config.txt")  # Corrected file path

        # Set XPaths for login
        self.password_element = "(//input[@name='password'])"
        self.login_button_element = "(//button[@id='signin-submit'])"

    def login(self):
        # Navigate to the URL from the config file
        self.driver.get(self.config["URL"])
        wait = WebDriverWait(self.driver, 20)  # Increased wait time (20 seconds)

        # Try to locate the email field (with index [2] first, fallback to [1])
        try:
            email_field = wait.until(EC.presence_of_element_located((By.XPATH, "(//input[@name='email'])[2]")))
        except:
            print("⚠️ Email field [2] not found, trying [1]")
            email_field = wait.until(EC.presence_of_element_located((By.XPATH, "(//input[@name='email'])[1]")))
        
        email_field.send_keys(self.config["USERNAME"])  # Enter the username
        time.sleep(1)  # Add delay after typing username

        # Locate and enter the password
        password_field = wait.until(EC.presence_of_element_located((By.XPATH, self.password_element)))
        password_field.send_keys(self.config["PASSWORD"])
        time.sleep(1)  # Add delay after typing password

        # Click the login button
        login_button = wait.until(EC.element_to_be_clickable((By.XPATH, self.login_button_element)))
        login_button.click()
        print("✅ Login completed.")
        
        # Wait for 10 seconds for the redirect to complete
        time.sleep(10)  # This ensures the next page loads

        # After waiting, ensure a specific element is available on the next page
        next_page_element = wait.until(EC.presence_of_element_located((By.XPATH, "Your next page element XPath")))
        print("✅ Redirected to the next page successfully.")

    def close(self):
        self.driver.quit()  # Close the browser once done

# ---------------- Run the Test ----------------
if __name__ == "__main__":
    test = WebTest()
    test.login()  # Perform login
    # test.user_module()  # Add future modules after login
    test.close()  # Close the browser once the test is done
