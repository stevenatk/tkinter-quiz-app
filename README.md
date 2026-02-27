# Turbonomic Quiz


# 1 - Introduction


As a customer success engineer working on IBM's automation platform, a need in my workplace is to assure and improve my colleagues' understanding in the key products of our portfolio. One product being Turbonomic (An application resource management solution), which is frequently in client conversations around observablity. New hires and cross functional team members often have different levels of understanding of Turbonomic and what it's capabilities actually are. In which the Turbonomic Quiz presented will help support onboarding and continous knowledge reinforcement for all staff who wish to participate.

This MVP addresses 2 practical needs:

First, it enables rapid knowledge check. A quick and easy GUI using Tkinter enables an employee to locally test their understanding of Turbonominc's fundamentals. For example, "What platforms may it support?" AWS, GCP, Azure?

Secondly, it helps with reporting and feedback. The results from the quiz are stored in a CSV file with timestamps, the user's name, role and score. This allows managers to be able to view knowledge trends from a birds eye view and provide more focused support in areas where needed.

The quiz helps fit my workplace's needs as it helps act as a low-friction way to get started in learning products without being overwhelmed by a lot of technical jargon. Additionally, to scale the quiz is very simple. In this MVP it only include 5 questions but adding more questions could provide more value and usefulness. However, intentionally using 5 questions shows how it can be adapted and reused for different IBM products too. 


# 2 - Design


What is the user journey?

1) Launching the Tkinter app
2) Enter your name and job title at IBM
3) Press Start Quiz
4) Answer 5 multiple choice questions
5) When finished, see a score summary of the quiz completed
6) Then the results are added into the CSV file

Wireframe Overview:

Frame 1 (pre-quiz questions): 
![Frame 1](<Frame 1 Turbonomic Quiz.png>)

Frame 2 (during quiz questions):
![Frame 2](<Frame 2 Turbonomic Quiz.png>)

Functional Requirements:

1) The app shows an interface where the user can input their name and job title before the quiz starts.

2) The app will validate the user's input. For example if they are including special charcters or numbers the app will not accept that input.

3) The app will then begin the quiz and show 5 multiple choice questions (one by one).

4) The app will take the user's input from the choice they selected.

5) The app will track how many the user gets correct throughout the quiz.

6) Once the user answers all 5 questions it will send the results to the CSV file.

7) It will then also show a message to the user with their final score and the equivalent percentage.

Non-functional Requirements:

1) Clear and coloured buttons for visibility (Buttons and text colour is not the same)

2) Clear title at the top so the user knows what the quiz is about.

3) Input validation for better logging of data.

4) Instant response on button clicks for each question.

5) Readable documentation throughout the code for understanding for changes if wanted/needed.


Tech Stack:

- Language: Python
- GUI: Tkinter
- Data Storage: CSV
- Version Control: GitHib
- CI: GitHub Actions

Code Design:

GUI Design using Tkinter.
- Input fields StringVar for Name and Job Title for the user to uniquely identify themselves
- Functions for validation (text_check, length_check, format_check)
- start_quiz -> Validate the users input -> show questions for the user
- next_question / check_answer for sequencing of the quiz and tracking score
- finish_quiz -> log all data in the CSV file and show message box of the user's final result


# 3 - Development


Here, I have imported everything I need for the app to work: Tkinter for the GUI, CSV for the data storage and re (regular expressions) for the validation:

```

import tkinter as tk
from tkinter import messagebox
import csv
from datetime import datetime
import re 

```

This is where I've added the validation functions to make sure the user's inputs are within the parameters I have set. The parameters being:

 1) text_check - Having some sort of text in the entry box
 2) length_check - For the text to be 25 charcters or less (no higher)
 3) format_check - Making sure the input only has letters (no special charcters nor numbers)

```

def text_check(text: str) -> bool:
    return bool(text)

def length_check(text: str) -> bool:
    return 0 < len(text) <= 25

def format_check(text: str) -> bool:
    pattern = re.compile(r"^[A-Za-z-' ]+$")
    return bool(pattern.match(text))

```

Here, I have added the list of questions I'm using for the quiz via a list of dictionaries. Using dictionaries helps to quickly be able to add and make a quick edits to the question list for new updates if needed:

```

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

```

