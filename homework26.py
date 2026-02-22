from time import sleep, time
from datetime import datetime
from pypresence.presence import Presence
import config as c

p = Presence(c.CLIENT_ID)
p.connect()

# 记录程序启动时间（或者本轮开始时间）
start_time = time()           # 用 time() 更轻量
# start_time = datetime.now().timestamp()  # 也可以


def update(name, l1, l2=None):
    now = datetime.now()
    elapsed = int(time() - start_time)  # 已过去多少秒

    p.update(
        name=name,
        state=l2,
        details=l1,
        start=int(start_time),               # 从程序/本轮开始计时
        large_image="dc_pencil",
        large_text=f"已肝了 {elapsed//60}分 {elapsed % 60}秒 ｜ 开始: {now.strftime('%m-%d %H:%M')}",
        buttons=[
            {'label': '加入思维服务器', 'url': 'https://discord.gg/Vvex8Z6zKs'},
            {'label': '速速观战', 'url': 'https://discord.com/channels/1061629481267245086/1385943585597292706'}
        ]
    )


print("Rich Presence 已启动，按 Ctrl+C 退出")

try:
    name = input("Name: ")
    if not name:
        raise ValueError("必须提供一个名称！")
    while True:
        details = input("Line 1|2: ").strip().split('|', 1)
        if not details:
            continue
        if len(details) > 1:
            update(name, details[0], details[1])
        else:
            update(name, details[0])
        sleep(12)   # 强烈建议至少 sleep 10–13 秒，避免触发频率限制

except KeyboardInterrupt:
    print("\n正在关闭...")
    try:
        p.clear()
        p.close()
    except:
        pass
    print("已关闭。")
except Exception as e:
    print(f"发生错误: {e}")
    p.close()
