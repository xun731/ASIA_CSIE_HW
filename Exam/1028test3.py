# 2227 - 1052

category = {
    "car":40,
    "moto":20,
}
num = int(input())
dataList = []
for i in range(num):
    dataInput = input().split(" ")
    dataList.append({
        "category": dataInput[0].lower(),
        "hour": int(dataInput[1]),
        "fee": category.get(dataInput[0].lower())*int(dataInput[1])
    })

total = sum(d["fee"] for d in dataList)
maxF = max(dataList, key=lambda d: d["fee"])
minF = min(dataList, key=lambda d: d["fee"])

for d in dataList:
    print(f"Fee: {d["fee"]}")
print("=== Summary ===")
print(f"TotalCars: {num}\nTotalFee: {total}\nMaxFee: {maxF["fee"]}\nMinFee: {minF["fee"]}")
