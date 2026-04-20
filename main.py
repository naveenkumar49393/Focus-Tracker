import time
import json
import os
from pynput import keyboard

keystrokes = 0
start_time = None
last_key_time = None
idle_time = 0


def on_press(key):
    global keystrokes, last_key_time, idle_time

    current_time = time.time()

    if last_key_time:
        gap = current_time - last_key_time
        if gap > 3:
            idle_time += gap

    keystrokes += 1
    last_key_time = current_time


def load_sessions():
    if not os.path.exists("sessions.json"):
        return []
    try:
        with open("sessions.json", "r") as f:
            return json.load(f)
    except:
        return []


def save_session(report):
    data = load_sessions()
    data.append(report)

    with open("sessions.json", "w") as f:
        json.dump(data, f, indent=4)


def generate_report():
    duration = time.time() - start_time
    active_time = duration - idle_time

    kpm = (keystrokes / duration) * 60 if duration > 0 else 0
    focus_score = (active_time / duration) * 100 if duration > 0 else 0

    return {
        "keystrokes": keystrokes,
        "duration_sec": round(duration, 2),
        "idle_time_sec": round(idle_time, 2),
        "active_time_sec": round(active_time, 2),
        "kpm": round(kpm, 2),
        "focus_score": round(focus_score, 2)
    }


print("🚀 Focus session started (Press ESC or Ctrl+C to stop)")
start_time = time.time()

with keyboard.Listener(on_press=on_press) as listener:
    try:
        listener.join()
    except KeyboardInterrupt:
        pass

report = generate_report()

print("\n📊 SESSION REPORT")
print("-" * 30)
for k, v in report.items():
    print(f"{k:20}: {v}")

save_session(report)

print("\n💾 Session saved successfully!")
