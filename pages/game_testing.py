from pages.Screen_Shots import ScreenShots   # adjust import path

class GameTesting:
    def __init__(self, page, provider_index):
        self.page = page
        self.provider_index = provider_index
        self.screenshot = ScreenShots(page)   # ✅ ADD THIS
    #add therapy
    async def GameOpenClose(self, page_no):
        PLAY_BTN = "xpath=//button[normalize-space()='Play Now']"
        GAME_NAME_REL = (
            "xpath=ancestor::div[contains(@class,'game_btn_content')]"
            "//div[@class='game_btn_content_text']"
        )

        TOAST_ERROR = "xpath=//div[contains(@class,'toast-message') and contains(text(),'Something went wrong')]"
        DEPOSIT_BTN = "xpath=//a[text()='Deposit']"

        BACK_HOME_BTN = "xpath=//button[text()='Back To Home']"
        CLOSE_BTN = "xpath=//div[@class='flex items-center']/button[@aria-label='Back']"
        LOGOUT_BTN = "xpath=//div[@class='flex items-center']/button[@aria-label='Logout']"

        await self.page.locator(PLAY_BTN).first.wait_for(state="visible", timeout=20000)
        total_games = await self.page.locator(PLAY_BTN).count()
        print(f"🎮 Games on page {page_no}: {total_games}")
        provider_name = f"Provider{self.provider_index}"
        for i in range(total_games):
            self.last_game_index = i
            play_btn = self.page.locator(PLAY_BTN).nth(i)

            name_el = play_btn.locator(GAME_NAME_REL)
            await name_el.wait_for(state="visible", timeout=10000)
            game_name = await name_el.inner_text()

            # print(f"▶ Opening: {game_name}")
            # Try normal click first
            try:
                play_btn = self.page.locator(PLAY_BTN).nth(i)
                await play_btn.wait_for(state="visible", timeout=10000)
                await play_btn.evaluate("el => el.click()")
            except Exception as e:
                print(f"❌ Failed to click on game: {game_name} | Reason: {e}")
                await self.screenshot.take_screenshot(
                    name=f"CLICK_FAIL_{provider_name}_P{page_no}_{game_name}"
                )
                continue   # ✅ IMPORTANT: move to next game          

            # --------------------------------------------------
            # 🔑 WAIT FOR RESULT: TOAST OR DEPOSIT
            # --------------------------------------------------
            result = None

            for _ in range(110):  # 60 × 1s = 60 seconds
                if await self.page.locator(TOAST_ERROR).is_visible():
                    result = "fail"
                    break

                if await self.page.locator(DEPOSIT_BTN).is_visible():
                    result = "success"
                    break

                await self.page.wait_for_timeout(1000)

            # --------------------------------------------------
            # 🔑 HANDLE RESULT
            # --------------------------------------------------
            if result == "fail":
                print(f"❌ Failed: {game_name}")
                action_btn = BACK_HOME_BTN

            elif result == "success":
                await self.page.wait_for_timeout(6000)
                print(f"✅ Success: {game_name}")
                action_btn = CLOSE_BTN

            else:
                print(f"⚠ Stuck game: {game_name}")
                action_btn = BACK_HOME_BTN


            # 🔑 COMMON EXIT + LOGOUT CHECK FLOW
            try:
                # 1️⃣ First click (Back Home / Close)
                await self.page.locator(action_btn).wait_for(state="visible", timeout=8000)
                await self.page.locator(action_btn).click()
                await self.page.wait_for_timeout(3000)

                # 2️⃣ If Logout visible → next game
                if await self.page.locator(LOGOUT_BTN).is_visible():
                    # print("✅ Logout visible → proceeding next game")
                    continue

                # 3️⃣ Retry click if Logout not visible
                print("⚠ Logout not visible → retrying exit click")
                
                # 4️⃣ Wait for Logout
                await self.page.locator(LOGOUT_BTN).wait_for(state="visible", timeout=10000)
                # print("✅ Logout appeared after retry → proceeding")

            except:
                # print("❌ Exit failed / Logout not visible → restarting flow")
                print(f"❌ Still logout btn not seen. on game: {game_name} | Reason: {e}")
                await self.screenshot.take_screenshot(name=f"CLICK_FAIL_{provider_name}_P{page_no}_{game_name}")
                await self._full_recovery(page_no)
                continue
                

                    
            # --------------------------------------------------
            # 🔑 ENSURE WE ARE BACK (LOGOUT VISIBLE)
            # --------------------------------------------------
            
            # --------------------------------------------------
            # 🔑 RETURN TO SAME PAGE
            # --------------------------------------------------
            if page_no>1:
                await self._return_to_page(page_no)

        await self.page.wait_for_timeout(2000)
                        
    # async def logoutvisibleotnot(self, LOGOUT_BTN, BACK_HOME_BTN, CLOSE_BTN, page_no):            
    #     # Wait until we are really back (Logout visible)
    #     for _ in range(20):  # 10 × 2s = 20s
    #         if await self.page.locator(LOGOUT_BTN).is_visible():
    #             break

    #         if await self.page.locator(BACK_HOME_BTN).is_visible():
    #             print("hi7")
    #             await self.page.locator(BACK_HOME_BTN).click()
    #         elif await self.page.locator(CLOSE_BTN).is_visible():
    #             print("hi6")
    #             await self.page.locator(CLOSE_BTN).click()

    #         await self.page.wait_for_timeout(2000)  
    #         print("hi8")
    #     # 🔑 THIS IS THE LINK YOU ASKED FOR
    #     await self._return_to_page(page_no)  
                
    async def _return_to_page(self, page_no):
        await self.page.wait_for_timeout(2000)
        PLAY_BTN = "xpath=//button[normalize-space()='Play Now']"
        PAGINATION_BUTTONS = (
            "xpath=//div[@class='p-holder admin-pagination']"
            "/button[not(contains(@class,'p-prev')) and not(contains(@class,'p-next'))]"
        )

        if page_no == 1:
            await self.page.locator(PLAY_BTN).first.wait_for(state="visible", timeout=20000)
            return

        paginations = self.page.locator(PAGINATION_BUTTONS)
        await paginations.first.wait_for(state="visible", timeout=20000)

        target_btn = self.page.locator(
            f"xpath=//div[@class='p-holder admin-pagination']"
            f"/button[normalize-space(text())='{page_no}']"
        )

        if await target_btn.count() > 0:
            await target_btn.click()
            await self.page.locator(PLAY_BTN).first.wait_for(state="visible", timeout=20000)
            return

        for _ in range(30):
            count = await paginations.count()
            if count < 2:
                break

            await paginations.nth(count - 2).click()
            await self.page.wait_for_timeout(2000)

            if await target_btn.count() > 0:
                await target_btn.click()
                await self.page.locator(PLAY_BTN).first.wait_for(state="visible", timeout=20000)
                return 
                
        await self.page.wait_for_timeout(2000)



    async def _full_recovery(self, page_no):
        print("🔄 Restarting browser state...")

        # CLEAR CACHE
        await self.page.context.clear_cookies()

        # RELAUNCH URL
        await self.page.goto("https://www.winx8.vip/en-th")
        await self.page.wait_for_load_state("networkidle")
        
        try:
            ClosePopup2 = ("//button[@class='mission_daily_close_btn']/img")
            await self.page.locator(ClosePopup2).wait_for(state="visible", timeout=20000)
            await self.page.locator(ClosePopup2).click()
            await self.page.wait_for_timeout(2000)
            print("closed after restart")
        except:
            print("Not seen after restart")  

        # LOGIN
        try:
            ClosePopup1 = ("//div[@style='max-height: var(--window-height);']//button[@class='close_btn']/img")
            await self.page.locator(ClosePopup1).wait_for(state="visible", timeout=4000)
            await self.page.locator(ClosePopup1).click()
            await self.page.wait_for_timeout(2000)
            print("closed after restart")
        except:
            print("Not seen after restart")

        await self.page.wait_for_timeout(2000)
        await self.page.click("//button[@class='topbar_btn_1 hidden md:block' and @aria-label ='Login']")
        await self.page.fill("//div[@class='relative mt-4']/input[@placeholder='Enter Your Username']", "testacc")
        await self.page.fill("//input[@placeholder='Password']", "qweqwe11")
        await self.page.click("//div[@class='relative flex justify-center']/button[@aria-label='Login']")
        await self.page.wait_for_timeout(2000)

        try:
            ClosePopuplw = ("//div[@class='fs-overlay show rewards-modal-wrapper']/div/button/i")
            await self.page.locator(ClosePopuplw).wait_for(state="visible", timeout=20000)
            await self.page.locator(ClosePopuplw).click()
            await self.page.wait_for_timeout(2000)
            print("closed after restart")
        except:
            print("Not seen after restart") 

        try:
            ClosePopup1 = ("//div[@style='max-height: var(--window-height);']//button[@class='close_btn']/img")
            await self.page.locator(ClosePopup1).wait_for(state="visible", timeout=4000)
            await self.page.locator(ClosePopup1).click()
            await self.page.wait_for_timeout(2000)
            print("closed after restart")
        except:
            print("Not seen after restart")
        
        try:
            ClosePopup2 = ("//button[@class='mission_daily_close_btn']/img")
            await self.page.locator(ClosePopup2).wait_for(state="visible", timeout=20000)
            await self.page.locator(ClosePopup2).click()
            await self.page.wait_for_timeout(2000)
            print("closed after restart")
        except:
            print("Not seen after restart")
            pass  
        
        # SLOT
        await self.page.click("//a[text()=' Slot']")
        await self.page.hover("//a[text()=' Home']")
        await self.page.wait_for_timeout(2000)

        # PREVIOUS PROVIDER
        PROVIDERS_LIST = (
            "xpath=//div[@class='mt-5 flex items-center slot_btn_container w-full "
            "overflow-auto light-scrollbar-h pb-[10px]']//button"
        )
        provider = self.page.locator(PROVIDERS_LIST).nth(self.provider_index)
        await provider.scroll_into_view_if_needed()
        await provider.click()
        await self.page.wait_for_timeout(2000)

        # PREVIOUS PAGE
        await self._return_to_page(page_no)

        print(f"✅ Restored: Provider={self.provider_index}, Page={page_no}, Game={self.last_game_index + 1}")


