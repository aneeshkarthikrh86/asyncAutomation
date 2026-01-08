from pages.game_testing import GameTesting

class PaginaionPage:
    def __init__(self, page, provider_index):
        self.page = page
        self.provider_index = provider_index  # ✅ store provider

    async def PaginationClicks(self):
        PROVIDERS_LIST = (
            "xpath=//div[@class='mt-5 flex items-center slot_btn_container "
            "w-full overflow-auto light-scrollbar-h pb-[10px]']//button"
        )

        PAGINATION_BUTTONS = (
            "xpath=//div[@class='p-holder admin-pagination']"
            "/button[not(contains(@class,'p-prev')) and not(contains(@class,'p-next'))]"
        )

        paginations = self.page.locator(PAGINATION_BUTTONS)
        await paginations.last.wait_for(state="visible", timeout=20000)
        total_pages = int(await paginations.last.inner_text())

        print(f"📄 Total Pages: {total_pages}")

        for j in range(1, total_pages + 1):
            print(f"\n📄 Page {j}")

            page_btn = self.page.locator(
                f"xpath=//div[@class='p-holder admin-pagination']"
                f"/button[normalize-space(text())='{j}']"
            )

            # Only scroll pagination if j > 1
            if j > 1:
                if not await page_btn.is_visible():
                    for _ in range(20):
                        paginations = self.page.locator(PAGINATION_BUTTONS)
                        count = await paginations.count()
                        if count == 0:
                            break

                        last_visible = paginations.nth(count - 1)
                        await last_visible.scroll_into_view_if_needed()
                        await last_visible.click()
                        await self.page.wait_for_timeout(2000)

                        if await page_btn.is_visible():
                            break

                await page_btn.click()

            # wait for page to load
            providers = self.page.locator(PROVIDERS_LIST)
            await providers.first.wait_for(state="visible", timeout=20000)
            await self.page.wait_for_timeout(2000)

            # test games on this page
            game_testing = GameTesting(self.page, self.provider_index)
            await game_testing.GameOpenClose(j)
