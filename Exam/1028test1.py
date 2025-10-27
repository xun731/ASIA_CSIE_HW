total = int(input())
def InputData():
    data_input = input()
    data_split = data_input.split(" ")
    if len(data_split) != total:
        print("資料數量錯誤，請重新輸入：", end="")
        InputData()
    return data_split
data_split = InputData()
T = float(input())

data = list(map(float, data_split))
avg = round(sum(data)/total,1)
maxD = max(data)
maxN = data.index(maxD)
minD = min(data)
minN = data.index(minD)
buckets = {
    "<18":0,
    "18-25":0,
    "25-30":0,
    ">=30":0
}
hot_list = []
for d in data:
    if d >= 30:
        buckets[">=30"] += 1
    elif d >= 25 and d < 30:
        buckets["25-30"] += 1    
    elif d >= 18 and d < 25:
        buckets["18-25"] += 1
    else:
        buckets["<18"] += 1
    if d > T:
        hot_list.append(d)
  
print( f"Total: {total}\nAvg: {avg}\nMax: {maxD} @ {maxN}\nMin: {minD} @ {minN}" )
print( "=== Buckets ===" )
print(buckets)
print( "=== Alerts ===" )
print( f"Threshold: {T}\nHotCount: {len(hot_list)}\nHotList: {hot_list}" )

# 26min
# 37min
