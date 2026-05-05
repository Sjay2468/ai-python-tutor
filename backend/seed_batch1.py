"""
Seed script — Run once to populate the database with all lesson content,
practice questions, and rule-base entries.

Usage (from backend/ folder):
    .\\venv\\Scripts\\python seed.py
"""
import json
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from app import create_app, db
from app.models import Lesson, PracticeQuestion

app = create_app()

# ─────────────────────────────────────────────
# LESSON DATA  (9 topics)
# Sources: T1=Think Python, O1=W3Schools, O2=Programiz, R1=Researcher-authored
# ─────────────────────────────────────────────
LESSONS = [
    {
        "id": "L01",
        "title": "Variables & Data Types",
        "order_index": 1,
        "explanation": (
            "A variable is a named storage location in your program's memory. "
            "You create one by writing a name, an equals sign, and a value. "
            "Python figures out the type automatically — you don't need to declare it. "
            "The four most common beginner data types are:\n"
            "  • int   — whole numbers  (e.g. 5, -3, 100)\n"
            "  • float — decimal numbers (e.g. 3.14, -0.5)\n"
            "  • str   — text in quotes  (e.g. \"Hello\")\n"
            "  • bool  — True or False"
        ),
        "analogy": (
            "Think of a variable like a labelled box. The label is the variable name, "
            "and whatever you put inside the box is the value. "
            "You can change what's inside the box at any time."
        ),
        "code_example": (
            "# Creating variables\n"
            "name = \"Amina\"       # str\n"
            "age = 19             # int\n"
            "gpa = 3.8            # float\n"
            "is_student = True    # bool\n\n"
            "# Printing values\n"
            "print(name)          # Output: Amina\n"
            "print(age)           # Output: 19\n"
            "print(type(gpa))     # Output: <class 'float'>"
        ),
        "code_breakdown": (
            "Line 2: name = \"Amina\" — creates a variable called 'name' storing the text Amina.\n"
            "Line 3: age = 19 — stores the whole number 19 in 'age'.\n"
            "Line 4: gpa = 3.8 — stores a decimal number in 'gpa'.\n"
            "Line 5: is_student = True — stores a boolean (True/False) value.\n"
            "Line 8: print(name) — displays the value stored in 'name'.\n"
            "Line 10: type(gpa) — returns the data type of a variable."
        ),
        "key_points": json.dumps([
            "A variable stores a value using the = sign.",
            "Python automatically detects the data type.",
            "The four basic types are int, float, str, and bool.",
            "Variable names are case-sensitive: 'Age' and 'age' are different.",
            "Use print() to display a variable's value.",
        ]),
    },
    {
        "id": "L02",
        "title": "Operators",
        "order_index": 2,
        "explanation": (
            "Operators are symbols that perform actions on values. Python has several types:\n"
            "  • Arithmetic: + - * / // % **\n"
            "  • Comparison: == != > < >= <=  (return True or False)\n"
            "  • Logical: and, or, not\n"
            "  • Assignment: =, +=, -=, *="
        ),
        "analogy": (
            "Operators are like the buttons on a calculator. "
            "Just as + adds numbers on a calculator, Python's + adds values in your program."
        ),
        "code_example": (
            "# Arithmetic\n"
            "x = 10\n"
            "y = 3\n"
            "print(x + y)    # 13\n"
            "print(x - y)    # 7\n"
            "print(x * y)    # 30\n"
            "print(x / y)    # 3.333...\n"
            "print(x // y)   # 3  (floor division)\n"
            "print(x % y)    # 1  (remainder)\n"
            "print(x ** y)   # 1000 (10 to the power 3)\n\n"
            "# Comparison\n"
            "print(x > y)    # True\n"
            "print(x == y)   # False\n\n"
            "# Logical\n"
            "print(x > 5 and y < 5)  # True"
        ),
        "code_breakdown": (
            "// is floor division — divides and drops the decimal part.\n"
            "% is the modulus — gives the remainder after division.\n"
            "** is exponentiation — raises a number to a power.\n"
            "== checks equality (two equals signs); = is assignment (one equals sign).\n"
            "'and' returns True only if BOTH conditions are True."
        ),
        "key_points": json.dumps([
            "Use + - * / for basic arithmetic.",
            "// gives the whole-number part of division; % gives the remainder.",
            "Comparison operators return True or False.",
            "Use == to compare, not = (which assigns a value).",
            "'and', 'or', 'not' are logical operators for combining conditions.",
        ]),
    },
    {
        "id": "L03",
        "title": "Conditionals (if/else)",
        "order_index": 3,
        "explanation": (
            "Conditionals let your program make decisions. "
            "If a condition is True, one block of code runs; otherwise a different block runs. "
            "The keywords are: if, elif (else if), and else. "
            "Python uses indentation (4 spaces) to mark which code belongs inside each block."
        ),
        "analogy": (
            "Think of a conditional like a traffic light. "
            "If the light is green, you go. If it's red, you stop. "
            "Your program does the same — checks a condition and picks a path."
        ),
        "code_example": (
            "score = 75\n\n"
            "if score >= 70:\n"
            "    print(\"Topic mastered!\")\n"
            "elif score >= 50:\n"
            "    print(\"Good effort. Keep practicing.\")\n"
            "else:\n"
            "    print(\"Review the lesson and try again.\")"
        ),
        "code_breakdown": (
            "Line 3: 'if score >= 70:' — checks if score is 70 or above.\n"
            "Line 4: indented code runs ONLY if the condition above is True.\n"
            "Line 5: 'elif' means 'else if' — checked only if the first 'if' was False.\n"
            "Line 7: 'else' catches everything that didn't match above.\n"
            "The colon (:) at the end of each if/elif/else line is required."
        ),
        "key_points": json.dumps([
            "Use 'if' to check a condition.",
            "Use 'elif' for additional conditions.",
            "Use 'else' as the default when no condition matches.",
            "Always end if/elif/else lines with a colon (:).",
            "Indentation (4 spaces) defines which code belongs inside a block.",
        ]),
    },
    {
        "id": "L04",
        "title": "Loops (for / while)",
        "order_index": 4,
        "explanation": (
            "Loops repeat a block of code multiple times. Python has two types:\n"
            "  • for loop — repeats a fixed number of times over a sequence.\n"
            "  • while loop — repeats as long as a condition stays True.\n"
            "Use range(n) to loop exactly n times. "
            "break exits a loop early; continue skips to the next iteration."
        ),
        "analogy": (
            "A loop is like a morning routine. "
            "You repeat the same steps (wake up, brush teeth, eat) every day "
            "until the week ends (for loop) or until you're on holiday (while loop)."
        ),
        "code_example": (
            "# for loop — print numbers 0 to 4\n"
            "for i in range(5):\n"
            "    print(i)\n\n"
            "# for loop over a list\n"
            "fruits = [\"apple\", \"banana\", \"cherry\"]\n"
            "for fruit in fruits:\n"
            "    print(fruit)\n\n"
            "# while loop\n"
            "count = 0\n"
            "while count < 3:\n"
            "    print(\"count is\", count)\n"
            "    count += 1   # important: avoid infinite loop!"
        ),
        "code_breakdown": (
            "range(5) generates numbers 0, 1, 2, 3, 4 — it stops BEFORE 5.\n"
            "'for fruit in fruits' assigns each list item to 'fruit' one at a time.\n"
            "'while count < 3' keeps looping as long as count is less than 3.\n"
            "'count += 1' increases count by 1 each time — without this the loop never ends."
        ),
        "key_points": json.dumps([
            "A 'for' loop repeats over a sequence or range.",
            "range(5) gives numbers 0 to 4 (not including 5).",
            "A 'while' loop runs as long as its condition is True.",
            "Always update the loop variable in a while loop to avoid infinite loops.",
            "'break' exits a loop; 'continue' skips to the next iteration.",
        ]),
    },
    {
        "id": "L05",
        "title": "Functions",
        "order_index": 5,
        "explanation": (
            "A function is a reusable block of code that performs a specific task. "
            "You define it once with 'def' and call it by name as many times as needed. "
            "Functions can accept inputs (parameters) and return outputs (return value). "
            "This avoids repeating the same code and makes programs easier to read."
        ),
        "analogy": (
            "A function is like a recipe. You write the recipe once, "
            "and anyone can follow it whenever they need that dish. "
            "The ingredients are the parameters; the finished dish is the return value."
        ),
        "code_example": (
            "# Defining a function\n"
            "def greet(name):\n"
            "    message = \"Hello, \" + name + \"!\"\n"
            "    return message\n\n"
            "# Calling the function\n"
            "result = greet(\"Amina\")\n"
            "print(result)   # Output: Hello, Amina!\n\n"
            "# Function with default parameter\n"
            "def add(a, b=0):\n"
            "    return a + b\n\n"
            "print(add(5, 3))   # 8\n"
            "print(add(5))      # 5  (b defaults to 0)"
        ),
        "code_breakdown": (
            "Line 2: 'def greet(name):' — defines a function called 'greet' that takes one input.\n"
            "Line 4: 'return message' — sends the result back to the caller.\n"
            "Line 7: 'greet(\"Amina\")' — calls the function, passing \"Amina\" as the argument.\n"
            "Line 11: 'b=0' is a default parameter — used when no value is provided for b."
        ),
        "key_points": json.dumps([
            "Define a function with 'def function_name(parameters):'.",
            "Call a function by writing its name followed by parentheses.",
            "Parameters are inputs; 'return' sends a value back.",
            "Functions can have default parameter values.",
            "A function without 'return' returns None automatically.",
        ]),
    },
]

