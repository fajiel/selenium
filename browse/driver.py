import re
import time
import random
import requests
from selenium.webdriver.common.keys import Keys
from browse.util import get_browser_driver, wait_driver

WAIT_TIME = 60
WATCH_STEP = 0.5
SEARCH_ID = {
    "baidu": "kw"
}

class BrowseKeywords():
    def __init__(self, url, key_word, count):
        self.driver = get_browser_driver()
        self.url = url
        self.key_word = key_word
        self.ukey = SEARCH_ID.get(url.split("//")[-1].replace("www.", "").split(".")[0], "")
        self.urls = []
        self.count = count
        self.curr_count = 0

    def browse_search(self):
        self.driver.get(self.url)
        url_key = self.url.split(".")[1]
        try:
            self.driver.get(self.url)
            print(u"已成功访问搜索引擎！")
        except Exception as e:
            print(e)
            print(u"搜索引擎访问失败，正在尝试连接，请等待{}秒！".format(WAIT_TIME))
            wait_driver(self.driver, SEARCH_ID.get(url_key, ""), WAIT_TIME, WATCH_STEP)

    def browse_keyword(self):
        self.driver.find_element_by_id(self.ukey).clear()
        elem = self.driver.find_element_by_id(self.ukey)
        elem.send_keys(self.key_word)
        print(u"已输入关键词,正在模拟随机等待时间！")
        time.sleep(random.randint(0, 10))
        elem.send_keys(Keys.ENTER)
        print(u"正在搜索页面，请等待！")
        time.sleep(random.randint(5, 10))

    def crawl_content(self):
        self.driver.current_window_handle
        search_items = self.driver.find_element_by_id("content_left").find_elements_by_css_selector(".result.c-container")
        for search_item in search_items:

            href = search_item.find_element_by_xpath(".//h3/a").get_attribute(u"href")
            resp = requests.get(href, allow_redirects=False)
            if resp.status_code == 200:
                url = re.search(r'URL=\'(.*?)\'', resp.text)
            elif resp.status_code == 302:
                url = resp.headers.get('location', None)
            else:
                url = None

            if url and url.startswith("http"):
                self.urls.append(url)
                self.curr_count += 1

            if self.curr_count >= self.count:
                break

    def browse_nextpage(self):
        self.driver.current_window_handle
        self.driver.find_element_by_id("page")\
            .find_element_by_partial_link_text(u"下一页").click()
        time.sleep(3)

