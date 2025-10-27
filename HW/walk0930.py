# 健走日誌統計器

import re
from datetime import datetime 

pattern = r"^\d{4}-\d{2}-\d{2},\d+,[a-z]+"
data = []
total_steps = 0
count = 0
happy_days = 0
happy_steps = 0
sad_days = 0
sad_steps = 0
tired_days = 0
tired_steps = 0
highest = {
    "date":"",
    "steps":0
}
lowest = {
    "date":"",
    "steps":None
}

# 確認日期存在

def checkDate(date):
    try:
        datetime.strptime( date, "%Y-%m-%d" )
        return True
    except ValueError:
        return False


# 輸入

print("健走日誌：請輸入日期,步數,心情\n格式為'2025-09-30,9487,happy'\n輸入空行或'END'結束輸入\n心情：happy,sad,tired")
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
    elif any(item["date"] == data_split[0] for item in data):
        if input("此日期已有紀錄，是否覆蓋之前的紀錄？(Y/N)").upper() == "Y":
            for i in data:
                if i["date"] == data_split[0]:
                    data.remove(i)
        else:
            continue
    data.append({
                "date": data_split[0],
                "steps": int(data_split[1]),
                "mood": data_split[2].lower()
            })
            

# 計算

for i in range(len(data)):
    total_steps += data[i]["steps"]

    if data[i]["steps"] > highest["steps"]:
        highest["date"] = data[i]["date"]
        highest["steps"] = data[i]["steps"]
    if lowest["steps"] is None or data[i]["steps"] < lowest["steps"]:
        lowest["date"] = data[i]["date"]
        lowest["steps"] = data[i]["steps"]

    if data[i]["steps"] >= 8000:
        count += 1
    
    if data[i]["mood"] == "happy":
        happy_days += 1
        happy_steps += data[i]["steps"]
    elif data[i]["mood"] == "sad":
        sad_days += 1
        sad_steps += data[i]["steps"]
    elif data[i]["mood"] == "tired":
        tired_days += 1
        tired_steps += data[i]["steps"]


# 輸出

print( f"《 統計結果 》\n總天數：{len(data)}天\n總步數：{total_steps}步\n平均步數：{round(total_steps/len(data) if len(data) != 0 else 0)}步" )
print( f"最高步數：{highest['steps']}步 日期：{highest['date']}")
print( f"最低步數：{lowest['steps'] if lowest['steps'] is not None else 0}步 日期：{lowest['date']}")
print( f"達標日數：{count}天")
print( f"Happy天數：{happy_days}天 平均步數：{round(happy_steps/happy_days if happy_days != 0 else 0)}步")
print( f"Sad天數：{sad_days}天 平均步數：{round(sad_steps/sad_days if sad_days != 0 else 0)}步")
print( f"Tired天數：{tired_days}天 平均步數：{round(tired_steps/tired_days if tired_days != 0 else 0)}步")
