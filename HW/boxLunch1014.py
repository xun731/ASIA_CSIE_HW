# 校園便當預購與結帳系統

import re
from datetime import datetime 

pattern = r"^\d{4}-\d{2}-\d{2},.+,.+,\d+,[a-zA-Z]+,[a-zA-Z],[a-zA-Z]"
orders = []
total_qty = 0
subtotal = 0
subtotal_id = 0
total = 0
items = {
    '雞腿飯': { 'price':95, 'total_qty':0, 'total':0 },
    '排骨飯': { 'price':90, 'total_qty':0, 'total':0 },
    '魚排飯': { 'price':100, 'total_qty':0, 'total':0 },
    '蔬食飯': { 'price':85, 'total_qty':0, 'total':0 },
    '咖哩飯': { 'price':90, 'total_qty':0, 'total':0 },
    '其他': { 'price':80, 'total_qty':0, 'total':0 },
}

def checkDate(date):
    try:
        datetime.strptime( date, "%Y-%m-%d" )
        return True
    except ValueError:
        return False

# 格式與規則
print(
    "基礎價目（每份）：\n雞腿飯 95 、排骨飯 90 、魚排飯 100 、蔬食飯 85 、咖哩飯 90 、其他 80",
    "加價 / 折扣：\n加大份：單份 +15 元",
    "自備餐具：整筆折抵 5 元",
    "身份係數（整筆金額乘係數）：\n- student → ×0.95 （學生優惠）\n- staff → ×1.00\n- guest → ×1.05 （含手續費）",
    "口味：不辣 / 微辣 / 中辣 / 大辣，不影響價格。",
    "輸入格式：\n日期 (YYYY-MM-DD), 品項 , 口味 , 份數 , 身分 (student/staff/guest), 是否加大 (Y/N), 是否自備餐具(Y/N)",
    "範例： 2025-10-10, 雞腿飯 , 微辣 , 2, student, Y, N",
    "直到輸入空白行或輸入 END （不分大小寫）才結束輸入。",
    sep='\n'
)


# 輸入與格式確認

while True:
    order_input = input("輸入：")
    order_split = order_input.split(',')
    if not bool(order_input) or order_input.isspace() or order_input.upper() == 'END':
        break
    elif not bool(re.match(pattern,order_input)):
        print("格式錯誤，請重新輸入此筆紀錄")
        continue
    elif not checkDate(order_split[0]):
        print("此日期不存在，請重新輸入")
        continue
    elif (order_split[5].upper() != 'N' and order_split[5].upper() != 'Y') or (order_split[6].upper() != 'N' and order_split[6].upper() != 'Y'):
        print("最後兩項請輸入Y或N")
        continue
    
    orders.append({
                'date': order_split[0],
                'item': order_split[1],
                'flavor': order_split[2],
                'qty': int(order_split[3]),
                'id': order_split[4].lower(),
                'increase': order_split[5].upper(),
                'tableware': order_split[6].upper(),
            })
    
# 計算與統計

discounts = {
    'student': { 'dis':0.95, 'desc':'5% off' },
    'staff': { 'dis':1, 'desc':'Non-dis' },
    'guest': { 'dis':1.05, 'desc':'5% charge' }
}

for order in orders:
    # 逐筆明細表-該筆小計
    order['subtotal'] = (items.get(order['item'],items['其他'])['price'] + (15 if order['increase'] == 'Y' else 0)) * order['qty']
    
    # 整體統計
    total_qty += order['qty']
    subtotal += order['subtotal']
    order['subtotal_id'] = order['subtotal'] * discounts.get(order['id'],discounts['guest']).get('dis')
    subtotal_id += order['subtotal_id']
    total += order['subtotal_id'] - (5 if order['tableware'] == 'Y' else 0)

    # 各品項彙整
    items.get(order['item'],items['其他'])['total_qty'] += order['qty']
    items.get(order['item'],items['其他'])['total'] += order['subtotal']

# 最高/低單筆
max_order = max(orders, key= lambda o: o['subtotal'])
min_order = min(orders, key= lambda o: o['subtotal'])

# 客製化訊息
if items['其他']['total_qty'] > 5:
    message = "歡迎投稿新菜色，這樣我們才能更好的備料喔~"
elif total >= 1000:
    message = "大訂單啊!!感謝捧場<3"
else:
    message = "要吃好吃飽，才有力氣迎接新的一天！"


# 輸出
with open('orders.csv', 'w', newline='', encoding='utf-8') as f:
    # print("《逐筆明細表》", file=f)
    print("日期,品項,口味,單價,是否加大,份數,該筆小計", file=f)
    for order in orders:
        # print( f'{order['date']}, {order['item']}, {order['flavor']}, 單價{items.get(order['item'],items['其他'])['price']}元, {'加大' if order['increase'] == 'Y' else '不加大'}, {order['qty']}份, {order['subtotal']}元', file=f)
        print( order['date'], order['item'], order['flavor'], items.get(order['item'],items['其他'])['price'], '加大' if order['increase'] == 'Y' else '不加大', order['qty'], order['subtotal'], sep = ',', file=f)

with open('report.txt', 'w', newline='', encoding='utf-8') as f:
    print("《整體統計》", file=f)
    print( f"總筆數: {len(orders)}筆\n總份數: {total_qty}份\n整體小計: {subtotal}元", file=f)
    print( f"身份係數後金額: {subtotal_id}元\n應付總金額: {round(total)}元", file=f)
    print( f"- 最高單筆交易:\n日期: {max_order['date']}\n品項: {max_order['item']}\n金額: {max_order['subtotal']}元", file=f)
    print( f"- 最低單筆交易:\n日期: {min_order['date']}\n品項: {min_order['item']}\n金額: {min_order['subtotal']}元", file=f)
    print("- 各品項彙整:", file=f)
    for item in items.keys():
        print( f"{item}: 份數: {items[item]['total_qty']}份 金額: {items[item]['total']}元", file=f)
    print( f"\n來自店家的一段話:\n{message}", file=f)
