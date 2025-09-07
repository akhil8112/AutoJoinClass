from flask import Flask, render_template, request,send_file
import tempfile


app = Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/generate', methods=['GET', 'POST'])
def generate():
    time_val = request.form['time']
    course = request.form['course']
    user = request.form['username']
    password = request.form['password']
    # Your Python code as a string
    python_code = """
import schedule
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException, TimeoutException


CLASS_URL = "https://myclass.lpu.in/"
JOIN_TIME = "timexyz"
USER_NAME = "userxyz"
PASSWORD = "passxyz"



def open_class_and_login():
  
    driver = None
    try:
        print("Setting up browser driver...")
        service = ChromeService(ChromeDriverManager().install())
        
        options = webdriver.ChromeOptions()
        options.add_experimental_option("detach", True)

        driver = webdriver.Chrome(service=service, options=options)
        
        print(f"Opening {CLASS_URL}...")
        driver.get(CLASS_URL)
        driver.maximize_window() # Maximize for better view
        
        wait = WebDriverWait(driver, 45)
        
        print("Website opened. Waiting for an initial login button to appear...")
        initial_login_button_xpath = "//*[self::button or self::a or self::input[@type='submit']][contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'login') or contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'sign in')]"
        login_button = wait.until(EC.element_to_be_clickable((By.XPATH, initial_login_button_xpath)))
        print("Initial login button found. Clicking it...")
        login_button.click()
        
        print("Page loaded. Looking for credential fields...")

        username_field_xpath = "//input[contains(@id, 'user') or contains(@name, 'user') or contains(@placeholder, 'User') or contains(@id, 'login') or contains(@name, 'login') or contains(@id, 'reg')]"
        username_input = wait.until(EC.visibility_of_element_located((By.XPATH, username_field_xpath)))
        print("Username field found. Entering username...")
        username_input.send_keys(USER_NAME)

        # Find password field and enter password
        password_field_xpath = "//input[@type='password']"
        password_input = wait.until(EC.visibility_of_element_located((By.XPATH, password_field_xpath)))
        print("Password field found. Entering password...")
        password_input.send_keys(PASSWORD)

        # Find and click the final login/submit button
        final_login_button_xpath = "//button[@type='submit'] | //input[@type='submit'] | //button[contains(., 'Login')] | //button[contains(., 'Sign In')]"
        submit_button = wait.until(EC.element_to_be_clickable((By.XPATH, final_login_button_xpath)))
        print("Final submit button found. Clicking to log in...")
        submit_button.click()
        
        print("Successfully logged in! Now navigating to your classes...")

        # --- Navigate to Classes/Meetings ---
        print("Waiting for 'View Classes/Meetings' button to appear...")
        # This XPath looks for an element with the exact text "View Classes/Meetings"
        view_classes_xpath = "//*[normalize-space()='View Classes/Meetings']"
        view_classes_button = wait.until(EC.element_to_be_clickable((By.XPATH, view_classes_xpath)))
        
        print("'View Classes/Meetings' button found. Clicking it...")
        view_classes_button.click()
        
        print("Waiting for the 11 AM class to appear in the schedule...")

        # Target the <a> tag directly using both the time and lecture name
        class_meeting_xpath = "//a[contains(@class, 'fc-time-grid-event') and contains(@title, 'coursexyz-Lecture') and contains(., '11:00 - 1:00')]"

        # Wait until the element is visible and clickable
        class_meeting_element = wait.until(
            EC.element_to_be_clickable((By.XPATH, class_meeting_xpath))
        )

        # Click it
        driver.execute_script("arguments[0].scrollIntoView(true);", class_meeting_element)
        class_meeting_element.click()

        print(" Successfully clicked on the 11 AM class!")

        print("Waiting for the 'Join' button...")

        # XPath to find the Join button by its text
        join_button_xpath = "//button[contains(., 'Join')] | //a[contains(., 'Join')]"

        join_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, join_button_xpath))
        )

        # Scroll and click
        driver.execute_script("arguments[0].scrollIntoView(true);", join_button)
        join_button.click()

        print(" Successfully clicked the 'Join' button!")

        print("The browser window will remain open.")
        print("The script's job is done for today.")

    except TimeoutException:
        print("The browser window will be left open for you to proceed manually.")
    except WebDriverException as e:
        print(f"An error occurred with the browser driver: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    
    # After running once, we tell the scheduler to remove this job for the day.
    return schedule.CancelJob

def main():
    
    print("Class Opener script started.")
    print(f"Your Class is scheduled to join at {JOIN_TIME} every day.")
    
    schedule.every().day.at(JOIN_TIME).do(open_class_and_login)
    
    print("Waiting for the scheduled time. You can minimize this window.")

    try:
        while True:
            schedule.run_pending()
            if not schedule.jobs:
                print("Daily task completed. The script will now exit.")
                break
            time.sleep(1)
    except KeyboardInterrupt:
        print("Script stopped by user.")

if __name__ == "__main__":
    main()
    """
    python_code = python_code.replace("timexyz", time_val)
    python_code = python_code.replace("userxyz", user)
    python_code = python_code.replace("passxyz", password)
    python_code = python_code.replace("coursexyz", course)
    # Save the string to a temporary file
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".py")
    with open(temp_file.name, "w", encoding="utf-8") as f:
        f.write(python_code)

    # Send it as downloadable file
    return send_file(temp_file.name, as_attachment=True, download_name="script.py")

@app.after_request
def inject_vercel_analytics(response):
    if response.content_type.startswith('text/html'):
        response.data = response.data.replace(b'<!-- VERCEL_ANALYTICS -->', b"<script>window.va = window.va || function () { (window.va.q = window.va.q || []).push(arguments); };</script><script defer src='/_vercel/insights/script.js'></script>")
    return response

if __name__ == "__main__":
    app.run(debug=True)
