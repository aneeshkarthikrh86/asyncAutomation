class GameTesting:
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

            await play_btn.click()

            result = await self._detect_game_result(
                game_name,
                TOAST_ERROR,
                CLOSE_BTN,
                BACK_HOME_BTN
            )

            closed = await self._ensure_game_closed(
                LOGOUT_BTN, LOGIN_BTN, BACK_HOME_BTN, CLOSE_BTN
            )

            if not closed:
                print("⚠ UI broken. Restarting session...")
                await self._full_recovery(page_no)
                continue

            await self._return_to_page(page_no)

    # ------------------------------------------------------------------

    async def _detect_game_result(self, game_name, TOAST_ERROR, CLOSE_BTN, BACK_HOME_BTN):
        """
        Determines SUCCESS / FAIL using multi-stage checks
        """
        toast = self.page.locator(TOAST_ERROR)
        close_btn = self.page.locator(CLOSE_BTN)
        back_home = self.page.locator(BACK_HOME_BTN)

        # 🔹 Phase 1 – quick failure
        await self.page.wait_for_timeout(4000)
        if await toast.is_visible():
            print(f"❌ Fail (toast early): {game_name}")
            return "fail"

        # 🔹 Phase 2 – normal success
        if await close_btn.is_visible() or await back_home.is_visible():
            print(f"✅ Success: {game_name}")
            return "success"

        # 🔹 Phase 3 – slow loading
        print("⏳ Still loading… waiting extra 30s")
        await self.page.wait_for_timeout(30000)

        if await toast.is_visible():
            print(f"❌ Fail (toast late): {game_name}")
            return "fail"

        if await close_btn.is_visible() or await back_home.is_visible():
            print(f"✅ Success (late close): {game_name}")
            return "success"

        print(f"⚠ UI stuck: {game_name}")
        return "stuck"

    # ------------------------------------------------------------------

    async def _ensure_game_closed(self, LOGOUT_BTN, LOGIN_BTN, BACK_HOME_BTN, CLOSE_BTN):
        """
        Safely close game without blocking waits
        """
        for _ in range(5):
            if await self.page.locator(LOGOUT_BTN).count() > 0:
                return True

            if await self.page.locator(LOGIN_BTN).count() > 0:
                return True

            if await self.page.locator(CLOSE_BTN).count() > 0:
                await self.page.locator(CLOSE_BTN).click()
            elif await self.page.locator(BACK_HOME_BTN).count() > 0:
                await self.page.locator(BACK_HOME_BTN).click()

            await self.page.wait_for_timeout(2000)

        return False

    # ------------------------------------------------------------------

    async def _full_recovery(self, page_no):
        print("🔄 Hard recovery started...")

        await self.page.goto("https://member-trackaud.ibstest.site/en-au")
        await self.page.wait_for_load_state("networkidle")

        await self.page.click("//button[text()='Login']")
        await self.page.fill("//input[@placeholder='Enter Your Username']", "testacc")
        await self.page.fill("//input[@placeholder='Enter Your Password']", "qweqwe11")
        await self.page.click("//button[text()='Confirm']")
        await self.page.wait_for_timeout(3000)

        await self.page.click("//a[text()=' Slot']")
        await self.page.hover("//a[text()=' Home']")
        await self.page.wait_for_timeout(2000)

        PROVIDERS_LIST = (
            "xpath=//div[@class='mt-5 flex items-center slot_btn_container "
            "w-full overflow-auto light-scrollbar-h pb-[10px]']//button"
        )

        providers = self.page.locator(PROVIDERS_LIST)
        await providers.nth(self.provider_index).click()
        await self.page.wait_for_timeout(2000)

        await self._return_to_page(page_no)

    # ------------------------------------------------------------------

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
