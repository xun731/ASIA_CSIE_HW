# 校園二手書交換平台

import re
from datetime import datetime 

pattern = r"^\d{4}-\d{2}-\d{2},.+,[a-zA-Z]+,\d+,\d+,\d+,[a-zA-Z]+"
data = []
total = 0
dis_total = 0
count = 0
highest = {
    "date":"",
    "price":0,
    "book":""
}
lowest = {
    "date":"",
    "price":None,
    "book":""
}
category = {
    "CS":{ "books":0, "total":0 },
    "EE":{ "books":0, "total":0 },
    "MATH":{ "books":0, "total":0 },
    "BUS":{ "books":0, "total":0 },
    "LIT":{ "books":0, "total":0 },
    "OTHER":{ "books":0, "total":0 }
}


def checkDate(date):
    try:
        datetime.strptime( date, "%Y-%m-%d" )
        return True
    except ValueError:
        return False


# 格式與規則

print("定價與費用規則 :\n1. 成交價（每本）以「成色」對定價打折：\n成色 >= 90 → 9 折\n80 <= 成色 < 90 → 85 折\n60 <= 成色 < 80 → 8 折\n成色 < 60 → 7 折")
print("2. 平台服務費：\nstudent → ×0.97 （學生優惠）\nstaff → ×1.00\nguest → ×1.05 （含手續費）")
print("3. 類別字典（可擴充）類別統一碼：\nCS （資工 / 程式）、 EE 、 MATH 、 BUS 、 LIT 、 OTHER")
print("輸入格式：\n日期 (YYYY-MM-DD), 書名 , 類別 , 定價 , 成色 (0-100), 數量 , 身分 (student/staff/guest)\n範例： 2025-09-26, Python 基礎 , CS, 450, 85, 2, student")


# 輸入與格式確認

while True:
    data_input = input("輸入：")
    data_split = data_input.split(",")
    if not bool(data_input) or data_input.isspace() or data_input.upper() == "END":
        break
    elif not bool(re.match(pattern,data_input)):
        print("格式錯誤，請重新輸入此筆紀錄")
        continue
    elif not checkDate(data_split[0]):
        print("此日期不存在，請重新輸入")
        continue
    elif int(data_split[4]) > 100 or int(data_split[4]) < 0:
        print("成色需在0-100之間，請重新輸入")
        continue
    
    data.append({
                "date": data_split[0],
                "book_name": data_split[1],
                "category": data_split[2].upper(),
                "price": int(data_split[3]),
                "quality": int(data_split[4]),
                "qty": int(data_split[5]),
                "id": data_split[6].lower(),
            })
    

# 計算與統計

discounts = {
    "student": { "dis":0.97, "desc":"3% off" },
    "staff": { "dis":1, "desc":"Non-dis" },
    "guest": { "dis":1.05, "desc":"5% charge" }
}

for i in range(len(data)):

    # 成色 (在subtotal就套用身分係數)
    if data[i]["quality"] >= 90:
        data[i]["sold"] = round(0.9*data[i]["price"])
        data[i]["subtotal"] = round(data[i]["sold"]*data[i]["qty"]*(discounts[data[i]["id"]]["dis"] if data[i]["id"] in discounts else 1.05))
    elif data[i]["quality"] >= 80 and data[i]["quality"] < 90:
        data[i]["sold"] = round(0.85*data[i]["price"])
        data[i]["subtotal"] = round(data[i]["sold"]*data[i]["qty"]*(discounts[data[i]["id"]]["dis"] if data[i]["id"] in discounts else 1.05))
    elif data[i]["quality"] >= 60 and data[i]["quality"] < 80:
        data[i]["sold"] = round(0.8*data[i]["price"])
        data[i]["subtotal"] = round(data[i]["sold"]*data[i]["qty"]*(discounts[data[i]["id"]]["dis"] if data[i]["id"] in discounts else 1.05))
    else:
        data[i]["sold"] = round(0.7*data[i]["price"])
        data[i]["subtotal"] = round(data[i]["sold"]*data[i]["qty"]*(discounts[data[i]["id"]]["dis"] if data[i]["id"] in discounts else 1.05))

    # 類別
    if data[i]["category"] in category:
        category[data[i]["category"]]["books"] += data[i]["qty"]
        category[data[i]["category"]]["total"] += data[i]["sold"]*data[i]["qty"]
    else:
        data[i]["category"] = "OTHER"
        category["OTHER"]["books"] += data[i]["qty"]
        category["OTHER"]["total"] += data[i]["sold"]*data[i]["qty"]

    # 總金額
    total += data[i]["sold"]*data[i]["qty"]
    dis_total += data[i]["subtotal"]
    count += data[i]["qty"]

    # 最高/最低
    if data[i]["sold"] > highest["price"]:
        highest["date"] = data[i]["date"]
        highest["price"] = data[i]["sold"]
        highest["book"] = data[i]["book_name"]
    if lowest["price"] is None or data[i]["sold"] < lowest["price"]:
        lowest["date"] = data[i]["date"]
        lowest["price"] = data[i]["sold"]
        lowest["book"] = data[i]["book_name"]


# 輸出

print("《明細表》")
for output in data:
    print( f"日期：{output['date']:15}書名：{output['book_name']:15}" )
    print( f"類別：{output['category']:15}定價：{output['price']:<15}成色：{output['quality']}" )
    print( f"數量：{output['qty']:<15}每本成交價：{output['sold']:}\n該筆金額(含手續費or折扣)：{output['subtotal']} \033[90m{discounts[output['id']]['desc'] if output['id'] in discounts else '5% charge'}\033[0m" )

print( "-"*45 )
print( "# 總計 #" )
print( f"總筆數：{len(data):<13}總本數：{count}\n整單小計(不含手續費or折扣)：{total}\n應付總金額：{dis_total}" )
print( "# 最貴的書籍 #" )
print( f"日期：{highest['date']}\n書名：{highest['book']}\n金額：{highest['price']}" )
print( "# 最便宜的書籍 #" )
print( f"日期：{lowest['date']}\n書名：{lowest['book']}\n金額：{lowest['price']}" )
print( "# 各類別統計 #" )
for output in category.keys():
    print( f"類別：{output:15}總本數：{category[output]['books']:<13}總金額：{category[output]['total']}" )
print("感謝您的使用~很高興為您服務!!")
