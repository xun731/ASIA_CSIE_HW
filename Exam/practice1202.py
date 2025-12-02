import csv
import sys
from datetime import datetime
import os

category_list = [ '書寫用品','紙品','收納','電子周邊','其他']
records = []
empty = {
    'name':'',
    'final':0
}

def add_new():
    date = input("日期：")
    name = input("商品名稱：")
    category = input("類別：")
    price = input("單價：")
    qty = input("數量：")
    membership = input("是否會員(Y/N)：").lower()

    try:
        datetime.strptime( date, '%Y-%m-%d' )
    except ValueError:
        print("日期格式錯誤，請重新輸入")
        add_new()
        return
    try:
        price = float(price)
        qty = int(qty)
    except ValueError:
        print("單價/數量輸入錯誤，請重新輸入")
        add_new()
        return
    if membership not in [ 'y', 'n' ]:
        print("會員錯誤請重新輸入(y/n)")
        add_new()
        return
    if category not in category_list:
        print("無匹配的類別，已分類至《其他》")
        category = "其他"
    total = round(price*qty*(0.95 if membership == 'y' else 1))

    records.append({
        'date':date,
        'name':name,
        'category':category,
        'price':price,
        'qty':qty,
        'membership':membership,
        'final':total
    })
    print( f"新增成功！本筆金額：{total}" )

def detail():
    count = 1
    for data in records:
        print( f"#{count} {data['date']} {data['name']} {data['category']} {data['price']}×{data['qty']} 會員:{data['membership']} 金額:{data['final']}" )
        count += 1
    print( "TotalAmount:",sum(d['final'] for d in records) )

def keyword():
    keyword = input("關鍵字：")
    matches = [d for d in records if keyword.lower() in d['name'].lower()]
    print( f"找到{len(matches)}筆；" )
    if len(matches) != 0:
        print( f"{matches[0]['date']} {matches[0]['name']} {matches[0]['category']} {matches[0]['price']}×{matches[0]['qty']} 會員:{matches[0]['membership']} 金額:{matches[0]['final']}" )

def statistic():
    total = sum(d['final'] for d in records)
    print( f"Count: {len(records)} TotalAmount: {total} Avg: {total/len(records) if len(records) != 0 else 0}" )
    maxD = (max( records,key=lambda d: d['final'] ) if len(records) != 0 else empty)
    minD = (min( records,key=lambda d: d['final'] ) if len(records) != 0 else empty)
    print( f"Max: {maxD['final']} ({maxD['name']}) Min: {minD['final']} ({minD['name']})" )

    category_total = {}
    for i in range(len(category_list)):
        category_sum = sum([d['final'] for d in records if category_list[i] in d['category']])
        if category_sum:
            category_total[category_list[i]] = category_sum
    print( f"By Category: {category_total}" )

def save():

    script_path = os.path.abspath(__file__)
    script_dir = os.path.dirname(script_path)

    txt_path = os.path.join(script_dir, "report.txt")
    csv_path = os.path.join(script_dir, "sales.csv")

    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
        print("日期,商品名稱,類別,單價,數量,會員,金額",file=f)
        for d in records:
            print(','.join(str(d[i]) for i in d),file=f)

    with open(txt_path, 'w', newline='', encoding='utf-8') as f:
        print( "--- Summary ---" ,file=f)
        total = sum(d['final'] for d in records)
        print( f"Count: {len(records)}\nTotalAmount: {total}\nAvg: {total/len(records) if len(records) != 0 else 0}",file=f )
        maxD = (max( records,key=lambda d: d['final'] ) if len(records) != 0 else empty)
        minD = (min( records,key=lambda d: d['final'] ) if len(records) != 0 else empty)
        print( f"Max: {maxD['final']} ({maxD['name']})\nMin: {minD['final']} ({minD['name']})",file=f )

        category_total = {}
        for i in range(len(records)):
            category_sum = sum([d['final'] for d in records if category_list[i] in d['category']])
            if category_sum:
                category_total[category_list[i]] = category_sum
        print( f"By Category:",file=f )
        for o in category_total.keys():
            print( f"{o}: {category_total[o]}",file=f )

def load():
    try:
        with open("sales.csv", 'r', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # 日期,商品名稱,類別,單價,數量,會員,金額
                records.append({
                    'date':row['日期'],
                    'name':row['商品名稱'],
                    'category':row['類別'],
                    'price':float(row['單價']),
                    'qty':int(row['數量']),
                    'membership':row['會員'],
                    'final':int(row['金額'])
                })
        print("已載入檔案")
    except FileNotFoundError:
        print("找不到檔案")

def leave():
    print("Bye")
    sys.exit()


menu = {
    1:add_new,
    2:detail,
    3:keyword,
    4:statistic,
    5:save,
    6:load,
    0:leave
}

while True:
    task = input("1) 新增銷售紀錄\n2) 列出所有明細與總金額\n3) 關鍵字查詢（商品名稱，大小寫不分）\n4) 統計摘要（筆數、總金額、平均、最高/最低、各類別合計）\n5) 另存新檔（sales.csv）＋輸出摘要（report.txt）\n6) 從檔案載入初始資料（sales_seed.csv）\n0) 離開\n請輸入功能：")
    try:
        task = int(task)
    except ValueError:
        print("請輸入數字")
        continue
    menu.get(task)()
