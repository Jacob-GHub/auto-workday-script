from includes import *
from sign import signup
from utils import safe_find


def load_profile():
    return Config('config/profile.yaml').load_profile()

def setup_driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    wait = WebDriverWait(driver, 10)
    return driver, wait

def run(url, profile):
    driver, wait = setup_driver()
    driver.get(url)
    time.sleep(3)

    # Try clicking apply button
    try:
        button = safe_find(driver, wait, [
            (By.CSS_SELECTOR, "a[role='button'][data-automation-id='ApplyAdventureButton']"),
            (By.CSS_SELECTOR, "a[role='button'][data-automation-id='Apply_AdventureButton']"),
            (By.CSS_SELECTOR, "a[role='button'][data-automation-id='Apply_Adventure_Button']"),
            (By.CSS_SELECTOR, "a[role='button'][data-automation-id='ApplyAdventure_Button']"),
            (By.XPATH, "//button[contains(text(),'Apply')]"),
            (By.XPATH, "//a[contains(text(),'Apply')]")
        ])
        button.click()
        print("Clicked Apply button")
    except:
        print("No Apply button found")

    # Try Apply Manually
    try:
        manual_button = safe_find(driver, wait, [
            (By.CSS_SELECTOR, "button[data-automation-id='applyManually']"),
            (By.CSS_SELECTOR, "a[role='button'][data-automation-id='applyManually']"),
            (By.CSS_SELECTOR, "div[role='button'][data-automation-id='applyManually']"),
            (By.XPATH, "//button[contains(text(),'Apply Manually')]"),
            (By.XPATH, "//a[contains(text(),'Apply Manually')]"),
            (By.XPATH, "//div[contains(text(),'Apply Manually')]"),
        ])
        manual_button.click()
        print("Selected 'Apply Manually'")
    except:
        try:
            resume_button = safe_find(driver, wait, [
                (By.CSS_SELECTOR, "button[data-automation-id='autoFillWithResume']"),
                (By.CSS_SELECTOR, "a[role='button'][data-automation-id='autoFillWithResume']"),
                (By.CSS_SELECTOR, "div[role='button'][data-automation-id='autoFillWithResume']"),
                (By.XPATH, "//button[contains(text(),'Resume')]"),
                (By.XPATH, "//a[contains(text(),'Resume')]"),
                (By.XPATH, "//div[contains(text(),'Resume')]"),
            ])
            resume_button.click()
            print("Selected 'Auto-fill with Resume'")
        except:
            print("No Apply option buttons found")

    time.sleep(3)  # give modal time to render
    try:
        create_btn = safe_find(driver, wait, [
            (By.CSS_SELECTOR, "button[data-automation-id='createAccountLink']"),
            (By.CSS_SELECTOR, "a[role='button'][data-automation-id='createAccountLink']"),
            (By.CSS_SELECTOR, "div[role='button'][data-automation-id='createAccountLink']"),
            (By.XPATH, "//button[contains(text(),'Create Account')]"),
            (By.XPATH, "//a[contains(text(),'Create Account')]"),
            (By.XPATH, "//div[contains(text(),'Create Account')]"),
        ])
        create_btn.click()
        print("Clicked 'Create Account'")
    except:
        print("No 'Create Account' button found")

    try:
        signup(driver, wait, profile)
    except:
        print("SIGNUP FAILED")

    # Example: fill first page of form
    # fillform_page_1(driver, wait, profile)


if __name__ == "__main__":
    print("Please share Workday URL:")
    url = str(input())
    profile = load_profile()
    run(url, profile)
