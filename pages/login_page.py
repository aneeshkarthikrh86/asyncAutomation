class LoginPage:
    def __init__(self, page):
        self.page = page

    async def load(self):
        await self.page.goto("https://www.winx8.vip/en-th")

    async def ClosePopus(self):
        try:
            ClosePopup1 = ("//div[@style='max-height: var(--window-height);']//button[@class='close_btn']/img")
            await self.page.locator(ClosePopup1).wait_for(state="visible", timeout=20000)
            await self.page.locator(ClosePopup1).click()
            await self.page.wait_for_timeout(2000)
        except:
            pass
        
    async def ClosePopus1(self):
        ClosePopup2 = ("//button[@class='mission_daily_close_btn']/img")
        try:
            popup = self.page.locator(ClosePopup2)

            # Check visibility instead of waiting blindly
            if await popup.is_visible(timeout=3000):
                await popup.click()
                await self.page.wait_for_timeout(1000)
            else:
                # Fallback: press Escape
                await self.page.keyboard.press("Escape")
                await self.page.wait_for_timeout(500)

        except Exception as e:
            # Final safety fallback
            await self.page.keyboard.press("Escape")
            
         
    async def closepopuplw(self):
        try:
            ClosePopuplw = ("//div[@class='fs-overlay show rewards-modal-wrapper']/div/button/i")
            await self.page.locator(ClosePopuplw).wait_for(state="visible", timeout=20000)
            await self.page.locator(ClosePopuplw).click()
            await self.page.wait_for_timeout(2000)
            print("closed after restart")
        except:
            print("Not seen after restart")  

    async def login(self, username, password):
        
        await self.page.wait_for_timeout(2000)
        await self.page.click("//button[@class='topbar_btn_1 hidden md:block' and @aria-label ='Login']")
        await self.page.fill("//div[@class='relative mt-4']/input[@placeholder='Enter Your Username']", username)
        await self.page.fill("//input[@placeholder='Password']", password)
        await self.page.click("//div[@class='relative flex justify-center']/button[@aria-label='Login']")
        await self.page.wait_for_timeout(2000)
    async def is_logged_in(self):
        return await self.page.is_visible("//div[@class='flex items-center']/button[@aria-label='Logout']")
    
    async def click_if_present(self, locator):
        if await self.page.is_visible(locator):
            await self.page.click(locator)
            

            

