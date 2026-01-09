class GameTesting:
    
    def __init__(self, page, provider_index):
        self.page = page
        self.provider_index = provider_index
    #add therapy
    async def GameOpenClose(self, page_no):
        PLAY_BTN = "xpath=//button[normalize-space()='Play Now']"
        GAME_NAME_REL = (
            "xpath=ancestor::div[contains(@class,'game_btn_content')]"
            "//div[@class='game_btn_content_text']"
        )

        TOAST_ERROR = (
            "xpath=//div[contains(@class,'toast-message') "
            "and contains(text(),'Something went wrong')]"
        )

        BACK_HOME_BTN = "xpath=//button[text()='Back To Home']"
        CLOSE_BTN = "xpath=//div[@class='flex items-center']/button[@aria-label='Back']"

        LOGOUT_BTN = "xpath=//div[@class='flex items-center']/button[text()='Logout']"
        LOGIN_BTN = "xpath=//button[@class='topbar_btn_2 hidden sm:block' and text()='Login']"

        await self.page.locator(PLAY_BTN).first.wait_for(state="visible", timeout=20000)
        total_games = await self.page.locator(PLAY_BTN).count()
        print(f"🎮 Games on page {page_no}: {total_games}")

        for i in range(total_games):
            play_btn = self.page.locator(PLAY_BTN).nth(i)
            await play_btn.scroll_into_view_if_needed()

            name_el = play_btn.locator(GAME_NAME_REL)
            await name_el.wait_for(state="visible", timeout=10000)
            game_name = await name_el.inner_text()

            # print(f"▶ Opening: {game_name}")
            await play_btn.click()

            toast_found = False
            
            for _ in range(6):  # 25 × 2s = 50 seconds
                if await self.page.locator(TOAST_ERROR).is_visible():  # 2 seconds
                    toast_found = True
                    print("❌ Toast appeared")
                    break
                await self.page.wait_for_timeout(2000)
                    
            if toast_found:
                print(f"Failed: {game_name}")
                await self.page.wait_for_timeout(1000)
                await self.page.locator(BACK_HOME_BTN).click()
                await self.page.wait_for_timeout(1000)
                        
            else:
                print(f"Success: {game_name}")
                await self.page.wait_for_timeout(5000)
                await self.page.locator(CLOSE_BTN).click()
                await self.page.wait_for_timeout(1000)
                    
            for _ in range(10):  # 50 seconds
                if await self.page.locator(LOGOUT_BTN).is_visible():
                    # print("✅ YES (Logout button seen)")
                    break
                await self.page.wait_for_timeout(2000)        
                
                



    async def _full_recovery(self, page_no):
        print("🔄 Hard recovery started...")

        await self.page.goto("https://member-trackaud.ibstest.site/en-au")
        await self.page.wait_for_load_state("networkidle")

        # LOGIN AGAIN
        await self.page.click("//div[@style='max-height: var(--window-height);']//button[@class='close_btn']/img")
        await self.page.click("//button[text()='Login']")
        await self.page.fill("//input[@placeholder='Enter Your Username']", "testacc")
        await self.page.fill("//input[@placeholder='Enter Your Password']", "qweqwe11")
        await self.page.click("//button[text()='Confirm']")
        await self.page.click("//div[@style='max-height: var(--window-height);']//button[@class='close_btn']/img")
        await self.page.click("//button[@class='mission_daily_close_btn']/img")
        await self.page.wait_for_timeout(3000)

        # GO TO SLOT
        await self.page.click("//a[text()=' Slot']")
        await self.page.hover("//a[text()=' Home']")
        await self.page.wait_for_timeout(2000)

        # 🔑 RESTORE PREVIOUS PROVIDER
        PROVIDERS_LIST = (
            "xpath=//div[@class='mt-5 flex items-center slot_btn_container "
            "w-full overflow-auto light-scrollbar-h pb-[10px]']//button"
        )

        providers = self.page.locator(PROVIDERS_LIST)
        provider_btn = providers.nth(self.provider_index)

        await provider_btn.scroll_into_view_if_needed()
        await provider_btn.click()
        await self.page.wait_for_timeout(2000)

        print(f"✅ Restored provider index {self.provider_index}")

        # 🔑 RESTORE PAGE
        await self._return_to_page(page_no)

