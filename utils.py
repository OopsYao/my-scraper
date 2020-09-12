import datetime


# 返回两天之间的日期
def days_between(d1, d2):
    return [(d1 + datetime.timedelta(days=x)) for x in range((d2-d1).days + 1)]


if __name__ == "__main__":
    d1 = datetime.date(2015, 1, 1)
    d2 = datetime.date(2015, 2, 6)
    print(days_between(d1, d2))
