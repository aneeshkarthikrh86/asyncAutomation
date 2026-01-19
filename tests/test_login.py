import pytest
from playwright.async_api import async_playwright
from pages.login_page import LoginPage
from pages.slot_pages import SlotPage
# from pages.LiveCasino_pages import LiveCasinoPage
# from pages.providers_page import ProvidersPage

@pytest.mark.asyncio
async def test_login():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, args=["--start-maximized"])
        page = await browser.new_page(no_viewport=True)

        login_page = LoginPage(page)
        await login_page.load()
<<<<<<< HEAD
        await login_page.ClosePopus()
        await login_page.ClosePopus1()
        await login_page.login("testacc", "qweqwe11")
        await login_page.closepopuplw()
        await login_page.ClosePopus()
        await login_page.ClosePopus1()
=======
        # await login_page.ClosePopus()
        # await login_page.ClosePopus1()
        await login_page.login("testacc", "qweqwe11")
        # await login_page.ClosePopus()
        # await login_page.ClosePopus1()
>>>>>>> 9f2af534ff4c7514e7a7139b0eecaed6ca6d9274
        assert await login_page.is_logged_in()
        print("Login successful")

        slot_page = SlotPage(page)
        await slot_page.slot_home()
        
        # LiveCasino_pages = LiveCasinoPage(page)
        # await LiveCasino_pages.LiveCasino_home()

        # providers_page = ProvidersPage(page)
        # await providers_page.providersnavigations()

        await browser.close()
