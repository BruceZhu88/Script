import sqlite3
from numpy import unique


def SQL(db_path, sql):
    conn = sqlite3.connect(db_path)
    conn.text_factory = str
    value = []
    c = conn.cursor()
    cursor = c.execute(sql)
    if ("select" or "SELECT") not in sql:
        conn.commit()
        conn.close()
    else:
        for row in cursor:
            value.append(row)
    conn.close()
    return value


def avg(region, room_type):
    prices = SQL(
        path, "select price from HOUSE where region='{}'".format(region))
    avg = round(sum([int(d[0]) for d in prices]) / len(prices), 0)
    return avg


path = '58house.db'

regions = []
for d in SQL(path, "select region from HOUSE"):
    if d[0] != '':
        regions.append(d[0])
regions = unique(regions)
# print(len(regions))
# print(regions)
'''
avgs = [(r, avg(r)) for r in regions]
for a in sorted(avgs, key=lambda item: item[1]):
    print('{} 平均租房价格:¥{}'.format(a[0], a[1]))
'''
print(SQL(path, "select * from HOUSE where room_type = '1室1厅1卫'"))