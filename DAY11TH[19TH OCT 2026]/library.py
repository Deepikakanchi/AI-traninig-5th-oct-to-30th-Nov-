# 1. Connect Python to PostgreSQL using psycopg2 .

# 2. Print:
#
# Connected to PostgreSQL successfully
#
# after the connection is established.
import psycopg2
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
app = FastAPI()

class Book(BaseModel):
    book_id:int
    title:str
    author:str
    category:str
    price:int
    stock:int
def get_connection():
    conn=psycopg2.connect(
        host="localhost",
        database="library_store",
        user="postgres",
        password="Admin@123"
    )
    print("coonected to postgres successfully")
    return conn

conn=get_connection()
conn.close()



@app.post("/books")
def add_book(book:Book):
    conn=get_connection()
    cursor=conn.cursor()
    cursor.execute(
        """
        INSERT INTO books(book_id,title,author,category,price,stock)
        VALUES (%s,%s,%s,%s,%s,%s)
        """,
        (book.book_id,book.title,book.author,book.category,book.price,book.stock)

    )
    conn.commit()
    cursor.close()
    conn.close()

    return {
        "message":"book added sucessfully",
        "book":book
    }
conn=get_connection()
conn.close()

#4. Read and display all books.

@app.get("/books")
def get_products():
    conn=get_connection()
    cursor=conn.cursor()
    cursor.execute("select * from books")
    rows=cursor.fetchall()
    cursor.close()
    conn.close()
    return rows

conn=get_connection()
conn.close()


#5. Display only books from the Technology category.

@app.get("/books/technology")
def get_technology_books():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM books WHERE category = 'Technology'")

    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    return rows

conn = get_connection()
conn.close()

#6. Display books whose price is greater than 600 .
@app.get("/books/price>600")
def get_price():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM books WHERE price > 600 ")

    rows = cursor.fetchall()

    cursor.close()
    conn.close()
    return rows

conn = get_connection()
conn.close()

# #7. Update the price of book 202 to 950 .
from fastapi import HTTPException
#
# @app.put("/books/{book_id}")
# def update_book_price(book: Book):
#     conn = get_connection()
#     cursor = conn.cursor()
#
#     cursor.execute(
#         """
#         UPDATE books
#         SET price = %s
#         WHERE book_id = %s
#         """,
#         (book.price, book.book_id)
#     )
#
#     if cursor.rowcount == 0:
#         cursor.close()
#         conn.close()
#         raise HTTPException(
#             status_code=404,
#             detail="Book not found"
#         )
#
#     conn.commit()
#
#     cursor.close()
#     conn.close()
#
#     return {
#         "message": "Book price updated successfully"
#     }

#8. Update the stock of book 204 to 14 .

@app.put("/books/{book_id}")
def update_stock(book_id: int,book: Book):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE books
        SET stock = %s
        WHERE book_id = %s
        """,
        (book.stock, book.book_id)
    )

    if cursor.rowcount == 0:
        cursor.close()
        conn.close()
        raise HTTPException(
            status_code=404,
            detail="Book not found"
        )

    conn.commit()

    cursor.close()
    conn.close()

    return {
        "message": "Book stock updated successfully"
    }


#10. Delete book 203 .
@app.delete("/books/{book_id}")
def delete_book(book_id: int):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM books WHERE book_id = %s",
        (book_id,)
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
        "message": "book deleted successfully"
    }
#11. Display all remaining books.

@app.get("/books")
def get_products():
    conn=get_connection()
    cursor=conn.cursor()
    cursor.execute("select * from books")
    rows=cursor.fetchall()
    cursor.close()
    conn.close()
    return rows

conn=get_connection()
conn.close()


# 12. Add one new book of your own choice.

# {
#     "book_id": 205,
#     "title": "Python Crash Course",
#     "author": "Eric Matthes",
#     "category": "Technology",
#     "price": 850,
#     "stock": 20
# }
@app.post("/books")
def add_book(book:Book):
    conn=get_connection()
    cursor=conn.cursor()
    cursor.execute(
        """
        INSERT INTO books(book_id,title,author,category,price,stock)
        VALUES (%s,%s,%s,%s,%s,%s)
        """,
        (book.book_id,book.title,book.author,book.category,book.price,book.stock)

    )
    conn.commit()
    cursor.close()
    conn.close()

    return {
        "message":"book added sucessfully",
        "book":book
    }
conn=get_connection()
conn.close()


# 13. Find the book with the highest price.
@app.get("/books/highest-price")
def get_highest_price_book():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM books ORDER BY price DESC LIMIT 1"
    )

    row = cursor.fetchone()

    cursor.close()
    conn.close()

    return row


# 14. Find the total stock available across all books.

@app.get("/books/total-stock")
def get_total_stock():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT SUM(stock) FROM books"
    )

    row = cursor.fetchone()

    cursor.close()
    conn.close()

    return {"total_stock": row[0]}

# 15. Count how many books exist in each category.

@app.get("/books/books_category")
def get_total_books():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT category, COUNT(*) FROM books GROUP BY category ORDER BY category "
    )

    row = cursor.fetchall()

    cursor.close()
    conn.close()

    return row