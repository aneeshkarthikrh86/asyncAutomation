from playwright.async_api import Page
from datetime import datetime

class ScreenShots:
    def __init__(self, page: Page):
        self.page = page

    async def take_screenshot(self, name="screenshot"):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{name}_{timestamp}.png"
        await self.page.screenshot(path=filename, full_page=True)
        print(f"📸 Screenshot saved: {filename}")
