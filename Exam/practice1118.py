
import sys


data_list = []
discount = {
    'S':0.9,
    'T':1.0,
    'G':1.1
}
price = {
    'A4':{ 'bw':1, 'color':3 },
    'A3':{ 'bw':2, 'color':6 }
}

def add_new():
    id = input("客戶ID：")
    pages = input("頁數：")
    mode = input("色彩(color/bw)：").lower()
    size = input("紙張(A4/A3)：").upper()
    duplex = input("雙面(Y/N)：").upper()

    if mode not in ['color','bw'] or size not in ['A4','A3'] or duplex not in ['Y','N']:
        print("輸入錯誤請重新輸入")
        add_new()
        return
    try:
        pages = int(pages)
    except ValueError:
        print("頁數錯誤請重新輸入")
        add_new()
        return
    if  pages < 1:
        print("頁數錯誤請重新輸入")
        add_new()
        return
    total = round(price.get(size).get(mode)*pages*(0.9 if duplex == 'Y' else 1)*discount.get(id[0].upper(),discount['G']))

    data_list.append({
        'id':id,
        'pages':pages,
        'mode':mode,
        'size':size,
        'duplex':duplex,
        'final':total
    })
    print( f"新增成功！本筆金額：{total}" )
def detail():
    for data in data_list:
        print( f"客戶 ID：{data['id']}\n頁數：{data['pages']}\n色彩(color/bw)：{data['mode']}\n紙張(A4/A3)：{data['size']}\n雙面(Y/N)：{data['duplex']}\n金額：{data['final']}" )
    print( "TotalAmount:",sum(d['final'] for d in data_list) )
def id_search():
    keyword = input("關鍵字：")
    matchs = [d for d in data_list if keyword in d['id']]
    print( f"找到{len(matchs)}筆；" )
    count = 1
    for data in matchs:
        print( f"第{count}筆：{data['id']}\n頁數：{data['pages']}\n色彩(color/bw)：{data['mode']}\n紙張(A4/A3)：{data['size']}\n雙面(Y/N)：{data['duplex']}\n金額：{data['final']}" )
        count += 1
def statistic():
    totalpages = sum(d['pages'] for d in data_list)
    totalamount = sum(d['final'] for d in data_list)
    print( f"Count: {len(data_list)}, TotalPages: {totalpages}, TotalAmount: {totalamount}, Avg: {totalamount/len(data_list)}" )
    maxD = max( data_list,key=lambda d: d['final'] )
    minD = min( data_list,key=lambda d: d['final'] )
    print( f"Max: {maxD['final']} ({maxD['id']}), Min: {minD['final']} ({minD['id']})" )
def delete_last():
    try:
        data_list.pop(-1)
        print("成功刪除最後一筆資料")
    except IndexError:
        print("無可刪除資料")
def finish():
    print("Bye")
    sys.exit()

menu = {
    1:add_new,
    2:detail,
    3:id_search,
    4:statistic,
    5:delete_last,
    0:finish
}

while True:
    task = input("1) 新增影印任務\n2) 列出所有明細與總金額\n3) 關鍵字查詢（依客戶 ID，大小寫不分）\n4) 統計摘要（筆數、總頁數、總金額、平均、最高/最低）\n5) 刪除最後一筆\n0) 離開\n請輸入功能：")
    try:
        task = int(task)
    except ValueError:
        print("請輸入數字")
        continue
    menu.get(task)()
