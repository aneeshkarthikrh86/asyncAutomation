class LoginPage:
    def __init__(self, page):
        self.page = page

    async def load(self):
        await self.page.goto("https://member-trackaud.ibstest.site/en-au")

    async def login(self, username, password):
        await self.page.click("//div[@style='max-height: var(--window-height);']//button[@class='close_btn']/img")
        await self.page.click("//button[@class='topbar_btn_2 hidden sm:block' and text()='Login']")
        await self.page.fill("//input[@placeholder='Enter Your Username']", username)
        await self.page.fill("//input[@placeholder='Enter Your Password']", password)
        await self.page.click("//div[@class='grid gap-4 pt-4']//button[text()='Confirm']")
        
        await self.page.click("//div[@style='max-height: var(--window-height);']//button[@class='close_btn']/img")
        await self.page.click("//button[@class='mission_daily_close_btn']/img")
        
    async def is_logged_in(self):
        return await self.page.is_visible("//div[@class='flex items-center']/button[text()='Logout']")
    
    async def click_if_present(self, locator):
        if await self.page.is_visible(locator):
            await self.page.click(locator)
            

            

