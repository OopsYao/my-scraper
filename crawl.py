from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from driver import Driver
import csv
import re
import random
import time
import utils
import datetime


user = 'bignilakke@enayu.com'
passwd = 'Lxnp7U63LaYGDik'


def login(driver):
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


if __name__ == "__main__":
    res = dict()
    with Driver() as driver:
        login(driver)
        for d in utils.days_between(datetime.date(2020, 9, 4), datetime.date.today()):
            # 遍历每一天的排行榜
            for app in handle_page(driver, d):
                app_id = app['app_id']
                app_name = app['app_name']
                rank_item = app['rank_item']

                rank = {
                    'date': d,
                    'rank': rank_item
                }
                if app_id not in res:
                    res[app_id] = {'ranks': [rank], 'app_name': app_name}
                else:
                    res[app_id]['ranks'].append(rank)

            time.sleep(0.5 + random.random() * 2)  # 等待0.5-2.5s

    print(res)

    # 计算平均排名 并写入
    with open('dist.csv', 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile)
        for app_id in res:
            app = res[app_id]
            ranks = app['ranks']
            avg = sum(r['rank'] for r in ranks) / len(ranks)
            spamwriter.writerow([str(app_id), str(app['app_name']), str(avg)])
