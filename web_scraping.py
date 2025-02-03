from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def extract_credentials():
    try:
        with open("config/userdata.txt", 'r') as file:
            lines = file.readlines()

        credentials = {}
        for line in lines:
            if line.startswith('USERNAME='):
                credentials['username'] = line.strip().split('=')[1]
            elif line.startswith('PASSWORD='):
                credentials['password'] = line.strip().split('=')[1]

        if not credentials.get('username') or not credentials.get('password'):
            raise ValueError("Username or password not found in the file.")

        return credentials

    except FileNotFoundError:
        logging.error("The file 'config/userdata.txt' was not found.")
        raise
    except Exception as e:
        logging.error(f"An error occurred while extracting credentials: {e}")
        raise

def retrieve_courses():
    try:
        credentials = extract_credentials()

        chrome_options = Options()
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-infobars")
        chrome_options.add_argument("--disable-dev-shm-usage")

        webdriver_service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=webdriver_service, options=chrome_options)

        try:
            driver.get("https://academic.ui.ac.id/main/Authentication/")
            wait = WebDriverWait(driver, 100)

            # Log in
            username_field = wait.until(EC.presence_of_element_located((By.NAME, "u")))
            password_field = wait.until(EC.presence_of_element_located((By.NAME, "p")))
            username_field.send_keys(credentials['username'])
            password_field.send_keys(credentials['password'])
            password_field.send_keys(Keys.RETURN)

            # Open course schedule page in a new tab
            driver.execute_script("window.open('https://academic.ui.ac.id/main/CoursePlan/CoursePlanViewSchedule', '_blank');")
            driver.switch_to.window(driver.window_handles[1])

            # Extract course data
            courses = driver.execute_script("""
                return Array.from(document.querySelectorAll('.sch-inner')).map(element => {
                    const tdElement = element.closest('td');
                    const parentRow = tdElement.parentElement;
                    const tdElements = Array.from(parentRow.children);
                    const index = tdElements.indexOf(tdElement);

                    let [time, name, room] = element.innerText.split("\\n").filter(text => text.trim() !== "");
                    return { name, time, room, day: index };
                });
            """)

            if not courses:
                logging.warning("No courses were found on the page.")

            return courses

        except Exception as e:
            logging.error(f"An error occurred while retrieving courses: {e}")
            raise
        finally:
            driver.quit()

    except Exception as e:
        logging.error(f"An error occurred in the retrieve_courses function: {e}")
        raise


if __name__ == "__main__":
    try:
        courses = retrieve_courses()
        if courses:
            logging.info("Courses retrieved successfully:")
            for course in courses:
                logging.info(course)
    except Exception as e:
        logging.error(f"Script failed: {e}")