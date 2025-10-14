item = input()
price = float(input())
qty = int(input())
tax_rate = int(input())

subtotal = round(price*qty,1)
tax = round(subtotal*(tax_rate/100),1)
total = subtotal + tax

# 品名: <飲料名稱>, 小計: <小計>, 稅額: <稅額>, 應付: <應付>
print( f"品名: {item}, 小計: {subtotal}, 稅額: {tax}, 應付: {total}" )
