import re, pytest
from playwright.sync_api import Page, expect
from pages.bank_details import BankDetails
from pages.home_page import HomePage

@pytest.mark.skip
def test_form_elements_assertions(page: Page):
  page.goto("http://localhost:8000/forms/kitchen-sink")

  # response not defined
  #expect(response).to_be_ok()
  expect(page).to_have_title(re.compile("Kitchen sink – GOV.UK"))

  # role/label locators are unreliable for me. dont really work.
  # page.get_by_role("textbox").fill("Jav") -- too many matches

  # Assertions test
  expect(page.get_by_label("EmailField")).to_be_attached()
  expect(page.get_by_label("EmailField")).to_be_visible()
  expect(page.get_by_label("EmailField")).to_have_text("")
  page.get_by_label("EmailField").fill("tester@ja.vid")

  # Have text doesn't apply to inputs, use have value
  # expect(page.get_by_label("EmailField")).to_have_text("tester@ja.vid")

  expect(page.get_by_label("EmailField")).to_have_value("tester@ja.vid")
  #page.get_by_role("checkbox", name="boolean_field").check()
  #page.get_by_label("BooleanField").check()
  #page.get_by_label("One").check()

  #ID selector also not working. However it works on some fields, 
  #so perhaps there's an issue with the form code.
  #page.locator("#boolean_field").click()

  page.get_by_label("SelectField").select_option("Two")

@pytest.mark.skip
def test_click_type_hover_file(page: Page):  
  page.goto("http://localhost:8000/forms/kitchen-sink")

  page.get_by_label("StringField").hover()
  page.get_by_label("TextAreaField").focus()
  # Press sequentially not working, stick to fill
  # page.locator("TextAreaField").pressSequentially("The quick brown fox jumps over the lazy dog")
  page.get_by_label("TextAreaField").press("Alt+C") # does nothing
  
  # matching multiplefilefield as well
  #page.get_by_label("FileField").set_input_files("halalvn.jpg") 
  # will work if files don't exist
  page.get_by_label("MultipleFileField").set_input_files("a.test,b.test") 

'''
@pytest.mark.skip
def test_has_title(page: Page):
  
  page.goto("https://playwright.dev/")

  # Expect a title "to contain" a substring.
  expect(page).to_have_title(re.compile("Playwright"))

@pytest.mark.skip_browser("chromium") # skipped on firefox
def test_get_started_link(page: Page):
  page.goto("https://playwright.dev/")

  # Click the get started link.
  page.get_by_role("link", name="Get started").click()

  # Expects page to have a heading with the name of Installation.
  expect(page.get_by_role("heading", name="Installation")).to_be_visible()

def test_e2e(page: Page):
	homePage = HomePage(page)

	homePage.navigate()

	assert page.get_by_text("Hello, World!").inner_text() != "Hello World!"

@pytest.mark.only_browser("chromium") # Only run on chrome
def test_generated(page: Page):
  page.goto("http://localhost:8000/")
  #page.wait_for_selector("button", state="visible")
  #page.get_by_role("button", name="Reject additional cookies").click()
  page.get_by_role("link", name="Forms", exact=True).click()
  page.get_by_role("link", name="Autocomplete").click()
  page.get_by_label("G20 Countries").click()
  page.get_by_label("G20 Countries").fill("Russia")
  page.get_by_role("button", name="Continue").click()
  page.get_by_role("link", name="Kitchen sink").click()
  page.get_by_label("StringField").click()
  page.get_by_label("StringField").fill("fghfhdf")
  page.get_by_label("EmailField").click()
  page.get_by_label("EmailField").fill("the quick brown@hotmail.com")
  page.get_by_label("EmailField").fill("the quick brown")
  page.get_by_label("EmailField").press("Tab")
  page.get_by_text("Two").nth(2).click()
  page.get_by_text("Three").nth(1).click()
  page.get_by_role("button", name="SubmitField").click()
  page.go_back()
  # breakpoint();
  page.locator("li").filter(has_text="Forms").click()
  page.wait_for_selector("li a", state="visible")
  page.get_by_role("link", name="Home").click()
  page.get_by_role("link", name="Components").click()
  page.get_by_role("link", name="Fieldset").click()
  page.get_by_role("link", name="Styled as medium text").click()
'''