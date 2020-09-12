from driver import Driver, handle_page, login
import csv
import random
import time
import utils
import datetime
from tqdm import tqdm # 进度条

if __name__ == "__main__":
    # 存储所有app的结果 格式如下
    # {
    #     000001: {
    #         app_name: xxx,
    #         ranks: [{ date: 某一天, rank: 排名 }]
    #     }
    # }
    res = dict()
    with Driver() as driver:
        print('登录中')
        login(driver)
        for d in tqdm(utils.days_between(datetime.date(2019, 9, 12), datetime.date.today())):
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

            # 避免太过规律被网站检测出来 可以考虑删除
            time.sleep(random.random())  # 等待0-1s

    # 计算平均排名 并写入csv文件
    with open('dist.csv', 'w') as csvfile:
        spamwriter = csv.writer(csvfile)
        spamwriter.writerow(['APP ID', 'APP NAME', 'RANK'])
        for app_id in res:
            app = res[app_id]
            ranks = app['ranks']
            # 计算平均值 比如只有一次上榜 则最终排名就是该排名(出现次数为1)
            avg = sum(r['rank'] for r in ranks) / len(ranks)
            spamwriter.writerow(
                # avg保留两位小数
                [str(app_id), str(app['app_name']), f'avg:.2f'])