Here, I have made my Tkinter window that includes a name, the size of the window and a light blue coloured background:

```
def turbo():
    app = tk.Tk()
    app.title("Turbonomic Quiz")
    app.geometry("1920x1080")
    app.config(bg="#add8e6")

```

Here, I have added my variables that will need inputs for the user's name and job title later on.

```

    user_name = tk.StringVar()
    job_title = tk.StringVar()

```

This is where Tkinter prepares the window with the widgets used for the pre-quiz page. It showcases adding labels and entry boxes to enter the reuqested information. It also has customisations of the font and size of text too. It also has padding around the widgets using pady.

```

    tk.Label(app, text="Turbonomic Quiz", font=("Arial", 24)).pack(pady=20)

    tk.Label(app, text="Your Name:", font=("Arial", 18)).pack(pady=5)
    tk.Entry(app, textvariable=user_name, font=("Arial", 18)).pack()

    tk.Label(app, text="IBM Role:", font=("Arial", 18)).pack(pady=5)
    tk.Entry(app, textvariable=job_title, font=("Arial", 18)).pack()

    question_label = tk.Label(app, text="", font=("Arial", 24))

```

Now, it's creating the buttons for the user to select their choice. The buttons are created empty and then later configured with both the text and click ability. Additionally, they are not displayed until .pack() happens after the quiz starts:

```

    buttons = []
    for button_options in range(4):
        button = tk.Button(app, text="", font=("Arial", 18,), width=50) 
        buttons.append(button)

```

Now adding the quiz state variables. This will show which question is being shown to the user and the total correct answers which will be used for the final score at the end of the quiz:

```

    current = 0
    score = 0

```

Here, it displays the current questions and assigns a purpose to each button. The code loops over 4 options and assigns each one option to a different button:

```

    def next_question():
        current_question = quiz_questions[current]
        question_label.config(text=current_question["question"])
        for i, option in enumerate(current_question["options"]):
            buttons[i].config(text=option, command=lambda answer=option: check_answer(answer))

```

This handler, validates the responses the user has given, increments the score and moves to the next state (finish_quiz). Using string comparison it allows the answers to be checked if they are correct. The score will only increase if there is a match. Then if there are still more questions remaining it will call next_question and if all questions have been answered it will call finish_quiz to indicate that the quiz has finished:

```

    def check_answer(selected):
        nonlocal current, score
        if selected == quiz_questions[current]["answer"]:
            score += 1
        current += 1
        if current < 5:
            next_question()
        else:
            finish_quiz()

```

This function here start_quiz() gathers the user's input to be used for quiz execution. It uses .get() to extract the inputs:

```

    def start_quiz():
        user_value = user_name.get()
        ob_value = job_title.get()

```

Here, it is running through all the validation functions for both the 'Name' and 'IBM Role'. In which each faliure of the validation will trigger 'return' which stops the quiz from starting and provides the retrospective error to the user so they are prompted to change their input:

```

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

```

Here is where the starting UI transitions into the actual quiz mode. Using .pack_forgert() it hides the start button. Then .pack() reveals the question label and all 4 answer button options:

```

        start_button.pack_forget()
        question_label.pack(pady=40)
        for button in buttons:
            button.pack(pady=5)
        next_question()

```

Here is when the quiz is completed and it calculates the final percentage for the user through a simple formula (score / 5) x 100 = percentage score. It then adds their timestamp, name, job title, score and percentage to the CSV file. Then it shows a message through messagebox.showinfo to indicate to the user what score they recieved and that their information has been stored into the turbonomic_quiz.csv file:

```

    def finish_quiz():
        percent = ((score / 5) * 100)

        with open("turbonomic_quiz.csv", mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([datetime.now().strftime("%Y-%m-%d %H:%M:%S"), user_name.get(), job_title.get(),score,"/5", percent])
    
        messagebox.showinfo("Finished!",f"You scored {score}/5 = ({percent}%). Results saved to turbonomic_quiz.csv")

```

This creates the 'Start Quiz' button to validate the user's input and also start the quiz if all inputs (Name and IBM Role) have been validated as true:

```

    start_button = tk.Button(app, text="Start Quiz", font=("Arial", 24), command=start_quiz)
    start_button.pack(pady=20)

```

