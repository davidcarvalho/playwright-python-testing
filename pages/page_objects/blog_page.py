from playwright.sync_api import Locator, Page
from pages.locators.blog_page_locators import BlogPageLocators
from pages.page_objects.base_page import BasePage


class BlogPage(BasePage):
    URL = '/blog'

    def __init__(self, page: Page) -> None:
        super(BlogPage, self).__init__(page)
        self.get__posts = page.locator(BlogPageLocators.POSTS)

    def get_link(self, link_text: str) -> Locator:
        return self.page.get_by_role('link', name=link_text)

