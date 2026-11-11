import pandas as pd  # type: ignore

data = {
    "product": ["Laptop", "Phone", "Headphones", "Tablet"],
    "city": ["Delhi", "Mumbai", "Bengaluru", "Hyderabad"],
    "quantity": [10, 15, 8, 12],
    "price": [50000, 25000, 3000, 18000]
}

df = pd.DataFrame(data)
print(df)
print(df.head())
print(df.shape)
print(df.columns)
print(df.dtypes)

print(df[df["city"]=="Hyderabad"])

print(df[["product","city"]])

df["total"]=df["quantity"]*df["price"]
print(df)

print(df.groupby("product")["total"].sum())


print(df.sort_values("total",ascending=False))

import matplotlib.pyplot as plt  # type: ignore
sales=df.groupby("product")["total"].sum()
sales.plot(kind="bar")

plt.show()