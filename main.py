import tkinter as tk
from tkinter import messagebox
from pynput import mouse, keyboard
import threading
import time

# =====================
# 설정
# =====================
recording = False
events = []

# 컨트롤러
mouse_controller = mouse.Controller()
key_controller = keyboard.Controller()

# =====================
# 이벤트 처리
# =====================
def on_click(x, y, button, pressed):
    global recording
    if recording:
        events.append(("mouse", button.name, pressed, time.time()))

def on_press(key):
    global recording
    if recording:
        try:
            events.append(("key", key.char, True, time.time()))
        except AttributeError:
            events.append(("key", str(key), True, time.time()))

def on_release(key):
    global recording
    if recording:
        try:
            events.append(("key", key.char, False, time.time()))
        except AttributeError:
            events.append(("key", str(key), False, time.time()))

# =====================
# 리스너 시작
# =====================
mouse_listener = mouse.Listener(on_click=on_click)
keyboard_listener = keyboard.Listener(on_press=on_press, on_release=on_release)
mouse_listener.start()
keyboard_listener.start()

# =====================
# 버튼 함수
# =====================
def toggle_record():
    global recording
    recording = not recording
    status_label.config(text=f"Recording: {'ON' if recording else 'OFF'}")

def playback():
    if len(events) == 0:
        messagebox.showinfo("InputFlow", "No events recorded.")
        return

    status_label.config(text="Playback: Running")
    start_time = events[0][3]
    for e in events:
        type_, key_or_btn, pressed, tstamp = e
        time.sleep(tstamp - start_time)
        start_time = tstamp

        if type_ == "mouse":
            btn = getattr(mouse.Button, key_or_btn)
            if pressed:
                mouse_controller.press(btn)
            else:
                mouse_controller.release(btn)
        elif type_ == "key":
            try:
                if len(key_or_btn) == 1:  # 일반 문자
                    if pressed:
                        key_controller.press(key_or_btn)
                    else:
                        key_controller.release(key_or_btn)
                else:  # 특수키
                    key_attr = getattr(keyboard.Key, key_or_btn.replace("Key.", ""))
                    if pressed:
                        key_controller.press(key_attr)
                    else:
                        key_controller.release(key_attr)
            except Exception:
                pass
    status_label.config(text="Playback: Done")

def quit_app():
    mouse_listener.stop()
    keyboard_listener.stop()
    root.destroy()

# =====================
# GUI 구성
# =====================
root = tk.Tk()
root.title("InputFlow")

record_btn = tk.Button(root, text="Toggle Recording", width=20, command=toggle_record)
record_btn.pack(pady=10,padx=80)

play_btn = tk.Button(root, text="Playback", width=20, command=playback)
play_btn.pack(pady=10,padx=80)

quit_btn = tk.Button(root, text="Quit", width=20, command=quit_app)
quit_btn.pack(pady=10,padx=80)

status_label = tk.Label(root, text="Recording: OFF", fg="blue")
status_label.pack(pady=10,padx=80)

root.mainloop()
