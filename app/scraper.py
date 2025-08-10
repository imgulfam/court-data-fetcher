# from playwright.sync_api import sync_playwright
# from bs4 import BeautifulSoup

# def fetch_case_details(case_type: str, case_number: str, case_year: str) -> dict:
#     """
#     Fetches case details from the Delhi High Court website.
#     """
#     print(f"--- Starting scraper for {case_type} {case_number}/{case_year} ---")
    
#     with sync_playwright() as p:
#         # Set headless=True for the final version to run faster without a visible browser.
#         browser = p.chromium.launch(headless=True) 
#         page = browser.new_page()
#         try:
#             print("Navigating to Delhi High Court website...")
#             page.goto("https://delhihighcourt.nic.in/app/get-case-type-status", timeout=60000)
#             print("Successfully navigated to the website.")

#             page.select_option("#case_type", value=case_type)
#             page.fill("#case_number", case_number)
#             page.select_option("#case_year", value=case_year)
            
#             captcha_text = page.inner_text("#captcha-code")
#             page.fill("#captchaInput", captcha_text)
#             print("Form filled successfully.")

#             page.click("#search")
#             print("Submit button clicked. Waiting for results...")
            
#             page.wait_for_selector("#caseTable tbody td.sorting_1", timeout=30000)
#             print("Results data loaded in the table.")

#             html_content = page.content()
#             soup = BeautifulSoup(html_content, 'html.parser')

#             party_names_element = soup.select_one("#caseTable td:nth-child(3)")
#             next_date_element = soup.select_one("#caseTable td:nth-child(4)")
            
#             # --- FINAL FIX FOR THE LINK ---
#             # Find the second column (td) in the table.
#             second_column = soup.select_one("#caseTable td:nth-child(2)")
#             pdf_link_element = None
#             if second_column:
#                 # Find the link inside that column that contains the text "Orders".
#                 # This is a very robust way to find the correct link.
#                 pdf_link_element = second_column.find('a', string='Orders')

#             party_names = party_names_element.get_text(separator=" ", strip=True) if party_names_element else "Not Found"
#             next_hearing_date = next_date_element.get_text(separator=" ", strip=True) if next_date_element else "Not Found"
            
#             # The href from the "Orders" link is a full URL.
#             pdf_link = pdf_link_element['href'] if pdf_link_element and pdf_link_element.has_attr('href') else "Not Found"
#             # --- END OF FINAL FIX ---

#             result = {
#                 "status": "Success",
#                 "party_names": party_names,
#                 "next_hearing_date": next_hearing_date,
#                 "pdf_link": pdf_link,
#                 "error_message": None
#             }

#         except Exception as e:
#             print(f"An error occurred during scraping: {e}")
#             result = {
#                 "status": "Error",
#                 "party_names": None,
#                 "next_hearing_date": None,
#                 "pdf_link": None,
#                 "error_message": f"An error occurred in the scraper: {e}"
#             }
        
#         finally:
#             browser.close()

#     print("--- Scraper finished ---")
#     return result


from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

def fetch_case_details(case_type: str, case_number: str, case_year: str) -> dict:
    """
    Fetches case details from the Delhi High Court website by performing a 2-step scrape.
    """
    print(f"--- Starting scraper for {case_type} {case_number}/{case_year} ---")
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        try:
            # --- STEP 1: Get to the first results page ---
            print("Navigating to Delhi High Court website...")
            page.goto("https://delhihighcourt.nic.in/app/get-case-type-status", timeout=60000)
            
            page.select_option("#case_type", value=case_type)
            page.fill("#case_number", case_number)
            page.select_option("#case_year", value=case_year)
            
            captcha_text = page.inner_text("#captcha-code")
            page.fill("#captchaInput", captcha_text)
            
            page.click("#search")
            print("Submit button clicked. Waiting for first results page...")
            
            page.wait_for_selector("#caseTable tbody td.sorting_1", timeout=30000)
            print("First results page loaded.")
            
            html_content = page.content()
            soup = BeautifulSoup(html_content, 'html.parser')

            party_names_element = soup.select_one("#caseTable td:nth-child(3)")
            next_date_element = soup.select_one("#caseTable td:nth-child(4)")
            
            party_names = party_names_element.get_text(separator=" ", strip=True) if party_names_element else "Not Found"
            next_hearing_date = next_date_element.get_text(separator=" ", strip=True) if next_date_element else "Not Found"

            # --- STEP 2: Find the 'Orders' link and navigate to the second page ---
            print("Finding link to the 'Orders' page...")
            orders_link_element = soup.select_one("#caseTable td:nth-child(2) a[style*='color:blue']")
            if not orders_link_element:
                raise ValueError("Could not find the 'Orders' link on the first results page.")
            
            orders_page_url = orders_link_element['href']
            print(f"Navigating to Orders page: {orders_page_url}")
            page.goto(orders_page_url, timeout=60000)

            # --- STEP 3: Find the final PDF link on the second page ---
            print("Waiting for final PDF link on the 'Orders' page...")
            final_pdf_selector = 'a[href*="showlogo"][href*=".pdf"]'
            
            final_link_element = page.locator(final_pdf_selector).first
            
            # --- THIS IS THE FIX ---
            # Removed 'await' from the next two lines
            final_link_element.wait_for(timeout=30000) # Wait for the element to be ready
            pdf_link = final_link_element.get_attribute('href')
            # --- END OF FIX ---

            print(f"Found final PDF link: {pdf_link}")

            result = {
                "status": "Success",
                "party_names": party_names,
                "next_hearing_date": next_hearing_date,
                "pdf_link": pdf_link,
                "error_message": None
            }

        except Exception as e:
            print(f"An error occurred during scraping: {e}")
            result = {
                "status": "Error",
                "party_names": None,
                "next_hearing_date": None,
                "pdf_link": None,
                "error_message": f"An error occurred in the scraper: {e}"
            }
        
        finally:
            browser.close()

    print("--- Scraper finished ---")
    return result