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
    