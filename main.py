import tkinter as tk
from tkinter import messagebox
import random
import time

# Load sentences
with open("sentences.txt", "r") as f:
    SENTENCES = [line.strip() for line in f if line.strip()]

# Load paragraphs
with open("paragraphs.txt", "r") as f:
    PARAGRAPHS = [para.strip() for para in f.read().split("\n\n") if para.strip()]

BEGINNER_LIMIT = 5
PARAGRAPH_LIMIT = 3
TIMED_LIMIT = 4
TIMER_DURATION = 75  # for stage 3

class TypingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Typing Speed Test")
        self.root.geometry("820x570")
        self.root.configure(bg="white")

        self.practice_count = 0
        self.paragraph_count = 0
        self.timed_count = 0
        self.stage = "beginner"
        self.text_to_type = ""
        self.start_time = None
        self.timer_running = False
        self.remaining_time = TIMER_DURATION
        self.correctly_typed = False
        self.congrats_shown = False

        # Progress Label (Top-Left Corner)
        self.progress_label = tk.Label(root, text="", font=("Helvetica", 12), fg="black", bg="white", anchor='w')
        self.progress_label.place(x=10, y=10)
        self.update_progress_label()

        self.title_label = tk.Label(root, text="Typing Speed Test", font=("Helvetica", 20, "bold"), bg="white")
        self.title_label.pack(pady=35)

        self.display = tk.Text(root, height=5, width=90, font=("Courier", 14), wrap=tk.WORD, bg="white", fg="blue")
        self.display.pack(pady=10)
        self.display.config(state=tk.DISABLED)

        self.entry = tk.Text(root, height=5, width=90, font=("Courier", 14), wrap=tk.WORD, bg="white", fg="black")
        self.entry.config(insertbackground="black")
        self.entry.pack()
        self.entry.bind("<KeyRelease>", self.on_typing)
        self.entry.bind("<Return>",lambda e: self.end_test())

        # Disable copy-paste
        for seq in ("<Control-v>", "<Control-V>", "<Command-v>", "<Command-V>",
                    "<Button-2>", "<Button-3>", "<Control-Insert>", "<Shift-Insert>",
                    "<Control-c>", "<Control-C>", "<Command-c>", "<Command-C>"):
            self.entry.bind(seq, lambda e: "break")

        self.timer_label = tk.Label(root, text="", font=("Helvetica", 14), fg="blue", bg="white")
        self.timer_label.pack(pady=5)

        self.button_frame = tk.Frame(root, bg="white")
        self.button_frame.pack(pady=10)

        self.start_button = tk.Button(self.button_frame, text="Start", command=self.start_test, width=12)
        self.start_button.grid(row=0, column=0, padx=10)

        self.check_button = tk.Button(self.button_frame, text="Check", command=self.end_test, width=12)
        self.check_button.grid(row=0, column=1, padx=10)

        self.reset_button = tk.Button(self.button_frame, text="Reset Progress", command=self.reset_progress, width=15)
        self.reset_button.grid(row=0, column=2, padx=10)

        self.next_button = tk.Button(self.button_frame, text="Next Sentence", command=self.next_sentence, width=15)
        self.next_button.grid(row=0, column=3, padx=10)

        self.result_label = tk.Label(root, text="", font=("Helvetica", 14), fg="green", bg="white")
        self.result_label.pack(pady=10)

    def update_progress_label(self):
        self.progress_label.config(
            text=f"Stage: {self.stage.capitalize()} | Sentences: {self.practice_count}/{BEGINNER_LIMIT} | "
                 f"Paragraphs: {self.paragraph_count}/{PARAGRAPH_LIMIT} | Timed: {self.timed_count}/{TIMED_LIMIT}"
        )

    def get_next_text(self):
        return random.choice(SENTENCES) if self.stage == "beginner" else random.choice(PARAGRAPHS)

    def start_test(self):
        if self.stage == "timed" and self.timed_count >= TIMED_LIMIT:
            return
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
        self.update_progress_label()
        if self.stage == "timed":
            self.remaining_time = TIMER_DURATION
            self.timer_running = True
            self.update_timer()

    def on_typing(self, event):
        typed_text = self.entry.get("1.0", tk.END).strip()
        self.display.tag_remove("correct", "1.0", tk.END)
        self.display.tag_remove("incorrect", "1.0", tk.END)
        for i, char in enumerate(typed_text):
            if i < len(self.text_to_type):
                if char == self.text_to_type[i]:
                    self.display.tag_add("correct", f"1.{i}", f"1.{i+1}")
                else:
                    self.display.tag_add("incorrect", f"1.{i}", f"1.{i+1}")
        self.display.tag_config("correct", foreground="green")
        self.display.tag_config("incorrect", foreground="red")

    def end_test(self):
        self.timer_running = False
        end_time = time.time()
        elapsed = max(end_time - self.start_time, 1)
        typed = self.entry.get("1.0", tk.END).strip()
        word_count = len(typed.split())
        wpm = round((word_count / elapsed) * 60)
        correct = sum(1 for i in range(min(len(typed), len(self.text_to_type))) if typed[i] == self.text_to_type[i])
        accuracy = round((correct / len(self.text_to_type)) * 100)

        self.result_label.config(text=f"Time: {int(elapsed)}s | WPM: {wpm} | Accuracy: {accuracy}%")

        if accuracy < 100:
            self.correctly_typed = False
            messagebox.showwarning("Try Again")
            return
        else:
            self.correctly_typed = True
            self.entry.config(state=tk.DISABLED)

        if self.stage == "beginner":
            self.practice_count += 1
            if self.practice_count >= BEGINNER_LIMIT:
                self.stage = "paragraph"
                messagebox.showinfo("Level Up", "You've completed beginner level!")

        elif self.stage == "paragraph":
            self.paragraph_count += 1
            if self.paragraph_count >= PARAGRAPH_LIMIT:
                self.stage = "timed"
                messagebox.showinfo("Level Up", "Now entering timed mode!")

        elif self.stage == "timed":
            self.timed_count += 1
            if self.timed_count >= TIMED_LIMIT and not self.congrats_shown:
                self.congrats_shown = True
                response = messagebox.askquestion("🎉 Congratulations!",
                    "🎉 Congratulations, you have passed the typing test!\nYou are good in typing now.\n\nDo you want to restart the test?")
                if response == "yes":
                    self.reset_progress()
                else:
                    self.root.destroy()

        self.update_progress_label()

    def next_sentence(self):
        if not self.correctly_typed:
            messagebox.showwarning("Not Allowed", "Please type the correct sentence before proceeding.")
            return
        self.start_test()

    def update_timer(self):
        if self.remaining_time > 0 and self.timer_running:
            self.timer_label.config(text=f"Time Left: {self.remaining_time}s")
            self.remaining_time -= 1
            self.root.after(1000, self.update_timer)
        elif self.timer_running:
            self.timer_label.config(text="Time's up!")
            self.end_test()

    def reset_progress(self):
        self.practice_count = 0
        self.paragraph_count = 0
        self.timed_count = 0
        self.stage = "beginner"
        self.correctly_typed = False
        self.congrats_shown = False
        self.result_label.config(text="")
        self.timer_label.config(text="")
        self.entry.config(state=tk.NORMAL)
        self.entry.delete("1.0", tk.END)
        self.display.config(state=tk.NORMAL)
        self.display.delete("1.0", tk.END)
        self.display.config(state=tk.DISABLED)
        self.update_progress_label()
        messagebox.showinfo("Reset", "Progress reset. You're back to beginner level.")

if __name__ == "__main__":
    root = tk.Tk()
    app = TypingApp(root)
    root.mainloop()
