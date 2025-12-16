import os,shutil
import csv,json
import sys,random
from datetime import datetime

class User:
    def __init__(self, username):
        self.username = username

        self.gacha_data = []
        self.gacha_state = {}

        self.folder_path = os.path.join(os.path.dirname(__file__), username)
        self.card_csv = os.path.join(self.folder_path, "card_log.csv")
        self.details_json = os.path.join(self.folder_path, "details.json")
        self.collection_json = os.path.join(os.path.dirname(__file__), "collection.json")


        with open(self.collection_json, "r", encoding="utf-8") as f:
            self.collection_data = json.load(f)

    def delete_account(self):
        while True:
            delete = input( f"是否確認要刪除'{self.username}'帳號(Y/N)，所有紀錄皆會消失且無法找回！！" ).upper()
            if delete in ['Y','N']:
                break
            else:
                print("請輸入'Y'或'N'")
                continue
        if delete == 'Y':
            shutil.rmtree(self.folder_path)
            print(f"已刪除帳號:{self.username}")
            return login()
        else:
            print("未刪除帳號")
            return self
        
    def create_gacha(self):
        with open(self.card_csv, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["date", "time", "card", "rarity"])
        self.gacha_state = {
            "rarity": {'SSR':0, 'SR':0, 'R':0},
            "total_pulls": 0,
            # 保底抽數0/80
            "pity": 0,
            "bag":{},
        }
        with open(self.details_json, "w", encoding="utf-8") as f:
            json.dump(self.gacha_state, f, ensure_ascii=False, indent=4)

    # 載入抽卡紀錄及詳細資料
    def load_gacha(self):
        with open(self.card_csv, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            self.gacha_data = list(reader) 

        with open(self.details_json, "r", encoding="utf-8") as f:
            self.gacha_state = json.load(f)
        
    # 儲存抽卡紀錄及詳細資料
    def save_gacha(self):
        with open(self.card_csv, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["date", "time", "card", "rarity"])
            writer.writeheader()
            writer.writerows(self.gacha_data)

        with open(self.details_json, "w", encoding="utf-8") as f:
            json.dump(self.gacha_state, f, ensure_ascii=False, indent=4)

# 登入(登出直接呼叫) ✓
def login():
    username = input("請登入您的帳號(輸入用戶名稱，輸入'0'離開):")
    if username.strip() in ["","0"] or username.isspace():
        finish()
    user = User(username)
    if os.path.isdir(user.folder_path):
        user.load_gacha()
        print( f"登入成功，歡迎{user.username}回來" )
    else:
        while True:
            create = input( f"未找到該帳號，請問是否以'{user.username}'為用戶名稱建立新帳號(Y/N)" ).upper()
            if create in ['Y','N']:
                break
            else:
                print("請輸入'Y'或'N'")
                continue
        if create == "Y":
            os.makedirs(user.folder_path, exist_ok=True)
            user.create_gacha()
            print( f"帳號建立成功，歡迎新用戶{user.username}" )
        else:
            return login()
    return user

# 查詢抽卡紀錄(包含平均出金、總抽數、總金數、距離下次保底抽數等等) ✓
def log():
    print( f"用戶名稱：{user.username}" )
    print( f"== 統計 ==\n總抽數：{user.gacha_state['total_pulls']}\n總SSR數量：{user.gacha_state['rarity']['SSR']}\n平均SSR抽數：{user.gacha_state["total_pulls"] / max(1, user.gacha_state["rarity"]["SSR"])}" )
    print( f"距離下次保底：{user.gacha_state['pity']}/80抽" )

    for d in user.gacha_data:
        print(f"{d["date"]} {d["time"]} - {d["rarity"]}．{d["card"]}")
    return

# 抽卡 ✓
def gacha():

    rarities = ["SSR", "SR", "R"]
    weights = [0.05, 0.25, 0.70]
    while True:
        pulls = int(input("請輸入要抽的抽數(1或10，0離開)："))
        if pulls in [1,10]:
            for i in range(pulls):

                now = datetime.now()

                if user.gacha_state["pity"] >= 80:
                    rarity = "SSR"
                else:
                    rarity = random.choices(rarities, weights=weights, k=1)[0]

                if rarity == "SSR":
                    user.gacha_state["pity"] = 0
                else:
                    user.gacha_state["pity"] += 1

                candidates = []
                for serie in user.collection_data:
                    for card in user.collection_data[serie]:
                        if card["rarity"] == rarity:
                            candidates.append(card)
                chosen = random.choice(candidates)
                print(f"{i+1}-{rarity}．{chosen["name"]}")

                user.gacha_state["total_pulls"] += 1
                user.gacha_state["rarity"][rarity] += 1

                user.gacha_state["bag"].setdefault(chosen["name"], 0)
                user.gacha_state["bag"][chosen["name"]] += 1
                user.gacha_data.append({
                    "date": now.strftime("%Y-%m-%d"),
                    "time": now.strftime("%H:%M:%S"),
                    "card": chosen["name"],
                    "rarity": rarity
                })
                user.save_gacha()
                
        elif pulls == 0:
            break
        else:
            print("暫不支持單抽或十連以外的抽數，請重新輸入")
    return

# 背包 ✓
def bag():
    for serie in user.collection_data.keys():
        print(f"-{serie}")
        for cards in user.collection_data[serie]:
            for name, quantity in user.gacha_state["bag"].items():
                if cards["name"] == name:
                    print( f"No.{cards['id']} - {cards['rarity']}．{cards['name']} ×{quantity}")
    return

# 圖鑑 ✓
def collection():
    
    print(f"輸入系列名稱查看詳細卡片：")
    for d in user.collection_data.keys():
        print(f"-{d}")
    serie = input()
    try:
        for d in user.collection_data[serie]:
            print( f"編號：{d['id']} 稀有度：{d['rarity']} 名稱：{d['name']}")
    except KeyError:
        print("無此系列")
    return

# 結束程式 ✓
def finish():
    print("下次見")
    sys.exit()

user = login()
menu = {
        1:log,
        2:gacha,
        3:bag,
        4:collection,
        5:login,
        0:finish
    }
while True:
    task = input("1) 查詢抽卡紀錄\n2) 抽卡\n3) 背包\n4) 圖鑑\n5) 登出\n6) 刪除帳號\n0) 離開\n請輸入功能(數字)：")
    try:
        task = int(task)
    except ValueError:
        print("請輸入數字")
        continue
    if task == 5:
        user = menu.get(task)()
    elif task == 6:
        user = user.delete_account()
    else:
        menu.get(task)()
