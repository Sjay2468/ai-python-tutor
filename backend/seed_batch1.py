"""
Seed script — Batch 1 (Amateur Tier)
======================================
Populates the database with the first 3 lessons of the Amateur tier:
  L01: Variables & Data Types
  L02: Operators
  L03: Basic I/O (input / print)   ← moved up so students can test code early

Topic hierarchy:
  🟢 AMATEUR  (beginner)    — L01, L02, L03
  🟡 INTERMEDIATE            — L04, L05, L06
  🔴 PRO (advanced)          — L07, L08, L09

Sources:
  T1 = Think Python 3rd ed. (Downey, 2024)   — Ch. 1–3
  T2 = Automate the Boring Stuff (Sweigart)   — Ch. 1
  T3 = Python Crash Course 3rd ed. (Matthes)  — Ch. 2
  O1 = W3Schools Python Tutorial
  O2 = Programiz — Learn Python
  O5 = Python Official Documentation (docs.python.org/3)
  R1 = Researcher-authored practice questions (Ayegba Shelter Iye)
  R2 = Real-world analogies (researcher-authored, Nigerian student context)
  E1 = Farah et al. (2023) — Common Python Errors Among Novice Learners
  E4 = Altadmri & Brown (2015) — 37 Million Compilations

Usage (from backend/ folder):
    .\\venv\\Scripts\\python seed_batch1.py
"""
import json
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from app import create_app, db
from app.models import Lesson, PracticeQuestion

app = create_app()

