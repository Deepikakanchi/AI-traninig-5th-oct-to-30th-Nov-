import psycopg2
from fastapi import FastAPI
from pydantic import BaseModel
app = FastAPI()
class Product(BaseModel):
    id:int
    name:str
    price:float

def get_connection():
    conn=psycopg2.connect(
        host="localhost",
        database="fastapi_store",
        user="postgres",
        password="Admin@123"
    )
    print("coonected to postgres successfully")
    return conn

conn=get_connection()
conn.close()


@app.get("/products")
def get_products():
    conn=get_connection()
    cursor=conn.cursor()
    cursor.execute("select * from products")
    rows=cursor.fetchall()
    cursor.close()
    conn.close()
    return rows

conn=get_connection()
conn.close()

@app.post("/products")
def add_product(product:Product):
    conn=get_connection()
    cursor=conn.cursor()
    cursor.execute(
        """
        INSERT INTO products (id,name,price)
        VALUES (%s,%s,%s)
        """,
        (product.id,product.name,product.price)

    )
    conn.commit()
    cursor.close()
    conn.close()

    return {
        "message":"Product added",
        "product":product
    }
conn=get_connection()
conn.close()


from fastapi import HTTPException

@app.put("/products/{product_id}")
def update_product(product_id: int, product: Product):
    conn= get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE products
        SET name = %s,
            price = %s
        WHERE id = %s
        """,
        (product.name, product.price, product_id)
    )

    if cursor.rowcount == 0:
        cursor.close()
        conn.close()
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    conn.commit()

    cursor.close()
    conn.close()

    return {
        "message": "Product updated successfully"
    }

@app.delete("/products/{product_id}")
def delete_product(product_id: int):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM products WHERE id = %s",
        (product_id,)
    )

    if cursor.rowcount == 0:
        cursor.close()
        conn.close()
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    conn.commit()

    cursor.close()
    conn.close()

    return {
        "message": "Product deleted successfully"
    }