import tkinter as tk
from tkinter import messagebox
import csv
from datetime import datetime
import re 

# Adding validation functions for the text inputs 'Name' and 'IBM Role'

def text_check(text: str) -> bool:
    return bool(text)

def length_check(text: str) -> bool:
    return 0 < len(text) <= 25

def format_check(text: str) -> bool:
    pattern = re.compile(r"^[A-Za-z-' ]+$")
    return bool(pattern.match(text))

# Adding all (5) Turbonomic Quiz Questions

quiz_questions = [
    {"question": "What is Turbonomic?", 
     "options": ["ARM", "APM", "UI", "GUI"], 
     "answer": "ARM"},

    {"question": "How does Turbonomic help clients?",
     "options": ["Provides insights into manufacturing spend.", "Helps automate allocation of compute resources.", "An AI tool that supports building infrastructure.", "Helps to manage warehouse storage"],
     "answer": "Helps automate allocation of compute resources."},

    {"question": "Does Turbonomic support AWS, Azure and GCP?",
     "options": ["Yes", "No", "Only AWS and Azure", "Only AWS and GCP"],
     "answer": "Yes"},

    {"question": "Can Turbonomic integrate with a wide range of APM tools?",
     "options": ["Yes", "No", "Only Instana", "Only DataDog"],
     "answer": "Yes"},

    {"question": "What specialism does Turbonomic come under?",
     "options": ["Asset Lifecycle Management", "Application Integration", "Observability", "Security"],
     "answer": "Observability"}
]

# Adding the foundation of the interface

def turbo():
    app = tk.Tk()
    app.title("Turbonomic Quiz")
    app.geometry("1920x1080")
    app.config(bg="#add8e6")

# Adding variables for 'Name' and 'Job Title' for CSV logging

    user_name = tk.StringVar()
    job_title = tk.StringVar()

# Adding the buttons Entry for the variables on the Tkinter window

    tk.Label(app, text="Turbonomic Quiz", font=("Arial", 24)).pack(pady=20)

    tk.Label(app, text="Your Name:", font=("Arial", 18)).pack(pady=5)
    tk.Entry(app, textvariable=user_name, font=("Arial", 18)).pack()

    tk.Label(app, text="IBM Role:", font=("Arial", 18)).pack(pady=5)
    tk.Entry(app, textvariable=job_title, font=("Arial", 18)).pack()

# Adding the label for the question to be asked

    question_label = tk.Label(app, text="", font=("Arial", 24))

# Adding buttons to the Turbonomic Quiz for when it starts only

    buttons = []
    for button_options in range(4):
        button = tk.Button(app, text="", font=("Arial", 18,), width=50) 
        buttons.append(button)

# Adding variables for the score and current question on the quiz (CSV logging)

    current = 0
    score = 0

# Adding functions to load the questions and also check the correct answer from the users input

    def next_question():
        current_question = quiz_questions[current]
        question_label.config(text=current_question["question"])
        for i, option in enumerate(current_question["options"]):
            buttons[i].config(text=option, command=lambda answer=option: check_answer(answer))

    def check_answer(selected):
        nonlocal current, score
        if selected == quiz_questions[current]["answer"]:
            score += 1
        current += 1
        if current < 5:
            next_question()
        else:
            finish_quiz()

# Starting the quiz

    def start_quiz():
        user_value = user_name.get()
        job_value = job_title.get()

# Validating the input that the user has entered (using the parameters)

        if not text_check(user_value):
            messagebox.showwarning("Text is not inputted.","Please enter a valid name.")
            return

        if not length_check(user_value):
            messagebox.showwarning("Input is too long.","Please enter a valid name, your input is too long.")
            return

        if not format_check(user_value):
            messagebox.showwarning("Input is invalid.","Please enter a valid name (letters and spaces only, no numbers or special characters).")
            return

        if not text_check(job_value):
            messagebox.showwarning("Text is not inputted.","Please enter a Job Title.")
            return

        if not length_check(job_value):
            messagebox.showwarning("Input is too long.","Please enter a Job Title, your input is too long.")
            return

        if not format_check(job_value):
            messagebox.showwarning("Input is invalid.","Please enter a Job Title (letters and spaces only, no numbers or special characters).")
            return

# Showing and hiding start buttons when starting the quiz

        start_button.pack_forget()
        question_label.pack(pady=40)
        for button in buttons:
            button.pack(pady=5)
        next_question()

# Calculating the score from the quiz, then logging all the data into the CSV file

    def finish_quiz():
        percent = ((score / 5) * 100)

        with open("turbonomic_quiz.csv", mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([datetime.now().strftime("%Y-%m-%d %H:%M:%S"), user_name.get(), job_title.get(),score,"/5", percent])
    
        messagebox.showinfo("Finished!",f"You scored {score}/5 = ({percent}%). Results saved to turbonomic_quiz.csv")

    start_button = tk.Button(app, text="Start Quiz", font=("Arial", 24), command=start_quiz)
    start_button.pack(pady=20)

    app.mainloop()

if __name__ == "__main__":
    turbo()