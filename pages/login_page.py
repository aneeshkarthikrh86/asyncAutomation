class LoginPage:
    def __init__(self, page):
        self.page = page

    async def load(self):
        await self.page.goto("https://www.npr8.com/en-np")

    async def ClosePopus(self):
        try:
            ClosePopup1 = ("//div[@style='max-height: var(--window-height);']//button[@class='close_btn']/img")
            await self.page.locator(ClosePopup1).wait_for(state="visible", timeout=20000)
            await self.page.locator(ClosePopup1).click()
            await self.page.wait_for_timeout(2000)
        except:
            pass
        
    async def ClosePopus1(self):
        try:
            ClosePopup2 = ("//button[@class='mission_daily_close_btn']/img")
            await self.page.locator(ClosePopup2).wait_for(state="visible", timeout=20000)
            await self.page.locator(ClosePopup2).click()
            await self.page.wait_for_timeout(2000)
        except:
            pass   

    async def login(self, username, password):
        await self.page.wait_for_timeout(2000)
        await self.page.click("//button[@class='topbar_btn_1 hidden md:block' and text()='Login']")
        await self.page.fill("//input[@placeholder='Username']", username)
        await self.page.fill("//input[@placeholder='Password']", password)
        await self.page.click("//div[@class='relative mt-8']/button[text()=' Login']")
        await self.page.wait_for_timeout(2000)
    async def is_logged_in(self):
        return await self.page.is_visible("//div[@class='wallet-container-desktop']/button[text()='Logout']")
    
    async def click_if_present(self, locator):
        if await self.page.is_visible(locator):
            await self.page.click(locator)
            

            

