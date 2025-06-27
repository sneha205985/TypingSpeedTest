import tkinter as tk
from tkinter import messagebox, simpledialog
import random
import time

# Load short sentences
with open("sentences.txt", "r") as f:
    SHORT_SENTENCES = [line.strip() for line in f if line.strip()]

# Load long sentences
with open("LongSentences.txt", "r") as f:
    LONG_SENTENCES = [line.strip() for line in f if line.strip()]

# Load paragraphs
with open("paragraphs.txt", "r") as f:
    PARAGRAPHS = [para.strip() for para in f.read().split("\n\n") if para.strip()]

SENTENCE_LIMIT = 10
LongSentence_Limit=4
PARAGRAPH_LIMIT = 6
TIMED_LIMIT = 7
TIMER_DURATION = 110  # for stage 4

class TypingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Typing Speed Test")
        self.root.geometry("850x600")
        self.root.configure(bg="white")

        self.stage = None
        self.path = []
        self.text_to_type = ""
        self.start_time = None
        self.timer_running = False
        self.remaining_time = TIMER_DURATION
        self.correctly_typed = False
        self.congrats_shown = False

        self.short_count = 0
        self.long_count = 0
        self.para_count = 0
        self.timed_count = 0

        self.total_stages = 0
        self.progress_label = tk.Label(root, text="", font=("Helvetica", 24), fg="black", bg="white")
        #self.progress_label.place(x=10, y=10)

        self.title_label = tk.Label(root, text="Typing Speed Test", font=("Helvetica", 20, "bold"), bg="white")
        self.title_label.pack(pady=10)

        self.display = tk.Text(root, height=5, width=90, font=("Courier", 14), wrap=tk.WORD, bg="white", fg="blue")
        self.display.pack(pady=10)
        self.display.config(state=tk.DISABLED)

        self.entry = tk.Text(root, height=5, width=90, font=("Courier", 14), wrap=tk.WORD, bg="white", fg="black", insertbackground="black")
        self.entry.pack()
        self.entry.bind("<KeyRelease>", self.on_typing)
        self.entry.bind("<Return>", lambda e: self.end_test())

        # Disable copy-paste
        for seq in ("<Control-v>", "<Control-V>", "<Command-v>", "<Command-V>",
                    "<Button-2>", "<Button-3>", "<Control-Insert>", "<Shift-Insert>",
                    "<Control-c>", "<Control-C>", "<Command-c>", "<Command-C>"):
            self.entry.bind(seq, lambda e: "break")

        self.timer_label = tk.Label(root, text="", font=("Helvetica", 14), fg="blue", bg="white")
        self.timer_label.pack(pady=5)

        self.button_frame = tk.Frame(root, bg="white")
        self.button_frame.pack(pady=10)

        self.start_button = tk.Button(self.button_frame, text="Start", command=self.begin_test, width=12)
        self.start_button.grid(row=0, column=0, padx=10)

        self.check_button = tk.Button(self.button_frame, text="Check", command=self.end_test, width=12)
        self.check_button.grid(row=0, column=1, padx=10)

        self.reset_button = tk.Button(self.button_frame, text="Reset", command=self.reset_progress, width=12)
        self.reset_button.grid(row=0, column=2, padx=10)

        self.next_button = tk.Button(self.button_frame, text="Next", command=self.next_sentence, width=12)
        self.next_button.grid(row=0, column=3, padx=10)

        self.progress_label.pack(pady=5)

        self.result_label = tk.Label(root, text="", font=("Helvetica", 14), fg="green", bg="white")
        self.result_label.pack(pady=10)

    def begin_test(self):
        initial_choice = messagebox.askquestion("Start Test", "Do you want to begin with sentences?")
        if initial_choice == "yes":
            style = messagebox.askquestion("Sentence Type", "Do you want to start with short sentences?")
            if style == "yes":
                self.path = ["short", "long", "paragraph", "timed"]
                messagebox.showinfo("Test Plan", 
                    "This test includes 4 stages:\n1. Short Sentences (10)\n2. Long Sentences (4)\n3. Paragraphs (6-7)\n4. Timed Paragraphs (6-7)")
            else:
                self.path = ["long", "paragraph", "timed"]
                messagebox.showinfo("Test Plan", 
                    "This test includes 3 stages:\n1. Long Sentences (10)\n2. Paragraphs (6-7)\n3. Timed Paragraphs (6-7)")
        else:
            self.path = ["paragraph", "timed"]
            messagebox.showinfo("Test Plan", 
                "This test includes 2 stages:\n1. Paragraphs (6-7)\n2. Timed Paragraphs (6-7)")
        self.stage = self.path[0]
        self.start_test()

    def get_next_text(self):
        if self.stage == "short":
            return random.choice(SHORT_SENTENCES)
        elif self.stage == "long":
            return random.choice(LONG_SENTENCES)
        else:
            return random.choice(PARAGRAPHS)

    def start_test(self):
        self.correctly_typed = False
        self.entry.config(state=tk.NORMAL)
        self.entry.delete("1.0", tk.END)
        self.text_to_type = self.get_next_text()
        self.display.config(state=tk.NORMAL)
        self.display.delete("1.0", tk.END)
        self.display.insert(tk.END, self.text_to_type)
        self.display.config(state=tk.DISABLED)
        self.start_time = time.time()
        self.result_label.config(text="")
        if self.stage == "timed":
            self.remaining_time = TIMER_DURATION
            self.timer_running = True
            self.update_timer()
        self.update_progress()

    def on_typing(self, event):
        typed_text = self.entry.get("1.0", tk.END).strip()
        self.display.tag_remove("correct", "1.0", tk.END)
        self.display.tag_remove("incorrect", "1.0", tk.END)
        for i, char in enumerate(typed_text):
            if i < len(self.text_to_type):
                tag = "correct" if char == self.text_to_type[i] else "incorrect"
                self.display.tag_add(tag, f"1.{i}", f"1.{i+1}")
        self.display.tag_config("correct", foreground="green")
        self.display.tag_config("incorrect", foreground="red")

    def end_test(self):
        self.timer_running = False
        elapsed = max(time.time() - self.start_time, 1)
        typed = self.entry.get("1.0", tk.END).strip()
        wpm = round((len(typed.split()) / elapsed) * 60)
        correct = sum(1 for i in range(min(len(typed), len(self.text_to_type))) if typed[i] == self.text_to_type[i])
        accuracy = round((correct / len(self.text_to_type)) * 100)
        self.result_label.config(text=f"Time: {int(elapsed)}s | WPM: {wpm} | Accuracy: {accuracy}%")
        self.entry.config(state=tk.DISABLED)
        self.correctly_typed = True

        if self.stage == "short":
            self.short_count += 1
            if self.short_count >= 10:
                self.stage = "long"
        elif self.stage == "long":
            self.long_count += 1
            if self.long_count >= 4:
                self.stage = "paragraph"
        elif self.stage == "paragraph":
            self.para_count += 1
            if self.para_count >= 6:
                self.stage = "timed"
        elif self.stage == "timed":
            self.timed_count += 1
            if self.timed_count >= 6:
                if accuracy == 100:
                    messagebox.showinfo("Congratulations", "You have successfully passed the test!")
                else:
                    messagebox.showinfo("Keep Practicing", f"You couldn't complete the test within the time limit.\nNeed to speed up your typing.")
                self.reset_progress()

        self.update_progress()

    def next_sentence(self):
        self.start_test()

    def update_timer(self):
        if self.remaining_time > 0 and self.timer_running:
            self.timer_label.config(text=f"Time Left: {self.remaining_time}s")
            self.remaining_time -= 1
            self.root.after(1000, self.update_timer)
        elif self.timer_running:
            self.timer_label.config(text="Time's up!")
            self.end_test()

    def update_progress(self):
        text = f"Progress â Short: {self.short_count}/10 | Long: {self.long_count}/4 | Para: {self.para_count}/6 | Timed: {self.timed_count}/6"
        self.progress_label.config(text=text)

    def reset_progress(self):
        self.short_count = 0
        self.long_count = 0
        self.para_count = 0
        self.timed_count = 0
        self.stage = None
        self.path = []
        self.result_label.config(text="")
        self.timer_label.config(text="")
        self.display.config(state=tk.NORMAL)
        self.display.delete("1.0", tk.END)
        self.display.config(state=tk.DISABLED)
        self.entry.config(state=tk.NORMAL)
        self.entry.delete("1.0", tk.END)
        self.progress_label.config(text="")

if __name__ == "__main__":
    root = tk.Tk()
    app = TypingApp(root)
    root.mainloop()
