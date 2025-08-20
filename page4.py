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