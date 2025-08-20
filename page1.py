from includes import *
from utils import safe_find, find_and_fill

FIELD_MAP = {
    "first_name": ["first", "fname", "legalname--firstname"],
    "family_name": ["last", "lname", "surname", "legalname--lastname"],
    "first_name_local": ["local", "firstnamelocal"],
    "address_line_1": ["address1", "addressline1", "address--addressline1"],
    "address_line_2": ["address2", "addressline2", "address--addressline2"],
    "address_line_3": ["address3", "addressline3"],
    "address_city": ["city", "address--city"],
    "address_state": ["state", "address--state", "region", "address--region"],
    "address_postal_code": ["postal", "zip", "postalcode", "address--postalcode"],
    "email": ["email", "mail", "emailaddress"],
    "phone_number": ["phone", "phonenumber"],
}

def fillform_page_1(driver):
    profile = profile

    # Collect all inputs
    inputs = driver.find_elements(By.CSS_SELECTOR, "input, textarea, select")
    input_map = {}

    for i, el in enumerate(inputs):
        try:
            attrs = driver.execute_script(
                "var items = {}; for (var i=0; i<arguments[0].attributes.length; i++) "
                "{ items[arguments[0].attributes[i].name] = arguments[0].attributes[i].value }; return items;",
                el
            )
            # Try also to fetch associated label text
            label_text = ""
            try:
                label_text = driver.execute_script(
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
    
        # --- Source selector (unchanged) ---
    try:
        safe_find([
            (By.CSS_SELECTOR, "div[data-automation-id='multiSelectContainer']")
        ]).click()
        time.sleep(1)
        source = profile.get('application_source', 'LinkedIn')
        safe_find([
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
            find_and_fill(keywords, value,input_map)

    # --- State dropdown ---
# --- State handling ---
    try:
        # Click the state dropdown (button)
        state_button = safe_find([
            (By.CSS_SELECTOR, "button[data-automation-id='addressSection_region']")
        ])
        state_button.click()

        # Grab the state from the profile, default to California
        state = profile.get("address_state", "California")

        # Click the matching option in the dropdown
        state_option = safe_find([
            (By.XPATH, f"//div[text()='{state}']"),
            (By.XPATH, f"//div[contains(text(), '{state}')]")
        ])
        state_option.click()

    except Exception as e:
        print("Exception: Could not select state:", e)

    # --- Country dropdown ---
    try:
        safe_find([
            (By.CSS_SELECTOR, "button[data-automation-id='addressSection_countryRegion']")
        ]).click()
        country = profile.get('address_country', 'United States')
        safe_find([
            (By.XPATH, f"//div[text()='{country}']"),
            (By.XPATH, f"//div[contains(text(),'{country}')]")
        ]).click()
    except:
        print("Exception: 'No country picker'")

    # --- Phone type dropdown ---
    try:
        safe_find([
            (By.CSS_SELECTOR, "button[data-automation-id='phone-device-type']")
        ]).click()
        phone_type = profile.get('phone_type', 'Mobile')
        safe_find([
            (By.XPATH, f"//div[text()='{phone_type}']"),
            (By.XPATH, f"//div[contains(text(),'{phone_type}')]")
        ]).click()
    except:
        print("Exception: 'No phone type dropdown'")