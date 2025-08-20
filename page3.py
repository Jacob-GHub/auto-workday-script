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