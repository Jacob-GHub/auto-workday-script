from includes import *

def safe_find(driver,wait,selectors):
    for by, selector in selectors:
        try:
            return driver.find_element(by, selector)
        except:
            continue
    raise Exception(f"No selector worked: {selectors}")

# def click_next():
#     button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-automation-id='bottom-navigation-next-button']")))
#     button.click()
#     try:
#       error_button = driver.find_element(By.CSS_SELECTOR, "button[data-automation-id='errorBanner']")
#       print("Exception: 'Errors on page. Please resolve and submit manually. You have 60 seconds to do so!'")
#       time.sleep(60)
#     except:
#       print("No Errors")
#     time.sleep(10)

def normalize(s):
    return "".join(ch for ch in s.lower() if ch.isalnum())

def find_and_fill(keywords, value,input_map):
    best_match = None
    best_score = 0

    for el, attrs in input_map.values():
        haystack = " ".join([normalize(str(v)) for v in attrs.values()])

        for k in keywords:
            nk = normalize(k)

            if nk in haystack:
                # Score exact ID/name match highest
                score = 1
                if normalize(attrs.get("id", "")) == nk or normalize(attrs.get("name", "")) == nk:
                    score = 3
                elif nk == haystack:  # exact whole-field match
                    score = 2

                if score > best_score:
                    best_score = score
                    best_match = el

    if best_match:
        try:
            if not best_match.is_enabled() or not best_match.is_displayed():
                print(f"Skipping hidden field for {keywords}")
                return False

            tag = best_match.tag_name.lower()
            if tag in ("input", "textarea"):
                best_match.clear()
                best_match.send_keys(value)
            elif tag == "select":
                from selenium.webdriver.support.ui import Select
                Select(best_match).select_by_visible_text(value)

            print(f"Filled {keywords} with {value}")
            return True
        except Exception as e:
            print(f"Could not fill {keywords}: {e}")
            return False

    print(f"No field found for {keywords}")
    return False


  # def fill_work_experience(, work_experience):
  #   work_experience['div'].find_element(By.CSS_SELECTOR, "input[type='text'][data-automation-id='jobTitle']").send_keys(work_experience['job_title'])
  #   work_experience['div'].find_element(By.CSS_SELECTOR, "input[type='text'][data-automation-id='company']").send_keys(work_experience['company'])
  #   try:
  #     location = work_experience['div'].find_element(By.CSS_SELECTOR, "input[type='text'][data-automation-id='location']")
  #     location.send_keys(work_experience['location'])
  #   except:
  #     print("Exception: 'no location field in experience'")
  #   work_experience['div'].find_element(By.CSS_SELECTOR, "textarea[data-automation-id='description']").send_keys(work_experience['role_description'])
    
  #   # location.location_once_scrolled_into_view
    
  #   start_date_div = work_experience['div'].find_element(By.CSS_SELECTOR, "div[data-automation-id='formField-startDate']")
  #   start_date_div.find_element(By.CSS_SELECTOR, "div[role='button'][data-automation-id='dateIcon']").click()
  #   time.sleep(2)
  #   month_picker = driver.find_element(By.CSS_SELECTOR, "span[data-automation-id='monthPickerSpinnerLabel']")
  #   while month_picker.text != work_experience['start_year']:
  #     driver.find_element(By.CSS_SELECTOR, "button[type='button'][data-automation-id='monthPickerLeftSpinner']").click()
  #   driver.find_element(By.XPATH, "//label[text()='"+work_experience['start_month']+"']").click()
    
  #   end_date_div = work_experience['div'].find_element(By.CSS_SELECTOR, "div[data-automation-id='formField-endDate']")
  #   end_date_div.find_element(By.CSS_SELECTOR, "div[role='button'][data-automation-id='dateIcon']").click()
  #   time.sleep(2)
  #   month_picker = driver.find_element(By.CSS_SELECTOR, "span[data-automation-id='monthPickerSpinnerLabel']")
  #   while month_picker.text != work_experience['end_year']:
  #     driver.find_element(By.CSS_SELECTOR, "button[type='button'][data-automation-id='monthPickerLeftSpinner']").click()
  #   driver.find_element(By.XPATH, "//label[text()='"+work_experience['end_month']+"']").click()
