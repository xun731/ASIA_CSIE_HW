# Rules
# Input return data
# Borrowings 逐筆明細表 return result
# Statistics 整體統計 
# Extreme 極值
# Category 各類別彙整


# 圖書館借閱結帳與報表系統（含函數版）

import re
from datetime import datetime
import os
import csv

data = []
result = []
category = {
    '參考書':{ 'fee':25, 'books':0, 'total':0 },
    '熱門新書':{ 'fee':20, 'books':0, 'total':0 },
    '普通藏書':{ 'fee':10, 'books':0, 'total':0 },
    '期刊':{ 'fee':8, 'books':0, 'total':0 },
    '其他':{ 'fee':12, 'books':0, 'total':0 }
}


def Rules():
    print("基本日費（依類別）（每本每日）：\n參考書 25 、熱門新書 20 、普通藏書 10 、期刊 8 、其他12")
    print("加價 / 折抵：\n逾期 (Y) ：整筆加收固定 30 元（手續費）\n自備袋 (Y) ：整筆折抵 5 元")
    print("身份係數（整筆金額乘係數）：\n student ×0.9 、 staff ×1.0 、 guest ×1.1")
    print("每筆輸入以逗號分隔，固定 7 欄：\n日期 (YYYY-MM-DD), 書名 , 類別 , 借日數 , 身分 (student/staff/guest), 是否逾期 (Y/N), 是否自備袋 (Y/N)")
    print("範例： 2025-10-15,資料結構,普通藏書,7,student,N,Y")

def checkDate(date):
    try:
        datetime.strptime( date, '%Y-%m-%d' )
        return True
    except ValueError:
        return False

def Input_data():
    pattern = r"^\d{4}-\d{2}-\d{2},.+,.+,\d+,[a-zA-Z]+,[a-zA-Z],[a-zA-Z]"
    while True:
        data_input = input("輸入：")
        data_split = data_input.split(',')
        if not bool(data_input) or data_input.isspace() or data_input.upper() == 'END':
            break
        elif not bool(re.match(pattern,data_input)):
            print("格式錯誤，請重新輸入此筆紀錄")
            continue
        elif not checkDate(data_split[0]):
            print("此日期不存在，請重新輸入")
            continue
        elif (data_split[5].upper() != 'N' and data_split[5].upper() != 'Y') or (data_split[6].upper() != 'N' and data_split[6].upper() != 'Y'):
            print("最後兩項請輸入Y或N")
            continue
        
        data.append({
                    'date': data_split[0],
                    'book_name': data_split[1],
                    'category': data_split[2],
                    'days': int(data_split[3]),
                    'id': data_split[4].lower(),
                    'delay': data_split[5].upper(),
                    'bag': data_split[6].upper(),
                })

def Borrowings():
    for d in data:
        day_fee = category.get(d['category'],category['其他'])['fee']
        result.append({
                    '日期': d['date'],
                    '書名': d['book_name'],
                    '類別': d['category'],
                    '日費':day_fee,
                    '借日數': d['days'],
                    '是否逾期': d['delay'],
                    '該筆小計': day_fee*d['days'] + (30 if d['delay'] == 'Y' else 0),
                })
        category.get(d['category'],category['其他'])['books'] += 1
        category.get(d['category'],category['其他'])['total'] += result[-1]['該筆小計']
    
def Statistics():
    discounts = {
    'student': 0.9,
    'staff': 1,
    'guest': 1.1
    }
    subtotal_id = sum(result[i]['該筆小計'] * discounts.get(data[i]['id'],discounts['guest']) for i in range(len(data)))
    total = round(subtotal_id - (len([x for x in data if x['bag'] == 'Y']))*5)
    result_overall = {
        '總筆數': len(data),
        '總天數': sum(d['days'] for d in data),
        '整單小計': sum(r['該筆小計'] for r in result),
        '身分係數': subtotal_id,
        '應付總金額': total if total >= 0 else 0
    }
    max_data = max(result, key= lambda r: r['該筆小計'])
    min_data = min(result, key= lambda r: r['該筆小計'])

    return result_overall, max_data, min_data

def Messages():
    if len(result) >= 5:
        message = "一起讀書，知識不嫌多"
    elif result_overall['總天數'] <= 3:
        message = "哇~讀書也要注意休息喔!晚點還也沒事的!!"
    else:
        message = "活到老學到老!多來看看書呀~"
    return message

Rules()
Input_data()
Borrowings()
result_overall, maxD, minD = Statistics()
message = Messages()

script_path = os.path.abspath(__file__)
script_dir = os.path.dirname(script_path)

txt_path = os.path.join(script_dir, "report.txt")
csv_path = os.path.join(script_dir, "borrowings.csv")

with open(csv_path, 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=result[0].keys())
    writer.writeheader()
    writer.writerows(result)
    # print("日期,書名,類別,日費,借日數,是否逾期,該筆小計")
print(','.join(result[0]))
for r in result:
    print(','.join(str(r[i]) for i in r))

with open(txt_path, 'w', newline='', encoding='utf-8') as f:
    print("《整體統計》", file=f)
    print( f"總筆數: {result_overall['總筆數']}筆\n總天數: {result_overall['總天數']}天\n整單小計: {result_overall['整單小計']}元", file=f)
    print( f"身份係數後金額: {result_overall['身分係數']}元\n應付總金額: {result_overall['應付總金額']}元", file=f)
    print( f"- 最高單筆交易:\n日期: {maxD['日期']}\n書名: {maxD['書名']}\n金額: {maxD['該筆小計']}元", file=f)
    print( f"- 最低單筆交易:\n日期: {minD['日期']}\n書名: {minD['書名']}\n金額: {minD['該筆小計']}元", file=f)
    print( f"\n來自店家的一段話:\n{message}", file=f)

print("《整體統計》")
print( f"總筆數: {result_overall['總筆數']}筆\n總天數: {result_overall['總天數']}天\n整單小計: {result_overall['整單小計']}元")
print( f"身份係數後金額: {result_overall['身分係數']}元\n應付總金額: {result_overall['應付總金額']}元")
print( f"- 最高單筆交易:\n日期: {maxD['日期']}\n書名: {maxD['書名']}\n金額: {maxD['該筆小計']}元")
print( f"- 最低單筆交易:\n日期: {minD['日期']}\n書名: {minD['書名']}\n金額: {minD['該筆小計']}元")
print("- 各品項彙整:")
for o in category.keys():
    print( f"{o}: 本數: {category[o]['books']}本 金額: {category[o]['total']}元")
print( f"\n一小段留言:\n{message}")
