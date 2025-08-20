from includes import *
from utils import safe_find

def signup(driver,wait,profile):
    print("signing up")
    time.sleep(1)
    # Email
    safe_find([
        (By.CSS_SELECTOR, "input[data-automation-id='email']"),
        (By.NAME, "email"),
        (By.XPATH, "//input[contains(@aria-label,'Email')]")
    ]).send_keys(profile['email'])

    # Password + verify
    safe_find([
        (By.CSS_SELECTOR, "input[data-automation-id='password']"),
        (By.NAME, "password")
    ]).send_keys(profile['password'])

    safe_find([
        (By.CSS_SELECTOR, "input[data-automation-id='verifyPassword']"),
        (By.NAME, "verifyPassword")
    ]).send_keys(profile['password'])

    # Checkbox (if present)
    try:
        safe_find([
            (By.CSS_SELECTOR, "input[data-automation-id='createAccountCheckbox']"),
            (By.NAME, "createAccountCheckbox")
        ]).click()
    except:
        print("Exception: 'No signup checkbox'")

    # Final submit
    try:
        submit_button = safe_find([
            (By.CSS_SELECTOR, "button[data-automation-id='createAccountSubmitButton']"),
            (By.XPATH, "//button[contains(text(),'Create Account')]"),
            (By.XPATH, "//div[contains(text(),'Create Account')]"),
        ])
        wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@data-automation-id='createAccountSubmitButton']")))

        ActionChains(driver).move_to_element(submit_button).click().perform()
        print("Clicked final 'Create Account'")
    except Exception as e:
        print("Exception: 'No final Create Account button found'", e)

    time.sleep(2)


# def signin(driver,wait,profile):
#       # Email
#       safe_find([
#           (By.CSS_SELECTOR, "input[data-automation-id='email']"),
#           (By.NAME, "username"),
#           (By.XPATH, "//input[contains(@aria-label,'Email')]")
#       ]).send_keys(profile['email'])

#       # Password
#       safe_find([
#           (By.CSS_SELECTOR, "input[data-automation-id='password']"),
#           (By.NAME, "password"),
#           (By.XPATH, "//input[contains(@aria-label,'Password')]")
#       ]).send_keys(profile['password'])

#       # Sign in button
#       button = wait.until(
#           EC.element_to_be_clickable((By.XPATH, "//div[contains(text(),'Sign In') or contains(text(),'Log In')]"))
#       )
#       button.click()
#       time.sleep(2)