import logging
import agentql
from playwright.sync_api import sync_playwright

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)
URL = "https://www.youtube.com/"

with sync_playwright() as playwright, playwright.chromium.launch(headless=False) as browser:
    page = agentql.wrap(browser.new_page())
    page.goto(URL)

    SEARCH_QUERY = """
    {
        search_input
        search_btn
    }
    """

    VIDEO_QUERY = """
    {
        videos[] {
            video_link
            video_title
            channel_name
        }
    }
    """

    VIDEO_CONTROL_QUERY = """
    {
        play_or_pause_btn
        expand_description_btn
    }
    """

    DESCRIPTION_QUERY = """
    {
        description_text
    }
    """

    COMMENT_QUERY = """
    {
        comments[] {
            channel_name
            comment_text
        }
    }
    """

    try:
        # search query
        response = page.query_elements(SEARCH_QUERY)
        response.search_input.type("learn javascript full course", delay=75)
        response.search_btn.click()

        # video query
        response = page.query_elements(VIDEO_QUERY)
        log.debug(f"Clicking Youtube Video: {response.videos[0].video_title.text_content()}")
        response.videos[0].video_link.click()  # click the first youtube video

        # video control query
        response = page.query_elements(VIDEO_CONTROL_QUERY)
        response.expand_description_btn.click()

        # description query
        response_data = page.query_data(DESCRIPTION_QUERY)
        log.debug(f"Captured the following description: \n{response_data['description_text']}")

          # Scroll down the page to load more comments
        for _ in range(9):
            page.keyboard.press("PageDown")
            page.wait_for_page_ready_state()

        # comment query
        response = page.query_data(COMMENT_QUERY)
        log.debug(f"Captured {len(response['comments'])} comments!")

        for comment in response['comments']:
            print(f"{comment['channel_name']}: {comment['comment_text']}")

    except Exception as e:
        log.error(f"Found Error: {e}")
        raise e
    
    # Used only for demo purposes. It allows you to see the effect of the script.
    page.wait_for_timeout(10000)