# ─────────────────────────────────────────────────────────────────────────────
# LESSON DATA  — Amateur Tier (difficulty = "beginner")
# ─────────────────────────────────────────────────────────────────────────────
LESSONS = [
    {
        "id": "L01",
        "title": "Variables & Data Types",
        "order_index": 1,
        "difficulty": "beginner",
        "explanation": (
            "WHAT IS A VARIABLE?\n"
            "A variable is a named storage location in your computer's memory that holds a value. "
            "You create a variable by writing a name, followed by an equals sign (=), "
            "followed by the value you want to store. "
            "In Python, you do not need to declare the type — Python automatically detects it for you "
            "(this is called dynamic typing).\n\n"
            "NAMING RULES (O5 — Python Docs):\n"
            "  • Names can only contain letters (a–z, A–Z), digits (0–9), and underscores (_)\n"
            "  • Names CANNOT start with a digit (e.g. '2score' is invalid)\n"
            "  • Names are CASE-SENSITIVE: 'age' and 'Age' are two completely different variables\n"
            "  • Avoid using Python reserved words like 'if', 'for', 'while' as variable names\n\n"
            "THE FOUR CORE DATA TYPES:\n"
            "  • int   — whole numbers with no decimal point  (e.g. 5, -3, 100, 0)\n"
            "  • float — numbers with a decimal point         (e.g. 3.14, -0.5, 2.0)\n"
            "  • str   — text (a sequence of characters) enclosed in quotes  (e.g. \"Hello\", 'Python')\n"
            "  • bool  — logical values: exactly True or False (capital T and F required)\n\n"
            "CHECKING THE TYPE:\n"
            "You can always ask Python what type a variable is by using the built-in type() function. "
            "This is especially useful when debugging.\n\n"
            "REASSIGNING VARIABLES:\n"
            "Unlike a constant, a variable's value can be changed at any time simply by assigning "
            "a new value to the same name. Python will forget the old value and remember the new one. "
            ""
        ),
        "analogy": (
            "Think of a variable like a labelled box in a storage room. "
            "The label on the box is the variable name, and whatever you put inside the box is the value. "
            "You can have many boxes with different labels (name, age, score), each holding different things. "
            "At any time you can open a box and replace what's inside — that's reassignment. "
            "Python reads the label to find the right box, not the position on the shelf."
        ),
        "code_example": (
            "# ── Creating variables of each data type ──────────────────────\n"
            "name       = \"Amina\"       # str   — text in quotes\n"
            "age        = 19             # int   — whole number\n"
            "gpa        = 3.8            # float — decimal number\n"
            "is_student = True           # bool  — True or False\n\n"
            "# ── Printing variable values ───────────────────────────────────\n"
            "print(name)                 # Output: Amina\n"
            "print(age)                  # Output: 19\n"
            "print(gpa)                  # Output: 3.8\n"
            "print(is_student)           # Output: True\n\n"
            "# ── Checking the data type ────────────────────────────────────\n"
            "print(type(name))           # Output: <class 'str'>\n"
            "print(type(age))            # Output: <class 'int'>\n"
            "print(type(gpa))            # Output: <class 'float'>\n\n"
            "# ── Reassigning a variable ────────────────────────────────────\n"
            "age = 20                    # age is now 20, not 19\n"
            "print(age)                  # Output: 20\n\n"
            "# ── Multiple assignment on one line ──────────────────────────\n"
            "x, y, z = 1, 2, 3          # x=1, y=2, z=3\n"
            "print(x, y, z)             # Output: 1 2 3"
        ),
        "code_breakdown": (
            "Line 2: name = \"Amina\"\n"
            "  → Creates a variable called 'name' and stores the string \"Amina\" inside it.\n"
            "  → Double quotes or single quotes both work for strings.\n\n"
            "Line 3: age = 19\n"
            "  → Creates an int variable called 'age'. No quotes around a number — quotes make it a string.\n\n"
            "Line 4: gpa = 3.8\n"
            "  → Creates a float variable. The decimal point is what makes it a float instead of an int.\n\n"
            "Line 5: is_student = True\n"
            "  → A bool variable. Note the capital T in True. Lowercase 'true' would cause a NameError.\n\n"
            "Line 8: print(name)\n"
            "  → The print() function displays the value stored in 'name' to the screen.\n\n"
            "Lines 12–14: print(type(...))\n"
            "  → type() is a built-in function that returns the class/type of any value.\n"
            "  → The output <class 'str'> confirms it is a string.\n\n"
            "Line 17: age = 20\n"
            "  → Reassigns the variable. The old value 19 is gone. age is now 20.\n\n"
            "Line 21: x, y, z = 1, 2, 3\n"
            "  → Python allows assigning multiple variables on one line using commas (tuple unpacking).\n"
            "  → This is shorthand for: x=1, then y=2, then z=3."
        ),
        "key_points": json.dumps([
            "A variable stores a value using the = (assignment) operator.",
            "Python detects the data type automatically — you don't declare it.",
            "The four core types are: int (whole number), float (decimal), str (text), bool (True/False).",
            "Variable names are case-sensitive: 'Name' and 'name' are different variables.",
            "Names must start with a letter or underscore, never a digit.",
            "Use type() to check what data type a variable holds.",
            "You can reassign a variable at any time — the old value is replaced.",
            "Always put text (strings) in quotes; numbers and booleans do NOT use quotes.",
        ]),
    },

    {
        "id": "L02",
        "title": "Operators",
        "order_index": 2,
        "difficulty": "beginner",
        "explanation": (
            "WHAT ARE OPERATORS?\n"
            "Operators are special symbols that tell Python to perform a specific action on "
            "one or more values (called operands). Python has five main categories of operators "
            "that beginners need to know.\n\n"
            "1. ARITHMETIC OPERATORS — for maths:\n"
            "  +   Addition          → 5 + 3  = 8\n"
            "  -   Subtraction       → 5 - 3  = 2\n"
            "  *   Multiplication    → 5 * 3  = 15\n"
            "  /   Division          → 5 / 2  = 2.5  (always gives a float)\n"
            "  //  Floor Division    → 5 // 2 = 2    (drops the decimal, rounds DOWN)\n"
            "  %   Modulus           → 5 % 2  = 1    (the REMAINDER after division)\n"
            "  **  Exponentiation    → 2 ** 3 = 8    (2 to the power of 3)\n\n"
            "2. COMPARISON OPERATORS — compare two values; always return True or False:\n"
            "  ==  Equal to          → 5 == 5 is True\n"
            "  !=  Not equal to      → 5 != 3 is True\n"
            "  >   Greater than      → 5 > 3  is True\n"
            "  <   Less than         → 5 < 3  is False\n"
            "  >=  Greater or equal  → 5 >= 5 is True\n"
            "  <=  Less or equal     → 3 <= 5 is True\n\n"
            "3. LOGICAL OPERATORS — combine conditions:\n"
            "  and → True only if BOTH sides are True\n"
            "  or  → True if AT LEAST ONE side is True\n"
            "  not → Reverses the boolean value (not True = False)\n\n"
            "4. ASSIGNMENT OPERATORS — store or update values:\n"
            "  =   Assign            → x = 5\n"
            "  +=  Add and assign    → x += 3  is shorthand for  x = x + 3\n"
            "  -=  Subtract & assign → x -= 2  is shorthand for  x = x - 2\n"
            "  *=  Multiply & assign → x *= 4  is shorthand for  x = x * 4\n\n"
            "COMMON BEGINNER MISTAKE:\n"
            "Using = (assignment) when you mean == (comparison) inside a condition. "
            "Remember: = stores a value; == checks if two values are equal."
        ),
        "analogy": (
            "Operators are like the buttons on a calculator. "
            "Just as pressing + on a calculator adds two numbers, "
            "Python's + operator adds two values in your program. "
            "Comparison operators are like a referee in a sports match — "
            "they look at both teams (values) and announce a verdict: True or False. "
            "Logical operators (and, or) are like combining rules: "
            "'You can enter the exam hall IF you have your student ID AND your exam form.'"
        ),
        "code_example": (
            "# ── Arithmetic operators ──────────────────────────────────────\n"
            "x = 10\n"
            "y = 3\n"
            "print(x + y)     # 13  — addition\n"
            "print(x - y)     # 7   — subtraction\n"
            "print(x * y)     # 30  — multiplication\n"
            "print(x / y)     # 3.3333... — true division (always float)\n"
            "print(x // y)    # 3   — floor division (drops decimal)\n"
            "print(x % y)     # 1   — modulus (remainder: 10 = 3×3 + 1)\n"
            "print(x ** y)    # 1000 — exponent (10 to the power of 3)\n\n"
            "# ── Comparison operators (return True or False) ───────────────\n"
            "print(x > y)     # True   — 10 is greater than 3\n"
            "print(x == y)    # False  — 10 is not equal to 3\n"
            "print(x != y)    # True   — 10 is not equal to 3\n"
            "print(x >= 10)   # True   — 10 is greater than or equal to 10\n\n"
            "# ── Logical operators ─────────────────────────────────────────\n"
            "print(x > 5 and y < 5)   # True  — both are true\n"
            "print(x > 5 and y > 5)   # False — second is false\n"
            "print(x > 5 or  y > 5)   # True  — first is true\n"
            "print(not x > 5)          # False — reverses True to False\n\n"
            "# ── Assignment operators ──────────────────────────────────────\n"
            "score = 50\n"
            "score += 10      # same as: score = score + 10  →  score is now 60\n"
            "score -= 5       # same as: score = score - 5   →  score is now 55\n"
            "print(score)     # 55"
        ),
        "code_breakdown": (
            "Lines 2–3: x = 10, y = 3\n"
            "  → Two int variables for the examples below.\n\n"
            "Line 6: print(x / y)  →  3.3333...\n"
            "  → The / operator ALWAYS returns a float, even if the result is a whole number.\n"
            "  → e.g. 4 / 2 returns 2.0, not 2.\n\n"
            "Line 7: print(x // y)  →  3\n"
            "  → Floor division divides and then ROUNDS DOWN to the nearest whole number.\n"
            "  → 10 / 3 = 3.333... → floor gives 3.\n\n"
            "Line 8: print(x % y)  →  1\n"
            "  → The modulus gives the REMAINDER after full division.\n"
            "  → 10 = 3×3 + 1, so the remainder is 1.\n"
            "  → Very useful: check if a number is even (n % 2 == 0) or odd (n % 2 == 1).\n\n"
            "Line 9: print(x ** y)  →  1000\n"
            "  → ** means 'to the power of'. 10**3 = 10 × 10 × 10 = 1000.\n\n"
            "Line 12: print(x > y)  →  True\n"
            "  → Comparison operators always produce a bool (True or False).\n\n"
            "Line 17: print(x > 5 and y < 5)  →  True\n"
            "  → 'and' requires BOTH conditions to be True. 10>5 is True AND 3<5 is True → True.\n\n"
            "Line 23: score += 10\n"
            "  → Shorthand for score = score + 10. Very common in loops to count up or down."
        ),
        "key_points": json.dumps([
            "Arithmetic operators: + - * / // % ** perform mathematical calculations.",
            "/ (true division) always returns a float. // (floor division) returns an int.",
            "% (modulus) gives the REMAINDER after division — useful for checking even/odd.",
            "Comparison operators (==, !=, >, <, >=, <=) always return True or False.",
            "CRITICAL: = is assignment (stores a value); == is comparison (checks equality).",
            "Logical operators: 'and' needs both True; 'or' needs at least one True; 'not' reverses.",
            "Shorthand operators (+=, -=, *=) update a variable without rewriting its name.",
            "Operator precedence follows BODMAS/PEMDAS — use parentheses () to control order.",
        ]),
    },

    {
        "id": "L03",
        "title": "Basic I/O (input / print)",
        "order_index": 3,
        "difficulty": "beginner",
        "explanation": (
            "WHAT IS I/O?\n"
            "I/O stands for Input and Output — the two ways your program communicates with the user. "
            "Without I/O, a program works in silence and nobody can interact with it.\n\n"
            "OUTPUT — print():\n"
            "The print() function displays text, numbers, or variable values on the screen. "
            "It is the most-used function in Python and the first thing every beginner learns.\n"
            "  • You can pass multiple values separated by commas — print() adds a space between them.\n"
            "  • You can customise the separator with the sep parameter: print('a','b', sep='-') → a-b\n"
            "  • By default print() adds a new line at the end. Use end='' to prevent this.\n\n"
            "F-STRINGS (Formatted Strings):\n"
            "The modern way to embed variable values directly inside a string is to use an f-string. "
            "Place the letter f before the opening quote, then put variable names inside curly braces {}.\n"
            "  Example: name = 'Amina'  →  print(f'Hello, {name}!')  →  Hello, Amina!\n\n"
            "INPUT — input():\n"
            "The input() function pauses the program and waits for the user to type something "
            "and press Enter. Whatever the user types is returned as a string.\n\n"
            "CRITICAL RULE — input() ALWAYS returns a string (str):\n"
            "This is one of the most common beginner mistakes. If a user types '25', Python stores "
            "the two-character string '25', NOT the number 25. "
            "To use it as a number you MUST convert it:\n"
            "  int(input(...))   — converts to whole number\n"
            "  float(input(...)) — converts to decimal number\n"
            "Skipping this conversion and then doing arithmetic will cause a TypeError."
        ),
        "analogy": (
            "Think of print() as your program's mouth — it speaks to the user by displaying text on screen. "
            "Think of input() as your program's ears — it listens to what the user types "
            "and remembers it as a string. "
            "The key rule to remember: your program's ears only understand text. "
            "If someone says the number 'twenty-five', you still hear it as a word, not a number. "
            "You have to translate (convert) it yourself before you can do maths with it."
        ),
        "code_example": (
            "# ── Basic output with print() ─────────────────────────────────\n"
            "print(\"Welcome to Python Tutor!\")         # plain text\n"
            "print(\"The answer is:\", 42)               # multiple args, auto-space\n"
            "print(\"Line 1\", end=\" \")                  # no newline at end\n"
            "print(\"still on same line\")               # joins to previous\n\n"
            "# ── F-strings (modern variable formatting) ────────────────────\n"
            "name  = \"Amina\"\n"
            "score = 87\n"
            "print(f\"Hello, {name}!\")                  # Hello, Amina!\n"
            "print(f\"{name} scored {score}/100.\")      # Amina scored 87/100.\n"
            "print(f\"Double score: {score * 2}\")       # expression inside {}\n\n"
            "# ── Basic input() ─────────────────────────────────────────────\n"
            "user_name = input(\"What is your name? \")  # waits for user to type\n"
            "print(f\"Nice to meet you, {user_name}!\")\n\n"
            "# ── Converting input to a number ──────────────────────────────\n"
            "age_str = input(\"Enter your age: \")        # returns a str, e.g. '19'\n"
            "age     = int(age_str)                      # convert '19' → 19 (int)\n"
            "print(f\"Next year you will be {age + 1}.\") # now arithmetic works\n\n"
            "# ── Shorter form: convert on the same line ────────────────────\n"
            "height = float(input(\"Enter your height in cm: \"))\n"
            "print(f\"Your height is {height} cm.\")"
        ),
        "code_breakdown": (
            "Line 2: print(\"Welcome to Python Tutor!\")\n"
            "  → Prints exactly the text inside the quotes.\n\n"
            "Line 3: print(\"The answer is:\", 42)\n"
            "  → Passing two arguments. print() joins them with a space: 'The answer is: 42'.\n\n"
            "Lines 4–5: print(\"Line 1\", end=\" \") then print(\"still on same line\")\n"
            "  → By default print() ends with a newline ('\\n'). Setting end=\" \" replaces it with a space,\n"
            "    so the next print() continues on the SAME line.\n\n"
            "Line 9: print(f\"Hello, {name}!\")\n"
            "  → The 'f' prefix turns this into an f-string.\n"
            "  → {name} is a placeholder — Python replaces it with the current value of 'name'.\n\n"
            "Line 11: print(f\"Double score: {score * 2}\")\n"
            "  → You can place any Python expression inside {} in an f-string, not just variable names.\n\n"
            "Line 14: user_name = input(\"What is your name? \")\n"
            "  → The string inside input() is the 'prompt' — it is shown to the user before they type.\n"
            "  → Whatever the user types is stored as a str in user_name.\n\n"
            "Lines 17–19: age_str = input(...) then age = int(age_str)\n"
            "  → input() returns '19' (a str). int('19') converts it to the integer 19.\n"
            "  → Without int(), doing age + 1 would cause TypeError: can only concatenate str (not 'int') to str.\n\n"
            "Line 22: float(input(...))\n"
            "  → A shortcut: wrap input() directly inside float() on the same line.\n"
            "  → Use int() for whole numbers, float() for decimals."
        ),
        "key_points": json.dumps([
            "print() displays output to the screen — it is the most-used function in Python.",
            "Separate multiple print() arguments with commas — Python adds a space between them.",
            "f-strings (f'Hello {name}') are the modern, readable way to embed variables in text.",
            "You can use any Python expression inside the {} of an f-string.",
            "input() pauses the program and waits for the user to type something.",
            "CRITICAL: input() ALWAYS returns a string (str), even if the user types a number.",
            "Convert input to a number using int() for whole numbers or float() for decimals.",
            "Forgetting to convert input before arithmetic is one of the most common beginner bugs.",
        ]),
    },
]

