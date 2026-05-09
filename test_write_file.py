from functions.write_file import write_file

print(write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum"))
print(write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet"))
# absolute path outside working dir — should be blocked
print(write_file("calculator", "/tmp/temp.txt", "this should not be allowed"))
