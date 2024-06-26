from playwright.sync_api import expect

from pages.page_objects.main_page import MainPage


def test_main_banner(main_page: MainPage) -> None:
    expected_banner = 'AI and Data Solutions built on a strong Python heritage'

    main_page.load_and_accept_cookies()

    expect(main_page.banner_title).to_contain_text(expected_banner)
