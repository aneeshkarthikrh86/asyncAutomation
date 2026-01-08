from pages.providers_page import ProvidersPage
class SlotPage:
    def __init__(self, page):
        self.page = page
        
    async def slot_home(self):
        await self.page.click("//a[text()=' Slot']")
        await self.page.hover("//a[text()=' Home']")
        providers_page = ProvidersPage(self.page)
        await providers_page.providersnavigations()