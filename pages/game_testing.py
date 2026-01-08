class GameTesting:
    #add therapy
    def __init__(self, page, provider_index):
        self.page = page
        self.provider_index = provider_index
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

            print(f"▶ Opening: {game_name}")
            await play_btn.click()

            try:
                await self.page.locator(TOAST_ERROR).wait_for(state="visible", timeout=4000)
                print(f"❌ Fail: {game_name}")
            except:
                print(f"✅ Success: {game_name}")

            # ✅ ENSURE GAME CLOSED
            closed = await self._ensure_game_closed(LOGOUT_BTN, LOGIN_BTN, BACK_HOME_BTN, CLOSE_BTN)

            # ❌ HARD RECOVERY if UI is broken
            if not closed:
                print("⚠ UI broken. Restarting session...")
                await self._full_recovery(page_no)
                continue

            # ✅ RETURN TO SAME PAGE
            await self._return_to_page(page_no)

    async def _ensure_game_closed(self, LOGOUT_BTN, LOGIN_BTN, BACK_HOME_BTN, CLOSE_BTN):
        """
        Try to close game & verify session state safely
        """
        for _ in range(5):
            # ✅ use count() – no waiting
            if await self.page.locator(LOGOUT_BTN).count() > 0:
                return True

            if await self.page.locator(LOGIN_BTN).count() > 0:
                return True

            if await self.page.locator(CLOSE_BTN).count() > 0:
                await self.page.locator(CLOSE_BTN).click()
            elif await self.page.locator(BACK_HOME_BTN).count() > 0:
                await self.page.locator(BACK_HOME_BTN).click()

            await self.page.wait_for_timeout(2000)

        return False  # UI stuck

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


    async def _return_to_page(self, page_no):
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
