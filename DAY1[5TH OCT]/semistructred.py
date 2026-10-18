import json
import pandas as pd

with open("support_tickets.json", "r") as f:
       tickets = json.load(f)

print(tickets)


print(tickets[0])
print(tickets[0]["issue"])
print(tickets[0]["customer"]["name"])

for ticket in tickets:
    print(ticket["ticket_id"],ticket["issue"])

#handle optional field

#print(tickets[1]["priority"])    #-> we get a KeyError: 'priority' instead of this we are writing the next line

print(tickets[1].get("priority","Not Assigned"))

#normalize  -> normalize json so that the data is converted to tabular format for easy analysis.
df=pd.json_normalize(tickets)
print(df)
