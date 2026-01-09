class LiveCasinoPage:
    def __init__(self, page):
        self.page = page
        
    async def KiveCasino_home(self):
        await self.page.click("//a[text()='  Live Casino']")
        await self.page.hover("//a[text()=' Home']")
        
    async def GameOpenclose(self):
        GamesNames_ElemeCASINOnt = "//div[@class='flex items-center overflow-auto py-[50px] none-scrollbar']/button//div[@class='casino_label']/div"
        Games_Element = "//div[@class='flex items-center overflow-auto py-[50px] none-scrollbar']/button/div//img[@class='logo not_allow_select_drag']"
        Games_Element_click = "//button[@class='category_live_play_btn']/div"
        
        LOGOUT_BTN = "xpath=//div[@class='flex items-center']/button[text()='Logout']"
        LOGIN_BTN = "xpath=//button[@class='topbar_btn_2 hidden sm:block' and text()='Login']"
        
        BACK_HOME_BTN = "xpath=//button[text()='Back To Home']"
        CLOSE_BTN = "xpath=//div[@class='flex items-center']/button[@aria-label='Back']"
        
        TOAST_ERROR = (
            "xpath=//div[contains(@class,'toast-message') "
            "and contains(text(),'Something went wrong')]"
        )
        
        await self.page.locator(Games_Element).first.wait_for(state="visible", timeout=20000)
        total_games = await self.page.locator(Games_Element).count()
        print(f"Total Games Present {total_games}")
        
        for k in range(total_games):
            Game_PLAY = self.page.locator(Games_Element).nth(k)
            gAME_Name = Game_PLAY.locator(GamesNames_ElemeCASINOnt)
            GameClick = Game_PLAY.locator(Games_Element_click)
            await gAME_Name.wait_for(state="visible", timeout=10000)
            game_name = await gAME_Name.inner_text()
            
            await Game_PLAY.click()
            
            await GameClick.click()
            
            toast_found = False
            
            for _ in range(25):  # 25 × 2s = 50 seconds
                if await self.page.locator(TOAST_ERROR).is_visible():  # 2 seconds
                    toast_found = True
                    print("❌ Toast appeared")
                    break
                await self.page.wait_for_timeout(2000)
                    
            if toast_found:
                print(f"Failed: {game_name}")
                for _ in range(5):
                    if await self.page.locator(BACK_HOME_BTN).is_visible():
                        await self.page.locator(BACK_HOME_BTN).click()
                        break
                    await self.page.wait_for_timeout(1000)
                        
            else:
                print(f"Success: {game_name}")
                for _ in range(5):
                    if await self.page.locator(CLOSE_BTN).is_visible():
                        await self.page.locator(CLOSE_BTN).click()
                        break
                    await self.page.wait_for_timeout(1000)
                    
            for _ in range(25):  # 50 seconds
                if await self.page.locator(LOGOUT_BTN).is_visible():
                    print("✅ YES (Logout button seen)")
                    break
                await self.page.wait_for_timeout(2000)        
            
            
            
        
        
        