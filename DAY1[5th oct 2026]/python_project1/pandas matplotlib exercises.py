import pandas as pd
import numpy as np
data = {

"Employee": ["Aisha", "Rahul", "Neha", "Omar", "Priya", "Karan", "Fatima", "Vikram"],
"Department": ["HR", "IT", "Finance", "IT", "HR", "Finance", "IT", "HR"],
"Training_Hours": [12, 18, 10, 22, 15, 8, 20, 14],
"Assessment_Score": [78, 88, 72, 91, 84, 69, 95, 80],
"Completed": ["Yes", "Yes", "No", "Yes", "Yes", "No", "Yes", "Yes"]
}
#1.1. Display the complete DataFrame.
df = pd.DataFrame(data)

print(df)
#2. Display only the first 4 rows.
print(df.head(4))

#3. Display only these columns:Employee,Assessment_Score

print(df[["Employee","Assessment_Score"]])

#4. Show only employees from the IT department.
print(df[df["Department"] == "IT"])

#5. Show employees whose Assessment_Score is greater than 80.
print(df[df["Assessment_Score"]>80])

#6. Show employees who completed the training:Completed = Yes
print(df[df["Completed"]=="Yes"])

#7. Show employees who:belong to IT ,and scored above 85
print(df[(df["Department"] == "IT") & (df["Assessment_Score"]>85)])

#8. Create a new column called:Passed Condition:Assessment_Score >= 75,,S tore:Pass,Fail

df["Passed"]=np.where(df["Assessment_Score"]>=75,"Pass","Fail")

#9. Find the average assessment score.
score=np.array([78, 88, 72, 91, 84, 69, 95, 80])
print("average assessment score:",np.mean(score))

#10. Find: highest assessment score ,lowest assessment score
print("highest assessment score :",np.max(score))
print("lowest assessment score :",np.min(score))

#11. Find the average training hours.
T_hours=np.array([12, 18, 10, 22, 15, 8, 20, 14])
print(" average training hours:",np.mean(T_hours))

#12. Sort employees by Assessment_Score from highest to lowest.
print(df.sort_values(by="Assessment_Score",ascending=False))

#13. Group by Department and find the average assessment score.
print(df.groupby("Department")["Assessment_Score"].mean())

#14.Group by Department and find the total training hours.
print(df.groupby("Department")["Training_Hours"].sum())

#15. Count how many employees belong to each department.
print(df["Department"].value_counts())

#16. Count how many employees completed training.
print((df["Completed"]=="Yes").sum())

#17. Using NumPy, take the assessment scores:scores = df["Assessment_Score"].to_numpy()Find:mean,maximum,minimum,standard deviation
scores = df["Assessment_Score"].to_numpy()
print("mean:",np.mean(scores))
print("min:",np.min(scores))
print("max:",np.max(scores))
print("standard deviation:",np.std(scores))

#18. Create a bar chart showing average score by department.
import matplotlib.pyplot as plt
avg_score=df.groupby("Department")["Assessment_Score"].mean()

avg_score.plot(kind="bar")
plt.title(" average score by department")
plt.xlabel("department")
plt.ylabel("average score")
plt.show()

#19. Create a bar chart showing total training hours by department.

total_hours=df.groupby("Department")["Training_Hours"].sum()

total_hours.plot(kind="bar")
plt.title(" total training hours by department")
plt.xlabel("department")
plt.ylabel("total training hours ")
plt.show()

#20. Create a Seaborn chart comparing: Department vs Assessment_Score


import seaborn as sns


sns.barplot(data=df, x="Department", y="Assessment_Score")

plt.title("Department vs Assessment_Score")
plt.show()