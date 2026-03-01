from time import sleep, time
from datetime import datetime
from pypresence.presence import Presence
import config as c

p = Presence(c.CLIENT_ID)
p.connect()

# 记录程序启动时间（或者本轮开始时间）
start_time = time()


print("Rich Presence 已启动，按 Ctrl+C 退出")
AVAILABLE = "Available: n (name), 1 (line 1), 2 (line 2), s (status l1|l2), l (label), u (url), b (label|url)"

n = l1 = l2 = l = u = ''

try:
    n = input("Name: ")
    if not n:
        raise ValueError("必须提供一个名称！")
    print(AVAILABLE)
    while True:
        inputed = input(">> ").strip()
        if len(inputed) <= 2:
            continue
        inp = inputed[2:]
        if not inp:
            inp = None
        match inputed[:1]:
            case 'n':
                n = inp
            case '1':
                l1 = inp
            case '2':
                l2 = inp
            case 's':
                if inp:
                    lines = inp.split('|', 1)
                    if len(lines) > 1:
                        l2 = lines[1]
                    l1 = lines[0]
                else:
                    l1 = l2 = None
            case 'l':
                l = inp
            case 'u':
                u = inp
            case 'b':
                if inp:
                    lines = inp.split('|', 1)
                    if len(lines) > 1:
                        u = lines[1]
                    l = lines[0]
                else:
                    l1 = l2 = None
            case _:
                print(AVAILABLE)
                continue
        if n and (l1 or l2):
            if l and u:
                p.update(
                    name=n,
                    details=l1 or None,  # 1
                    state=l2 or None,  # 2
                    start=int(start_time),               # 从程序/本轮开始计时
                    large_image="head_subqq",
                    buttons=[
                        {'label': l, 'url': u},
                        {'label': '我也要状态显示!', 'url': 'https://github.com/wyf9/pypresence-ws'}
                    ]
                )
            else:
                p.update(
                    name=n,
                    details=l1 or None,  # 1
                    state=l2 or None,  # 2
                    start=int(start_time),               # 从程序/本轮开始计时
                    large_image="head_subqq",
                    buttons=[
                        {'label': '我也要状态显示!', 'url': 'https://github.com/wyf9/pypresence-ws'}
                    ]
                )
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
