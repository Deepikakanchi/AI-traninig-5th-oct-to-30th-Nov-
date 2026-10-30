# Use: urban_mobility.csv, equipment_events.json, and coastal_monitoring_log.txt.

import pandas as pd


# A1. Load urban_mobility.csv into a Pandas DataFrame and display the first five rows.
df=pd.read_csv("urban_mobility.csv")
print(df.head(5))

# A2. Create a new column Energy_Per_Km = Energy_Used_kWh / Distance_Km.
df["Energy_Per_Km"]=df["Energy_Used_kWh"] / df["Distance_Km"]
print(df)

# A3. Display only Electric Van records where Maintenance_Flag is Yes.
print(df[(df["Vehicle_Type"]=="Electric Van") &(df["Maintenance_Flag"]=="Yes")])


# A4. Group by Vehicle_Type and display average Distance_Km and total Trips_Count.
print(df.groupby("Vehicle_Type")["Distance_Km"].mean())
print(df.groupby("Vehicle_Type")["Trips_Count"].sum())

# A5. Use NumPy to calculate the mean, maximum and minimum of Energy_Used_kWh.
import numpy as np
print(np.mean(df["Energy_Used_kWh"]))
print(np.min(df["Energy_Used_kWh"]))
print(np.max(df["Energy_Used_kWh"]))


# A6. Create one bar chart showing average Energy_Used_kWh by Vehicle_Type using Matplotlib or Seaborn.
import matplotlib.pyplot as plt
plt.bar(df["Energy_Used_kWh"],df["Vehicle_Type"])
plt.show()

# A7. Load equipment_events.json and print event_id, asset type, site and severity for every event.
import json
with open("equipment_events.json","r") as f:
    data=json.load(f)
print(data)
for event in data:
    print(event["event_id"],event["asset"]["type"],event["asset"]["site"],event["severity"])


# A8. Display JSON records with temperature above 70. If actions is missing, display 'No actions recorded'.
for event in data:
    if event["temperature"]>70:
        print(event)


# A9. Read coastal_monitoring_log.txt and count total words and the number of times the word 'inspection'
# appears.

with open("coastal_monitoring_log.txt","r") as f:
    text=f.read()
print(text)

print(text.lower().count("inspection"))


# A10. Print only the lines containing either 'boardwalk', 'maintenance', or 'wind'.
for line in text.splitlines():
    if "boardwalk" or "maintenance" or "wind" in line:
        print(line)