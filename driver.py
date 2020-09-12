from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import random
import re


class Driver:
    def __enter__(self):
        agents = [
            "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
            "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
            "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
            "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36"
        ]
        opts = Options()
        opts.add_argument("--headless")  # 不显示界面
        # 随机设置user-agent
        opts.add_argument(f"user-agent={random.choice(agents)}")
        # 避免webdriver检测
        # see https://www.cnblogs.com/presleyren/p/12936553.html
        opts.add_experimental_option("excludeSwitches", ["enable-automation"])
        opts.add_experimental_option('useAutomationExtension', False)
        driver = webdriver.Chrome(options=opts)
        driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": """
                Object.defineProperty(navigator, 'webdriver', {
                  get: () => undefined
                })
            """
        })
        driver.delete_all_cookies()
        self._driver = driver
        return driver

    def __exit__(self, type, value, trace):
        self._driver.quit()


def login(driver):
    user = 'bignilakke@enayu.com'
    passwd = 'Lxnp7U63LaYGDik'

    def until_clickable(xpath):
        return WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, xpath)
            )
        )
    driver.get('https://www.qimai.cn/')
    # 七周年回馈浮动广告 会影响点击登录按钮
    until_clickable('//*[@id="app"]/div[9]/div/i').click()
    # 登录按钮
    until_clickable(
        '//*[@id="app"]/div[1]/div/div/div/div[2]/div/a[1]').click()
    # 点击密码登录
    until_clickable('//*[@id="signin"]/ul/li[2]').click()
    # 邮箱名
    until_clickable(
        '//*[@id="password-logon"]/form/div[1]/div/div/input').send_keys(user)
    # 密码
    until_clickable(
        '//*[@id="password-logon"]/form/div[2]/div/div/input').send_keys(passwd)
    # 确认登录
    until_clickable('//*[@id="password-logon"]/div[3]').click()


# 每日排行榜
# 爬取某一天的对应网址
def handle_page(driver, date):
    driver.get(
        f"https://www.qimai.cn/rank/index/brand/all/device/iphone/country/cn/genre/36/date/{date.strftime('%Y-%m-%d')}")

    ul = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located(
            # 免费榜
            (By.XPATH, '//*[@id="rank-all-list"]/div[2]/div[2]/div[1]/div/ul'))
    )
    items = ul.find_elements_by_class_name('info-content')
    rank = []
    for div in items:
        a = div.find_element_by_tag_name('a')
        app_id = re.search(r'appid/(\d+)', a.get_attribute('href')).group(1)
        app_name = a.text
        rank_item = div.find_element_by_class_name('rank-item').text
        rank.append({'app_id': app_id, 'app_name': app_name,
                     'rank_item': int(rank_item)})
    return rank
