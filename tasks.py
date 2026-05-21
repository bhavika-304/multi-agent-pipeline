TASKS = [
    {
        "id": 1,
        "goal": "write a Python function that adds two numbers, save to add.py, and run it",
        "expected_file": "add.py",
        "check": {
            "import_from": "add",
            "function": "add_numbers",
            "test_cases": [
                {"args": [2, 3], "expected": 5},
                {"args": [-1, 1], "expected": 0},
                {"args": [0, 0], "expected": 0}
            ]
        }
    },
    {
        "id": 2,
        "goal": "write a Python function that checks if a number is even or odd, save to even_odd.py, and run it",
        "expected_file": "even_odd.py",
        "check": {
            "import_from": "even_odd",
            "function": "check_even_odd",
            "test_cases": [
                {"args": [2], "expected": "even"},
                {"args": [3], "expected": "odd"},
                {"args": [0], "expected": "even"}
            ]
        }
    },
    {
        "id": 3,
        "goal": "write a Python function that finds the maximum of a list, save to find_max.py, and run it",
        "expected_file": "find_max.py",
        "check": {
            "import_from": "find_max",
            "function": "find_max",
            "test_cases": [
                {"args": [[1, 5, 3]], "expected": 5},
                {"args": [[-1, -5, -3]], "expected": -1}
            ]
        }
    },
    {
        "id": 4,
        "goal": "write a Python function that counts vowels in a string, save to count_vowels.py, and run it",
        "expected_file": "count_vowels.py",
        "check": {
            "import_from": "count_vowels",
            "function": "count_vowels",
            "test_cases": [
                {"args": ["hello"], "expected": 2},
                {"args": ["aeiou"], "expected": 5},
                {"args": ["xyz"], "expected": 0}
            ]
        }
    },
    {
        "id": 5,
        "goal": "write a Python function that reverses a list, save to reverse_list.py, and run it",
        "expected_file": "reverse_list.py",
        "check": {
            "import_from": "reverse_list",
            "function": "reverse_list",
            "test_cases": [
                {"args": [[1, 2, 3]], "expected": [3, 2, 1]},
                {"args": [[]], "expected": []}
            ]
        }
    }
    
]