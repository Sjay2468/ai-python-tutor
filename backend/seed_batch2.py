"""
Seed batch 2 — Lessons L06-L09 (Lists, Dictionaries, Errors, Basic I/O)
and their practice questions.

Usage:
    .\\venv\\Scripts\\python seed_batch2.py
"""
import json
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from app import create_app, db
from app.models import Lesson, PracticeQuestion

app = create_app()

LESSONS = [
    {
        "id": "L06",
        "title": "Lists",
        "order_index": 6,
        "explanation": (
            "A list is an ordered collection of items stored in a single variable. "
            "Lists can hold any data types and allow duplicates. "
            "Items are accessed by their index, which starts at 0. "
            "You can add, remove, and change items after creating the list."
        ),
        "analogy": (
            "A list is like a shopping list on paper. "
            "Each item has a position (item 1, item 2, ...) and you can add or cross off items. "
            "In Python, that position starts counting from 0 instead of 1."
        ),
        "code_example": (
            "# Creating a list\n"
            "fruits = [\"apple\", \"banana\", \"cherry\"]\n\n"
            "# Accessing items by index (starts at 0)\n"
            "print(fruits[0])   # apple\n"
            "print(fruits[1])   # banana\n"
            "print(fruits[-1])  # cherry (last item)\n\n"
            "# Modifying a list\n"
            "fruits.append(\"mango\")    # add to end\n"
            "fruits.remove(\"banana\")   # remove by value\n"
            "fruits[0] = \"grape\"       # change an item\n\n"
            "print(len(fruits))         # number of items\n"
            "print(fruits)              # ['grape', 'cherry', 'mango']"
        ),
        "code_breakdown": (
            "fruits[0] — index 0 is the first item ('apple').\n"
            "fruits[-1] — negative index counts from the end; -1 is the last item.\n"
            "append() — adds one item to the end of the list.\n"
            "remove() — removes the first matching value from the list.\n"
            "len() — returns the number of items in the list."
        ),
        "key_points": json.dumps([
            "Lists are created with square brackets: [item1, item2, ...].",
            "Indexing starts at 0, not 1.",
            "Use negative indices to count from the end (-1 = last item).",
            "append() adds; remove() deletes; len() counts items.",
            "Lists are mutable — you can change them after creation.",
        ]),
    },
    {
        "id": "L07",
        "title": "Dictionaries",
        "order_index": 7,
        "explanation": (
            "A dictionary stores data as key-value pairs. "
            "Instead of using a number index, you look up values by a meaningful key (like a word). "
            "Keys must be unique. Values can be any type. "
            "Dictionaries are defined with curly braces {}."
        ),
        "analogy": (
            "A dictionary works exactly like a real dictionary: "
            "you look up a word (key) to find its definition (value). "
            "Each word appears only once, but definitions can be anything."
        ),
        "code_example": (
            "# Creating a dictionary\n"
            "student = {\n"
            "    \"name\": \"Amina\",\n"
            "    \"age\": 19,\n"
            "    \"course\": \"Computer Science\"\n"
            "}\n\n"
            "# Accessing values\n"
            "print(student[\"name\"])    # Amina\n"
            "print(student[\"age\"])     # 19\n\n"
            "# Adding and updating\n"
            "student[\"grade\"] = \"A\"   # adds new key\n"
            "student[\"age\"] = 20       # updates existing key\n\n"
            "# Useful methods\n"
            "print(student.keys())     # all keys\n"
            "print(student.values())   # all values\n"
            "print(\"name\" in student)  # True"
        ),
        "code_breakdown": (
            "student[\"name\"] — access the value stored under the key \"name\".\n"
            "student[\"grade\"] = \"A\" — adds a new key-value pair.\n"
            "student[\"age\"] = 20 — updates an existing value.\n"
            ".keys() — returns all the keys in the dictionary.\n"
            ".values() — returns all the values.\n"
            "'in' — checks whether a key exists in the dictionary."
        ),
        "key_points": json.dumps([
            "Dictionaries use curly braces: {key: value, key: value}.",
            "Access values using the key in square brackets: dict[key].",
            "Keys must be unique; values can repeat.",
            "Use .keys(), .values(), and .items() to iterate.",
            "Check membership with 'key in dict'.",
        ]),
    },
    {
        "id": "L08",
        "title": "Error Types & Debugging",
        "order_index": 8,
        "explanation": (
            "Errors in Python fall into two main categories:\n"
            "  • Syntax Errors — Python cannot understand your code because of a typo or missing symbol. "
            "The program won't run at all.\n"
            "  • Runtime Errors (Exceptions) — the code runs but something goes wrong during execution. "
            "Common ones: NameError, TypeError, IndexError, ZeroDivisionError, KeyError.\n\n"
            "Reading the error message carefully — especially the line number — is the first step in debugging."
        ),
        "analogy": (
            "A syntax error is like a grammatical mistake in a sentence — "
            "the reader can't understand it at all. "
            "A runtime error is like giving someone correct directions to the wrong address — "
            "everything looks fine until something goes wrong on the way."
        ),
        "code_example": (
            "# SyntaxError — missing colon\n"
            "# if x > 5       <- SyntaxError: expected ':'\n\n"
            "# NameError — variable not defined\n"
            "# print(score)   <- NameError if 'score' was never created\n\n"
            "# TypeError — wrong type operation\n"
            "# print(\"Age: \" + 19)  <- TypeError: can only concatenate str to str\n\n"
            "# ZeroDivisionError\n"
            "# result = 10 / 0     <- ZeroDivisionError\n\n"
            "# IndexError\n"
            "items = [1, 2, 3]\n"
            "# print(items[5])     <- IndexError: list index out of range\n\n"
            "# Fix: use try/except to handle errors gracefully\n"
            "try:\n"
            "    result = 10 / 0\n"
            "except ZeroDivisionError:\n"
            "    print(\"Cannot divide by zero!\")"
        ),
        "code_breakdown": (
            "SyntaxError — check for missing colons, brackets, or quote marks.\n"
            "NameError — you used a variable before defining it; check spelling.\n"
            "TypeError — you tried to mix incompatible types (e.g. str + int).\n"
            "ZeroDivisionError — you divided by zero; always check divisors.\n"
            "IndexError — you used an index that doesn't exist in the list.\n"
            "try/except — wraps risky code; 'except' runs if an error occurs."
        ),
        "key_points": json.dumps([
            "Syntax errors prevent the program from running at all.",
            "Runtime errors (exceptions) occur while the program is running.",
            "Always read the error type and line number in the traceback.",
            "Common errors: NameError, TypeError, IndexError, ZeroDivisionError, KeyError.",
            "Use try/except to handle errors gracefully without crashing.",
        ]),
    },
    {
        "id": "L09",
        "title": "Basic I/O (input / print)",
        "order_index": 9,
        "explanation": (
            "I/O means Input and Output — how your program communicates with the user.\n"
            "  • print() — displays text or values on screen (output).\n"
            "  • input() — pauses the program and waits for the user to type something (input).\n\n"
            "Important: input() always returns a string. "
            "If you need a number, convert it with int() or float()."
        ),
        "analogy": (
            "print() is your program speaking to you. "
            "input() is your program asking you a question and waiting for your answer. "
            "Together they form a conversation between the user and the program."
        ),
        "code_example": (
            "# Basic output\n"
            "print(\"Welcome to Python Tutor!\")\n"
            "name = \"Amina\"\n"
            "print(\"Hello,\", name)             # Hello, Amina\n"
            "print(f\"Hello, {name}!\")          # f-string (modern way)\n\n"
            "# Basic input\n"
            "user_name = input(\"What is your name? \")\n"
            "print(\"Nice to meet you,\", user_name)\n\n"
            "# Converting input to a number\n"
            "age_str = input(\"Enter your age: \")  # always a string\n"
            "age = int(age_str)                    # convert to int\n"
            "print(\"Next year you will be\", age + 1)"
        ),
        "code_breakdown": (
            "print(\"Hello,\", name) — multiple arguments separated by commas are printed with a space between them.\n"
            "f\"Hello, {name}!\" — f-strings let you embed variable values directly in a string using {}.\n"
            "input() — always returns a str, even if the user types a number.\n"
            "int(age_str) — converts a string to an integer; use float() for decimals.\n"
            "Without conversion, age + 1 would cause a TypeError."
        ),
        "key_points": json.dumps([
            "print() displays output; input() collects user input.",
            "input() always returns a string (str).",
            "Convert input to int or float before doing arithmetic.",
            "f-strings (f'Hello {name}') are the modern way to format output.",
            "print() can accept multiple arguments separated by commas.",
        ]),
    },
]

