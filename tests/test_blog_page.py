from playwright.sync_api import expect

from pages.page_objects.blog_page import BlogPage


def test_blog_page_and_filter_articles(blog_page: BlogPage):
    article_titles = (
        'Top 10 Python Apps: Why Are They So Successful?',
        'Why our Data Engineers use Python as our go-to tool',
        'How Does the Scrum Master Help Your Software Development Team?'
    )
    blog_page.load_and_accept_cookies()
    for article in article_titles:
        expect(blog_page.get_link(article)).to_be_visible()
    expect(blog_page.get__posts).to_have_count(3)