# ─────────────────────────────────────────────
# PRACTICE QUESTIONS  (L01–L05, 5 each)
# ─────────────────────────────────────────────
QUESTIONS_BATCH_1 = [
    # L01 — Variables & Data Types
    {
        "topic_id": "L01",
        "question_text": "What is the data type of the value in: x = 3.14?",
        "option_a": "int", "option_b": "float",
        "option_c": "str",  "option_d": "bool",
        "correct_option": "B",
        "hint_1": "Think about whether 3.14 is a whole number or a decimal number.",
        "hint_2": "In Python, numbers with a decimal point are called 'float' (floating point).",
        "hint_3": "3.14 has a decimal point, so its type is 'float'. The answer is B.",
    },
    {
        "topic_id": "L01",
        "question_text": "Which of the following creates a variable that stores the text 'Python'?",
        "option_a": "x = Python", "option_b": "x = 'Python'",
        "option_c": "x == 'Python'", "option_d": "str = Python",
        "correct_option": "B",
        "hint_1": "Text (strings) must be wrapped in quotes in Python.",
        "hint_2": "Single quotes or double quotes both work for strings. Look for quotes around Python.",
        "hint_3": "B is correct: x = 'Python'. Without quotes, Python thinks 'Python' is a variable name, not text.",
    },
    {
        "topic_id": "L01",
        "question_text": "What does the print(type(x)) function return if x = 10?",
        "option_a": "float", "option_b": "str",
        "option_c": "<class 'int'>", "option_d": "True",
        "correct_option": "C",
        "hint_1": "10 is a whole number. Which type represents whole numbers?",
        "hint_2": "type() returns the class of the value. For whole numbers it returns 'int'.",
        "hint_3": "The answer is C: <class 'int'>. The type() function always returns the class name.",
    },
    {
        "topic_id": "L01",
        "question_text": "Which of the following is a valid Python variable name?",
        "option_a": "2score", "option_b": "my-score",
        "option_c": "my_score", "option_d": "my score",
        "correct_option": "C",
        "hint_1": "Variable names cannot start with a number or contain spaces or hyphens.",
        "hint_2": "Python variable names can only use letters, digits, and underscores (_).",
        "hint_3": "C is correct: my_score. Underscores are allowed; spaces, hyphens, and leading digits are not.",
    },
    {
        "topic_id": "L01",
        "question_text": "What value does a bool variable hold?",
        "option_a": "Numbers only", "option_b": "Text only",
        "option_c": "True or False", "option_d": "Any value",
        "correct_option": "C",
        "hint_1": "Think about the word 'boolean' — it refers to logic.",
        "hint_2": "Boolean types have only two possible states, like an on/off switch.",
        "hint_3": "C is correct: True or False. These are the only two values a bool can hold.",
    },
    # L02 — Operators
    {
        "topic_id": "L02",
        "question_text": "What is the result of 10 % 3 in Python?",
        "option_a": "3", "option_b": "0",
        "option_c": "1", "option_d": "3.33",
        "correct_option": "C",
        "hint_1": "The % operator gives the remainder after division, not the quotient.",
        "hint_2": "10 divided by 3 is 3 with a remainder of 1.",
        "hint_3": "C is correct: 1. 10 = 3×3 + 1, so 10 % 3 = 1.",
    },
    {
        "topic_id": "L02",
        "question_text": "Which operator checks if two values are equal?",
        "option_a": "=", "option_b": "==",
        "option_c": "!=", "option_d": ">=",
        "correct_option": "B",
        "hint_1": "One equals sign (=) assigns a value. Another symbol is used to compare.",
        "hint_2": "Equality comparison uses two equals signs together.",
        "hint_3": "B is correct: ==. A single = assigns; double == compares.",
    },
    {
        "topic_id": "L02",
        "question_text": "What does 2 ** 3 evaluate to?",
        "option_a": "6", "option_b": "5",
        "option_c": "9", "option_d": "8",
        "correct_option": "D",
        "hint_1": "The ** operator means 'to the power of'.",
        "hint_2": "2 ** 3 means 2 raised to the power of 3, which is 2 × 2 × 2.",
        "hint_3": "D is correct: 8. 2³ = 2 × 2 × 2 = 8.",
    },
    {
        "topic_id": "L02",
        "question_text": "What is the result of: True and False?",
        "option_a": "True", "option_b": "False",
        "option_c": "None", "option_d": "Error",
        "correct_option": "B",
        "hint_1": "'and' requires BOTH sides to be True to return True.",
        "hint_2": "Since one side is False, the whole expression is False.",
        "hint_3": "B is correct: False. 'and' only returns True when both operands are True.",
    },
    {
        "topic_id": "L02",
        "question_text": "What does 15 // 4 return?",
        "option_a": "3.75", "option_b": "4",
        "option_c": "3", "option_d": "11",
        "correct_option": "C",
        "hint_1": "// is floor division — it drops the decimal part of the result.",
        "hint_2": "15 / 4 = 3.75. Floor division keeps only the whole number part.",
        "hint_3": "C is correct: 3. Floor division discards the decimal, so 3.75 becomes 3.",
    },
    # L03 — Conditionals
    {
        "topic_id": "L03",
        "question_text": "What keyword is used to check an additional condition if the first 'if' is False?",
        "option_a": "else", "option_b": "then",
        "option_c": "elif", "option_d": "ifelse",
        "correct_option": "C",
        "hint_1": "Python uses a shortened form of 'else if'.",
        "hint_2": "It's a combination of 'else' and 'if' merged together.",
        "hint_3": "C is correct: elif. It means 'else if' and is checked only when the previous condition was False.",
    },
    {
        "topic_id": "L03",
        "question_text": "What is required at the end of an 'if' statement line?",
        "option_a": "Semicolon (;)", "option_b": "Colon (:)",
        "option_c": "Brackets ({})", "option_d": "Nothing",
        "correct_option": "B",
        "hint_1": "Python uses a specific punctuation mark to signal the start of a code block.",
        "hint_2": "Unlike Java or C, Python doesn't use curly braces — it uses a different character.",
        "hint_3": "B is correct: a colon (:). Every if, elif, else, for, while, and def line ends with ':'.",
    },
    {
        "topic_id": "L03",
        "question_text": "What will print? x = 5\nif x > 10:\n    print('A')\nelse:\n    print('B')",
        "option_a": "A", "option_b": "Nothing",
        "option_c": "B", "option_d": "Error",
        "correct_option": "C",
        "hint_1": "Check whether 5 > 10 is True or False.",
        "hint_2": "5 is NOT greater than 10, so the 'if' block is skipped.",
        "hint_3": "C is correct: B. Since 5 > 10 is False, the 'else' block runs and prints 'B'.",
    },
    {
        "topic_id": "L03",
        "question_text": "How does Python know which code belongs inside an 'if' block?",
        "option_a": "Curly braces {}", "option_b": "Parentheses ()",
        "option_c": "Indentation (spaces)", "option_d": "END keyword",
        "correct_option": "C",
        "hint_1": "Python doesn't use braces like other languages.",
        "hint_2": "The code inside a block is shifted to the right using spaces.",
        "hint_3": "C is correct: Indentation. Python uses 4 spaces to group code inside blocks.",
    },
    {
        "topic_id": "L03",
        "question_text": "Which block runs when none of the 'if' or 'elif' conditions are True?",
        "option_a": "elif", "option_b": "default",
        "option_c": "finally", "option_d": "else",
        "correct_option": "D",
        "hint_1": "This block is the fallback — it runs when everything else fails.",
        "hint_2": "It doesn't have a condition — it catches all remaining cases.",
        "hint_3": "D is correct: else. It runs when no 'if' or 'elif' condition was True.",
    },
    # L04 — Loops
    {
        "topic_id": "L04",
        "question_text": "How many times does this loop run? for i in range(4): print(i)",
        "option_a": "3", "option_b": "4",
        "option_c": "5", "option_d": "0",
        "correct_option": "B",
        "hint_1": "range(4) generates a sequence of numbers — count how many.",
        "hint_2": "range(4) produces: 0, 1, 2, 3 — count those values.",
        "hint_3": "B is correct: 4. range(4) gives 0, 1, 2, 3 — four values, four iterations.",
    },
    {
        "topic_id": "L04",
        "question_text": "What happens if you forget to increment the counter in a while loop?",
        "option_a": "The loop stops after one run", "option_b": "Python throws an error",
        "option_c": "The loop runs forever (infinite loop)", "option_d": "The counter resets to 0",
        "correct_option": "C",
        "hint_1": "Think about what the condition checks and whether it can ever become False.",
        "hint_2": "If the variable never changes, the condition stays True permanently.",
        "hint_3": "C is correct: infinite loop. Without incrementing, the while condition never becomes False.",
    },
    {
        "topic_id": "L04",
        "question_text": "What does 'break' do inside a loop?",
        "option_a": "Skips the current iteration", "option_b": "Exits the loop immediately",
        "option_c": "Restarts the loop", "option_d": "Pauses the loop",
        "correct_option": "B",
        "hint_1": "The word 'break' means to stop something.",
        "hint_2": "It terminates the loop entirely, not just one iteration.",
        "hint_3": "B is correct: exits the loop immediately. Execution continues after the loop block.",
    },
    {
        "topic_id": "L04",
        "question_text": "What does range(2, 6) produce?",
        "option_a": "2, 3, 4, 5, 6", "option_b": "2, 3, 4, 5",
        "option_c": "1, 2, 3, 4, 5", "option_d": "2, 4, 6",
        "correct_option": "B",
        "hint_1": "range(start, stop) starts at the first number and stops BEFORE the second.",
        "hint_2": "It includes 2 but excludes 6.",
        "hint_3": "B is correct: 2, 3, 4, 5. range(2, 6) starts at 2 and stops before 6.",
    },
    {
        "topic_id": "L04",
        "question_text": "Which loop is best when you don't know in advance how many times to repeat?",
        "option_a": "for loop", "option_b": "while loop",
        "option_c": "range loop", "option_d": "if loop",
        "correct_option": "B",
        "hint_1": "One type of loop runs a set number of times; another runs until a condition changes.",
        "hint_2": "When the number of repetitions depends on user input or an event, which loop fits?",
        "hint_3": "B is correct: while loop. Use it when you don't know how many iterations are needed upfront.",
    },
    # L05 — Functions
    {
        "topic_id": "L05",
        "question_text": "What keyword is used to define a function in Python?",
        "option_a": "function", "option_b": "define",
        "option_c": "def", "option_d": "fun",
        "correct_option": "C",
        "hint_1": "It's an abbreviation of the word 'define'.",
        "hint_2": "It's three letters long and starts with 'd'.",
        "hint_3": "C is correct: def. You write 'def function_name():' to create a function.",
    },
    {
        "topic_id": "L05",
        "question_text": "What does the 'return' keyword do in a function?",
        "option_a": "Prints the result to the screen",
        "option_b": "Sends a value back to the caller",
        "option_c": "Stops the program",
        "option_d": "Repeats the function",
        "correct_option": "B",
        "hint_1": "Think about what happens after a function finishes its work.",
        "hint_2": "The value doesn't automatically appear on screen — it's sent somewhere.",
        "hint_3": "B is correct: sends a value back to the caller. You can then store or print that value.",
    },
    {
        "topic_id": "L05",
        "question_text": "What is a parameter in a function?",
        "option_a": "The name of the function",
        "option_b": "An input value the function receives",
        "option_c": "The value the function returns",
        "option_d": "A comment inside the function",
        "correct_option": "B",
        "hint_1": "Parameters allow you to pass information into a function.",
        "hint_2": "They appear inside the parentheses in the 'def' line.",
        "hint_3": "B is correct: an input value. Parameters are listed in parentheses when defining the function.",
    },
    {
        "topic_id": "L05",
        "question_text": "What does a function return if it has no 'return' statement?",
        "option_a": "0", "option_b": "False",
        "option_c": "None", "option_d": "An error",
        "correct_option": "C",
        "hint_1": "Python always returns something from a function, even if you don't specify.",
        "hint_2": "The default return value in Python represents 'nothing'.",
        "hint_3": "C is correct: None. Python implicitly returns None when there's no return statement.",
    },
    {
        "topic_id": "L05",
        "question_text": "Which line correctly calls a function named 'greet' with 'Amina' as the argument?",
        "option_a": "def greet('Amina')", "option_b": "call greet('Amina')",
        "option_c": "greet('Amina')", "option_d": "greet = 'Amina'",
        "correct_option": "C",
        "hint_1": "You call a function by using its name followed by parentheses.",
        "hint_2": "'def' is for defining, not calling. Look for just the function name.",
        "hint_3": "C is correct: greet('Amina'). To call a function, write its name with arguments in parentheses.",
    },
]


def seed_lessons_batch1():
    """Seed lessons L01–L05 and their practice questions."""
    with app.app_context():
        seeded = 0
        for data in LESSONS:
            if not db.session.get(Lesson, data["id"]):
                lesson = Lesson(**data)
                db.session.add(lesson)
                seeded += 1
        db.session.commit()
        print(f"[OK] Seeded {seeded} lessons (L01-L05).")

        q_seeded = 0
        for q in QUESTIONS_BATCH_1:
            existing = PracticeQuestion.query.filter_by(
                topic_id=q["topic_id"], question_text=q["question_text"]
            ).first()
            if not existing:
                db.session.add(PracticeQuestion(**q))
                q_seeded += 1
        db.session.commit()
        print(f"[OK] Seeded {q_seeded} practice questions (L01-L05).")


if __name__ == "__main__":
    seed_lessons_batch1()
