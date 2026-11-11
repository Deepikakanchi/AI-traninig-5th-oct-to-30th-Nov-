import json
import pandas as pd



# 1. Load the JSON using Python.
with open("festival_events.json", "r") as f:
    events= json.load(f)

print(events)
# 2. Print the name of every event.
for event in events:
    print(event["name"])

# 3. Print the city of each event.
for event in events:
    print("city of each event.",event["location"]["city"])

# 4. Display only events with more than 700 visitors.
print("Display only events with more than 700 visitors.")
for event in events:
    if[event["visitors"]>700]:
        print(event)
# 5. Some events do not have features . Display: the features if available,"No features listed" if missing
for event in events:
    if "features" in event:
        print(event["features"])
    else:
        print("No features listed")

# 6. Convert the JSON into a Pandas DataFrame using pd.json_normalize() .
#normalize  -> normalize json so that the data is converted to tabular format for easy analysis.
df=pd.json_normalize(events)
print(df)