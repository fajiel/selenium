from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

SELENIUM_TIMEOUT = 12

def get_browser_driver():
    """获取浏览器服务 使用后记得 driver.quit() 否则容易引起状态污染"""
    try:
        # PhantomJS 设置不加载图片
        driver = webdriver.PhantomJS(service_args=['--load-images=no'])
    except WebDriverException:
        # chrome 设置不加载图片
        chrome_options = webdriver.ChromeOptions()
        chrome_profile = {"profile.managed_default_content_settings.images": 2}
        chrome_options.add_experimental_option("prefs", chrome_profile)
        driver = webdriver.Chrome(chrome_options=chrome_options)
    driver.set_page_load_timeout(SELENIUM_TIMEOUT)
    driver.implicitly_wait(SELENIUM_TIMEOUT)
    return driver

def wait_driver(driver, id, wait_time, watch_step):
    locator = (By.ID, id)
    try:
        WebDriverWait(driver, wait_time, watch_step).until(EC.presence_of_element_located(locator))
        print(u"成功访问搜索引擎！")
    except Exception as e:
        print(e)
        print(u"搜索引擎未加载成功，浏览器将被退出！")
        driver.quit()