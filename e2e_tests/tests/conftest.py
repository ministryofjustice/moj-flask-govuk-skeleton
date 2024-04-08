import pytest
from playwright.sync_api import Page, BrowserType, Playwright
from typing import Dict
from datetime import datetime


@pytest.fixture(autouse=True)
def setup_and_teardown(page: Page):
	# before each test
	page.set_default_timeout(2000) # Note, this is too fast for webkit
	yield page
	# after each test
	#page.goto("about:blank") # some useful teardown rather than this

# Using the name "browser_context_args" makes pytest automatically 
# call this and feed into the context method
@pytest.fixture(scope="session")
def browser_context_args(browser_context_args, playwright):
    # See device emulations: https://github.com/microsoft/playwright/blob/main/packages/playwright-core/src/server/deviceDescriptorsSource.json
    iphone_11 = playwright.devices['iPhone 11 Pro']
    return {
        **browser_context_args,
        **iphone_11,
        "ignore_https_errors": True,
        "viewport": { # override viewport from iphone
            "width": 1920, 
            "height": 1080,
        },
         #or can do via the CLI --device="iPhone 11 Pro"
    }

# Using the name "context" makes pytest cli automatically call this
@pytest.fixture(scope="session")
def context(
    browser_type: BrowserType,
    browser_type_launch_args: Dict,
    browser_context_args: Dict
):
    # for some reason iphone11 subdict passes this but he doesn't like it
    if 'default_browser_type' in browser_context_args:
        del browser_context_args['default_browser_type']

    # Note, first time will be incognito, after that it will use the data
    # folder to get browser cache/cookies etc. So cookie message not there
    context = browser_type.launch_persistent_context("./browser_data", **{
        **browser_type_launch_args,
        **browser_context_args,
        "locale": "en-UK",
    })
    context.tracing.start(screenshots=True, snapshots=True, sources=True)
    yield context
    context.tracing.stop(path=f'./debug/traces/trace{str(datetime.now()).replace(" ","_")}.zip')
    context.close()