# ─────────────────────────────────────────────────────────────────────────────
# PRACTICE QUESTIONS  — Amateur Tier (5 per lesson, 15 total)
# Sources: R1 (researcher-authored), E1, E4 (error pattern literature)
# ─────────────────────────────────────────────────────────────────────────────
QUESTIONS_BATCH_1 = [
    # ── L01 — Variables & Data Types ─────────────────────────────────────────
    {
        "topic_id": "L01",
        "question_text": "What is the data type of the value in: x = 3.14?",
        "option_a": "int", "option_b": "float",
        "option_c": "str",  "option_d": "bool",
        "correct_option": "B",
        "hint_1": "Think about whether 3.14 is a whole number or a decimal number.",
        "hint_2": "In Python, numbers WITH a decimal point are called 'float' (floating-point numbers).",
        "hint_3": "3.14 has a decimal point, so its type is float. The answer is B.",
    },
    {
        "topic_id": "L01",
        "question_text": "Which of the following correctly creates a variable that stores the text 'Python'?",
        "option_a": "x = Python",
        "option_b": "x = 'Python'",
        "option_c": "x == 'Python'",
        "option_d": "str = Python",
        "correct_option": "B",
        "hint_1": "Text (strings) must be wrapped in quotes in Python.",
        "hint_2": "Single quotes or double quotes both work for strings. Look for quotes around the word Python.",
        "hint_3": "B is correct: x = 'Python'. Without quotes, Python thinks 'Python' is a variable name, not text.",
    },
    {
        "topic_id": "L01",
        "question_text": "What does print(type(x)) display if x = 10?",
        "option_a": "float",
        "option_b": "str",
        "option_c": "<class 'int'>",
        "option_d": "True",
        "correct_option": "C",
        "hint_1": "10 is a whole number — no decimal point. Which type represents whole numbers?",
        "hint_2": "type() returns the full class name of the value. For whole numbers Python reports 'int'.",
        "hint_3": "C is correct: <class 'int'>. The type() function always returns the class name in angle brackets.",
    },
    {
        "topic_id": "L01",
        "question_text": "Which of the following is a valid Python variable name?",
        "option_a": "2score",
        "option_b": "my-score",
        "option_c": "my_score",
        "option_d": "my score",
        "correct_option": "C",
        "hint_1": "Variable names cannot start with a digit, and cannot contain spaces or hyphens.",
        "hint_2": "Python variable names can only use letters, digits, and underscores (_).",
        "hint_3": "C is correct: my_score. Underscores are allowed. Spaces, hyphens, and leading digits are not.",
    },
    {
        "topic_id": "L01",
        "question_text": "What are the only two possible values a bool variable can hold?",
        "option_a": "0 and 1",
        "option_b": "yes and no",
        "option_c": "True or False",
        "option_d": "on and off",
        "correct_option": "C",
        "hint_1": "Think about the word 'boolean' — it comes from binary logic with exactly two states.",
        "hint_2": "In Python, the two boolean values are capitalised. Lowercase 'true' would be a NameError.",
        "hint_3": "C is correct: True or False. These are the only two values a bool can hold. Capital letters are required.",
    },

    # ── L02 — Operators ───────────────────────────────────────────────────────
    {
        "topic_id": "L02",
        "question_text": "What is the result of 10 % 3 in Python?",
        "option_a": "3", "option_b": "0",
        "option_c": "1", "option_d": "3.33",
        "correct_option": "C",
        "hint_1": "The % operator gives the REMAINDER after division, not the quotient.",
        "hint_2": "10 divided by 3 is 3 remainder 1. That remainder is what % returns.",
        "hint_3": "C is correct: 1. 10 = 3×3 + 1, so 10 % 3 = 1.",
    },
    {
        "topic_id": "L02",
        "question_text": "Which operator checks whether two values are EQUAL?",
        "option_a": "=", "option_b": "==",
        "option_c": "!=", "option_d": ">=",
        "correct_option": "B",
        "hint_1": "One equals sign (=) assigns a value to a variable. Another symbol is used for comparison.",
        "hint_2": "Equality comparison uses TWO equals signs together: ==.",
        "hint_3": "B is correct: ==. A single = assigns; double == compares. Mixing them up is the #1 beginner error.",
    },
    {
        "topic_id": "L02",
        "question_text": "What does 2 ** 3 evaluate to?",
        "option_a": "6", "option_b": "5",
        "option_c": "9", "option_d": "8",
        "correct_option": "D",
        "hint_1": "The ** operator means 'to the power of' — it is Python's exponentiation operator.",
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
        "hint_2": "Since one side (False) is not True, the entire 'and' expression is False.",
        "hint_3": "B is correct: False. 'and' only returns True when BOTH operands are True.",
    },
    {
        "topic_id": "L02",
        "question_text": "What does 15 // 4 return?",
        "option_a": "3.75", "option_b": "4",
        "option_c": "3", "option_d": "11",
        "correct_option": "C",
        "hint_1": "// is floor division — it divides and then removes the decimal part, rounding DOWN.",
        "hint_2": "15 / 4 = 3.75. Floor division keeps only the whole number part: 3.",
        "hint_3": "C is correct: 3. Floor division discards the decimal, so 3.75 becomes 3.",
    },

    # ── L03 — Basic I/O ───────────────────────────────────────────────────────
    {
        "topic_id": "L03",
        "question_text": "What data type does input() ALWAYS return?",
        "option_a": "int",
        "option_b": "float",
        "option_c": "str",
        "option_d": "It depends on what the user types",
        "correct_option": "C",
        "hint_1": "Even if the user types a number like 25, input() still wraps it in a specific type.",
        "hint_2": "input() always treats what the user typed as text, regardless of what they typed.",
        "hint_3": "C is correct: str. input() ALWAYS returns a string. Convert with int() or float() to use it as a number.",
    },
    {
        "topic_id": "L03",
        "question_text": "Which of the following correctly uses an f-string to display a variable?",
        "option_a": "print('Hello ' + {name})",
        "option_b": "print(f'Hello {name}')",
        "option_c": "print('Hello', {name})",
        "option_d": "print(Hello name)",
        "correct_option": "B",
        "hint_1": "f-strings start with the letter f placed directly before the opening quote.",
        "hint_2": "Variable names are embedded inside curly braces {} within the f-string.",
        "hint_3": "B is correct: print(f'Hello {name}'). The 'f' prefix enables variable embedding with {}.",
    },
    {
        "topic_id": "L03",
        "question_text": "What happens when you run: age = input('Enter age: ') then print(age + 1)?",
        "option_a": "It prints the age plus 1 correctly",
        "option_b": "It causes a TypeError",
        "option_c": "It prints 'age1'",
        "option_d": "It prints 0",
        "correct_option": "B",
        "hint_1": "Remember what type input() always returns.",
        "hint_2": "You cannot add a string and an integer directly in Python — the types must match.",
        "hint_3": "B is correct: TypeError. age is a str (e.g. '19') and you can't add str + int. Fix: age = int(input('Enter age: ')).",
    },
    {
        "topic_id": "L03",
        "question_text": "What does print('A', 'B', 'C') output?",
        "option_a": "ABC",
        "option_b": "A,B,C",
        "option_c": "A B C",
        "option_d": "Error",
        "correct_option": "C",
        "hint_1": "print() accepts multiple arguments separated by commas.",
        "hint_2": "By default, print() places a space between each argument it receives.",
        "hint_3": "C is correct: A B C. print() uses a space as the default separator. Use sep='' to remove it.",
    },
    {
        "topic_id": "L03",
        "question_text": "Which function is used to display output on the screen in Python?",
        "option_a": "input()",
        "option_b": "display()",
        "option_c": "show()",
        "option_d": "print()",
        "correct_option": "D",
        "hint_1": "You have already seen this function used in every example in the lesson.",
        "hint_2": "It is the most basic output function in Python and starts with the letter 'p'.",
        "hint_3": "D is correct: print(). It is Python's built-in function for displaying values on the screen.",
    },
]


def seed_lessons_batch1():
    """Seed Amateur-tier lessons (L01–L03) and their practice questions."""
    with app.app_context():
        seeded = 0
        for data in LESSONS:
            existing = db.session.get(Lesson, data["id"])
            if existing:
                # Update existing record with new detailed content
                for key, value in data.items():
                    setattr(existing, key, value)
                seeded += 1
            else:
                lesson = Lesson(**data)
                db.session.add(lesson)
                seeded += 1
        db.session.commit()
        print(f"[OK] Seeded/updated {seeded} Amateur-tier lessons (L01-L03).")

        q_seeded = 0
        for q in QUESTIONS_BATCH_1:
            existing = PracticeQuestion.query.filter_by(
                topic_id=q["topic_id"], question_text=q["question_text"]
            ).first()
            if not existing:
                db.session.add(PracticeQuestion(**q))
                q_seeded += 1
        db.session.commit()
        print(f"[OK] Seeded {q_seeded} practice questions (L01-L03).")


if __name__ == "__main__":
    seed_lessons_batch1()
