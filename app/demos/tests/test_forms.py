import pytest
from playwright.sync_api import Page, expect
from flask import url_for, current_app
import re


# The live_server fixture will start a test application using the client defined in app/conftest.py
# This ensures the tests run inside an application context and url_for will return URLs for the test client.
@pytest.mark.usefixtures("live_server")
# Tests marked with 'playwright' can be exclusively executed by running `pytest -m playwright``
# or omitted using `pytest -m "not playwright"` 
@pytest.mark.playwright
class TestForms:
    @pytest.fixture(scope="function", autouse=True)
    def before_each(self, page: Page):

        # Go to the starting url before each test.
        forms_url = url_for("demos.forms", _external=True)  # PlayWright expects an external URL
        page.goto(forms_url)
        yield
        page.context.clear_cookies()

    def test_has_title(self, page: Page):
        # Expect a title "to contain" a substring.
        expect(page).to_have_title(re.compile(current_app.config["SERVICE_NAME"]))

    def test_autofill_form(self, page: Page):

        page.get_by_role("link", name="Autocomplete").click()

        page.get_by_label("G20 Countries").fill("Brazil")

        page.get_by_role("button", name="Continue").click()

        expect(page.get_by_text("Demo form successfully"))

    def test_bank_statement_form(self, page: Page):

        page.get_by_role("link", name="Bank details").click()

        page.get_by_label("Name on the account").fill("John Doe")
        page.get_by_label("Sort code").fill("123456")
        page.get_by_label("Account number").fill("12345678")
        page.get_by_label("Building society roll number").fill("1234")

        page.get_by_role("button", name="Continue").click()
        expect(page.get_by_text("Demo form successfully"))

    def test_bank_statement_form_no_input(self, page: Page):

        page.get_by_role("link", name="Bank details").click()
        page.get_by_role("button", name="Continue").click()

        expect(page.get_by_text("Enter an account number"))
        expect(page.get_by_text("Enter a sort code"))
        expect(page.get_by_text("Enter the name on the account"))
