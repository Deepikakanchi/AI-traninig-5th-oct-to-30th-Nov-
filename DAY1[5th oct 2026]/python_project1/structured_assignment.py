#1. Load the CSV into a Pandas DataFrame.
import pandas as pd
import numpy as np
df=pd.read_csv("library_loans.csv")
print(df)


# 2. Display only Member_Name , Book_Category , and Fine .
print(df[["Member_Name" , "Book_Category" ,"Fine"]])

# 3. Show only members whose Fine is greater than 50.
print(df[df["Fine"]>50])

# 4. Create a new column called Status :No Fine if Fine = 0,Fine Due otherwise
df["Status"]=np.where(df["Fine"]==0,"No Fine","Due")
print(df)
# 5. Find the average number of days borrowed.
print("average number of days borrowed:",df["Days_Borrowed"].mean())

# 6. Find the total fine collected by Book_Category.
print("total fine collected by Book_Category:",df.groupby("Book_Category")["Fine"].sum())