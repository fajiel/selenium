from browse.driver import BrowseKeywords

def search_keyword(search_url, key_word, count):
    bk = BrowseKeywords(search_url, key_word, count)
    bk.browse_search()
    bk.browse_keyword()
    bk.crawl_content()
    while bk.curr_count < count:
        bk.browse_nextpage()
        bk.crawl_content()
    bk.driver.quit()
    return bk.urls

def main():
    search_url = "http://www.baidu.com"
    key_word = "selenium"
    count = 10
    search_keyword(search_url, key_word, count)

if __name__ == u"__main__":
    main()