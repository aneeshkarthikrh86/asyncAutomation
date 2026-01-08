import pytest
from playwright.async_api import async_playwright
from pages.login_page import LoginPage
from pages.slot_pages import SlotPage
from pages.providers_page import ProvidersPage

@pytest.mark.asyncio
async def test_login():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, args=["--start-maximized"])
        page = await browser.new_page(no_viewport=True)

        login_page = LoginPage(page)
        await login_page.load()
        await login_page.login("testacc", "qweqwe11")

        assert await login_page.is_logged_in()
        print("Login successful")

        slot_page = SlotPage(page)
        await slot_page.slot_home()

        # providers_page = ProvidersPage(page)
        # await providers_page.providersnavigations()

        await browser.close()
