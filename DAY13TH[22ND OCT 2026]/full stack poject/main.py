#
# import psycopg2
# from fastapi import FastAPI,HTTPException
# from fastapi.middleware.cors import CORSMiddleware
#
# from pydantic import BaseModel
#
# app = FastAPI()
#
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["http://localhost:5173"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )
#
# #5th step
# def get_connection():
#
#     return psycopg2.connect(
#         host="localhost",
#         database="product_store",
#         user="postgres",
#         password="Admin@123"
# )
#
# # if __name__ == "__main__":
# #     try:
# #         connection = get_connection()
# #         print("Connected to PostgreSQL database")
# #         connection.close()
# #     except Exception as e:
# #         print(e)
#
# class Product(BaseModel):
#     name: str
#     price: float
#     image: str
# #6step
# @app.get("/products")
# def get_products():
#     conn = get_connection()
#     cursor = conn.cursor()
#     cursor.execute("""
#     SELECT id, name, price, image
#     FROM products
#     ORDER BY id
#     """)
#     rows = cursor.fetchall()
#     cursor.close()
#     conn.close()
#     products = []
#     for row in rows:
#         products.append({
#             "id": row[0],
#             "name": row[1],
#             "price": float(row[2]),
#             "image": row[3]
#         })
#     return products
#
# #7. POST should insert into PostgreSQL
# @app.post("/products")
# def add_product(product: Product):
#     conn = get_connection()
#     cursor = conn.cursor()
#
#     cursor.execute(
#         """
#         INSERT INTO products (name, price, image)
#         VALUES (%s, %s, %s)
#         RETURNING id
#         """,
#      (product.name, product.price, product.image)
#     )
#
#     product_id = cursor.fetchone()[0]
#
#     conn.commit()
#
#     cursor.close()
#     conn.close()
#
#     return {
#         "message": "Product added successfully",
#         "id": product_id
#     }
#
#
# @app.put("/products/{product_id}")
# def update_product(
#         product_id: int,
#         updated_product: Product
# ):
#     conn = get_connection()
#     cursor = conn.cursor()
#
#     cursor.execute(
#         """
#         UPDATE products
#         SET name=%s,
#             price=%s,
#             image=%s
#         WHERE id=%s
#         """,
#         (
#             updated_product.name,
#             updated_product.price,
#             updated_product.image,
#             product_id
#         )
#     )
#
#     if cursor.rowcount == 0:
#         cursor.close()
#         conn.close()
#
#         raise HTTPException(
#             status_code=404,
#             detail="Product not found"
#         )
#
#     conn.commit()
#
#     cursor.close()
#     conn.close()
#
#     return {
#         "message": "Product updated successfully",
#         "product": updated_product
#     }
#
#
# @app.delete("/products/{product_id}")
# def delete_product(product_id: int):
#     conn = get_connection()
#     cursor = conn.cursor()
#
#     cursor.execute(
#         "DELETE FROM products WHERE id = %s",
#         (product_id,)
#     )
#
#     if cursor.rowcount == 0:
#         cursor.close()
#         conn.close()
#
#         raise HTTPException(
#             status_code=404,
#             detail="Product not found"
#         )
#
#     conn.commit()
#
#     cursor.close()
#     conn.close()
#
#     return {
#         "message": "Product deleted successfully"
#     }

import psycopg2
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

# Configure CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Database Connection Utility
def get_connection():
    return psycopg2.connect(
        host="localhost",
        database="product_store",
        user="postgres",
        password="Admin@123"
    )


# Pydantic Model for Data Validation
class Product(BaseModel):
    name: str
    price: float
    image: str


# 1. GET all products
@app.get("/products")
def get_products():
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, name, price, image
            FROM products
            ORDER BY id
        """)
        rows = cursor.fetchall()

        products = []
        for row in rows:
            products.append({
                "id": row[0],
                "name": row[1],
                "price": float(row[2]),
                "image": row[3]
            })
        return products
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


# 2. POST (Create) a product
@app.post("/products")
def add_product(product: Product):
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO products (name, price, image)
            VALUES (%s, %s, %s)
            RETURNING id
            """,
            (product.name, product.price, product.image)
        )

        result = cursor.fetchone()
        if result is None:
            raise HTTPException(status_code=500, detail="Failed to insert product.")

        product_id = result[0]
        conn.commit()

        return {
            "message": "Product added successfully",
            "id": product_id
        }
    except Exception as e:
        if conn:
            conn.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


# 3. PUT (Update) a product
@app.put("/products/{product_id}")
def update_product(product_id: int, updated_product: Product):
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            UPDATE products
            SET name=%s,
                price=%s,
                image=%s
            WHERE id=%s
            """,
            (
                updated_product.name,
                updated_product.price,
                updated_product.image,
                product_id
            )
        )

        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Product not found")

        conn.commit()
        return {
            "message": "Product updated successfully",
            "product": updated_product
        }
    except HTTPException:
        raise  # Re-raise the 404 exception directly
    except Exception as e:
        if conn:
            conn.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


# 4. DELETE a product
@app.delete("/products/{product_id}")
def delete_product(product_id: int):
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "DELETE FROM products WHERE id = %s",
            (product_id,)
        )

        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Product not found")

        conn.commit()
        return {"message": "Product deleted successfully"}
    except HTTPException:
        raise  # Re-raise the 404 exception directly
    except Exception as e:
        if conn:
            conn.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