This final line starts the GUI and allows Tkinter to run a continous event loop until closed:

```

    app.mainloop()
if __name__ == "__main__":
    turbo()

```


# 4 - Testing


For the testing of my quiz app, I have manually inputted different combinations of inputs into the 'Name' and 'IBM Role' variables to find out if the errors return back the correct message that user needs to see. Using manual testing this allows me to try the inputs from the users perspective and understand how the application performs under the combinations of valid and invalid inputs within the 'Turbonomic Quiz' GUI. Additionally, I have tested the flow of my application to make sure:

 1) The quiz goes through all the questions listed.
 2) Calculates the correct score of the user's quiz inputs.
 3) If the app logs all the data wanted into the CSV after the quiz finishes.

I have documented the results into an excel spreadsheet and screenshotted it below for viewing:

![Manual Tests for Turbonomic Quiz](<Manual Tests Turbonomic Quiz.png>)


Additionally, I have also tested my application with unit testing for the validation parameters of 'Name' and 'IBM Role', these were the tests I ran:

![Unit Tests](<Unit Testing Turbonomic Quiz.png>)

And these were the results from the test:

![Unit Test Results](<Successful Unit Testing.png>)

The pytest code can also be found in test_unit_quiz.py if needed.


# 5 - Documentation


User Documentation:

1) Enter your 'Name' and 'IBM Role'. (Only use letters, spaces, hyphens and apotrophes ONLY and the inputs must be 25 charcters or less).

2) When ready, click on 'Start Quiz'.

3) When each question pops up, choose one option to click on as your answer to the question.

4) After you complete the fifth question, a message will pop up with your score and percentage. Then the results will be added into the turbonomic_quiz.csv

Data privacy:

Only your timestamp (date and time of quiz completion), name, job title, score and percentage are stored locally. Avoid using any sensitive information beyond what is asked for.

CSV Layout:

- timestamp (YYYY-MM-DD HH:MM:SS)
- name (str)
- role (str)
- score (int)
- "/5" (for readability of how many questions are in the quiz)
- percentage (float)

Technical Documentation:

To run tests locally, you can start the quiz by running the file within the terminal. From there, you can try different inputs for your Name and IBM Role, while doing so you can see if the validation system will let you start the quiz if your inputs are invalid. The parameters you should test for are:

1) There must be an input in both 'Name' and 'IBM Role'.
2) Both inputs must be 25 characters or less.
3) Both inputs must not include any numbers or special charcters such !,? and others.

More technical documentation on how the code works can be found within and throughout turbo_quiz.py if needed.

# 6 - Evaluation


The Turbonomic Quiz app that was built, I think went successfully for the purpose it was intended for. The quiz works, it has the functionality to score and log that data. It also has easy implementation to add more questions if wanted/needed to.

Overall, what went well: The UI was built to be simple and easy to navigate, which is ideal for enablement sessions or demos. It helps people understand how easy it is to use with useful functionality. The validation gives clear error messages to the user if something that they have inputted is invalid, helping to ensure that valid data is logged in an organised manner. The CSV logs can help managers or other senior employees to track progression and knowledge of Turbonomic. With that being said, the quiz is also easily adaptable to other IBM products just by changing the list of dictionaires to suit another product.

On the other hand, what could've been improved: Adding in an option to restart the quiz may have been useful as this would've implemented a way for users to continously test their knowledge rather than restarting the application to log a new entry for the quiz. Furthermore, I think an additonal radio select option using Tkinter for users to select the function they're in at IBM could be useful as it helps showcase product knowledge across departments which may have provide useful for reporting for managers. Natrually, adding more questions (making the quiz 15-20 questions long) could've made the quiz more interesting but as mentioned before it's a simple MVP to display the functionalities of the quiz.

To conclude, this MVP works to fulfil the main purpose of enabling users to complete a quiz and understand their gaps in knowledge of IBM Turbonomic. This provides value in my workplace as product knowledge is incredibly important in many roles, especially as a customer success enginner in which you're communicating about IBM's portfolio everyday with prospects and clients. Being able to communicate accurate and cohesive knowledge is crucial for success in the role. Therefore this quiz provides value to the business as a whole as it has options for flexibility in topics and scalability in length, assuring that all areas of the business can be supported through this MVP.