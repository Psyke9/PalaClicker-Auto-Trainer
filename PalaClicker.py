from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import time

DATA_FILE = 'src/data.json'  # Data of all the questions and answers.
PSEUDO = 'YOURNAME'  # Your Minecraft username.
QUESTION_SELECTOR = 'p.pb-4'
REVEAL_BUTTON_XPATH = '//button[contains(text(), "Révéler la solution")]'
ANSWER_SELECTOR = 'div.max-h-64.overflow-auto'

used_answers = {}
data = {}

def load_data():
    
    try:
        with open(DATA_FILE, 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_data(data):
    
    with open(DATA_FILE, 'w') as file:
        json.dump(data, file, indent=4)

def get_current_question(driver):

    try:
        question_element = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, QUESTION_SELECTOR))
        )
        return question_element.text.strip()
    except Exception:
        return None

def reveal_answer(driver):

    try:
        reveal_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, REVEAL_BUTTON_XPATH))
        )
        time.sleep(1)  
        reveal_button.click()

        answer_element = WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ANSWER_SELECTOR))
        )
        return answer_element.text.strip()
    except Exception:
        return None

def input_answer(driver, answer):
    
    try:
        input_field = WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located((By.ID, 'user_answer'))
        )
        input_field.clear()
        input_field.send_keys(answer)
        input_field.send_keys(Keys.RETURN)
    except Exception:
        pass

def process_question(driver):
    
    global used_answers, data

    current_question = get_current_question(driver)
    if not current_question or current_question in used_answers:
        return

    if current_question in data:
        input_answer(driver, data[current_question])
    else:
        answer_text = reveal_answer(driver)
        if answer_text:
            data[current_question] = answer_text
            save_data(data)
            input_answer(driver, answer_text)

    used_answers[current_question] = True

def setup_driver():
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    return driver

def main():
    
    global data
    data = load_data()
    driver = setup_driver()

    try:
        driver.get("https://brominee.github.io/PaladiumClicker/")

        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//a[contains(text(), "PalaAnimation Trainer")]'))
        ).click()

        pseudo_field = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, 'pseudo'))
        )
        pseudo_field.clear()
        pseudo_field.send_keys(PSEUDO)
        driver.find_element(By.ID, 'pseudo-submit').click()

        last_question = None
        same_question_start_time = time.time()

        while True:
            current_question = get_current_question(driver)

            if current_question == last_question:
                if time.time() - same_question_start_time >= 5:
                    reveal_answer(driver)
                    same_question_start_time = time.time()
            else:
                same_question_start_time = time.time()

            last_question = current_question
            process_question(driver)

    finally:
        driver.quit()

if __name__ == "__main__":
    main()
