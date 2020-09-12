# Scraper

爬取[七麦数据](https://qimai.cn)上的每日榜单

## How to use

由于要爬取的网站为SPA，该项目依赖于[selenium](https://selenium-python.readthedocs.io/)
来启动相关的浏览器进行模拟操作。
暂时选用的浏览器为Chrome，故需要保证Chrome和相关的[driver](https://sites.google.com/a/chromium.org/chromedriver/downloads)
的安装。可以参考[其他浏览器driver](https://selenium-python.readthedocs.io/installation.html#drivers)的安装。

再安装相关python依赖
```bash
pip install -r requirements.txt
```
然后即可进行爬取。
```bash
python crawl.py
```
