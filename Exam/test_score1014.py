count = 0
highest = None
lowest = None
data = []
levelA = 0
levelB = 0
levelC = 0
levelD = 0
levelE = 0
total = 0
while True:
    try:
        score_input = int(input())
    except ValueError:
        print("Invalid")
        continue
    if (score_input < 0 or score_input > 100) and score_input != -1:
        print("Invalid")
        continue
    elif score_input == -1:
        break
    count += 1
    if highest == None or score_input > highest:
        highest = score_input
    if lowest == None or score_input < lowest:
        lowest = score_input
    if score_input <= 100 and score_input >= 90:
        levelA += 1
    elif score_input <= 89 and score_input >= 80:
        levelB += 1
    elif score_input <= 79 and score_input >= 70:
        levelC += 1
    elif score_input <= 69 and score_input >= 60:
        levelD += 1
    else:
        levelE += 1
    total += score_input
    data.append(score_input)

# Count: <N>
# Avg: <平均>
# Max: <最高>
# Min: <最低>
# A: <數量>, B: <數量>, C: <數量>, D: <數量>, E: <數量>

print( f"Count: {count}\nAvg: {round(total/len(data),2)}\nMax: {highest}\nMin: {lowest}" )
print( f"A: {levelA}, B: {levelB}, C:{levelC}, D: {levelD}, E:{levelE}" )
