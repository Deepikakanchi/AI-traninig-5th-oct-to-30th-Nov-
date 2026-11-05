import json
import os

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
BOOKS_FILE = os.path.join(PROJECT_DIR, "books.json")
RESERVATIONS_FILE = os.path.join(PROJECT_DIR, "reservations.json")

#HELPER FUNTION TO READ JSON 
def read_json_file(file_path):
    if not os.path.exists(file_path):
        return []
    with open(file_path, 'r') as file:
        return json.load(file)

    
#HELPER FUNCTION TO WRITE JSON
def write_json_file(file_path, data):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)


#TOOL 1:SEARCH BOOKS()
def search_books(keyword:str)->str:
    """accepts a keyword and returns a list of books that match the keyword in their title or author."""
    books = read_json_file(BOOKS_FILE)
    keyword_lower = keyword.lower()
    matches=[]

    #search for book by title,category,or author (case in sensitive)
    for book in books:
        if (keyword_lower in book['title'].lower() or
            keyword_lower in book['author'].lower() or
            keyword_lower in book['category'].lower()):
            matches.append(book)

    if not matches:
        return "No books found matching the keyword."

    return json.dumps(matches, indent=2)

#TOOL 2: RESERVE BOOK

def reserve_book(book_id:int,customer_name:str)->str:
    """accept a book id and customer name
    check availability ask for confirmation and save reservation and reduce the count.
    """
    books = read_json_file(BOOKS_FILE)
    book_to_reserve = next((b for b in books if b['id'] == book_id), None)
    if not book_to_reserve:
        return "Book not found."

    if book_to_reserve['available_copies'] <= 0:
        return "Book is not available for reservation."
    # #askk for confirmation
    # confirmation = input(f"Confirm reservation for '{book_to_reserve['title']}' by {customer_name}? (y/n): ")
    # if confirmation.lower() != 'y':
    #     return "Reservation cancelled."

    #create reservation
    reservation = {
        "book_id": book_id,
        "customer_name": customer_name
    }
    reservations = read_json_file(RESERVATIONS_FILE)
    reservations.append(reservation)
    write_json_file(RESERVATIONS_FILE, reservations)

    #reduce available copies
    book_to_reserve['available_copies'] -= 1
    write_json_file(BOOKS_FILE, books)

    return f"Reservation successful for '{book_to_reserve['title']}' by {customer_name}."