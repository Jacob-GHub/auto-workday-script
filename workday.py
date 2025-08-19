import time, sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import urlparse
from getpass import getpass
from config import Config

class Workday:
  def __init__(self, url):
      self.url = url
      self.profile = Config('config/profile.yaml').load_profile()
      self.companies_file = Config('config/companies.txt')

      # Set up Selenium WebDriver
      self.driver = webdriver.Chrome()
      self.wait = WebDriverWait(self.driver, 10)
      self.driver.maximize_window()

  # Helper: try multiple selectors until one works
  def safe_find(self, selectors):
      for by, selector in selectors:
          try:
              return self.driver.find_element(by, selector)
          except:
              continue
      raise Exception(f"No selector worked: {selectors}")

  def signup(self):
      # Create account button
      button = self.wait.until(
          EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-automation-id='createAccountLink']"))
      )
      button.click()
      time.sleep(2)

      # Email
      self.safe_find([
          (By.CSS_SELECTOR, "input[data-automation-id='email']"),
          (By.NAME, "email"),
          (By.XPATH, "//input[contains(@aria-label,'Email')]")
      ]).send_keys(self.profile['email'])

      # Password + verify
      self.safe_find([
          (By.CSS_SELECTOR, "input[data-automation-id='password']"),
          (By.NAME, "password")
      ]).send_keys(self.profile['password'])

      self.safe_find([
          (By.CSS_SELECTOR, "input[data-automation-id='verifyPassword']"),
          (By.NAME, "verifyPassword")
      ]).send_keys(self.profile['password'])

      # Checkbox (if present)
      try:
          self.safe_find([
              (By.CSS_SELECTOR, "input[data-automation-id='createAccountCheckbox']"),
              (By.NAME, "createAccountCheckbox")
          ]).click()
      except:
          print("Exception: 'No signup checkbox'")

      # Final submit
      button = self.wait.until(
          EC.element_to_be_clickable((By.XPATH, "//div[contains(text(),'Create Account')]"))
      )
      button.click()
      time.sleep(2)

  def signin(self):
      # Email
      self.safe_find([
          (By.CSS_SELECTOR, "input[data-automation-id='email']"),
          (By.NAME, "username"),
          (By.XPATH, "//input[contains(@aria-label,'Email')]")
      ]).send_keys(self.profile['email'])

      # Password
      self.safe_find([
          (By.CSS_SELECTOR, "input[data-automation-id='password']"),
          (By.NAME, "password"),
          (By.XPATH, "//input[contains(@aria-label,'Password')]")
      ]).send_keys(self.profile['password'])

      # Sign in button
      button = self.wait.until(
          EC.element_to_be_clickable((By.XPATH, "//div[contains(text(),'Sign In') or contains(text(),'Log In')]"))
      )
      button.click()
      time.sleep(2)

  def fillform_page_1(self):
    profile = self.profile

    # Collect all inputs
    inputs = self.driver.find_elements(By.CSS_SELECTOR, "input, textarea, select")
    input_map = {}

    for i, el in enumerate(inputs):
        try:
            attrs = self.driver.execute_script(
                "var items = {}; for (var i=0; i<arguments[0].attributes.length; i++) "
                "{ items[arguments[0].attributes[i].name] = arguments[0].attributes[i].value }; return items;",
                el
            )
            # Try also to fetch associated label text
            label_text = ""
            try:
                label_text = self.driver.execute_script(
                    "return document.querySelector('label[for=\"'+arguments[0].id+'\"]').innerText",
                    el
                )
            except:
                pass
            if label_text:
                attrs["label"] = label_text

            print(f"[{i}] {attrs}")
            input_map[i] = (el, attrs)
        except Exception as e:
            print(f"[{i}] Could not read element: {e}")

    def normalize(s):
        return "".join(ch for ch in s.lower() if ch.isalnum())

    def find_and_fill(keywords, value):
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


    # Configurable field map
    FIELD_MAP = {
    "first_name": ["first", "fname", "legalname--firstname"],
    "family_name": ["last", "lname", "surname", "legalname--lastname"],
    "first_name_local": ["local", "firstnamelocal"],
    "address_line_1": ["address1", "addressline1", "address--addressline1"],
    "address_line_2": ["address2", "addressline2", "address--addressline2"],
    "address_line_3": ["address3", "addressline3", "address--addressline3"],
    "address_city": ["city", "address--city"],
    "address_state": ["state", "address--state", "region", "address--region"],
    "address_postal_code": ["postal", "zip", "postalcode", "address--postalcode"],
    "email": ["email", "mail", "emailaddress"],
    "phone_number": ["phone", "phonenumber"],
}


    # --- Source selector (unchanged) ---
    try:
        self.safe_find([
            (By.CSS_SELECTOR, "div[data-automation-id='multiSelectContainer']")
        ]).click()
        time.sleep(1)
        source = profile.get('application_source', 'LinkedIn')
        self.safe_find([
            (By.XPATH, f"//div[text()='{source}']"),
            (By.XPATH, f"//div[contains(text(),'{source}')]")
        ]).click()
        time.sleep(1)
    except:
        print("Exception: 'No Source selector'")

    # --- Fill dynamically ---
    for field, keywords in FIELD_MAP.items():
        value = profile.get(field, "")
        if value:
            find_and_fill(keywords, value)

    # --- State dropdown ---
