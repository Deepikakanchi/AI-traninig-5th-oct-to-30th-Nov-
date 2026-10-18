# 1. Read the complete text file.
with open("wildlife_report.txt")as file:
    text=file.read()
print(text)

# 2. Count the total number of words.
#count words:
words=text.split()
print("total words:",len(words))
# 3. Check whether the word elephant appears in the report.
#search
if "elephant" in text.lower():
    print("elephant was mentioned")
# 4. Count how many times elephant appears.
print("elephant count",text.lower().count("elephant"))
# 5. Print only the lines containing the word trail
for line in text.splitlines():
    if "trail" in line:
        print(line)
# 6. Print only the lines containing the word animal .
for line in text.splitlines():
    if "animal" in line:
        print(line)


