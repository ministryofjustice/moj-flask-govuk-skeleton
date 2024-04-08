import re, pytest

from playwright.sync_api import Page, expect

def test_assertions(page: Page):
	page.goto("http://localhost:8000/")
	expect(page).to_have_url("http://localhost:8000/")
	expect(page).to_have_title("SERVICE_NAME – GOV.UK")
	expect(page.get_by_text("Hello, World!")).to_be_attached()
	expect(page.get_by_text("Demos")).to_be_visible()
	expect(page.get_by_text("Demos")).to_have_class("govuk-heading-m")
	# CSS has to be set rather than inherited
	expect(page.get_by_text("Demos")).to_have_css("display", "block")
	expect(page.locator(".govuk-phase-banner__content__tag")).to_contain_text("_PHASE")
	expect(page.locator(".govuk-phase-banner__content__tag")).to_have_text("SERVICE_PHASE")
	expect(page.get_by_text("Hello, World!")).to_be_in_viewport()
	expect(page.locator(".govuk-footer__meta path")).to_be_empty()
	expect(page.get_by_text("feedback")).to_have_attribute("href", "mailto:CONTACT_EMAIL")
		

  # Hidden won't work for gov uk hidden, probably will for css display:none/visibility:hidden
	# expect(page.locator(".govuk-skip-link")).to_be_hidden()