# --- State handling ---
    try:
        # Click the state dropdown (button)
        state_button = self.safe_find([
            (By.CSS_SELECTOR, "button[data-automation-id='addressSection_region']")
        ])
        state_button.click()

        # Grab the state from the profile, default to California
        state = profile.get("address_state", "California")

        # Click the matching option in the dropdown
        state_option = self.safe_find([
            (By.XPATH, f"//div[text()='{state}']"),
            (By.XPATH, f"//div[contains(text(), '{state}')]")
        ])
        state_option.click()

    except Exception as e:
        print("Exception: Could not select state:", e)

    # --- Country dropdown ---
    try:
        self.safe_find([
            (By.CSS_SELECTOR, "button[data-automation-id='addressSection_countryRegion']")
        ]).click()
        country = profile.get('address_country', 'United States')
        self.safe_find([
            (By.XPATH, f"//div[text()='{country}']"),
            (By.XPATH, f"//div[contains(text(),'{country}')]")
        ]).click()
    except:
        print("Exception: 'No country picker'")

    # --- Phone type dropdown ---
    try:
        self.safe_find([
            (By.CSS_SELECTOR, "button[data-automation-id='phone-device-type']")
        ]).click()
        phone_type = profile.get('phone_type', 'Mobile')
        self.safe_find([
            (By.XPATH, f"//div[text()='{phone_type}']"),
            (By.XPATH, f"//div[contains(text(),'{phone_type}')]")
        ]).click()
    except:
        print("Exception: 'No phone type dropdown'")

  # def fillform_page_2(self):
  #   delete_work_experiences = self.driver.find_elements(By.CSS_SELECTOR, "button[data-automation-id='panel-set-delete-button']")
  #   i = 1
  #   while i <= len(delete_work_experiences):
  #     self.driver.find_element(By.CSS_SELECTOR, "button[data-automation-id='panel-set-delete-button']").click()
  #     i = i+1
  #     time.sleep(1)
    
  #   for work_experience_index, work_experience in enumerate(self.profile['work_experiences']):
  #     if work_experience_index == 0:
  #       try:
  #         self.driver.find_element(By.CSS_SELECTOR, "button[data-automation-id='Add']").click()
  #       except:
  #         print("Exception: 'Add button not found'")
  #     else:
  #       self.driver.find_element(By.CSS_SELECTOR, "button[data-automation-id='Add Another']").click()
        
  #     time.sleep(2)
  #     work_experience_div = self.driver.find_element(By.CSS_SELECTOR, "div[data-automation-id='workExperience-"+str(work_experience_index+1)+"']")
  #     work_experience.update({'div': work_experience_div})
  #     self.fill_work_experience(work_experience)
  #     time.sleep(2)
    
  #   resume_section = self.driver.find_element(By.CSS_SELECTOR, "div[data-automation-id='resumeSection']")
  #   resume_section.location_once_scrolled_into_view
  #   time.sleep(2)
      
  #   delete_resumes = self.driver.find_elements(By.CSS_SELECTOR, "button[data-automation-id='delete-file']")
  #   i = 1
  #   while i <= len(delete_resumes):
  #     self.driver.find_element(By.CSS_SELECTOR, "button[data-automation-id='delete-file']").click()
  #     i = i+1
  #     time.sleep(1)
    
  #   file_input = self.driver.find_element(By.CSS_SELECTOR, "input[type='file']")
  #   file_input.send_keys(self.profile['resume_path'])
  #   time.sleep(10)
    
  #   try:
  #     linkedin_question = self.driver.find_element(By.CSS_SELECTOR, "input[type='text'][data-automation-id='linkedinQuestion']")
  #     linkedin_question.clear()
  #     linkedin_question.send_keys(self.profile['linkedin_question'])
  #   except:
  #     print("Exception: 'No Linkedin input'")
    
  # def fillform_page_3(self):
  #   try:
  #     self.driver.find_element(By.CSS_SELECTOR, "button[type='button'][aria-label='Are you legally authorized to work in the country to which you are applying? select one required']").click()
  #     time.sleep(2)
  #     self.driver.find_element(By.XPATH, "//div[text()='Yes']").click()
  #     time.sleep(2)
  #   except:
  #     print("Exception: 'Work Authorization already selected'")
    
  #   try:
  #     self.driver.find_element(By.CSS_SELECTOR, "button[type='button'][aria-label='Will you require sponsorship to continue and/or extend your current work authorization status? select one required']").click()
  #     time.sleep(2)
  #     self.driver.find_element(By.XPATH, "//div[text()='No']").click()
  #     time.sleep(2)
  #   except:
  #     print("Exception: 'Visa Sponsorship already selected'")
    
  # def fillform_page_4(self):
  #   try:
  #     self.driver.find_element(By.CSS_SELECTOR, "button[type='button'][data-automation-id='gender']").click()
  #     time.sleep(2)
  #     self.driver.find_element(By.XPATH, "//div[text()='Male']").click()
  #     time.sleep(2)
  #   except:
  #     print("Exception: 'Gender not present'")

  #   try:
  #     self.driver.find_element(By.CSS_SELECTOR, "button[type='button'][data-automation-id='nationality']").click()
  #     time.sleep(2)
  #     self.driver.find_element(By.XPATH, "//div[text()='India']").click()
  #     time.sleep(2)
  #   except:
  #     print("Exception: 'Nationality not present")

  #   try:
  #     agreement_checkbox = self.driver.find_element(By.CSS_SELECTOR, "input[type='checkbox'][data-automation-id='agreementCheckbox']")
  #     agreement_checkbox.location_once_scrolled_into_view
  #     agreement_checkbox.click()
  #   except:
  #     print("Exception: agreementCheckbox not present")

  # def fill_work_experience(self, work_experience):
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
  #   month_picker = self.driver.find_element(By.CSS_SELECTOR, "span[data-automation-id='monthPickerSpinnerLabel']")
  #   while month_picker.text != work_experience['start_year']:
  #     self.driver.find_element(By.CSS_SELECTOR, "button[type='button'][data-automation-id='monthPickerLeftSpinner']").click()
  #   self.driver.find_element(By.XPATH, "//label[text()='"+work_experience['start_month']+"']").click()
    
  #   end_date_div = work_experience['div'].find_element(By.CSS_SELECTOR, "div[data-automation-id='formField-endDate']")
  #   end_date_div.find_element(By.CSS_SELECTOR, "div[role='button'][data-automation-id='dateIcon']").click()
  #   time.sleep(2)
  #   month_picker = self.driver.find_element(By.CSS_SELECTOR, "span[data-automation-id='monthPickerSpinnerLabel']")
  #   while month_picker.text != work_experience['end_year']:
  #     self.driver.find_element(By.CSS_SELECTOR, "button[type='button'][data-automation-id='monthPickerLeftSpinner']").click()
  #   self.driver.find_element(By.XPATH, "//label[text()='"+work_experience['end_month']+"']").click()

  def click_next(self):
    button = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-automation-id='bottom-navigation-next-button']")))
    button.click()
    try:
      error_button = self.driver.find_element(By.CSS_SELECTOR, "button[data-automation-id='errorBanner']")
      print("Exception: 'Errors on page. Please resolve and submit manually. You have 60 seconds to do so!'")
      time.sleep(60)
    except:
      print("No Errors")
    time.sleep(10)
    
  def run(self):
    parsed_url = urlparse(self.url)
    company = parsed_url.netloc.split('.')[0]
    existing_company = company in self.companies_file.read_companies()
        
    self.driver.get(self.url) # Open a webpage
    time.sleep(5)
    
    # accept cookies
    # try:
    #   button = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-automation-id='legalNoticeAcceptButton']")))
    #   button.click()
    # except:
    #   print("Exception: 'No button for Cookies!")
    
    # try:
    #   if existing_company:
    #     self.signin()
    #   else:
    #     self.signup()
    #     self.companies_file.write_company(company)
    # except:
    #   print("No Signup/Signin - Apply without Signin")

    time.sleep(5)
    if len(self.driver.find_elements(By.CSS_SELECTOR, "div[data-automation-id='alreadyApplied']")) > 0:
      print("alreadyApplied job, exiting the program...")
      self.driver.quit()
      sys.exit()
    
    # try:
    #   button = self.driver.find_element(By.CSS_SELECTOR, "a[role='button'][data-automation-id='applyManually']")
    #   button.click()
    # except:
    #   print("NoSuchElementException")

    # time.sleep(10)
    self.fillform_page_1()
    # self.click_next()
    
    # self.fillform_page_2()
    # self.click_next()
    
    # self.fillform_page_3()
    # self.click_next()
    
    # self.fillform_page_4()
    # self.click_next()
    
    # # review and submit
    # self.click_next()
    
    # # Wait for half minute
    # time.sleep(30)

    # Close the browser
    # self.driver.quit()