QUESTIONS_BATCH_2 = [
    # L06 — Lists
    {
        "topic_id": "L06",
        "question_text": "What is the index of the first item in a Python list?",
        "option_a": "1", "option_b": "0",
        "option_c": "-1", "option_d": "None",
        "correct_option": "B",
        "hint_1": "Python doesn't start counting from 1 like humans naturally do.",
        "hint_2": "Most programming languages, including Python, start index counting from zero.",
        "hint_3": "B is correct: 0. The first item is always at index 0 in Python.",
    },
    {
        "topic_id": "L06",
        "question_text": "Which method adds an item to the end of a list?",
        "option_a": "add()", "option_b": "insert()",
        "option_c": "append()", "option_d": "push()",
        "correct_option": "C",
        "hint_1": "Think of the word that means 'to attach something to the end'.",
        "hint_2": "It's a list method starting with the letter 'a'.",
        "hint_3": "C is correct: append(). It adds one item to the end of the list.",
    },
    {
        "topic_id": "L06",
        "question_text": "What does fruits[-1] return for the list ['apple', 'banana', 'cherry']?",
        "option_a": "apple", "option_b": "banana",
        "option_c": "cherry", "option_d": "Error",
        "correct_option": "C",
        "hint_1": "Negative indices count from the end of the list.",
        "hint_2": "-1 refers to the very last item in any list.",
        "hint_3": "C is correct: cherry. -1 is always the last element.",
    },
    {
        "topic_id": "L06",
        "question_text": "What does len([10, 20, 30, 40]) return?",
        "option_a": "3", "option_b": "40",
        "option_c": "4", "option_d": "10",
        "correct_option": "C",
        "hint_1": "len() counts something about the list.",
        "hint_2": "It counts the total number of items, not their values.",
        "hint_3": "C is correct: 4. There are four items in the list.",
    },
    {
        "topic_id": "L06",
        "question_text": "How do you create an empty list in Python?",
        "option_a": "list = {}", "option_b": "list = []",
        "option_c": "list = ()", "option_d": "list = \"\"",
        "correct_option": "B",
        "hint_1": "Lists use a specific type of bracket.",
        "hint_2": "Square brackets [] are used for lists; {} is for dictionaries.",
        "hint_3": "B is correct: []. An empty pair of square brackets creates an empty list.",
    },
    # L07 — Dictionaries
    {
        "topic_id": "L07",
        "question_text": "How do you access the value for key 'name' in: student = {'name': 'Amina', 'age': 19}?",
        "option_a": "student.name", "option_b": "student[0]",
        "option_c": "student['name']", "option_d": "student.get(0)",
        "correct_option": "C",
        "hint_1": "Dictionaries are accessed by key, not by position.",
        "hint_2": "You use the key inside square brackets, similar to a list index.",
        "hint_3": "C is correct: student['name']. Use the key in square brackets to look up a value.",
    },
    {
        "topic_id": "L07",
        "question_text": "What are keys in a dictionary required to be?",
        "option_a": "Integers only", "option_b": "Strings only",
        "option_c": "Unique", "option_d": "In alphabetical order",
        "correct_option": "C",
        "hint_1": "Think about a real dictionary — can the same word appear twice?",
        "hint_2": "If two entries had the same key, Python wouldn't know which value to return.",
        "hint_3": "C is correct: Unique. Each key must appear only once in a dictionary.",
    },
    {
        "topic_id": "L07",
        "question_text": "Which symbol is used to define a dictionary in Python?",
        "option_a": "[]", "option_b": "()",
        "option_c": "{}", "option_d": "<>",
        "correct_option": "C",
        "hint_1": "Lists use square brackets. Dictionaries use a different pair.",
        "hint_2": "They look like curly/wavy braces.",
        "hint_3": "C is correct: {}. Curly braces define a dictionary.",
    },
    {
        "topic_id": "L07",
        "question_text": "What does the .keys() method return?",
        "option_a": "All values", "option_b": "All keys",
        "option_c": "The first key only", "option_d": "The length of the dictionary",
        "correct_option": "B",
        "hint_1": "The method name tells you exactly what it returns.",
        "hint_2": "keys() and values() are two different methods — each returns one side of the pairs.",
        "hint_3": "B is correct: All keys. .keys() returns a view of all the dictionary's keys.",
    },
    {
        "topic_id": "L07",
        "question_text": "How do you add a new key 'grade' with value 'A' to a dictionary called 'student'?",
        "option_a": "student.add('grade', 'A')", "option_b": "student.grade = 'A'",
        "option_c": "student['grade'] = 'A'", "option_d": "student.append({'grade': 'A'})",
        "correct_option": "C",
        "hint_1": "Adding to a dictionary uses the same syntax as accessing it.",
        "hint_2": "Assign a value to a new key using square brackets.",
        "hint_3": "C is correct: student['grade'] = 'A'. If the key doesn't exist it's created; if it does, it's updated.",
    },
    # L08 — Error Types
    {
        "topic_id": "L08",
        "question_text": "Which error occurs when Python cannot understand your code before it even runs?",
        "option_a": "RuntimeError", "option_b": "NameError",
        "option_c": "SyntaxError", "option_d": "TypeError",
        "correct_option": "C",
        "hint_1": "This error is caught before the program starts running.",
        "hint_2": "It's caused by breaking Python's grammar rules (missing colon, wrong indentation, etc.).",
        "hint_3": "C is correct: SyntaxError. It means Python can't interpret the code structure.",
    },
    {
        "topic_id": "L08",
        "question_text": "What error does print(score) cause if 'score' was never assigned a value?",
        "option_a": "TypeError", "option_b": "IndexError",
        "option_c": "SyntaxError", "option_d": "NameError",
        "correct_option": "D",
        "hint_1": "You are using a name (variable) that doesn't exist yet.",
        "hint_2": "This error literally says your variable 'name' is not defined.",
        "hint_3": "D is correct: NameError. Python can't find 'score' because it was never created.",
    },
    {
        "topic_id": "L08",
        "question_text": "What error does print('Age: ' + 19) cause?",
        "option_a": "SyntaxError", "option_b": "TypeError",
        "option_c": "ValueError", "option_d": "NameError",
        "correct_option": "B",
        "hint_1": "You are combining two different data types with +.",
        "hint_2": "Python can't add a string and an integer directly.",
        "hint_3": "B is correct: TypeError. Use str(19) or an f-string to fix it: f'Age: {19}'.",
    },
    {
        "topic_id": "L08",
        "question_text": "What is the purpose of a try/except block?",
        "option_a": "To speed up the program",
        "option_b": "To handle errors gracefully without crashing",
        "option_c": "To define a function",
        "option_d": "To repeat code multiple times",
        "correct_option": "B",
        "hint_1": "The word 'try' suggests attempting something that might fail.",
        "hint_2": "'except' catches the error if it happens.",
        "hint_3": "B is correct: handle errors gracefully. The program continues instead of crashing.",
    },
    {
        "topic_id": "L08",
        "question_text": "What error does items[5] cause for the list items = [1, 2, 3]?",
        "option_a": "KeyError", "option_b": "NameError",
        "option_c": "IndexError", "option_d": "ValueError",
        "correct_option": "C",
        "hint_1": "The list only has 3 items (indices 0, 1, 2). You are asking for index 5.",
        "hint_2": "You are accessing an 'index' that is out of the valid range.",
        "hint_3": "C is correct: IndexError. Index 5 doesn't exist in a 3-item list.",
    },
    # L09 — Basic I/O
    {
        "topic_id": "L09",
        "question_text": "What data type does input() always return?",
        "option_a": "int", "option_b": "float",
        "option_c": "str", "option_d": "It depends on what the user types",
        "correct_option": "C",
        "hint_1": "Even if the user types a number, input() wraps it in a specific type.",
        "hint_2": "It always treats the typed value as text.",
        "hint_3": "C is correct: str. input() always returns a string — convert with int() or float() as needed.",
    },
    {
        "topic_id": "L09",
        "question_text": "Which of the following correctly uses an f-string to display a variable?",
        "option_a": "print('Hello ' + {name})", "option_b": "print(f'Hello {name}')",
        "option_c": "print('Hello', {name})", "option_d": "print(Hello name)",
        "correct_option": "B",
        "hint_1": "f-strings start with the letter f before the opening quote.",
        "hint_2": "Variable names are placed inside curly braces {} within the f-string.",
        "hint_3": "B is correct: print(f'Hello {name}'). The 'f' prefix enables variable embedding.",
    },
    {
        "topic_id": "L09",
        "question_text": "What function is used to display output to the screen?",
        "option_a": "input()", "option_b": "write()",
        "option_c": "show()", "option_d": "print()",
        "correct_option": "D",
        "hint_1": "You've seen this function used in almost every Python example so far.",
        "hint_2": "It's the most basic output function in Python.",
        "hint_3": "D is correct: print(). It displays text and values to the console.",
    },
    {
        "topic_id": "L09",
        "question_text": "How do you convert the string '25' to an integer?",
        "option_a": "str('25')", "option_b": "convert('25')",
        "option_c": "integer('25')", "option_d": "int('25')",
        "correct_option": "D",
        "hint_1": "There is a built-in Python function that converts to integer.",
        "hint_2": "It's named after the word 'integer' but shortened.",
        "hint_3": "D is correct: int('25'). int() converts a string to an integer.",
    },
    {
        "topic_id": "L09",
        "question_text": "What happens when print() is called with two arguments separated by a comma: print('Hi', name)?",
        "option_a": "It causes an error",
        "option_b": "It prints only the first argument",
        "option_c": "It prints both with a space between them",
        "option_d": "It joins them with no space",
        "correct_option": "C",
        "hint_1": "print() accepts multiple arguments and handles spacing automatically.",
        "hint_2": "By default, print() separates arguments with a single space.",
        "hint_3": "C is correct. print('Hi', name) prints 'Hi Amina' (with a space) if name = 'Amina'.",
    },
]


def seed_batch2():
    with app.app_context():
        seeded_l = 0
        for data in LESSONS:
            if not db.session.get(Lesson, data["id"]):
                db.session.add(Lesson(**data))
                seeded_l += 1
        db.session.commit()
        print(f"[OK] Seeded {seeded_l} lessons (L06-L09).")

        seeded_q = 0
        for q in QUESTIONS_BATCH_2:
            exists = PracticeQuestion.query.filter_by(
                topic_id=q["topic_id"], question_text=q["question_text"]
            ).first()
            if not exists:
                db.session.add(PracticeQuestion(**q))
                seeded_q += 1
        db.session.commit()
        print(f"[OK] Seeded {seeded_q} practice questions (L06-L09).")


if __name__ == "__main__":
    seed_batch2()
