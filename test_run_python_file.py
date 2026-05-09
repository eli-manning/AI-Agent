from functions.run_python_file import run_python_file

print(run_python_file("calculator", "main.py"))
print(run_python_file("calculator", "main.py", ["3 + 5"]))
print(run_python_file("calculator", "tests.py"))
# traversal outside working dir — should be blocked
print(run_python_file("calculator", "../main.py"))
print(run_python_file("calculator", "nonexistent.py"))
# not a .py file — should be rejected by running check
print(run_python_file("calculator", "lorem.txt"))
