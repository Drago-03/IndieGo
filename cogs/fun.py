import discord
from discord.ext import commands
from discord import app_commands
import random
import asyncio

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="roll")
    async def roll_command(self, ctx, dice: str = None):
        """Rolls a dice in NdN format."""
        if dice is None:
            embed = discord.Embed(
                title="Error",
                description="You must specify the dice format (e.g., 2d6).",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
            return

        try:
            rolls, limit = map(int, dice.split('d'))
            result = [random.randint(1, limit) for r in range(rolls)]
            embed = discord.Embed(
                title="Dice Roll",
                description=f'Results: {", ".join(map(str, result))}',
                color=discord.Color.green()
            )
            await ctx.send(embed=embed)
        except Exception:
            embed = discord.Embed(
                title="Error",
                description="Format has to be in NdN!",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)

    @app_commands.command(name="roll", description="Rolls a dice in NdN format.")
    async def roll(self, interaction: discord.Interaction, dice: str = None):
        """Rolls a dice in NdN format."""
        if dice is None:
            embed = discord.Embed(
                title="Error",
                description="You must specify the dice format (e.g., 2d6).",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        try:
            rolls, limit = map(int, dice.split('d'))
            result = [random.randint(1, limit) for r in range(rolls)]
            embed = discord.Embed(
                title="Dice Roll",
                description=f'Results: {", ".join(map(str, result))}',
                color=discord.Color.green()
            )
            await interaction.response.send_message(embed=embed)
        except Exception:
            embed = discord.Embed(
                title="Error",
                description="Format has to be in NdN!",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)

    @commands.command(name="choose")
    async def choose_command(self, ctx, *, choices: str = None):
        """Chooses between multiple choices."""
        if choices is None:
            embed = discord.Embed(
                title="Error",
                description="You must specify choices separated by commas.",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
            return

        choices_list = choices.split(',')
        choice = random.choice(choices_list)
        embed = discord.Embed(
            title="Choice",
            description=f'I choose: {choice.strip()}',
            color=discord.Color.green()
        )
        await ctx.send(embed=embed)

    @app_commands.command(name="choose", description="Chooses between multiple choices.")
    async def choose(self, interaction: discord.Interaction, choices: str = None):
        """Chooses between multiple choices."""
        if choices is None:
            embed = discord.Embed(
                title="Error",
                description="You must specify choices separated by commas.",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        choices_list = choices.split(',')
        choice = random.choice(choices_list)
        embed = discord.Embed(
            title="Choice",
            description=f'I choose: {choice.strip()}',
            color=discord.Color.green()
        )
        await interaction.response.send_message(embed=embed)

    @commands.command(name="poll")
    async def poll_command(self, ctx, question: str = None, *, options: str = None):
        """Creates a poll with reactions."""
        if question is None or options is None:
            embed = discord.Embed(
                title="Error",
                description="You must specify a question and options.",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
            return

        options_list = options.split(',')
        if len(options_list) > 10:
            embed = discord.Embed(
                title="Error",
                description="You can only have up to 10 options!",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
            return

        reactions = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣', '🔟']
        
        description = []
        for i, option in enumerate(options_list):
            description.append(f'{reactions[i]} {option}')
        
        embed = discord.Embed(title=question, description='\n'.join(description), color=discord.Color.blue())
        poll_message = await ctx.send(embed=embed)
        
        for i in range(len(options_list)):
            await poll_message.add_reaction(reactions[i])

    @app_commands.command(name="poll", description="Create a poll")
    async def poll(self, interaction: discord.Interaction, question: str):
        """Create a poll"""
        embed = discord.Embed(
            title="Poll",
            description=question,
            color=discord.Color.blue()
        )
        message = await interaction.response.send_message(embed=embed)
        await message.add_reaction("👍")
        await message.add_reaction("👎")

    @commands.command(name="trivia")
    async def trivia_command(self, ctx):
        """Starts a trivia game with programming questions."""
        questions = [
            {"question": "What does 'HTML' stand for?", "answer": "HyperText Markup Language"},
            {"question": "What is the purpose of CSS in web development?", "answer": "Styling and layout"},
            {"question": "What is the latest version of Python as of 2024?", "answer": "Python 3.12"},
            {"question": "What is the full form of 'JSON'?", "answer": "JavaScript Object Notation"},
            {"question": "Which programming language is known as the backbone of the web?", "answer": "JavaScript"},
            {"question": "What is the main use of SQL?", "answer": "Managing and querying databases"},
            {"question": "Which language is primarily used for iOS app development?", "answer": "Swift"},
            {"question": "Which language is famous for its tagline 'write once, run anywhere'?", "answer": "Java"},
            {"question": "What is the primary purpose of the Git version control system?", "answer": "Tracking changes in code"},
            {"question": "Which keyword is used to create a function in Python?", "answer": "def"},
            {"question": "What is the extension of a C++ source file?", "answer": ".cpp"},
            {"question": "Which symbol is used for comments in JavaScript?", "answer": "//"},
            {"question": "What is the command to initialize a Git repository?", "answer": "git init"},
            {"question": "Which Python library is commonly used for data analysis?", "answer": "Pandas"},
            {"question": "What does 'OOP' stand for?", "answer": "Object-Oriented Programming"},
            {"question": "Which operator is used to access members of a class in C++?", "answer": "."},
            {"question": "Which function in Python is used to get user input?", "answer": "input()"},
            {"question": "What is the name of the first element in an array in most programming languages?", "answer": "Index 0"},
            {"question": "Which programming language is commonly used for machine learning?", "answer": "Python"},
            {"question": "Which language is primarily used to create dynamic and interactive web pages?", "answer": "JavaScript"},
            {"question": "What is the file extension for JavaScript files?", "answer": ".js"},
            {"question": "Which keyword is used to declare a constant in JavaScript?", "answer": "const"},
            {"question": "What is a 'for loop' used for in programming?", "answer": "Iterating over a sequence"},
            {"question": "What does 'API' stand for?", "answer": "Application Programming Interface"},
            {"question": "Which database uses collections and documents instead of tables and rows?", "answer": "MongoDB"},
            {"question": "Which library is commonly used for creating user interfaces in React?", "answer": "ReactDOM"},
            {"question": "What is the main purpose of Docker?", "answer": "Containerization"},
            {"question": "Which programming paradigm focuses on 'functions' as the primary building blocks?", "answer": "Functional Programming"},
            {"question": "What is the command to install a Python package using pip?", "answer": "pip install"},
            {"question": "What is the use of the 'return' keyword in programming?", "answer": "To return a value from a function"},
            {"question": "Which tag is used to add JavaScript in an HTML file?", "answer": "<script>"},
            {"question": "What is the default port number for HTTP?", "answer": "80"},
            {"question": "Which data structure uses a Last In First Out (LIFO) approach?", "answer": "Stack"},
            {"question": "What is the extension for a Python script file?", "answer": ".py"},
            {"question": "Which language is known for its turtle graphics module?", "answer": "Python"},
            {"question": "Which keyword is used to declare a variable in C++?", "answer": "int, float, char, etc."},
            {"question": "What does the acronym 'DOM' stand for?", "answer": "Document Object Model"},
            {"question": "What is the process of finding and fixing errors in code called?", "answer": "Debugging"},
            {"question": "Which language is widely used for backend development?", "answer": "Node.js (JavaScript)"},
            {"question": "What is the output of the expression 3**2 in Python?", "answer": "9"},
            {"question": "Which CSS property is used to change text color?", "answer": "color"},
            {"question": "What is the keyword for inheritance in Python?", "answer": "class <ChildClass>(<ParentClass>):"},
            {"question": "Which company developed the Java programming language?", "answer": "Sun Microsystems"},
            {"question": "What is the output of True and False in Python?", "answer": "False"},
            {"question": "Which function is used to convert a string to an integer in Python?", "answer": "int()"},
            {"question": "What is the name of the process of creating an object from a class?", "answer": "Instantiation"},
            {"question": "Which programming language uses 'schemas' for strongly typed databases?", "answer": "GraphQL"},
            {"question": "What does 'HTTP' stand for?", "answer": "HyperText Transfer Protocol"},
            {"question": "Which programming language is widely used for competitive programming?", "answer": "C++"},
            {"question": "Which Python keyword is used to handle exceptions?", "answer": "try"},
            {"question": "Which type of loop checks the condition after executing the body of the loop?", "answer": "do-while loop"},
            {"question": "What is the output of the expression 5//2 in Python?", "answer": "2"},
            {"question": "Which keyword is used to define a function in JavaScript?", "answer": "function"},
            {"question": "What is the main purpose of the 'this' keyword in JavaScript?", "answer": "Refers to the current object"},
            {"question": "Which operator is used to concatenate strings in JavaScript?", "answer": "+"},
            {"question": "What is the output of the expression 2 + '3' in JavaScript?", "answer": "23"},
            {"question": "Which keyword is used to declare a variable in JavaScript?", "answer": "var, let, const"},
            {"question": "What is the output of the expression 3 == '3' in JavaScript?", "answer": "true"},
            {"question": "Which function is used to add an element to the end of an array in JavaScript?", "answer": "push()"},
            {"question": "What is the output of the expression 5 > 3 && 2 < 4 in JavaScript?", "answer": "true"},
            {"question": "Which operator is used to access properties of an object in JavaScript?", "answer": "."},
            {"question": "What is the output of the expression 'hello'.toUpperCase() in JavaScript?", "answer": "HELLO"},
            {"question": "Which keyword is used to define a class in JavaScript?", "answer": "class"},
            {"question": "What is the output of the expression 2 + 3 * 4 in JavaScript?", "answer": "14"},
            {"question": "Which function is used to remove the last element of an array in JavaScript?", "answer": "pop()"},
            {"question": "What is the output of the expression 2 + '3' in JavaScript?", "answer": "23"},
            {"question": "Which operator is used to compare two values in JavaScript?", "answer": "==="},
            {"question": "What is the output of the expression 'hello'.length in JavaScript?", "answer": "5"},
            {"question": "Which function is used to remove the first element of an array in JavaScript?", "answer": "shift()"},
]
        question = random.choice(questions)
        await ctx.send(question["question"])

        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        try:
            answer = await self.bot.wait_for('message', check=check, timeout=15.0)
        except asyncio.TimeoutError:
            embed = discord.Embed(
                title="Timeout",
                description=f'Sorry, you took too long. The correct answer was {question["answer"]}.',
                color=discord.Color.red()
            )
            return await ctx.send(embed=embed)

        if answer.content.lower() == question["answer"].lower():
            embed = discord.Embed(
                title="Correct",
                description='Correct!',
                color=discord.Color.green()
            )
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                title="Incorrect",
                description=f'Incorrect. The correct answer was {question["answer"]}.',
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)

    @app_commands.command(name="trivia", description="Start a trivia game")
    async def trivia(self, interaction: discord.Interaction):
        """Start a trivia game"""
        questions = [
            {"question": "What does 'HTML' stand for?", "answer": "HyperText Markup Language"},
            {"question": "What is the purpose of CSS in web development?", "answer": "Styling and layout"},
            {"question": "What is the latest version of Python as of 2024?", "answer": "Python 3.12"},
            {"question": "What is the full form of 'JSON'?", "answer": "JavaScript Object Notation"},
            {"question": "Which programming language is known as the backbone of the web?", "answer": "JavaScript"},
            {"question": "What is the main use of SQL?", "answer": "Managing and querying databases"},
            {"question": "Which language is primarily used for iOS app development?", "answer": "Swift"},
            {"question": "Which language is famous for its tagline 'write once, run anywhere'?", "answer": "Java"},
            {"question": "What is the primary purpose of the Git version control system?", "answer": "Tracking changes in code"},
            {"question": "Which keyword is used to create a function in Python?", "answer": "def"},
            {"question": "What is the extension of a C++ source file?", "answer": ".cpp"},
            {"question": "Which symbol is used for comments in JavaScript?", "answer": "//"},
            {"question": "What is the command to initialize a Git repository?", "answer": "git init"},
            {"question": "Which Python library is commonly used for data analysis?", "answer": "Pandas"},
            {"question": "What does 'OOP' stand for?", "answer": "Object-Oriented Programming"},
            {"question": "Which operator is used to access members of a class in C++?", "answer": "."},
            {"question": "Which function in Python is used to get user input?", "answer": "input()"},
            {"question": "What is the name of the first element in an array in most programming languages?", "answer": "Index 0"},
            {"question": "Which programming language is commonly used for machine learning?", "answer": "Python"},
            {"question": "Which language is primarily used to create dynamic and interactive web pages?", "answer": "JavaScript"},
            {"question": "What is the file extension for JavaScript files?", "answer": ".js"},
            {"question": "Which keyword is used to declare a constant in JavaScript?", "answer": "const"},
            {"question": "What is a 'for loop' used for in programming?", "answer": "Iterating over a sequence"},
            {"question": "What does 'API' stand for?", "answer": "Application Programming Interface"},
            {"question": "Which database uses collections and documents instead of tables and rows?", "answer": "MongoDB"},
            {"question": "Which library is commonly used for creating user interfaces in React?", "answer": "ReactDOM"},
            {"question": "What is the main purpose of Docker?", "answer": "Containerization"},
            {"question": "Which programming paradigm focuses on 'functions' as the primary building blocks?", "answer": "Functional Programming"},
            {"question": "What is the command to install a Python package using pip?", "answer": "pip install"},
            {"question": "What is the use of the 'return' keyword in programming?", "answer": "To return a value from a function"},
            {"question": "Which tag is used to add JavaScript in an HTML file?", "answer": "<script>"},
            {"question": "What is the default port number for HTTP?", "answer": "80"},
            {"question": "Which data structure uses a Last In First Out (LIFO) approach?", "answer": "Stack"},
            {"question": "What is the extension for a Python script file?", "answer": ".py"},
            {"question": "Which language is known for its turtle graphics module?", "answer": "Python"},
            {"question": "Which keyword is used to declare a variable in C++?", "answer": "int, float, char, etc."},
            {"question": "What does the acronym 'DOM' stand for?", "answer": "Document Object Model"},
            {"question": "What is the process of finding and fixing errors in code called?", "answer": "Debugging"},
            {"question": "Which language is widely used for backend development?", "answer": "Node.js (JavaScript)"},
            {"question": "What is the output of the expression 3**2 in Python?", "answer": "9"},
            {"question": "Which CSS property is used to change text color?", "answer": "color"},
            {"question": "What is the keyword for inheritance in Python?", "answer": "class <ChildClass>(<ParentClass>):"},
            {"question": "Which company developed the Java programming language?", "answer": "Sun Microsystems"},
            {"question": "What is the output of True and False in Python?", "answer": "False"},
            {"question": "Which function is used to convert a string to an integer in Python?", "answer": "int()"},
            {"question": "What is the name of the process of creating an object from a class?", "answer": "Instantiation"},
            {"question": "Which programming language uses 'schemas' for strongly typed databases?", "answer": "GraphQL"},
            {"question": "What does 'HTTP' stand for?", "answer": "HyperText Transfer Protocol"},
            {"question": "Which programming language is widely used for competitive programming?", "answer": "C++"},
            {"question": "Which Python keyword is used to handle exceptions?", "answer": "try"},
            {"question": "Which type of loop checks the condition after executing the body of the loop?", "answer": "do-while loop"},
            {"question": "What is the output of the expression 5//2 in Python?", "answer": "2"},
            {"question": "Which keyword is used to define a function in JavaScript?", "answer": "function"},
            {"question": "What is the main purpose of the 'this' keyword in JavaScript?", "answer": "Refers to the current object"},
            {"question": "Which operator is used to concatenate strings in JavaScript?", "answer": "+"},
            {"question": "What is the output of the expression 2 + '3' in JavaScript?", "answer": "23"},
            {"question": "Which keyword is used to declare a variable in JavaScript?", "answer": "var, let, const"},
            {"question": "What is the output of the expression 3 == '3' in JavaScript?", "answer": "true"},
            {"question": "Which function is used to add an element to the end of an array in JavaScript?", "answer": "push()"},
            {"question": "What is the output of the expression 5 > 3 && 2 < 4 in JavaScript?", "answer": "true"},
            {"question": "Which operator is used to access properties of an object in JavaScript?", "answer": "."},
            {"question": "What is the output of the expression 'hello'.toUpperCase() in JavaScript?", "answer": "HELLO"},
            {"question": "Which keyword is used to define a class in JavaScript?", "answer": "class"},
            {"question": "What is the output of the expression 2 + 3 * 4 in JavaScript?", "answer": "14"},
            {"question": "Which function is used to remove the last element of an array in JavaScript?", "answer": "pop()"},
            {"question": "What is the output of the expression 2 + '3' in JavaScript?", "answer": "23"},
            {"question": "Which operator is used to compare two values in JavaScript?", "answer": "==="},
            {"question": "What is the output of the expression 'hello'.length in JavaScript?", "answer": "5"},
            {"question": "Which function is used to remove the first element of an array in JavaScript?", "answer": "shift()"},
]
        question = random.choice(questions)
        embed = discord.Embed(
            title="Trivia",
            description=question["question"],
            color=discord.Color.blue()
        )
        await interaction.response.send_message(embed=embed)

        def check(m):
            return m.author == interaction.user and m.channel == interaction.channel

        try:
            answer = await self.bot.wait_for('message', check=check, timeout=15.0)
        except asyncio.TimeoutError:
            await interaction.followup.send(f'Time is up! The correct answer was {question["answer"]}.')
        else:
            if answer.content.lower() == question["answer"].lower():
                await interaction.followup.send('Correct!')
            else:
                await interaction.followup.send(f'Incorrect! The correct answer was {question["answer"]}.')

    @commands.command(name="codechallenge")
    async def codechallenge_command(self, ctx):
        """Gives a random coding challenge."""
        challenges = [
            "Write a function that reverses a string.",
            "Write a function that checks if a number is prime.",
            "Write a function that sorts a list of numbers.",
            "Write a function that finds the factorial of a number.",
            "Write a function that checks if a string is a palindrome."
            "Write a program that prints numbers from 1 to 100, but for multiples of 3, print Fizz, for multiples of 5, print Buzz, and for multiples of both, print FizzBuzz."
            "Create a function that checks if a given string is a palindrome (reads the same backward as forward)"
            "Write a function that takes a string and returns it reversed without using built-in reverse functions."
            "Build a function that calculates the factorial of a given number."
            "Given an array of numbers 1 to N with one number missing, find the missing number in O(n) time."
            "Check if a given string has all unique characters."
            "Write a function to count the number of vowels and consonants in a string."
            "Write a function that calculates the sum of the digits of a given number."
            "Build a function that checks if two strings are anagrams of each other."
            "Rotate a given N x N matrix by 90 degrees in place."
            "Given a string, find the length of the longest substring without repeating characters."
            "Check if a string has balanced brackets (e.g., {}, [], () are properly closed and nested)."
            "Write a program to generate all prime numbers up to a given number N."
            "Implement a binary search algorithm to find an element in a sorted array."
            "Implement popular sorting algorithms like Bubble Sort, Merge Sort, and Quick Sort from scratch."
            "Implement a calculator that can handle operations like addition, subtraction, multiplication, and division. Extend it to support parentheses."
            "Write a program to solve a given Sudoku puzzle using backtracking."
            "Generate all permutations of a given string or list."
            "Implement a Least Recently Used (LRU) cache with O(1) time complexity for get and put operations."
            "Given a 2D board and a word, find if the word exists in the grid by moving horizontally, vertically, or diagonally."
            "Implement a Trie data structure to efficiently store and retrieve strings, and add functions like insertion, search, and auto-complete suggestions."
            "Implement Dijkstra’s or A* algorithm to find the shortest path between two nodes in a weighted graph."
            "Solve the 0/1 Knapsack problem using dynamic programming to maximize the value of items that can fit into a given capacity."
            "Build a rate limiter to handle API requests, ensuring only a certain number of requests are processed in a given time window."
            "Given a list of words and a width, format the text so that it’s fully justified, with words evenly distributed across lines."
            "Place N queens on an N×N chessboard so that no two queens threaten each other."
            "Given a 2D binary matrix filled with 0s and 1s, find the largest rectangle containing only 1s and return its area."
            "Implement a function to perform a binary search on a rotated sorted array."
            "Write a function to find the longest common prefix string amongst an array of strings."
            "Given a list of intervals, merge overlapping intervals."
            "Implement a function to convert a Roman numeral to an integer."
            "Given a list of words, group anagrams together."
            "Implement a function to reverse a linked list."
            "Write a function to find the kth largest element in an unsorted array."
            "Implement a function to find the longest palindromic substring in a string."
            "Given a list of non-negative integers, arrange them such that they form the largest number."
            "Implement a function to find the longest increasing subsequence in an array."
            "Write a function to find the minimum window in a string that contains all characters of another string."
            "Given a string, find the length of the longest substring with at most two distinct characters."
            "Implement a function to find the median of two sorted arrays."
            "Write a function to find the longest common subsequence between two strings."
            "Given a string, find the longest palindromic substring."
            "Implement a function to find the longest substring without repeating characters."
            "Write a function to find the longest increasing subsequence in an array."
            "Given a list of intervals, merge overlapping intervals."
            "Implement a function to convert a Roman numeral to an integer."
            "Write a function to find the kth largest element in an unsorted array."
            "Implement a function to reverse a linked list."
            "Given a list of words, group anagrams together."
            "Implement a function to perform a binary search on a rotated sorted array."
            "Write a function to find the longest common prefix string amongst an array of strings."
            "Given a 2D binary matrix filled with 0s and 1s, find the largest rectangle containing only 1s and return its area."
            "Create a virtual file system that supports commands like mkdir, ls, touch, read, and write, with hierarchical structures and efficient navigation."
            "Implement a thread-safe producer-consumer system using a bounded buffer. Handle edge cases like underflow, overflow, and multithreading."
            "Build a simple chat application using sockets to send and receive messages between clients and a server."
            "Create a RESTful API for a simple todo list application with endpoints for creating, updating, deleting, and fetching tasks."
            "Implement a basic web server that can handle HTTP requests like GET, POST, PUT, and DELETE, and serve static files."
            "Write a program to find the shortest path between cities using graph traversal algorithms like Dijkstra’s or A*."
            "Implement a function to calculate the edit distance between two strings, measuring the minimum number of operations required to convert one string into another."
            "Given a list of words, find the longest word made of other words in the list."
            "Build a function to calculate the maximum sum of a subarray within a given array of integers."
            "Implement a function to find the longest word in a dictionary that can be built one character at a time by other words in the dictionary."
            "Write a program to find the longest increasing subsequence in an array of integers."
            "Given a list of integers, write a function to return the maximum sum of non-adjacent numbers."
            "Implement a function to find the maximum product of two integers in a given list."
            "Create a function to find the minimum number of coins required to make a given amount of change."
            "Given a list of integers, write a function to return the maximum sum of a contiguous subarray."
            "Implement a function to find the maximum sum of a subarray with at least k elements."
            "Write a program to find the longest common subsequence between two strings."
            "Given a list of integers, write a function to return the maximum sum of a subarray with at least k elements."
            "Implement a function to find the maximum product of three integers in a given list."
            "Create a function to find the minimum number of coins required to make a given amount of change."
            "Given a list of integers, write a function to return the maximum sum of a contiguous subarray."
            "Implement a function to find the maximum sum of a subarray with at least k elements."
            "Write a program to find the longest common subsequence between two strings."
            "Given a list of integers, write a function to return the maximum sum of a subarray with at least k elements."
            "Implement a function to find the maximum product of three integers in a given list."
            "Create a function to find the minimum number of coins required to make a given amount of change."
            "Given a list of integers, write a function to return the maximum sum of a contiguous subarray."
            "Implement a function to find the maximum sum of a subarray with at least k elements."
            "Write a program to find the longest common subsequence between two strings."
            "Given a list of integers, write a function to return the maximum sum of a subarray with at least k elements."
            "Implement a function to find the maximum product of three integers in a given list."
            "Create a function to find the minimum number of coins required to make a given amount of change."
            "Given a list of integers, write a function to return the maximum sum of a contiguous subarray."
            "Implement a function to find the maximum sum of a subarray with at least k elements."
            "Write a program to find the longest common subsequence between two strings."
            "Given a list of integers, write a function to return the maximum sum of a subarray with at least k elements."
            "Implement a function to find the maximum product of three integers in a given list."
            "Create a function to find the minimum number of coins required to make a given amount of change."
            "Given a list of integers, write a function to return the maximum sum of a contiguous subarray."
            "Implement a function to find the maximum sum of a subarray with at least k elements."
            "Write a program to find the longest common subsequence between two strings."
            "Given a list of integers, write a function to return the maximum sum of a subarray with at least k elements."
            "Implement a function to find the maximum product of three integers in a given list."
            "Create a function to find the minimum number of coins required to make a given amount of change."
        ]
        challenge = random.choice(challenges)
        embed = discord.Embed(
            title="Coding Challenge",
            description=f'Your coding challenge is: {challenge}',
            color=discord.Color.blue()
        )
        await ctx.send(embed=embed)

    @commands.command(name="quote")
    async def quote_command(self, ctx):
        """Sends a random inspirational quote."""
        quotes = [
            "Code is like humor. When you have to explain it, it’s bad. – Cory House",
            "Fix the cause, not the symptom. – Steve Maguire",
            "Optimism is an occupational hazard of programming: feedback is the treatment. – Kent Beck",
            "When to use iterative development? You should use iterative development only on projects that you want to succeed. – Martin Fowler",
            "Simplicity is the soul of efficiency. – Austin Freeman"
            "Any fool can write code that a computer can understand. Good programmers write code that humans can understand. — Martin Fowler"
            "Programs must be written for people to read, and only incidentally for machines to execute. — Harold Abelson"
            "The only way to learn a new programming language is by writing programs in it. — Dennis Ritchie"
            "Before software can be reusable, it first has to be usable. — Ralph Johnson"
            "First, solve the problem. Then, write the code. — John Johnson"
            "The best error message is the one that never shows up. — Thomas Fuchs"
            "It's not a bug – it's an undocumented feature. — Anonymous"
            "Simplicity is the soul of efficiency. — Austin Freeman"
            "Talk is cheap. Show me the code. — Linus Torvalds"
            "Fix the cause, not the symptom. — Steve Maguire"
            "Code is like humor. When you have to explain it, it’s bad. — Cory House"
            "Deleted code is debugged code. — Jeff Sickel"
            "When debugging, novices insert corrective code; experts remove defective code. — Richard Pattis"
            "In order to be irreplaceable, one must always be different. — Coco Chanel (but this applies so well to unique code design!)"
            "Programming isn’t about what you know; it’s about what you can figure out. — Chris Pine"
            "Don’t comment bad code – rewrite it. — Brian W. Kernighan"
            "Walking on water and developing software from a specification are easy if both are frozen. — Edward V. Berard"
            "The most disastrous thing that you can ever learn is your first programming language. — Alan Kay"
            "Always code as if the guy who ends up maintaining your code will be a violent psychopath who knows where you live. — John Woods"
            "Good code is its own best documentation. — Steve McConnell"
        ]
        quote = random.choice(quotes)
        embed = discord.Embed(
            title="Inspirational Quote",
            description=quote,
            color=discord.Color.purple()
        )
        await ctx.send(embed=embed)

    @commands.command(name="joke")
    async def joke_command(self, ctx):
        """Tells a random programming joke."""
        jokes = [
            "Why do programmers prefer dark mode? Because light attracts bugs!",
            "Why do Java developers wear glasses? Because they don't see sharp.",
            "How many programmers does it take to change a light bulb? None, that's a hardware problem.",
            "Why do Python programmers have low self-esteem? Because they're constantly comparing their self to others.",
            "Why do programmers hate nature? It has too many bugs."
            "Why do programmers last so long in bed? Because they keep optimizing their loops."
            "My girlfriend called me a function with no returns. I told her, I'm just waiting for the right input to blow up your stack."
            "Why was the database administrator bad at flirting? They couldn't handle relationships unless they were one-to-many."
            "Why do programmers prefer one-night stands?No need to commit to the repository."
            "I tried debugging my girlfriend… Turns out, the issue was in the hardware configuration. 😏"
            "How do programmers practice safe sex? They use a try-catch block for protection."
            "My ex told me, You're too into your work! I told her, I'm not into you because your interface sucks."
            "A designer, a coder, and a tester walk into a bar... The coder ends up alone because they were too busy handling exceptions."
            "Why was the programmer’s date upset? They seg-faulted and dumped core halfway through."
            "What’s the dirtiest thing a programmer can whisper in bed? I’ll show you my hidden attribute. 😈"
            "Why do programmers like older partners? They come with a well-documented API."
            "My partner left me because I was too much of a nerd. Jokes on them—I’ve got 5G, unlimited data, and a vibrator script."
            "What’s a programmer’s favorite foreplay? Penetration testing."
            "Why don’t programmers get jealous? Because they know how to handle multiple threads."
            "My crush called me a console log... I said, Why? Because I’m always showing my output?"
            "What do you call it when a programmer is bad in bed? Hard-coded disappointment. 😏"
            "My girlfriend asked why I spend so much time coding. I told her, “Because I’ve already hacked into your source control."
            "Why did the programmer break up with their partner? They couldn’t handle their spaghetti logic."
            "What’s the most awkward thing a programmer says during sex? Wait, let me merge conflicts."
            "Why was the programmer’s partner mad? They were tired of being in the back-end all the time. 😂"
            "My crush called me a console log... I said, Why? Because I’m always showing my output?"
            "Why don’t programmers do it in the dark? Because they keep looking for a light mode to turn them on."
            "My ex said I was too much into programming. I told her, “Well, at least I know how to push the right buttons."
            "Why do coders love foreplay? Because they hate going straight to production without testing."
            "I told her I’d give her the best experience. She said, Prove it! So, I ran intensity++."
            "Why did the programmer bring a condom to the meeting? Just in case they had to protect their package."
            "I told my partner I was debugging… Turns out, I was just trying to find the missing climax."
            "Why are programmers so good in bed? They’re all about deep penetration testing."
            "My girlfriend asked me why I take so long to finish. I said, Baby, I’m just loading the assets."
            "What’s a coder’s version of dirty talk? Let me get inside your private variables."
            "Why do programmers date models? Because they love playing with big data."
            "I told her I’d take her to cloud nine. Turns out, she couldn’t handle my high availability."
            "She said, Talk dirty to me! So, I whispered, “I’ll optimize your back-end until you can’t handle the throughput."
            "Why was the programmer’s date annoyed? Because they kept asking, Are you responsive yet?"
            "My ex said I didn’t satisfy her. I said, It’s not me—it’s your poor user experience."
            "Why do coders never break up? Because they always find a way to resolve conflicts."
            "My crush told me she likes guys who write clean code... So, I wiped my browser history and said, “You mean like this?”"
            "Why do programmers make bad flings? Because they’re too busy debugging their ex’s trauma."
            "She said, “Talk dirty to me.” I replied, “Your alignment is off, your flow’s broken, and your backend’s outdated.”"
            "I tried flirting with a designer. She ghosted me, saying, “You lack responsiveness.”"
            "My girlfriend broke up with me because I said, “You’re like JavaScript.”She asked why, and I said, “Everyone uses you, but no one fully understands you.”"
            "I told her I’d make her scream like my code editor does when I forget a semicolon. Now she calls me syntax daddy."
            "She asked me what I’m good at in bed. I said, “Ctrl + Z. Undoing all my mistakes.”"
            "Why don’t programmers date often? Because they get stuck in an infinite loop of “What did I do wrong?”"
            "My crush asked me to teach her coding... Now she just complains, “Stop trying to insert yourself everywhere!”"
            "Why do programmers love WiFi? Because it’s the only thing they’ve ever connected to."
            "I told her, “I’ll optimize your backend tonight.” She said, “You better. Last night it crashed halfway through.”"
            "Why do programmers suck at breakups? They keep saying, “Let’s try one more iteration.”"
            "My ex said I’m like an old iPhone. “You’re slow, outdated, and your battery doesn’t last long.”"
            "I asked her why she likes me. She said, “You’re like open-source software—free, but I still feel like I’m paying for it.”"
            "Why was the coder so bad at sexting? They kept writing in CamelCase."
            "I told her I’m good with tech... She said, “Okay, but can you handle my settings?”"
            "Why don’t programmers do casual dating? They hate working on temporary projects."
            "My partner said, “I don’t think you’re putting in enough effort.” So, I upgraded my RAM and said, “Try me now.”"
            "I dated a programmer once. Worst mistake of my life—they tried to compress all my emotions into a zip file."
            "Why do programmers last longer in relationships? Because they’re too scared to delete their cache."
        ]
        joke = random.choice(jokes)
        embed = discord.Embed(
            title="Programming Joke",
            description=joke,
            color=discord.Color.orange()
        )
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Fun(bot))