print("Please share Workday URL:")
url = str(input())

workday = Workday(url)
# ipdb.set_trace()
workday.run()


# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC

# # Start driver
# driver = webdriver.Chrome()

# driver.get("https://freddiemac.wd5.myworkdayjobs.com/en-US/External/job/McLean%2C-VA/Technology-Intern_JR16008/apply/applyManually?utm_source=Simplify&ref=Simplify")

# # Possible variations of field names
# field_map = {
#     "first_name": ["first", "fname", "given"],
#     "last_name": ["last", "lname", "surname", "family"],
#     "email": ["email", "mail"],
#     "phone": ["phone", "mobile", "cell"]
# }

# def find_input(possible_keywords, timeout=10):
#     """Wait for an input matching any keyword to appear and return it."""
#     xpath_conditions = []
#     for kw in possible_keywords:
#         xpath_conditions.append(f"contains(translate(@id,'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'), '{kw}')")
#         xpath_conditions.append(f"contains(translate(@name,'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'), '{kw}')")
#         xpath_conditions.append(f"contains(translate(@aria-label,'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'), '{kw}')")
#         xpath_conditions.append(f"contains(translate(@placeholder,'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'), '{kw}')")

#     xpath = "//input[" + " or ".join(xpath_conditions) + "]"
    
#     # Wait until visible
#     return WebDriverWait(driver, timeout).until(
#         EC.presence_of_element_located((By.XPATH, xpath))
#     )

# # Example usage
# first_name_input = find_input(field_map["first_name"])
# first_name_input.send_keys("Jacob")

# last_name_input = find_input(field_map["last_name"])
# last_name_input.send_keys("Perez")

# email_input = find_input(field_map["email"])
# email_input.send_keys("jacob@example.com")

# phone_input = find_input(field_map["phone"])
# phone_input.send_keys("123-456-7890")
