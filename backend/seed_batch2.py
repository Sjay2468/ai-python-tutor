"""
Seed script — Batch 2 (Intermediate & Pro Tiers)
==================================================
Populates the database with 6 lessons across two tiers:

  🟡 INTERMEDIATE (difficulty = "intermediate"):
      L04: Conditionals (if / elif / else)
      L05: Loops (for / while)
      L06: Functions

  🔴 PRO (difficulty = "advanced"):
      L07: Lists
      L08: Dictionaries
      L09: Error Types & Debugging

Sources:
  T1 = Think Python 3rd ed. (Downey, 2024)   — Ch. 3, 5, 7, 10, 11
  T2 = Automate the Boring Stuff (Sweigart)   — Ch. 2, 3, 4
  T3 = Python Crash Course 3rd ed. (Matthes)  — Ch. 3, 4, 5, 7
  T4 = Learning Python (Lutz, 2013)           — Ch. 9, 13
  O1 = W3Schools Python Tutorial
  O2 = Programiz — Learn Python
  O3 = GeeksforGeeks — Python Programming Language
  O4 = Real Python
  O5 = Python Official Documentation
  R1 = Researcher-authored practice questions (Ayegba Shelter Iye)
  R2 = Real-world analogies (researcher-authored, Nigerian student context)
  E1 = Farah et al. (2023) — Common Python Errors Among Novice Learners
  E2 = Huang et al. (2023) — Classifying Beginner Errors in Python (ICER 2023)
  E3 = Mow (2006) — Problems in Teaching 'Introduction to Programming'
  E4 = Altadmri & Brown (2015) — 37 Million Compilations

Usage (from backend/ folder):
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
    # ─────────────────────────────────────────────────────────────────────────
    # INTERMEDIATE TIER
    # ─────────────────────────────────────────────────────────────────────────
    {
        "id": "L04",
        "title": "Conditionals (if / elif / else)",
        "order_index": 4,
        "difficulty": "intermediate",
        "explanation": (
            "WHAT ARE CONDITIONALS?\n"
            "Conditionals allow your program to make decisions — to choose a different path "
            "of execution depending on whether a condition is True or False. "
            "Without conditionals, every program would do exactly the same thing every time it runs. "
            "\n\n"
            "THE THREE KEYWORDS:\n"
            "  • if   — checks the first condition. Its code block runs only if the condition is True.\n"
            "  • elif — short for 'else if'. Checked only if all previous conditions were False.\n"
            "           You can chain as many elif blocks as needed.\n"
            "  • else — the fallback. Runs only when NO previous condition was True.\n"
            "           There can only be ONE else per if-block, and it comes last.\n\n"
            "INDENTATION IS MANDATORY:\n"
            "Python uses indentation (4 spaces) to define which lines of code belong inside "
            "a conditional block. Unlike other languages that use curly braces {}, "
            "Python uses whitespace. Incorrect indentation is one of the most common beginner errors. "
            "\n\n"
            "THE COLON IS MANDATORY:\n"
            "Every if, elif, and else line MUST end with a colon (:). "
            "Forgetting the colon is the #1 SyntaxError for beginners.\n\n"
            "NESTED CONDITIONALS:\n"
            "You can place an if-block inside another if-block. This is called nesting. "
            "Each nested level requires an additional 4 spaces of indentation. "
            "Keep nesting shallow (max 2–3 levels) to keep your code readable.\n\n"
            "TRUTHINESS AND FALSINESS:\n"
            "In Python, conditions do not have to be strict True/False booleans. "
            "Values that are considered False: 0, 0.0, '' (empty string), [] (empty list), None.\n"
            "Everything else is considered True."
        ),
        "analogy": (
            "Think of a conditional like the security checkpoint at a university gate. "
            "If you have a valid student ID, you enter through the main gate. "
            "Elif you are a staff member with a staff card, you enter through the staff gate. "
            "Else (none of the above), you must wait at the visitor's desk. "
            "The guard checks each condition IN ORDER and stops at the first match — "
            "that is exactly how Python's if/elif/else works."
        ),
        "code_example": (
            "# ── Basic if / elif / else ────────────────────────────────────\n"
            "score = 75\n\n"
            "if score >= 70:\n"
            "    print(\"Excellent! Topic mastered.\")\n"
            "elif score >= 50:\n"
            "    print(\"Good effort. Keep practicing.\")\n"
            "elif score >= 30:\n"
            "    print(\"Needs improvement. Review the lesson.\")\n"
            "else:\n"
            "    print(\"Please re-read the lesson from the start.\")\n\n"
            "# ── Conditional with user input ────────────────────────────────\n"
            "age = int(input(\"Enter your age: \"))\n\n"
            "if age >= 18:\n"
            "    print(\"You are an adult.\")\n"
            "else:\n"
            "    print(\"You are a minor.\")\n\n"
            "# ── Nested conditional ─────────────────────────────────────────\n"
            "marks = 85\n"
            "attended = True\n\n"
            "if marks >= 50:\n"
            "    if attended:                    # nested inside the first if\n"
            "        print(\"Pass with attendance bonus!\")\n"
            "    else:\n"
            "        print(\"Pass, but attendance is low.\")\n"
            "else:\n"
            "    print(\"Fail.\")\n\n"
            "# ── Combining conditions with 'and' / 'or' ─────────────────────\n"
            "x = 15\n"
            "if x > 10 and x < 20:\n"
            "    print(f\"{x} is a teen number\")  # prints: 15 is a teen number"
        ),
        "code_breakdown": (
            "Line 4: if score >= 70:\n"
            "  → The 'if' keyword checks whether score >= 70 is True.\n"
            "  → The colon (:) at the end is REQUIRED. Missing it causes SyntaxError.\n\n"
            "Line 5:     print(\"Excellent! Topic mastered.\")\n"
            "  → 4 spaces of indentation tell Python this line belongs inside the if block.\n"
            "  → This line runs ONLY if score >= 70 is True.\n\n"
            "Line 6: elif score >= 50:\n"
            "  → Checked only if the first 'if' was False.\n"
            "  → If score is 75, this elif is SKIPPED — Python stops at the first True match.\n\n"
            "Line 9: else:\n"
            "  → No condition here — it catches EVERYTHING that didn't match above.\n"
            "  → It must come last and there can only be one else per if-block.\n\n"
            "Lines 13–14: age = int(input(...))\n"
            "  → Converts the string input to an int before comparing.\n"
            "  → Without int(), comparing age >= 18 with a string would cause TypeError.\n\n"
            "Lines 20–26: Nested conditional\n"
            "  → The inner if/else (lines 22–25) only runs if the outer if (line 20) is True.\n"
            "  → Each nested level adds another 4 spaces of indentation.\n\n"
            "Line 30: if x > 10 and x < 20:\n"
            "  → Combines two conditions with 'and' — both must be True for the block to run."
        ),
        "key_points": json.dumps([
            "if checks the first condition; elif checks additional conditions; else is the fallback.",
            "Python uses indentation (4 spaces) to group code inside a block — NOT curly braces.",
            "Every if, elif, and else line MUST end with a colon (:) — missing it is a SyntaxError.",
            "Python evaluates conditions TOP to BOTTOM and stops at the FIRST True match.",
            "A condition does not need to be a bool — 0, '', [], None are treated as False.",
            "You can combine conditions with 'and', 'or', 'not' in a single if statement.",
            "Nested if statements are allowed but should be kept shallow (max 2–3 levels).",
            "There can only be one 'else' per if-block, and it must come last.",
        ]),
    },

    {
        "id": "L05",
        "title": "Loops (for / while)",
        "order_index": 5,
        "difficulty": "intermediate",
        "explanation": (
            "WHAT ARE LOOPS?\n"
            "A loop is a control structure that repeats a block of code multiple times. "
            "Without loops, you would have to copy-paste the same code hundreds of times. "
            "Python has two types of loops: for and while.\n\n"
            "THE FOR LOOP — iterate over a sequence:\n"
            "A for loop goes through each item in a sequence (a list, string, or range) "
            "one at a time, running the loop body for each item.\n"
            "  Syntax: for variable in sequence:\n"
            "               code to repeat\n\n"
            "THE range() FUNCTION:\n"
            "range(n)        → generates 0, 1, 2, ... n-1  (n items, starting at 0)\n"
            "range(a, b)     → generates a, a+1, ... b-1   (starts at a, stops BEFORE b)\n"
            "range(a, b, s)  → generates a, a+s, a+2s ...  (step s between each number)\n\n"
            "THE WHILE LOOP — repeat based on condition:\n"
            "A while loop repeats its body AS LONG AS its condition is True. "
            "It is used when you do NOT know in advance how many iterations you need — "
            "for example, when waiting for valid user input.\n"
            "  Syntax: while condition:\n"
            "               code to repeat\n\n"
            "CRITICAL — AVOID INFINITE LOOPS:\n"
            "If the while loop's condition never becomes False, the loop runs forever "
            "(an infinite loop). Always make sure the loop variable is updated inside the body.\n\n"
            "LOOP CONTROL KEYWORDS:\n"
            "  • break    — exits the loop immediately, regardless of the condition\n"
            "  • continue — skips the rest of the current iteration and goes to the next one\n"
            "  • else     — (unique to Python) runs after a loop completes NORMALLY (not broken)\n\n"
            "NESTED LOOPS:\n"
            "You can place a loop inside another loop. The inner loop completes ALL of its "
            "iterations for EACH single iteration of the outer loop. "
            "Use nested loops carefully — they multiply execution time rapidly."
        ),
        "analogy": (
            "A for loop is like a market trader calling out each item on a fixed list: "
            "'Apple!... Banana!... Cherry!' — one by one until the list is done. "
            "A while loop is like a student studying for an exam: "
            "they keep reading WHILE they don't fully understand the topic yet. "
            "Once they understand, they stop. The key difference: "
            "for loops know exactly how many times they repeat (fixed list), "
            "while loops repeat until something changes (condition)."
        ),
        "code_example": (
            "# ── for loop with range() ─────────────────────────────────────\n"
            "for i in range(5):\n"
            "    print(i)             # prints: 0, 1, 2, 3, 4\n\n"
            "# ── range(start, stop, step) ─────────────────────────────────\n"
            "for i in range(1, 10, 2):\n"
            "    print(i)             # prints: 1, 3, 5, 7, 9 (odd numbers)\n\n"
            "# ── for loop over a list ──────────────────────────────────────\n"
            "fruits = [\"apple\", \"banana\", \"cherry\"]\n"
            "for fruit in fruits:\n"
            "    print(f\"I like {fruit}\")\n\n"
            "# ── for loop over a string ────────────────────────────────────\n"
            "word = \"Python\"\n"
            "for letter in word:\n"
            "    print(letter)       # prints each letter on its own line\n\n"
            "# ── while loop ────────────────────────────────────────────────\n"
            "count = 0\n"
            "while count < 3:\n"
            "    print(f\"count = {count}\")\n"
            "    count += 1          # IMPORTANT: update count or loop runs forever!\n"
            "# Output: count=0, count=1, count=2\n\n"
            "# ── break and continue ────────────────────────────────────────\n"
            "for n in range(10):\n"
            "    if n == 3:\n"
            "        continue        # skip 3\n"
            "    if n == 6:\n"
            "        break           # stop loop at 6\n"
            "    print(n)            # prints: 0, 1, 2, 4, 5\n\n"
            "# ── while loop for user input validation ──────────────────────\n"
            "answer = \"\"\n"
            "while answer != \"yes\":\n"
            "    answer = input(\"Type 'yes' to continue: \")\n"
            "print(\"Thank you!\")"
        ),
        "code_breakdown": (
            "Lines 2–3: for i in range(5): print(i)\n"
            "  → range(5) generates the sequence 0, 1, 2, 3, 4.\n"
            "  → Each iteration assigns one number to 'i' and runs the indented body.\n\n"
            "Lines 6–7: for i in range(1, 10, 2)\n"
            "  → Starts at 1, stops BEFORE 10, steps by 2 → produces 1, 3, 5, 7, 9.\n\n"
            "Lines 10–11: for fruit in fruits\n"
            "  → Iterates directly over a list. 'fruit' holds each item in turn.\n"
            "  → No index numbers needed — Python handles the position automatically.\n\n"
            "Lines 14–15: for letter in word\n"
            "  → Strings are sequences too — you can loop over them character by character.\n\n"
            "Lines 18–21: while count < 3\n"
            "  → The condition is checked BEFORE each iteration.\n"
            "  → count += 1 is critical — without it, count stays 0 forever (infinite loop).\n\n"
            "Lines 24–29: break and continue\n"
            "  → continue (line 25): skips the rest of the loop body for n=3 and jumps to n=4.\n"
            "  → break (line 27): exits the entire loop immediately when n=6.\n"
            "  → Result: 0, 1, 2 (skips 3), 4, 5 (stops at 6, 6 is not printed).\n\n"
            "Lines 32–34: while loop for input validation\n"
            "  → Keeps asking for input until the user types exactly 'yes'.\n"
            "  → This pattern (input validation loop) is very common in real programs."
        ),
        "key_points": json.dumps([
            "A 'for' loop iterates over a sequence (list, string, range) for a fixed number of steps.",
            "range(n) produces 0 to n-1. range(a,b) produces a to b-1. range(a,b,s) adds a step.",
            "A 'while' loop repeats as long as its condition is True — use when count is unknown.",
            "ALWAYS update the loop variable in a while loop to avoid an infinite loop.",
            "'break' exits the loop immediately; 'continue' skips to the next iteration.",
            "You can loop over strings character-by-character just like a list.",
            "Nested loops run the inner loop fully for each single step of the outer loop.",
            "Python's loop 'else' clause runs only if the loop completed without hitting 'break'.",
        ]),
    },

    {
        "id": "L06",
        "title": "Functions",
        "order_index": 6,
        "difficulty": "intermediate",
        "explanation": (
            "WHAT IS A FUNCTION?\n"
            "A function is a named, reusable block of code that performs a specific task. "
            "You define it once and call it as many times as needed, from anywhere in your program. "
            "Functions are fundamental to writing clean, non-repetitive code. "
            "\n\n"
            "WHY USE FUNCTIONS?\n"
            "  • Avoid repetition (Don't Repeat Yourself — the DRY principle)\n"
            "  • Break a big problem into smaller, manageable pieces\n"
            "  • Make code easier to read, test, and debug\n"
            "  • Reuse the same logic with different input values\n\n"
            "DEFINING A FUNCTION:\n"
            "  def function_name(parameter1, parameter2):\n"
            "      code body\n"
            "      return value     ← optional\n\n"
            "PARAMETERS vs ARGUMENTS:\n"
            "  • Parameters are the variable names listed in the def line (the blueprint).\n"
            "  • Arguments are the actual values you pass when calling the function.\n"
            "  • Example: def greet(name)  ← 'name' is the parameter\n"
            "             greet('Amina')   ← 'Amina' is the argument\n\n"
            "DEFAULT PARAMETERS:\n"
            "You can give a parameter a default value using =. If no argument is passed for that "
            "parameter when calling the function, Python uses the default value.\n"
            "  Example: def power(base, exponent=2) → power(5) returns 25 (5²)\n\n"
            "THE RETURN STATEMENT:\n"
            "  • return sends a value BACK to the caller of the function.\n"
            "  • Once Python hits a return statement, the function STOPS immediately.\n"
            "  • A function without a return statement automatically returns None.\n"
            "  • return is different from print() — print() displays output on screen,\n"
            "    but does NOT send a value back to the rest of the program.\n\n"
            "SCOPE — LOCAL vs GLOBAL VARIABLES:\n"
            "Variables created INSIDE a function are local — they only exist within that function "
            "and are destroyed when the function finishes. "
            "Variables created OUTSIDE functions are global — accessible everywhere. "
            "Beginners often try to use a function's local variable outside the function and get "
            "a NameError."
        ),
        "analogy": (
            "A function is like a recipe in a cookbook. You write the recipe once (define the function), "
            "specifying what ingredients you need (parameters). "
            "Whenever you want to cook that dish, you follow the recipe (call the function), "
            "providing the actual ingredients you have (arguments). "
            "The dish you produce at the end is the return value. "
            "Anyone in the house can use the same recipe (reusability), "
            "and you don't need to rewrite it each time."
        ),
        "code_example": (
            "# ── Defining and calling a simple function ────────────────────\n"
            "def greet(name):\n"
            "    message = f\"Hello, {name}! Welcome to Python Tutor.\"\n"
            "    return message\n\n"
            "result = greet(\"Amina\")       # call the function\n"
            "print(result)                  # Hello, Amina! Welcome to Python Tutor.\n"
            "print(greet(\"Chukwuemeka\"))    # call again with different argument\n\n"
            "# ── Function with multiple parameters ─────────────────────────\n"
            "def add(a, b):\n"
            "    return a + b\n\n"
            "print(add(3, 7))               # 10\n"
            "print(add(100, 250))           # 350\n\n"
            "# ── Default parameter value ───────────────────────────────────\n"
            "def power(base, exponent=2):\n"
            "    return base ** exponent\n\n"
            "print(power(5))                # 25  ← exponent defaults to 2\n"
            "print(power(2, 10))            # 1024 ← exponent is 10\n\n"
            "# ── Function without return (returns None) ────────────────────\n"
            "def show_info(name, age):\n"
            "    print(f\"Name: {name}, Age: {age}\")\n\n"
            "show_info(\"Amina\", 19)         # Name: Amina, Age: 19\n"
            "x = show_info(\"Emeka\", 24)     # x is None (no return statement)\n"
            "print(x)                        # None\n\n"
            "# ── Scope example ─────────────────────────────────────────────\n"
            "def calculate():\n"
            "    local_var = 42              # only exists inside calculate()\n"
            "    return local_var\n\n"
            "print(calculate())             # 42 — OK\n"
            "# print(local_var)             # NameError — local_var doesn't exist here"
        ),
        "code_breakdown": (
            "Lines 2–4: def greet(name): ... return message\n"
            "  → 'def' is the keyword that DEFINES a function.\n"
            "  → 'name' is the parameter — a placeholder for whatever is passed as an argument.\n"
            "  → 'return message' sends the built string back to the caller.\n\n"
            "Line 6: result = greet(\"Amina\")\n"
            "  → Calls greet() with 'Amina' as the argument.\n"
            "  → The returned string is stored in the variable 'result'.\n\n"
            "Line 7: print(result)\n"
            "  → Prints whatever was stored in result: Hello, Amina! Welcome to Python Tutor.\n\n"
            "Lines 10–11: def add(a, b): return a + b\n"
            "  → A function with two parameters. Called on lines 13–14 with different pairs of numbers.\n\n"
            "Lines 16–18: def power(base, exponent=2)\n"
            "  → exponent=2 is a default value. When power(5) is called (line 20), exponent is 2.\n"
            "  → When power(2, 10) is called (line 21), the default is overridden with 10.\n\n"
            "Lines 23–25: show_info — no return statement\n"
            "  → This function uses print() to display output. It does NOT return a value.\n"
            "  → Line 27: x = show_info(...) → x gets None because there is no return.\n\n"
            "Lines 30–32: Scope\n"
            "  → local_var is created inside calculate(). It is DESTROYED when calculate() ends.\n"
            "  → Trying to access local_var outside the function raises NameError."
        ),
        "key_points": json.dumps([
            "Define a function with: def function_name(parameters): then an indented body.",
            "Call (run) a function by writing its name followed by parentheses: greet('Amina').",
            "Parameters are the placeholders in the def line; arguments are the values you pass in.",
            "Default parameters use = in the def line and are used when no argument is given.",
            "'return' sends a value back to the caller and STOPS the function immediately.",
            "A function without 'return' automatically returns None — not 0, not ''.",
            "print() inside a function displays output but does NOT return a value.",
            "Variables created inside a function are LOCAL — they don't exist outside it.",
        ]),
    },

    # ─────────────────────────────────────────────────────────────────────────
    # PRO TIER
    # ─────────────────────────────────────────────────────────────────────────
    {
        "id": "L07",
        "title": "Lists",
        "order_index": 7,
        "difficulty": "advanced",
        "explanation": (
            "WHAT IS A LIST?\n"
            "A list is an ordered, mutable (changeable) collection of items stored in a single variable. "
            "Lists can hold items of any data type, and they can even hold different types at the same time. "
            "Lists allow duplicates.\n\n"
            "CREATING A LIST:\n"
            "  my_list = [item1, item2, item3]  ← square brackets\n"
            "  empty_list = []                  ← empty list\n\n"
            "INDEXING — accessing items:\n"
            "  • Each item has a position number called an index, starting at 0 (not 1).\n"
            "  • fruits[0]  → first item\n"
            "  • fruits[1]  → second item\n"
            "  • fruits[-1] → LAST item (negative indices count from the end)\n"
            "  • fruits[-2] → second to last\n\n"
            "SLICING — getting a sub-list:\n"
            "  • fruits[1:3]  → items at index 1 and 2 (stops BEFORE index 3)\n"
            "  • fruits[:2]   → first two items (from the start up to but not including index 2)\n"
            "  • fruits[2:]   → from index 2 to the end\n"
            "  • fruits[::2]  → every other item\n\n"
            "COMMON LIST METHODS:\n"
            "  • .append(x)   — adds x to the END of the list\n"
            "  • .insert(i,x) — inserts x at position i\n"
            "  • .remove(x)   — removes the FIRST occurrence of x (raises ValueError if not found)\n"
            "  • .pop()       — removes and RETURNS the last item (or item at given index)\n"
            "  • .sort()      — sorts the list IN PLACE (modifies the original list)\n"
            "  • .reverse()   — reverses the list IN PLACE\n"
            "  • .index(x)    — returns the index of the first occurrence of x\n"
            "  • .count(x)    — returns how many times x appears\n"
            "  • .clear()     — removes all items\n\n"
            "COMMON BEGINNER ERRORS:\n"
            "  • IndexError: accessing an index that doesn't exist (e.g. items[10] on a 3-item list)\n"
            "  • Starting indexing at 1 instead of 0 (off-by-one error)"
        ),
        "analogy": (
            "A list is like a numbered queue of people waiting at a bank. "
            "Position 0 is the first person in line, position 1 is the second, and so on. "
            "You can call any person by their position number, "
            "add a new person to the end of the queue (append), "
            "remove someone from the middle (remove), "
            "or check how many people are waiting (len). "
            "The queue maintains order — the positions don't shift unless you explicitly change them."
        ),
        "code_example": (
            "# ── Creating lists ────────────────────────────────────────────\n"
            "fruits  = [\"apple\", \"banana\", \"cherry\", \"mango\"]\n"
            "numbers = [10, 20, 30, 40, 50]\n"
            "mixed   = [\"Amina\", 19, 3.8, True]   # mixed types allowed\n\n"
            "# ── Indexing ──────────────────────────────────────────────────\n"
            "print(fruits[0])    # apple  (first item)\n"
            "print(fruits[2])    # cherry (third item)\n"
            "print(fruits[-1])   # mango  (last item)\n"
            "print(fruits[-2])   # cherry (second to last)\n\n"
            "# ── Slicing ───────────────────────────────────────────────────\n"
            "print(fruits[1:3])  # ['banana', 'cherry'] — index 1 and 2\n"
            "print(fruits[:2])   # ['apple', 'banana']  — first two items\n"
            "print(fruits[2:])   # ['cherry', 'mango']  — from index 2 onwards\n\n"
            "# ── Common methods ────────────────────────────────────────────\n"
            "fruits.append(\"pineapple\")     # ['apple','banana','cherry','mango','pineapple']\n"
            "fruits.insert(1, \"orange\")     # inserts 'orange' at index 1\n"
            "fruits.remove(\"banana\")        # removes first 'banana'\n"
            "last = fruits.pop()            # removes and returns last item\n"
            "print(last)                    # pineapple\n\n"
            "# ── Sorting and reversing ─────────────────────────────────────\n"
            "nums = [5, 3, 8, 1, 9]\n"
            "nums.sort()\n"
            "print(nums)                    # [1, 3, 5, 8, 9]\n"
            "nums.reverse()\n"
            "print(nums)                    # [9, 8, 5, 3, 1]\n\n"
            "# ── Useful built-in functions on lists ────────────────────────\n"
            "print(len(fruits))             # number of items\n"
            "print(min(numbers))            # 10\n"
            "print(max(numbers))            # 50\n"
            "print(sum(numbers))            # 150\n"
            "print(\"apple\" in fruits)       # True — membership check"
        ),
        "code_breakdown": (
            "Line 2: fruits = [\"apple\", \"banana\", \"cherry\", \"mango\"]\n"
            "  → Square brackets [] create a list. Items are separated by commas.\n\n"
            "Line 6: print(fruits[0])  →  apple\n"
            "  → Index 0 is always the FIRST item. Python (and most programming languages) start at 0.\n\n"
            "Line 8: print(fruits[-1])  →  mango\n"
            "  → Negative indexing counts from the right. -1 is last, -2 is second to last, etc.\n\n"
            "Line 11: print(fruits[1:3])  →  ['banana', 'cherry']\n"
            "  → Slicing syntax: list[start:stop]. Includes start, EXCLUDES stop.\n"
            "  → So [1:3] gives indices 1 and 2, NOT index 3.\n\n"
            "Line 16: fruits.append(\"pineapple\")\n"
            "  → append() adds to the end. To add to a specific position use insert(index, value).\n\n"
            "Line 18: fruits.remove(\"banana\")\n"
            "  → Removes the FIRST occurrence of \"banana\". If \"banana\" isn't in the list → ValueError.\n\n"
            "Line 19: last = fruits.pop()\n"
            "  → pop() removes the last item AND returns it, so you can save it in a variable.\n\n"
            "Lines 22–25: nums.sort() then nums.reverse()\n"
            "  → Both methods modify the list IN PLACE (they change the original list, not a copy).\n"
            "  → They return None — don't write nums = nums.sort() or you'll lose the list!\n\n"
            "Line 31: print(\"apple\" in fruits)\n"
            "  → The 'in' keyword checks if an item exists in a list. Returns True or False."
        ),
        "key_points": json.dumps([
            "Lists store an ordered collection of items in square brackets: [item1, item2, ...].",
            "Indexing starts at 0 — the first item is always at index 0, not 1.",
            "Negative indices count from the end: -1 is last, -2 is second to last.",
            "Slicing list[start:stop] returns a sub-list. stop is EXCLUDED from the result.",
            "append() adds to the end; insert(i, x) adds at position i; remove(x) removes first match.",
            "sort() and reverse() modify the list IN PLACE and return None.",
            "len() counts items; min(), max(), sum() work on numeric lists.",
            "Use 'item in list' to check membership. IndexError means the index doesn't exist.",
        ]),
    },

    {
        "id": "L08",
        "title": "Dictionaries",
        "order_index": 8,
        "difficulty": "advanced",
        "explanation": (
            "WHAT IS A DICTIONARY?\n"
            "A dictionary stores data as key-value pairs. "
            "Instead of accessing items by a position number (like a list), "
            "you look up values by a meaningful key — similar to looking up a word in a real dictionary. "
            "\n\n"
            "CREATING A DICTIONARY:\n"
            "  my_dict = {key1: value1, key2: value2}\n"
            "  empty_dict = {}   or   empty_dict = dict()\n\n"
            "RULES FOR KEYS:\n"
            "  • Keys must be UNIQUE — if you assign the same key twice, the second value overwrites the first.\n"
            "  • Keys must be IMMUTABLE — strings, integers, and tuples can be keys; lists cannot.\n"
            "  • Values can be anything: strings, integers, lists, even other dictionaries.\n\n"
            "ACCESSING VALUES:\n"
            "  • dict[key]        — gets the value; raises KeyError if key doesn't exist\n"
            "  • dict.get(key)    — gets the value; returns None if key doesn't exist (safer)\n"
            "  • dict.get(key, d) — returns default value d if key is not found\n\n"
            "ADDING AND UPDATING:\n"
            "  • dict[new_key] = value   — adds a new key-value pair\n"
            "  • dict[exist_key] = value — updates the value for an existing key\n\n"
            "REMOVING ENTRIES:\n"
            "  • del dict[key]    — removes a key-value pair (KeyError if key not found)\n"
            "  • dict.pop(key)    — removes and returns the value (KeyError if not found)\n"
            "  • dict.clear()     — removes ALL entries\n\n"
            "ITERATING OVER A DICTIONARY:\n"
            "  • dict.keys()    — returns all keys\n"
            "  • dict.values()  — returns all values\n"
            "  • dict.items()   — returns all (key, value) pairs as tuples — best for looping\n\n"
            "COMMON BEGINNER ERROR:\n"
            "Accessing a key that doesn't exist with dict[key] raises a KeyError. "
            "Use dict.get(key) to avoid crashes when the key may or may not exist."
        ),
        "analogy": (
            "A dictionary works exactly like a real physical dictionary: "
            "you look up a word (the key) to find its definition (the value). "
            "In a real dictionary, no word appears twice (keys are unique), "
            "but the same word can have a long or complex definition (values can be complex). "
            "Another good analogy: think of a student ID card system — "
            "each student has a unique ID number (key) linked to their personal information (value). "
            "You look up a student by their ID, not by their position in a list."
        ),
        "code_example": (
            "# ── Creating a dictionary ─────────────────────────────────────\n"
            "student = {\n"
            "    \"name\":   \"Amina\",\n"
            "    \"age\":    19,\n"
            "    \"course\": \"Computer Science\",\n"
            "    \"gpa\":    3.8\n"
            "}\n\n"
            "# ── Accessing values ──────────────────────────────────────────\n"
            "print(student[\"name\"])          # Amina\n"
            "print(student[\"age\"])           # 19\n"
            "print(student.get(\"grade\"))     # None  (key doesn't exist — no crash)\n"
            "print(student.get(\"grade\", \"N/A\"))  # N/A  (default value)\n\n"
            "# ── Adding and updating entries ────────────────────────────────\n"
            "student[\"grade\"] = \"A\"          # adds a new key\n"
            "student[\"age\"]   = 20           # updates existing value\n"
            "print(student[\"age\"])           # 20\n\n"
            "# ── Removing entries ──────────────────────────────────────────\n"
            "del student[\"gpa\"]              # removes gpa key entirely\n"
            "removed = student.pop(\"grade\")  # removes and returns value\n"
            "print(removed)                  # A\n\n"
            "# ── Iterating over a dictionary ────────────────────────────────\n"
            "for key in student.keys():\n"
            "    print(key)\n\n"
            "for value in student.values():\n"
            "    print(value)\n\n"
            "for key, value in student.items():   # best way to loop\n"
            "    print(f\"{key}: {value}\")\n\n"
            "# ── Membership check ──────────────────────────────────────────\n"
            "print(\"name\" in student)        # True\n"
            "print(\"gpa\"  in student)        # False (we deleted it)\n"
            "print(len(student))             # number of key-value pairs"
        ),
        "code_breakdown": (
            "Lines 2–7: student = {\"name\": \"Amina\", ...}\n"
            "  → Curly braces {} create a dictionary. Each entry is key: value separated by commas.\n"
            "  → Keys are usually strings. Values can be any type (str, int, float, bool, list, etc.).\n\n"
            "Line 9: print(student[\"name\"])  →  Amina\n"
            "  → Access a value using its key in square brackets.\n"
            "  → If the key doesn't exist, this raises a KeyError and crashes the program.\n\n"
            "Line 11: print(student.get(\"grade\"))  →  None\n"
            "  → .get() is safer — it returns None instead of crashing if the key is missing.\n\n"
            "Line 12: print(student.get(\"grade\", \"N/A\"))  →  N/A\n"
            "  → Providing a second argument to .get() sets a custom default value.\n\n"
            "Line 15: student[\"grade\"] = \"A\"\n"
            "  → If \"grade\" doesn't exist, this ADDS it. If it does exist, this UPDATES it.\n"
            "  → The same syntax handles both adding and updating.\n\n"
            "Line 19: del student[\"gpa\"]\n"
            "  → Permanently removes the key-value pair. Raises KeyError if key not found.\n\n"
            "Lines 23–30: Iterating\n"
            "  → .keys()   — loop over keys only\n"
            "  → .values() — loop over values only\n"
            "  → .items()  — loop over (key, value) PAIRS — the most useful method for loops\n\n"
            "Line 32: print(\"name\" in student)  →  True\n"
            "  → 'in' checks KEY membership, not value membership, in a dictionary."
        ),
        "key_points": json.dumps([
            "Dictionaries store data as key-value pairs in curly braces: {key: value}.",
            "Keys must be unique and immutable (strings or integers are typical keys).",
            "Access values with dict[key] — raises KeyError if missing. Use .get(key) to be safe.",
            ".get(key, default) returns a custom default value when the key doesn't exist.",
            "Add or update with dict[key] = value — same syntax handles both operations.",
            "Delete with del dict[key] or dict.pop(key). dict.clear() removes everything.",
            "Iterate with .keys(), .values(), or .items() — use .items() in for loops.",
            "'key in dict' checks for KEY membership; it does NOT search values.",
        ]),
    },

    {
        "id": "L09",
        "title": "Error Types & Debugging",
        "order_index": 9,
        "difficulty": "advanced",
        "explanation": (
            "WHY DO ERRORS HAPPEN?\n"
            "Errors (also called exceptions or bugs) are a normal part of programming. "
            "Every programmer — including professionals — encounters errors every day. "
            "The skill is learning to READ the error message and fix the cause. "
            "\n\n"
            "TWO MAIN CATEGORIES OF ERRORS:\n\n"
            "1. SYNTAX ERRORS — Python cannot even parse your code:\n"
            "   The program refuses to run at all. Common causes:\n"
            "   • Missing colon (:) after if, for, while, def\n"
            "   • Wrong or missing indentation\n"
            "   • Unclosed brackets, parentheses, or quotes\n"
            "   • Using = instead of == inside a condition\n\n"
            "2. RUNTIME ERRORS (Exceptions) — code is valid but something goes wrong while running:\n"
            "   The program starts but crashes at a specific line. The most important ones:\n\n"
            "   • NameError      — you used a variable name that was never defined\n"
            "                      Fix: check spelling; make sure the variable was assigned first\n"
            "   • TypeError      — you applied an operation to incompatible types\n"
            "                      e.g. '5' + 5  or  len(42)  \n"
            "                      Fix: convert types with int(), str(), float()\n"
            "   • ValueError     — the type is correct but the value doesn't make sense\n"
            "                      e.g. int('hello') — can't convert 'hello' to an integer\n"
            "   • IndexError     — you accessed a list index that doesn't exist\n"
            "                      Fix: check list length with len(); don't exceed index n-1\n"
            "   • KeyError       — you accessed a dictionary key that doesn't exist\n"
            "                      Fix: use dict.get(key) or check 'key in dict' first\n"
            "   • ZeroDivisionError — you divided a number by zero\n"
            "                      Fix: always check the divisor before dividing\n"
            "   • AttributeError — you called a method that doesn't exist on that type\n"
            "                      e.g. (5).append(3)  (integers don't have append)\n\n"
            "READING A TRACEBACK:\n"
            "When an error occurs, Python prints a traceback — a step-by-step trail of where "
            "the error happened. Always read it from the BOTTOM up:\n"
            "  1. The LAST line tells you the error type and message (most important)\n"
            "  2. The lines above show which file and line number the crash happened on\n\n"
            "HANDLING ERRORS — try / except:\n"
            "Instead of letting an error crash your program, you can 'catch' it using try/except. "
            "Code inside 'try' runs normally. If an error occurs, the 'except' block runs instead.\n"
            "You can also add 'finally' to run code regardless of whether an error occurred.\n\n"
            "DEBUGGING STRATEGIES:\n"
            "  • Print debugging: add print() statements to see variable values at different points\n"
            "  • Read error messages carefully — they tell you the exact line and error type\n"
            "  • Test small pieces of code in isolation\n"
            "  • Work backwards from the crash line"
        ),
        "analogy": (
            "A Syntax Error is like a grammatical mistake in a written essay — "
            "the reader (Python) cannot understand the sentence at all and stops immediately. "
            "A Runtime Error is like giving someone perfect directions to the wrong address — "
            "the instructions look fine, but something goes wrong when you actually follow them. "
            "Reading the traceback is like reading the error log in a car's black box: "
            "it tells you exactly when and where something went wrong so you can fix it."
        ),
        "code_example": (
            "# ── Common Syntax Errors (these WON'T run) ────────────────────\n"
            "# if x > 5         ← SyntaxError: missing colon\n"
            "#     print('hi')  ← IndentationError: wrong indentation\n\n"
            "# ── Common Runtime Errors ─────────────────────────────────────\n"
            "# print(score)     ← NameError: 'score' is not defined\n\n"
            "# name = \"Amina\"\n"
            "# print(name + 5)  ← TypeError: can't concatenate str and int\n\n"
            "# items = [1, 2, 3]\n"
            "# print(items[10]) ← IndexError: list index out of range\n\n"
            "# result = 10 / 0  ← ZeroDivisionError\n\n"
            "# ── Basic try / except ────────────────────────────────────────\n"
            "try:\n"
            "    result = 10 / 0\n"
            "except ZeroDivisionError:\n"
            "    print(\"Error: Cannot divide by zero!\")\n\n"
            "# ── Handling multiple error types ─────────────────────────────\n"
            "try:\n"
            "    number = int(input(\"Enter a number: \"))\n"
            "    print(f\"Double is: {number * 2}\")\n"
            "except ValueError:\n"
            "    print(\"Error: Please enter a whole number, not text.\")\n"
            "except ZeroDivisionError:\n"
            "    print(\"Error: Division by zero is not allowed.\")\n\n"
            "# ── try / except / else / finally ─────────────────────────────\n"
            "try:\n"
            "    score = int(input(\"Enter score: \"))\n"
            "except ValueError:\n"
            "    print(\"That's not a valid number.\")\n"
            "else:\n"
            "    print(f\"Score accepted: {score}\")   # runs only if no error\n"
            "finally:\n"
            "    print(\"Done.\")                       # ALWAYS runs\n\n"
            "# ── Print debugging technique ─────────────────────────────────\n"
            "def calculate_grade(marks):\n"
            "    print(f\"DEBUG: marks received = {marks}\")  # temporary debug print\n"
            "    grade = marks / 10\n"
            "    print(f\"DEBUG: grade computed = {grade}\")\n"
            "    return grade"
        ),
        "code_breakdown": (
            "Lines 2–3: Commented-out syntax errors\n"
            "  → These lines would cause SyntaxError/IndentationError and prevent ANY code from running.\n"
            "  → The entire file fails if there is even one syntax error.\n\n"
            "Lines 14–16: try / except ZeroDivisionError\n"
            "  → The 'try' block runs normally. If 10/0 raises ZeroDivisionError, Python jumps to 'except'.\n"
            "  → The program does NOT crash — it prints the error message and continues.\n\n"
            "Lines 19–24: Multiple except clauses\n"
            "  → You can have separate except blocks for different error types.\n"
            "  → Python checks them in order and runs the FIRST one that matches.\n\n"
            "Lines 27–32: else and finally\n"
            "  → else — runs only when NO exception occurred in the try block.\n"
            "  → finally — runs REGARDLESS of whether an exception occurred or not.\n"
            "  → 'finally' is useful for cleanup (e.g. closing a file or database connection).\n\n"
            "Lines 35–39: Print debugging\n"
            "  → Adding temporary print() statements with labels (DEBUG:) lets you see\n"
            "    what value a variable holds at a specific point in the program.\n"
            "  → Remove debug prints before submitting your final code."
        ),
        "key_points": json.dumps([
            "SyntaxError prevents the program from running at all — check for missing colons and indentation.",
            "Runtime errors (exceptions) crash the program mid-execution at the specific error line.",
            "Read tracebacks from the BOTTOM UP — the last line tells you the error type and message.",
            "NameError: undefined variable. TypeError: wrong type. ValueError: wrong value. IndexError: bad index.",
            "KeyError: missing dictionary key — use .get() to avoid it. ZeroDivisionError: divide by zero.",
            "Use try/except to catch errors gracefully so the program doesn't crash.",
            "The 'else' clause in try/except runs only if no error occurred.",
            "The 'finally' clause always runs — use it for cleanup actions.",
        ]),
    },
]

# ─────────────────────────────────────────────────────────────────────────────
# PRACTICE QUESTIONS — Intermediate & Pro Tiers (5 per lesson, 30 total)
# ─────────────────────────────────────────────────────────────────────────────
QUESTIONS_BATCH_2 = [
    # ── L04 — Conditionals ────────────────────────────────────────────────────
    {
        "topic_id": "L04",
        "question_text": "What keyword checks additional conditions if the first 'if' is False?",
        "option_a": "else", "option_b": "then",
        "option_c": "elif", "option_d": "ifelse",
        "correct_option": "C",
        "hint_1": "Python uses a shortened combination of two English words.",
        "hint_2": "It is a blend of 'else' and 'if' merged into one keyword.",
        "hint_3": "C is correct: elif. It means 'else if' and is checked only when all previous conditions are False.",
    },
    {
        "topic_id": "L04",
        "question_text": "What is required at the END of an 'if' statement line?",
        "option_a": "Semicolon (;)", "option_b": "Colon (:)",
        "option_c": "Curly brace ({)", "option_d": "Nothing",
        "correct_option": "B",
        "hint_1": "Python uses a specific punctuation mark to signal the start of a new code block.",
        "hint_2": "Unlike Java or C, Python uses one character instead of curly braces to open a block.",
        "hint_3": "B is correct: colon (:). Every if, elif, else, for, while, and def line must end with ':'.",
    },
    {
        "topic_id": "L04",
        "question_text": "What will print?\n  x = 5\n  if x > 10:\n      print('A')\n  else:\n      print('B')",
        "option_a": "A", "option_b": "Nothing",
        "option_c": "B", "option_d": "Error",
        "correct_option": "C",
        "hint_1": "First evaluate whether the condition 5 > 10 is True or False.",
        "hint_2": "5 is NOT greater than 10, so the 'if' block is skipped entirely.",
        "hint_3": "C is correct: B. Since 5 > 10 is False, Python runs the 'else' block and prints 'B'.",
    },
    {
        "topic_id": "L04",
        "question_text": "How does Python know which lines of code belong inside an 'if' block?",
        "option_a": "Curly braces {}", "option_b": "Parentheses ()",
        "option_c": "Indentation (spaces)", "option_d": "END keyword",
        "correct_option": "C",
        "hint_1": "Python uses whitespace instead of braces, unlike most other languages.",
        "hint_2": "The code inside a block is shifted to the RIGHT by a consistent number of spaces.",
        "hint_3": "C is correct: Indentation. Python uses 4 spaces to group code inside blocks — it is mandatory.",
    },
    {
        "topic_id": "L04",
        "question_text": "Which block runs when NONE of the 'if' or 'elif' conditions are True?",
        "option_a": "elif", "option_b": "default",
        "option_c": "finally", "option_d": "else",
        "correct_option": "D",
        "hint_1": "This block has no condition — it is the last resort fallback.",
        "hint_2": "It catches all cases that were not handled by any if or elif above it.",
        "hint_3": "D is correct: else. It runs when no 'if' or 'elif' condition was True. There can only be one else.",
    },

    # ── L05 — Loops ───────────────────────────────────────────────────────────
    {
        "topic_id": "L05",
        "question_text": "How many times does this loop run?\n  for i in range(4):\n      print(i)",
        "option_a": "3", "option_b": "4",
        "option_c": "5", "option_d": "0",
        "correct_option": "B",
        "hint_1": "range(4) generates a sequence of numbers — count exactly how many there are.",
        "hint_2": "range(4) produces: 0, 1, 2, 3 — that is four values.",
        "hint_3": "B is correct: 4. range(4) gives 0, 1, 2, 3 — four iterations.",
    },
    {
        "topic_id": "L05",
        "question_text": "What happens if you forget to increment the counter in a while loop?",
        "option_a": "The loop stops after one run",
        "option_b": "Python throws an error",
        "option_c": "The loop runs forever (infinite loop)",
        "option_d": "The counter resets to 0",
        "correct_option": "C",
        "hint_1": "Think about what the condition checks — can it ever become False without incrementing?",
        "hint_2": "If the variable never changes, the condition stays True permanently.",
        "hint_3": "C is correct: infinite loop. Without incrementing, the while condition never becomes False. This is a classic beginner mistake.",
    },
    {
        "topic_id": "L05",
        "question_text": "What does 'break' do inside a loop?",
        "option_a": "Skips the current iteration and goes to the next",
        "option_b": "Exits the entire loop immediately",
        "option_c": "Restarts the loop from the beginning",
        "option_d": "Pauses the loop temporarily",
        "correct_option": "B",
        "hint_1": "The word 'break' literally means to stop something.",
        "hint_2": "It terminates the entire loop, not just one iteration. Execution continues after the loop.",
        "hint_3": "B is correct: exits the loop immediately. The keyword for skipping ONE iteration is 'continue'.",
    },
    {
        "topic_id": "L05",
        "question_text": "What does range(2, 6) produce?",
        "option_a": "2, 3, 4, 5, 6", "option_b": "2, 3, 4, 5",
        "option_c": "1, 2, 3, 4, 5", "option_d": "2, 4, 6",
        "correct_option": "B",
        "hint_1": "range(start, stop) starts at the first number and stops BEFORE the second.",
        "hint_2": "It includes 2 but does NOT include 6.",
        "hint_3": "B is correct: 2, 3, 4, 5. range(2, 6) starts at 2 and stops before 6 (exclusive).",
    },
    {
        "topic_id": "L05",
        "question_text": "Which loop type is best when you don't know in advance how many iterations are needed?",
        "option_a": "for loop", "option_b": "while loop",
        "option_c": "range loop", "option_d": "do loop",
        "correct_option": "B",
        "hint_1": "One loop type runs for a fixed number of steps; the other runs until a condition changes.",
        "hint_2": "When the number of repetitions depends on runtime conditions (like user input), one loop type fits better.",
        "hint_3": "B is correct: while loop. Use it when the number of iterations is not known ahead of time.",
    },

    # ── L06 — Functions ───────────────────────────────────────────────────────
    {
        "topic_id": "L06",
        "question_text": "What keyword is used to DEFINE a function in Python?",
        "option_a": "function", "option_b": "define",
        "option_c": "def", "option_d": "fun",
        "correct_option": "C",
        "hint_1": "It is an abbreviation of the word 'define'.",
        "hint_2": "It is three letters long and starts with 'd'.",
        "hint_3": "C is correct: def. You write 'def function_name():' to create a function.",
    },
    {
        "topic_id": "L06",
        "question_text": "What does the 'return' keyword do in a function?",
        "option_a": "Prints the result to the screen",
        "option_b": "Sends a value back to the caller and stops the function",
        "option_c": "Stops the entire program",
        "option_d": "Repeats the function from the beginning",
        "correct_option": "B",
        "hint_1": "Think about what happens AFTER a function finishes its job.",
        "hint_2": "The value doesn't automatically appear on screen — it is sent somewhere back to the code that called the function.",
        "hint_3": "B is correct: sends a value back to the caller and stops the function. You can then store or print that returned value.",
    },
    {
        "topic_id": "L06",
        "question_text": "What does a function automatically return if it has NO 'return' statement?",
        "option_a": "0", "option_b": "False",
        "option_c": "None", "option_d": "An error",
        "correct_option": "C",
        "hint_1": "Python always returns something from a function, even when you don't specify.",
        "hint_2": "The special value representing 'nothing' in Python is a specific keyword.",
        "hint_3": "C is correct: None. Python implicitly returns None when there is no return statement.",
    },
    {
        "topic_id": "L06",
        "question_text": "What is a parameter in a function?",
        "option_a": "The name of the function",
        "option_b": "A variable that receives an input value when the function is called",
        "option_c": "The value that the function returns",
        "option_d": "A comment inside the function",
        "correct_option": "B",
        "hint_1": "Parameters allow you to pass information INTO a function.",
        "hint_2": "They appear inside the parentheses in the 'def' line.",
        "hint_3": "B is correct: a variable that receives input. Parameters are listed in () when defining the function. Arguments are the actual values passed in when calling it.",
    },
    {
        "topic_id": "L06",
        "question_text": "Which line correctly CALLS a function named 'greet' with 'Amina' as the argument?",
        "option_a": "def greet('Amina')", "option_b": "call greet('Amina')",
        "option_c": "greet('Amina')", "option_d": "greet = 'Amina'",
        "correct_option": "C",
        "hint_1": "You call (run) a function by using its name followed by parentheses containing arguments.",
        "hint_2": "'def' is for DEFINING a function, not for calling it. Look for just the function name.",
        "hint_3": "C is correct: greet('Amina'). To call a function, write its name with arguments in parentheses.",
    },

    # ── L07 — Lists ───────────────────────────────────────────────────────────
    {
        "topic_id": "L07",
        "question_text": "What is the index of the FIRST item in a Python list?",
        "option_a": "1", "option_b": "0",
        "option_c": "-1", "option_d": "None",
        "correct_option": "B",
        "hint_1": "Python does not start counting from 1 the way humans naturally do.",
        "hint_2": "Most programming languages, including Python, start index counting from zero.",
        "hint_3": "B is correct: 0. The first item is always at index 0. Accessing index 1 would give the SECOND item.",
    },
    {
        "topic_id": "L07",
        "question_text": "Which method adds an item to the END of a list?",
        "option_a": "add()", "option_b": "insert()",
        "option_c": "append()", "option_d": "push()",
        "correct_option": "C",
        "hint_1": "Think of the word that means 'to attach something to the end'.",
        "hint_2": "It is a list method starting with the letter 'a'. Use insert() to add at a specific position.",
        "hint_3": "C is correct: append(). It adds one item to the end of the list.",
    },
    {
        "topic_id": "L07",
        "question_text": "What does fruits[-1] return for: fruits = ['apple', 'banana', 'cherry']?",
        "option_a": "apple", "option_b": "banana",
        "option_c": "cherry", "option_d": "IndexError",
        "correct_option": "C",
        "hint_1": "Negative indices count from the END of the list.",
        "hint_2": "-1 always refers to the very last item in any list.",
        "hint_3": "C is correct: cherry. fruits[-1] is the last element. fruits[-2] would be 'banana'.",
    },
    {
        "topic_id": "L07",
        "question_text": "What does fruits[1:3] return for: fruits = ['apple','banana','cherry','mango']?",
        "option_a": "['apple','banana','cherry']",
        "option_b": "['banana','cherry']",
        "option_c": "['banana','cherry','mango']",
        "option_d": "['apple','banana']",
        "correct_option": "B",
        "hint_1": "Slicing syntax: list[start:stop] — the stop index is EXCLUDED from the result.",
        "hint_2": "Index 1 is 'banana' and index 2 is 'cherry'. Index 3 ('mango') is not included.",
        "hint_3": "B is correct: ['banana','cherry']. Slicing includes start (1) and excludes stop (3).",
    },
    {
        "topic_id": "L07",
        "question_text": "Which error occurs when you access a list index that doesn't exist?",
        "option_a": "KeyError", "option_b": "NameError",
        "option_c": "IndexError", "option_d": "ValueError",
        "correct_option": "C",
        "hint_1": "You are accessing a list position (index) that is beyond the valid range.",
        "hint_2": "The error name contains the word 'Index'.",
        "hint_3": "C is correct: IndexError. For example, accessing index 10 on a 3-item list (valid: 0,1,2).",
    },

    # ── L08 — Dictionaries ────────────────────────────────────────────────────
    {
        "topic_id": "L08",
        "question_text": "How do you access the value for key 'name' in: student = {'name': 'Amina', 'age': 19}?",
        "option_a": "student.name", "option_b": "student[0]",
        "option_c": "student['name']", "option_d": "student.get(0)",
        "correct_option": "C",
        "hint_1": "Dictionaries are accessed by KEY, not by position number.",
        "hint_2": "You use the key inside square brackets, just like indexing a list but with a key name.",
        "hint_3": "C is correct: student['name']. Use the key in square brackets to look up a value.",
    },
    {
        "topic_id": "L08",
        "question_text": "What makes dictionary KEYS different from values?",
        "option_a": "Keys must be integers only", "option_b": "Keys must be unique",
        "option_c": "Keys must be in alphabetical order", "option_d": "Keys cannot be strings",
        "correct_option": "B",
        "hint_1": "Think about a real dictionary — can the same word appear on two different pages?",
        "hint_2": "If two entries had the same key, Python wouldn't know which value to return.",
        "hint_3": "B is correct: Keys must be UNIQUE. Each key can appear only once; values can repeat.",
    },
    {
        "topic_id": "L08",
        "question_text": "Which is the SAFER way to get a value when the key might not exist?",
        "option_a": "dict[key]", "option_b": "dict.key",
        "option_c": "dict.get(key)", "option_d": "dict.find(key)",
        "correct_option": "C",
        "hint_1": "One method crashes with a KeyError; the other returns None if the key is missing.",
        "hint_2": "The safer method is a built-in dictionary method that accepts an optional default value.",
        "hint_3": "C is correct: dict.get(key). It returns None instead of raising KeyError if the key doesn't exist.",
    },
    {
        "topic_id": "L08",
        "question_text": "What does the .items() method return when iterating over a dictionary?",
        "option_a": "Only the keys", "option_b": "Only the values",
        "option_c": "Key-value pairs as tuples", "option_d": "The length of the dictionary",
        "correct_option": "C",
        "hint_1": "There are three iteration methods: .keys(), .values(), and .items().",
        "hint_2": ".items() returns both pieces of each entry — the key AND the value together.",
        "hint_3": "C is correct: key-value pairs as tuples. Use: for key, value in dict.items():",
    },
    {
        "topic_id": "L08",
        "question_text": "How do you add a new key 'grade' with value 'A' to a dictionary called 'student'?",
        "option_a": "student.add('grade', 'A')",
        "option_b": "student.grade = 'A'",
        "option_c": "student['grade'] = 'A'",
        "option_d": "student.append({'grade': 'A'})",
        "correct_option": "C",
        "hint_1": "Adding to a dictionary uses the same syntax as accessing it.",
        "hint_2": "Assign a value to a key using square brackets — if the key doesn't exist, it is created.",
        "hint_3": "C is correct: student['grade'] = 'A'. If the key exists it is UPDATED; if not, it is ADDED.",
    },

    # ── L09 — Error Types & Debugging ────────────────────────────────────────
    {
        "topic_id": "L09",
        "question_text": "Which error occurs when Python cannot understand your code BEFORE it even runs?",
        "option_a": "RuntimeError", "option_b": "NameError",
        "option_c": "SyntaxError", "option_d": "TypeError",
        "correct_option": "C",
        "hint_1": "This error is caught during the 'parsing' phase, before any line is executed.",
        "hint_2": "It is caused by breaking Python's grammar rules — missing colons, wrong indentation, etc.",
        "hint_3": "C is correct: SyntaxError. It means Python could not parse the code structure.",
    },
    {
        "topic_id": "L09",
        "question_text": "What error does print(score) cause if 'score' was NEVER assigned a value?",
        "option_a": "TypeError", "option_b": "IndexError",
        "option_c": "SyntaxError", "option_d": "NameError",
        "correct_option": "D",
        "hint_1": "You are using a name (variable) that Python has never seen before.",
        "hint_2": "The error name literally says your variable 'name' is not defined.",
        "hint_3": "D is correct: NameError. Python cannot find 'score' because it was never created or assigned.",
    },
    {
        "topic_id": "L09",
        "question_text": "What error does print('Age: ' + 19) cause?",
        "option_a": "SyntaxError", "option_b": "TypeError",
        "option_c": "ValueError", "option_d": "NameError",
        "correct_option": "B",
        "hint_1": "You are combining two values of DIFFERENT data types using the + operator.",
        "hint_2": "Python cannot add a string and an integer directly — the types are incompatible.",
        "hint_3": "B is correct: TypeError. Fix it with str(19) or use an f-string: f'Age: {19}'.",
    },
    {
        "topic_id": "L09",
        "question_text": "What is the main purpose of a try/except block?",
        "option_a": "To make the program run faster",
        "option_b": "To handle errors gracefully without crashing the program",
        "option_c": "To define a new function",
        "option_d": "To repeat code multiple times",
        "correct_option": "B",
        "hint_1": "The word 'try' suggests attempting something that might fail.",
        "hint_2": "'except' catches the error if it happens and runs an alternative block of code.",
        "hint_3": "B is correct: handle errors gracefully. The program continues instead of crashing.",
    },
    {
        "topic_id": "L09",
        "question_text": "In which direction should you read a Python traceback to find the error?",
        "option_a": "Top to bottom", "option_b": "Middle first",
        "option_c": "Bottom up", "option_d": "Left to right",
        "correct_option": "C",
        "hint_1": "The most important information in a traceback is at a specific end.",
        "hint_2": "The error type and exact message are always printed LAST.",
        "hint_3": "C is correct: Bottom up. The last line shows the error type and message. Lines above show the call stack.",
    },
]


def seed_batch2():
    """Seed Intermediate and Pro tier lessons (L04–L09) and their practice questions."""
    with app.app_context():
        seeded_l = 0
        for data in LESSONS:
            existing = db.session.get(Lesson, data["id"])
            if existing:
                for key, value in data.items():
                    setattr(existing, key, value)
                seeded_l += 1
            else:
                db.session.add(Lesson(**data))
                seeded_l += 1
        db.session.commit()
        print(f"[OK] Seeded/updated {seeded_l} Intermediate & Pro lessons (L04-L09).")

        seeded_q = 0
        for q in QUESTIONS_BATCH_2:
            exists = PracticeQuestion.query.filter_by(
                topic_id=q["topic_id"], question_text=q["question_text"]
            ).first()
            if not exists:
                db.session.add(PracticeQuestion(**q))
                seeded_q += 1
        db.session.commit()
        print(f"[OK] Seeded {seeded_q} practice questions (L04-L09).")


if __name__ == "__main__":
    seed_batch2()
