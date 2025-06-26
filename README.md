# Typing Speed Test Application

## Overview

This is a Python-based GUI application developed using Tkinter to help users practice and test their typing speed and accuracy. The program guides the user through different levels of difficulty (sentences, paragraphs, and timed tests) and tracks progress, accuracy, and speed.

## Features

### User Journey & Stage Selection
- At launch, the user selects whether to begin with **sentences** or **paragraphs**.
- If **sentences** are selected, another choice is shown: **short** or **long** sentences.
- Based on selection:
  - **Short Sentences** Path: 4 stages
    1. Short Sentences (10 sentences)
    2. Long Sentences (4 sentences)
    3. Paragraphs (6–7 paragraphs)
    4. Timed Paragraphs (6–7 with 100-second timer each)
  - **Long Sentences** Path: 3 stages
    1. Long Sentences (10 sentences)
    2. Paragraphs (6–7 paragraphs)
    3. Timed Paragraphs (6–7 with 100-second timer each)

### Test Logic & Typing Interaction
- Timer starts automatically during timed stages.
- Real-time color-coded feedback (Green for correct, Red for incorrect).
- Disables copy/paste functionality including right-click on Windows/macOS.
- Users can use the cursor to edit incorrect parts manually.
- Test only progresses after clicking **Next Sentence**.
- Mandatory 100% accuracy to proceed is removed. Users may advance with any accuracy.

### Progress & Feedback
- Progress Tracker is visible at the top-left corner, showing stage progress.
- Real-time timer display during timed mode.
- At the end of the test:
  - Shows average WPM (Words Per Minute) and average accuracy.
  - Pop-up message:
    - If passed with high accuracy: “Congratulations, you have passed the typing test!”
    - If not: “You did well, but you should practice more.”

### Interactive Prompts
- Upon selecting **Start**, prompts guide users through the selection path.
- An explanation box appears describing all stages based on the chosen path.

## Technologies Used
- Python
- Tkinter

## File Structure
- `main.py` – Main GUI application
- `sentences.txt` – Contains short practice sentences
- `long_sentences.txt` – Contains long-form sentences
- `paragraphs.txt` – Contains paragraphs for paragraph-based and timed tests

## Setup Instructions

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/typing-speed-test.git
   cd typing-speed-test
   ```

2. Ensure you have Python 3 installed.

3. Install Tkinter (if not already installed):
   ```bash
   pip install tk
   ```

4. Run the app:
   ```bash
   python main.py
   ```

## Author

Developed by Sneha Gupta