# trackaudstaging/pages/providers_page.py
from pages.pagination_page import PaginaionPage
class ProvidersPage:
    def __init__(self, page):
        self.page = page
        self.current_provider_index = None

    async def providersnavigations(self):
        PROVIDERS_LIST = (
            "xpath=//div[@class='mt-5 flex items-center slot_btn_container w-full "
            "overflow-auto light-scrollbar-h pb-[10px]']//button"
        )

        providers = self.page.locator(PROVIDERS_LIST)
        total = await providers.count()

        for i in range(1, total):
            self.current_provider_index = i   # ✅ SAVE PROVIDER INDEX

            provider_btn = providers.nth(i)
            await provider_btn.scroll_into_view_if_needed()
            provider_name = await provider_btn.inner_text()

            print(f"Clicking provider {i}/{total}: {provider_name}")
            await provider_btn.click()

            pagination_page = PaginaionPage(self.page, i)
            await pagination_page.PaginationClicks()
