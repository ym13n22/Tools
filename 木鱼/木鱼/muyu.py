import sys
import time
import threading
import pygame
import keyboard
from pystray import Icon, Menu, MenuItem
from PIL import Image, ImageDraw
import tkinter as tk
from tkinter import ttk

# =========================
# 状态
# =========================
running = True
paused = False

base_volume = 0.5     # 原始音量（你定义的 0.5）
user_volume = 1.0     # 用户调节倍率（0~2）
last_time = 0
cooldown = 0.05

# =========================
# 音频初始化
# =========================
pygame.mixer.init()
sound = pygame.mixer.Sound("muyu.mp3")

def apply_volume():
    """应用音量（核心逻辑）"""
    final_volume = base_volume * user_volume

    # pygame 上限是 1.0
    sound.set_volume(min(final_volume, 1.0))

    print(f"[音量] base={base_volume}, user={user_volume:.2f}, final={final_volume:.2f}")

# 初始化音量
apply_volume()

# =========================
# 键盘敲击
# =========================
def on_key(event):
    global last_time

    if paused or not running:
        return

    now = time.time()
    if now - last_time > cooldown:
        sound.play()
        last_time = now

# =========================
# 音量控制
# =========================
def set_user_volume(v):
    global user_volume
    user_volume = max(0.0, min(2.0, float(v)))
    apply_volume()

def volume_up():
    set_user_volume(user_volume + 0.1)

def volume_down():
    set_user_volume(user_volume - 0.1)

# =========================
# Tk 滑块窗口
# =========================
def open_volume_window():
    def on_change(val):
        set_user_volume(val)
        label.config(text=f"当前音量倍率: {float(val):.2f}")

    win = tk.Tk()
    win.title("木鱼音量调节")
    win.geometry("300x130")
    win.resizable(False, False)

    label = tk.Label(win, text=f"当前音量倍率: {user_volume:.2f}")
    label.pack(pady=5)

    slider = ttk.Scale(
        win,
        from_=0.0,
        to=2.0,
        orient="horizontal",
        command=on_change
    )
    slider.set(user_volume)
    slider.pack(fill="x", padx=20)

    win.mainloop()

# =========================
# 托盘图标
# =========================
def create_image():
    img = Image.new("RGB", (64, 64), "white")
    d = ImageDraw.Draw(img)

    # 木鱼外形
    d.ellipse((10, 10, 54, 54), fill=(120, 80, 40))
    d.ellipse((25, 25, 39, 39), fill=(80, 50, 30))

    return img

# =========================
# 托盘功能
# =========================
def toggle_pause(icon, item):
    global paused
    paused = not paused
    item.text = "继续敲击" if paused else "暂停敲击"

def quit_app(icon, item):
    global running
    running = False
    icon.stop()
    sys.exit()

def tray_menu(icon=None):
    return Menu(
        MenuItem(lambda text: f"音量倍率: {user_volume:.2f}", lambda: None, enabled=False),
        MenuItem("调节音量", lambda icon, item: threading.Thread(target=open_volume_window).start()),
        MenuItem("暂停敲击", toggle_pause),
        MenuItem("退出", quit_app)
    )

# =========================
# 托盘刷新（动态音量显示）
# =========================
def refresh_tray(icon):
    while running:
        icon.menu = tray_menu(icon)
        icon.update_menu()
        time.sleep(1)

# =========================
# 托盘线程
# =========================
def tray_worker():
    icon = Icon("muyu", create_image(), "电子木鱼", tray_menu())

    threading.Thread(target=refresh_tray, args=(icon,), daemon=True).start()

    icon.run()

# =========================
# 主程序
# =========================
def main():
    print("🪵 电子木鱼启动")

    # 键盘监听
    keyboard.on_press(on_key)

    # 快捷键调音量
    keyboard.add_hotkey("ctrl+up", volume_up)
    keyboard.add_hotkey("ctrl+down", volume_down)

    # 托盘
    threading.Thread(target=tray_worker, daemon=True).start()

    while running:
        time.sleep(0.5)

if __name__ == "__main__":
    main()