# 2033 - 2116

num = int(input())
inputList = []
for i in range(num):
    inputData = input()
    inputList.append(inputData)
discount = int(input())
data = []
for d in inputList:
    data_split = d.split(" ")
    data.append({
        "name": data_split[0],
        "price": float(data_split[1]),
        "qty": int(data_split[2]),
        "subtotal": float(data_split[1])*int(data_split[2]),
        "total": round((float(data_split[1])*int(data_split[2]))*(discount/100),1)
    })
    
total = sum(x["total"] for x in data)
avg = round(total/num,1)
maxD = max(data, key=lambda d: d["total"])
minD = min(data, key=lambda d: d["total"])

print( "=== Summary ===" )
print(f"總人數: {num}\n折扣: {discount}%\n總金額: {total}\n平均: {avg}")
print( f"最高: {maxD["name"]} {maxD["total"]}\n最低: {minD["name"]} {minD["total"]}" )
