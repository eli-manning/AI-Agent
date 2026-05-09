from functions.get_file_content import get_file_content

# print(get_file_content("calculator", "lorem.txt"))
print(get_file_content("calculator", "main.py"))
print(get_file_content("calculator", "pkg/calculator.py"))
# absolute path — should be blocked by validate_path
print(get_file_content("calculator", "/bin/cat"))
print(get_file_content("calculator", "pkg/does_not_exist.py"))
