with open("sample.txt", "w") as f:
    f.write("This is a test log entry.")

with open("sample.txt", "r") as f:
    print(f.read())
