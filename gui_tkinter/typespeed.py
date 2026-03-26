import time
import tkinter as tk
from tkinter import messagebox
import random

root = tk.Tk()
root.title("Type Speed Test")
root.geometry("900x400")

target_text_list = [
    "Now we have devised robots that are much more complicated than.",
    "Switzerland is the most peaceful country in the world. Although.",
    "The sun has a family of other planets which keep circling about."
]

target_text = random.choice(target_text_list)
current_idx = 0
start_time = 0
wrong_types = 0
correct_types = 0
characters_not_typed = 0

type_frame = tk.Frame(root, padx=20, pady=20)
type_frame.pack(side=tk.LEFT, fill=tk.Y)

timer_frame = tk.Frame(root, padx=20, pady=20)
timer_frame.pack(side=tk.RIGHT, fill=tk.Y)

display_text = tk.Text(type_frame, font=('Helvetica', 12),
                       height=5, width=60, wrap="word")
scrollbar = tk.Scrollbar(type_frame, command=display_text.yview)
display_text.configure(yscrollcommand=scrollbar.set)
display_text.insert("1.0", target_text)
display_text.config(state="disabled")
display_text.grid(row=0, column=0, pady=0, padx=0, sticky="nsew")
scrollbar.grid(row=0, column=1, sticky="ns")

display_text.tag_configure("correct", foreground="green")
display_text.tag_configure("wrong", foreground="red")
display_text.tag_configure("current", background="yellow")

seconds = tk.StringVar(value='00')
remaining_seconds = tk.StringVar(value='60')
timer_running = False  # Flag to prevent multiple timers starting

seconds_label = tk.Label(
    timer_frame, textvariable=seconds, font=('Helvetica', 44))
col1_label = tk.Label(timer_frame, text="Seconds: ", font=('Helvetica', 24))

col1_label.grid(row=2, column=0)
seconds_label.grid(row=2, column=1)

remaining_seconds_label = tk.Label(
    timer_frame, textvariable=remaining_seconds, font=('Helvetica', 10))
col1_left_label = tk.Label(
    timer_frame, text="Remaining Time: ", font=('Helvetica', 8))

col1_left_label.grid(row=3, column=0)
remaining_seconds_label.grid(row=3, column=1)

typed_text = tk.StringVar()
typed_text_entry = tk.Text(type_frame, font=(
    'Helvetica', 12), height=5, width=60, wrap="word")
typed_text_entry_scrollbar = tk.Scrollbar(
    type_frame, command=typed_text_entry.yview)
typed_text_entry.configure(yscrollcommand=typed_text_entry_scrollbar.set)
typed_text_entry.insert("1.0", typed_text.get())
typed_text_entry.grid(row=1, column=0, pady=20, sticky="nsew")
typed_text_entry_scrollbar.grid(row=1, column=1, sticky="ns")
typed_text_entry.focus_set()


def update_timer():
    global current_idx, characters_not_typed
    if timer_running:
        now = time.time()
        total_seconds_passed = now - start_time
        elapsed_time = int(total_seconds_passed)
        remaining_time = max(0, int(60 - total_seconds_passed))

        seconds.set(f"{elapsed_time:02d}")
        remaining_seconds.set(f"{remaining_time:02d}")

        if remaining_time < 0:
            characters_not_typed = len(target_text) - current_idx
            stop_test()
            return

        root.after(1000, update_timer)


def stop_test():
    global timer_running, characters_not_typed
    if not timer_running:
        return  # Prevent double-triggering
    timer_running = False

    typed_text_entry.config(state="disabled")

    final_now = time.time()
    total_time_seconds = final_now - start_time
    total_time_minutes = total_time_seconds / 60

    characters_not_typed = len(target_text) - current_idx

    wpm = (correct_types / 5) / \
        total_time_minutes if total_time_minutes > 0 else 0

    final_message = f"Final Speed: {round(wpm)} WPM\n\n"
    if correct_types > 0:
        final_message += f"Correct Characters: {correct_types}\n"
    if wrong_types > 0:
        final_message += f"Wrong Characters: {wrong_types}\n"
    if characters_not_typed > 0:
        final_message += f"Remaining: {characters_not_typed}\n"

    messagebox.showinfo("Test Finished", final_message)


def on_keypress(event):
    global timer_running, start_time, current_idx, wrong_types, correct_types

    # Filter out system keys (Shift, Caps, etc.)
    # We only care about keys that have a 'char' and aren't control characters
    if not event.char or ord(event.char) < 32:
        return

    if not timer_running:
        timer_running = True
        start_time = time.time()
        update_timer()

    typed_char = event.char

    if current_idx < len(target_text):
        display_text.tag_remove("current", f"1.{current_idx}")

        if typed_char == target_text[current_idx]:
            display_text.tag_add("correct", f"1.{current_idx}")
            correct_types += 1
        else:
            display_text.tag_add("wrong", f"1.{current_idx}")
            wrong_types += 1

        current_idx += 1

        if current_idx == len(target_text):
            stop_test()
        else:
            display_text.tag_add("current", f"1.{current_idx}")


typed_text_entry.bind("<Key>", on_keypress)

# Initial highlight for the first character
display_text.tag_add("current", "1.0")

root.lift()
root.attributes('-topmost', True)
root.after(200, lambda: root.attributes('-topmost', False))

root.mainloop()
