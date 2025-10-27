# 校園飲料快點
'''
價格規則
1) 基本品項與尺寸單價
BlackTea ： S 25 、 M 30 、 L 35
GreenTea ： S 30 、 M 35 、 L 40
MilkTea ： S 40 、 M 50 、 L 60
2) 加料（可 0 或 1 種）
boba +10 、 pudding +15 、 none +0
3) 身分別折扣（整單）
學生 student ： 95 折（ ×0.95 ）
教職 staff ： 9 折（ ×0.9 ）
訪客 guest ：無折扣（ ×1.0 ）
'''
# Menu

items = {
    "BlackTea": { "S":25, "M":30, "L":35 },
    "GreenTea": { "S":30, "M":35, "L":40 },
    "MilkTea": { "S":40, "M":50, "L":60 }
}
toppings = {
    "boba":10,
    "pudding":15
}
discounts = {
    "student": { "dis":0.95, "desc":"5% off" },
    "staff": { "dis":0.9, "desc":"10% off" },
    "guest": { "dis":1, "desc":"Non-dis" }
}

print("┏━━━━━━━━━━━━━━━━━━━━┓\n┃        MENU        ┃\n┗━━━━━━━━━━━━━━━━━━━━┛")
print(" Drinks      S/M/L\n" + "-"*22)
for drink, size in items.items():
    print(f" {drink:12}{size["S"]}/{size["M"]}/{size["L"]}")
print("\n Topping     +$\n" + "-"*22)
for topping, price in toppings.items():
    print(f" {topping:12}+{price}")
print("\n Discount\n" + "="*22)
for id, discount in discounts.items():
    print(f" {id:12}{discount["desc"]}")

# Input Orders & 處理字串

def item_str(item:str):
    item = item[0].upper() + item[1:-3].lower() + item[-3].upper() + item[-2:].lower()
    return item

count = 1
orders = []
name = input("\n請輸入您的名字：")
id = input("請輸入您的身分(student/staff/guest)：")
while (count < 4):
    order = input(f"\n第{count}筆訂單\n請輸入您的訂單(品項, 尺寸(S/M/L), 加料(至多1樣), 數量)，並用'/'分隔：")
    if count == 1 and order == "":
        print("請至少輸入一筆訂單")
    elif order == "":
        break
    else:
        try:
            item, size, topping, qty = order.split("/")
            orders.append({
                "item": item_str(item),
                "size": size.upper(),
                "topping": topping.strip().lower(),
                "qty": int(qty)
            })
            count += 1
        except:
            print("輸入錯誤或格式錯誤，請重新輸入此訂單")

# 計算帳單

total = 0
for order in orders:
    order["price"] = (items.get(order["item"]).get(order["size"])+toppings.get(order["topping"], 0))*order["qty"]
    total += order["price"]
    
# 輸出明細

print( f"《 {name} 的訂單 》\n身分認證 ‹{id if id in discounts else "guest"}›" )
print( "item" + " "*13 + "size qty $\n" + "-"*30 )
for order in orders:
    print( f"{order["item"]:9}\033[90m{order["topping"] if order["topping"] in toppings else "":8}\033[0m{order["size"]:5}{order["qty"]:<4}{order["price"]}")
print( "-"*30 + f"\nSubtotal：{total:>5} 元\nDiscount：{total-round(total*discounts.get(id,discounts["guest"]).get("dis")):>5} 元 \033[90m{discounts.get(id,discounts["guest"]).get("desc")}\033[0m" )
print( "-"*30 + f"\nTotal：{round(total*discounts.get(id,discounts["guest"]).get("dis"))} 元\n# 謝謝{name}的購買，歡迎下次光臨" )
