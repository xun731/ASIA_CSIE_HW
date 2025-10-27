# 多品項咖啡訂單系統

from tabulate import tabulate

def Order():

    # Menu
    '''
    價格規則 ( 價格自訂 / 品項可以增加 )
    Latte : 小杯 40 元、中杯 50 元、大杯 60 元
    Americano : 小杯 35 元、中杯 45 元、大杯 55元
    Mocha : 小杯 50 元、中杯 60 元、大杯 70 元
    '''
    menu = [
        [ 1, "Coke", "15/25/35" ],
        [ 2, "Milk", "20/30/40" ],
        [ 3, "Latte", "30/40/50"],
        [ 4, "Tea", "25/35/45" ]
    ]
    menu_header = [ "No.", "Drinks", "$$ S/M/L" ]

    print( tabulate( menu, menu_header, tablefmt="fancy_grid" ))


    # 點餐

    order = input( "1.請先輸入名字，並以','結尾\n2.輸入品名(or編號)、大小(僅限英文字母)、數量，並以'/'分隔\n3.若要點複數品項，請在兩個品項中間使用'&'連接\n請輸入您的訂單：\n")
    if "," not in order:
        print("未輸入名字，或是格式錯誤(名字後面以','結尾！)")
        Order()
        return
    name = order.split( ",", maxsplit = 1 )[0]
    drinks = order.split( ",", maxsplit = 1 )[1].split( "&" )
    drink_list = [[0] * 3 for _ in range(len(drinks))]
    for i in range(len(drinks)):
        drink_list[i] = drinks[i].split( "/" )[:3]


    # Prices

    prices = {
        "coke": { "S": 15, "M": 25, "L": 35 },
        "milk": { "S": 20, "M": 30, "L": 40 },
        "latte": { "S": 30, "M": 40, "L": 50 },
        "tea": { "S": 25, "M": 35, "L": 45 }
    }

    num = {
        1: "coke",
        2: "milk",
        3: "latte",
        4: "tea"
    }
    price = []
    total = 0
    for i in range(len(drinks)):
        drink_list[i][2] = int(drink_list[i][2])
        try:
            drink_list[i][0] = num.get(int(drink_list[i][0]))
        except ValueError:
            pass
        try:
            price.append(prices.get(str(drink_list[i][0]).lower().strip()).get(str(drink_list[i][1]).upper().strip())*drink_list[i][2])
            total += price[i]
            drink_list[i].append(price[i])
        except:
            print("查無品項或輸入錯誤！請重新填寫訂單")
            Order()
            return


    # 合併訂單

    count = 0
    for i in range(len(drinks)-1):
        for j in range(1,len(drinks)-i):
            try:
                if str(drink_list[i][0]).lower() == str(drink_list[i+j-count][0]).lower() and str(drink_list[i][1]).upper() == str(drink_list[i+j-count][1]).upper() and i+j-count != i:
                    drink_list[i][2] += drink_list[i+j-count][2]
                    drink_list[i][3] += drink_list[i+j-count][3]
                    drink_list.pop(i+j-count)
                    count += 1
            except:
                continue


    # 明細

    print( f"《 {name} 的訂單 》" )
    print( tabulate( drink_list, headers = [ "Item", "Size", "Qty", "Price"], tablefmt = "simple" ))
    print( "-"*30 + f"\n總金額：{total} 元\n# 期待與{name}的下次相遇~希望您喜歡今日的餐點" )

Order()
