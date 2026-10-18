with open("incident_notes.txt")as file:
    text=file.read()
print(text)

#count words:
words=text.split()
print("total words:",len(words))

#search
if "vibration" in text.lower():
    print("vibration was mentioned")
#