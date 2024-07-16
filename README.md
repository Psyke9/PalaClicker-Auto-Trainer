---

# Paladium Clicker Automation Script

This script automates the process of answering questions in the Paladium Clicker: ( https://brominee.github.io/PaladiumClicker/ ) game using Selenium WebDriver. It stores previously answered questions and their corresponding answers in a JSON file, enabling automated and efficient gameplay.

## Prerequisites

Make sure you have the following installed:
- Python 3.x
- Google Chrome browser
- ChromeDriver
- The following Python packages:
  - `selenium`
  - `webdriver_manager`
  - `json`

You can install the required packages using pip:

```
pip install selenium webdriver_manager
```

## Setup

1. Clone the repository to your local machine.
2. Navigate to the project directory.
3. Ensure you have the `src/data.json` file in place to store the questions and answers. If not, create an empty JSON file named `data.json` in the `src` directory.

## Configuration

Update the following variables in the script according to your needs:

- `DATA_FILE`: Path to the JSON file where the questions and answers will be stored.
- `PSEUDO`: Your Minecraft username.

```python
DATA_FILE = 'src/data.json'  # Path to the data file.
PSEUDO = 'YOURNAME'  # Your Minecraft username.
```

## Usage

Run the script using Python:

```
python script.py
```

The script will open a Chrome browser window and navigate to the Paladium Clicker game. It will automatically handle the following tasks:

1. Navigate to the PalaAnimation Trainer page.
2. Enter your Minecraft username.
3. Start answering questions automatically using previously stored answers or by revealing the answer if it's a new question.

## Script Breakdown

### Loading and Saving Data

The script uses a JSON file to store questions and their corresponding answers.

- `load_data()`: Loads the data from the JSON file.
- `save_data(data)`: Saves the updated data back to the JSON file.

### Interacting with the Game

The script uses Selenium WebDriver to interact with the game elements.

- `get_current_question(driver)`: Retrieves the current question from the page.
- `reveal_answer(driver)`: Clicks the "Révéler la solution" button to reveal the answer.
- `input_answer(driver, answer)`: Inputs the answer into the answer field and submits it.
- `process_question(driver)`: Processes the current question, checking if the answer is already known or needs to be revealed.

### Main Automation Loop

The `main()` function sets up the WebDriver, navigates to the game, and enters a loop to continuously process questions.

### Example Usage

```python
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
```

## Notes

- The script includes exception handling to ensure the browser is properly closed in case of an error.
- Adjust the `time.sleep()` and `WebDriverWait` durations if you experience issues with timing or loading elements.

Feel free to contribute to the repository by submitting issues or pull requests.

---
