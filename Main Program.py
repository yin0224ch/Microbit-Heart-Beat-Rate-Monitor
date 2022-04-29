from microbit import *
import utime as time
from ssd1306 import initialize, clear_oled
from ssd1306_text import add_text

gender = 0
threshold = 550
count = 0
sample = 0
bpm = 0
age = 0
previous = 0
window = []
values = []
bpm_store = []
beat = False
mean_hr = 0


mean = lambda datalist: sum(datalist) / len(datalist)


initialize()
clear_oled()
add_text(0, 0, "Button A", 1)
add_text(0, 1, " - Start", 1)

while True:
    if button_b.was_pressed():
        continue
    if button_a.was_pressed():
        clear_oled()
        add_text(0, 0, "Age:", 1)
        add_text(0, 1, "18-35", 1)
        add_text(0, 2, "Yes - A", 1)
        add_text(0, 3, " No - B", 1)
        while True:
            if button_a.was_pressed():
                age = 1
                break
            elif button_b.was_pressed():
                add_text(0, 1, "36-55", 1)
                while True:
                    if button_a.was_pressed():
                        age = 2
                        break
                    if button_b.was_pressed():
                        age = 3
                        break
                break
        break

clear_oled()
add_text(0, 0, "Male - A", 1)
add_text(0, 1, "Female - B", 1)
while True:
    if button_a.was_pressed():
        gender = 1
        break
    if button_b.was_pressed():
        gender = 2
        break
clear_oled()

display.scroll("Running...", wait=False, loop=True)
while True:
    window.append(pin1.read_analog())
    avg = round(mean(window))
    values.append(avg)
    if len(window) == 11:
        window.pop(0)
    if beat is False and avg >= threshold + 10:
        beat = True
        count += 1
        if count == 1:
            t1 = time.ticks_ms()
        if count == 11:
            clear_oled()
            T = time.ticks_ms() - t1
            previous = bpm
            bpm = round(600 * 1000 / (T))
            add_text(0, 0, "Heart Rate:", 1)
            add_text(0, 1, str(bpm) + " bpm", 1)
            add_text(0, 2, "Previous:", 1)
            if previous != 0:
                add_text(0, 3, str(previous) + " bpm", 1)
                bpm_store.append(previous)
            else:
                add_text(0, 3, "No Record", 1)
            count = 0
    elif beat is True and avg <= threshold - 10:
        beat = False
    sample += 1
    if sample == 125:
        threshold = mean(values)
        values = []
        sample = 0
    if len(bpm_store) == 5:
        clear_oled()
        break
    sleep(20)
mean_hr = mean(bpm_store)
display.clear()
add_text(0, 0, "Your Heart", 1)
add_text(0, 1, "Rate(avg) is:", 1)
add_text(0, 2, str(mean_hr), 1)
if gender == 1:
    if mean_hr < 50 + age / 2:
        add_text(0, 3, "Too Low!", 1)
    elif mean_hr < 84 + age / 2:
        add_text(0, 3, "Average!", 1)
    else:
        add_text(0, 3, "Too High!", 1)
else:
    if mean_hr < 54 + age / 2:
        add_text(0, 3, "Too Low!", 1)
    elif mean_hr < 85 + age / 2:
        add_text(0, 3, "Normal!", 1)
    else:
        add_text(0, 3, "Too High!", 1)
