import pandas as pd



data={
    "product":["Laptop","Mouse","keyboard","laptop","Mouse"],
    "city":["hyderbad","mumbai","delhi","hyderbad","Delhi"],
    "quantity":[2,5,3,1,4],
    "price":[60000,800,15000,60000,800]
}
df=pd.DataFrame(data)
#print(df)

#to get the head of the head where if we have more that a 100 data then we get to knwo teh head informatiomn
print(df.head())
#to know the shape of the data
print(df.shape)
#to know the columns of the data
print(df.columns)
#to know the datatypes of our dataset
print(df.dtypes)

#Data manipulations

print(df[df["city"]=="hyderbad"])

#selecting columns
print(df[["product","price"]])

#adding new columns
df["total"]=df["quantity"]*df["price"]
print(df)

print(df.groupby("product")["total"].sum())

print(df.sort_values(by="total",ascending=False))

#
# import matplotlib.pyplot as plt
# sales=df.groupby("product")["total"].sum()
#
# sales.plot(kind="bar")
# plt.title("sales by product")
# plt.xlabel("product")
# plt.ylabel("sales")
# plt.show()

import seaborn as sns
import matplotlib.pyplot as plt

sns.barplot(data=df, x="product", y="total")

plt.title("Sales by Product")
plt.show()

