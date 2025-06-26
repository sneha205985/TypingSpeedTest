# Typing Speed Test - Python Tkinter Application

This project is a desktop-based Typing Speed Test application built with Python and Tkinter. It is designed to help users practice and improve their typing skills through progressive levels of difficulty and provides a structured and user-friendly interface.

## Features

•⁠  ⁠Three typing stages: Sentence Practice, Paragraph Practice, and Timed Test
•⁠  ⁠Requires 100% accuracy to proceed to the next sentence
•⁠  ⁠Real-time feedback using color indicators (green for correct, red for incorrect)
•⁠  ⁠Manual "Next Sentence" control to proceed
•⁠  ⁠Retry prompt for incorrect sentences
•⁠  ⁠Timer for the final stage (75 seconds duration)
•⁠  ⁠Visual cursor support for easier text correction
•⁠  ⁠Copy-paste and right-click context menu are disabled to ensure fair typing practice
•⁠  ⁠Final congratulatory message after successful completion of the timed test
•⁠  ⁠Options to restart or end the test after completion
•⁠  ⁠Reset progress functionality to return to beginner stage

## Project Structure


TypingSpeedTest/files:
----main.py             # Main GUI application logic
----sentences.txt       # Sentences used for the beginner stage
----paragraphs.txt      # Paragraphs used for paragraph and timed stages
----README.md           # Documentation


## How to Run

### Prerequisites

•⁠  ⁠Python 3.6 or higher
•⁠  ⁠Tkinter (usually bundled with Python)

### Steps

1.⁠ ⁠Download or clone the repository.
2.⁠ ⁠Ensure that ⁠ main.py ⁠, ⁠ sentences.txt ⁠, and ⁠ paragraphs.txt ⁠ are in the same directory.
3.⁠ ⁠Open a terminal and navigate to the project folder.
4.⁠ ⁠Run the application:

⁠ bash
python main.py
 ⁠

## Usage

1.⁠ ⁠Click the *Start* button to begin.
2.⁠ ⁠Type the displayed sentence or paragraph exactly as shown.
3.⁠ ⁠Use the *Check* button to validate your typing.
4.⁠ ⁠If the typed content is correct, you can use the *Next Sentence* button to continue.
5.⁠ ⁠Incorrect typing will prompt a message to try again.
6.⁠ ⁠After completing the final (timed) stage, a congratulatory message will appear.
7.⁠ ⁠You may then choose to restart the test or exit.

## Notes

•⁠  ⁠The application strictly requires 100% accuracy before allowing users to proceed.
•⁠  ⁠The timer only activates in the final stage.
•⁠  ⁠Copying, pasting, and right-click operations are disabled to promote honest practice.

## Author

Developed by SNEHA GUPTA