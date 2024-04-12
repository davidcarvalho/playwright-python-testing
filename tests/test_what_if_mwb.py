import json
from time import sleep
from playwright.sync_api import Playwright


def test_page(playwright: Playwright) -> None:
    base_url = 'http://azenpdactdb023.dev.corp.local:7011/jda/shell/'
    user = "System"
    password = "Password2@"
    instance = []
    # instance = ['SCPO Instance','BY_MP']
    wb = "DSWB"
    search = 'ACT_ALL-SKUS (P)'
    product = "AC-FG-002"
    location = 'AC_CDC01'
    customer = 'AC_CUSTOMER'
    measure = "IndDmd"
    column = 'Q3-2018'
    change_value = 100

    browser = playwright.chromium.launch(headless=False, args=["--start-maximized"])
    context = browser.new_context(no_viewport=True, record_video_dir="videos/")
    page = context.new_page()
    page.goto(base_url)
    page.get_by_placeholder("Username").click()
    page.get_by_placeholder("Username").fill(user)
    page.get_by_placeholder("Username").press("Tab")
    page.get_by_placeholder("Password").fill(password)
    page.get_by_placeholder("Password").click()
    page.get_by_placeholder("Username").click()

    page.get_by_text("Sign in").click()
    if len(instance) > 0:
        page.get_by_title("Instance").click()
        page.locator("[id=\"_appInstances_\"]").select_option("SCPO Instance")
        page.locator("#InstanceApproach_instances").select_option("BY_MP")
        page.locator("[id=\"_directoryInput\"]").click()
    page.locator("[id=\"_directoryInput\"]").type(wb)
    sleep(3)
    page.get_by_text(wb, exact=True).click()
    sleep(5)
    page.frame_locator("iframe[name=\"appFrame\"]").get_by_text("Live", exact=True).click()
    page.frame_locator("iframe[name=\"appFrame\"]").locator("#Live_checkbox").uncheck()
    page.frame_locator("iframe[name=\"appFrame\"]").get_by_text("TestAutomationParent").click()
    page.frame_locator("iframe[name=\"appFrame\"]").get_by_role("gridcell", name="TestAutomationParent").locator(
        "div").nth(2).click()
    page.frame_locator("iframe[name=\"appFrame\"]").get_by_text("TestAutomationChild").click()
    page.frame_locator("iframe[name=\"appFrame\"]").locator("#TestAutomationChild_checkbox").check()
    page.frame_locator("iframe[name=\"appFrame\"]").get_by_role("button", name="Done").click()

    sleep(10)
    page.frame_locator("iframe[name=\"appFrame\"]").locator("#search_content").click(click_count=3)
    sleep(2)
    page.frame_locator("iframe[name=\"appFrame\"]").get_by_role("link", name="×").click()
    sleep(2)
    page.frame_locator("iframe[name=\"appFrame\"]").locator("#search_content").type(search)
    page.frame_locator("iframe[name=\"appFrame\"]").get_by_role("link", name=search).click()
    page.frame_locator("iframe[name=\"appFrame\"]").locator("#searchGoBtn").click()
    sleep(1)

    elem = page.frame_locator("iframe[name=\"appFrame\"]").get_by_role("link", name="Resynchronize")
    if elem.is_visible():
        elem.click()
        elem.is_hidden(timeout=50000)

    # member filters
    #
    page.frame_locator("iframe[name=\"appFrame\"]").locator('(//div[@class="dhx_ss_center_scroll"])[1]').click(
        button="right")
    sleep(2)
    show_member = page.frame_locator("iframe[name=\"appFrame\"]").get_by_text('Show Member Filters')
    for i in range(3):
        if show_member.is_hidden():
            page.frame_locator("iframe[name=\"appFrame\"]").locator('(//div[@class="dhx_ss_center_scroll"])[1]').click()
            page.frame_locator("iframe[name=\"appFrame\"]").locator('(//div[@class="dhx_ss_center_scroll"])[1]').click(
                button="right")
            sleep(2)
    show_member.click()
    sleep(2)

    # filter product
    page.frame_locator("iframe[name=\"appFrame\"]").locator('button[id$=\'PRODUCT\']').click()
    page.frame_locator("iframe[name=\"appFrame\"]").locator('input[type="radio"][value ="PRODUCT"]').click()
    page.frame_locator("iframe[name=\"appFrame\"]").get_by_placeholder("Search text").type(product)
    sleep(2)
    # page.frame_locator("iframe[name=\"appFrame\"]").locator("//span[contains(text(),"+item+")]").click()
    page.frame_locator("iframe[name=\"appFrame\"]").locator("div[id *= '" + product + "'] > span").click()
    sleep(2)
    page.frame_locator("iframe[name=\"appFrame\"]").locator('//button[@aria-label="move selected right"]').click()

    # filter location
    page.frame_locator("iframe[name=\"appFrame\"]").locator('button[id$=\'SITE\']').click()
    page.frame_locator("iframe[name=\"appFrame\"]").locator('input[type="radio"][value ="LOCATION"]').click()
    page.frame_locator("iframe[name=\"appFrame\"]").get_by_placeholder("Search text").type(location)
    sleep(2)
    # page.frame_locator("iframe[name=\"appFrame\"]").locator("//span[contains(text(),"+item+")]").click()
    page.frame_locator("iframe[name=\"appFrame\"]").locator("div[id *= '" + location + "'] > span").click()
    sleep(2)
    page.frame_locator("iframe[name=\"appFrame\"]").locator('//button[@aria-label="move selected right"]').click()

    # filter customer
    page.frame_locator("iframe[name=\"appFrame\"]").locator('button[id$=\'CUSTOMER\']').click()
    page.frame_locator("iframe[name=\"appFrame\"]").locator('input[type="radio"][value ="CUSTOMER"]').click()
    page.frame_locator("iframe[name=\"appFrame\"]").get_by_placeholder("Search text").type(customer)
    sleep(2)
    # page.frame_locator("iframe[name=\"appFrame\"]").locator("//span[contains(text(),"+item+")]").click()
    page.frame_locator("iframe[name=\"appFrame\"]").locator("div[id *= '" + customer + "'] > span").click()
    sleep(2)
    page.frame_locator("iframe[name=\"appFrame\"]").locator('//button[@aria-label="move selected right"]').click()

    sleep(2)
    page.frame_locator("iframe[name=\"appFrame\"]").get_by_test_id('pivot-dailog-apply-btn').click()
    sleep(6)

    # get row number
    list_elements_headers = page.frame_locator("iframe[name=\"appFrame\"]").locator(
        '//div[starts-with(@id,"jdapivot")]/div['
        '@class="dhx_ss_header"]//table[@id="centerHdrTable"]/tr['
        'starts-with(@class,"pivotHdrRow")]//span['
        '@class="pivot_member_name "]').all()
    index = 0
    for idx, element in enumerate(list_elements_headers):
        if element.text_content() == column:
            index = idx
            break

    # get demand name
    element = page.frame_locator("iframe[name=\"appFrame\"]").locator(
        '//div[starts-with(@id,"jdapivot")]/div[@class="dhx_ss_body"]/div[@class="dhx_ss_left"]/div['
        '@class="dhx_ss_center_scroll"]//span[@class="pivot_member_name "]').filter(
        has_text=measure)
    temp_json = json.loads(element.locator('..').get_attribute('data-facet-data'))

    # construct xpath
    xpath_edit = ('(//div[starts-with(@id,"jdapivot")]/div[@class="dhx_ss_body"]/div[@class="dhx_ss_center"]/div['
                  '@class="dhx_ss_center_scroll"]//div[@measure="') + temp_json['measureId'] + '"])[' + str(
        index + 1) + ']'

    # edit
    page.frame_locator("iframe[name=\"appFrame\"]").locator(xpath_edit).click()
    current_value = page.frame_locator("iframe[name=\"appFrame\"]").locator(xpath_edit).inner_text().replace(',', '')
    value_to_enter = change_value * float(current_value)
    sleep(1)
    page.frame_locator("iframe[name=\"appFrame\"]").locator(xpath_edit).type(str(value_to_enter))
    page.frame_locator("iframe[name=\"appFrame\"]").locator(xpath_edit).press('Enter')
    sleep(1)
    assert page.frame_locator("iframe[name=\"appFrame\"]").locator(xpath_edit).inner_text() == f"{value_to_enter:,.2f}"
    # refresh
    page.frame_locator("iframe[name=\"appFrame\"]").get_by_role("link", name="").click()
    # tblvpApptitleRefresh > div > span > a
    # what if
    page.frame_locator("iframe[name=\"appFrame\"]").get_by_text('What If').click()
    sleep(6)

    # ---------------------
    context.close()
    browser.close()

# with sync_playwright() as playwright:
#     test_page(playwright)
