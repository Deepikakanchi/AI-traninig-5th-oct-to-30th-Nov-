import json
from pathlib import Path
from langchain.tools import tool

FILE=Path(__file__).parent /"restaurants.json"

def get_restaurants():
    return json.loads(FILE.read_text())


@tool
def search_restaurants(keyword:str)->str:
    """Accept a cuisine type or restaurant keyword from the user for searching the restaurant JSON file.
Display matching restaurants with prices and available seats."""
    if not keyword.strip():
        return "Please provide a restaurant name or cuisine to search for."
    restaurants = get_restaurants()
    # cuisine = input("Enter a cuisine type or restaurant keyword: ").lower()
    search_term = keyword.strip().lower()
    matching_restaurants = [
        r for r in restaurants
        if search_term in r["name"].lower() or search_term in r["cuisine"].lower()
    ]
    if not matching_restaurants:
        return "No matching restaurants found."

    return "\n\n".join(
        f"Name: {restaurant['name']}\n"
        f"Cuisine: {restaurant['cuisine']}\n"
        f"Price: {restaurant['price_per_person']}\n"
        f"Available Seats: {restaurant['available_seats']}"
        for restaurant in matching_restaurants
    )

@tool
def calculate_dining_cost(restaurant_id: str, number_of_guests: int):
    """Accept restaurant ID and number of guests.
        Retrieve the price per person.
        Calculate and return the estimated total dining cost.
        Return an appropriate message if the restaurant doesn't exist."""
    if (
        isinstance(number_of_guests, bool)
        or not isinstance(number_of_guests, int)
        or not 1 <= number_of_guests <= 20
    ):
        return "Number of guests must be between 1 and 20."

    restaurants = get_restaurants()
    for r in restaurants:
        if r["id"] == restaurant_id:
            total_cost = r["price_per_person"] * number_of_guests
            return json.dumps({
                "restaurant_name": r["name"],
                "number_of_guests": number_of_guests,
                "price per person": r["price_per_person"],
                "total_cost": total_cost
            })
    return "Restaurant not found."


#testing the tools
if __name__ == "__main__":
    # Test search_restaurants tool
    print("Testing search_restaurants tool:")
    print(search_restaurants.invoke({"keyword":"italian"}))

    # Test calculate_dining_cost tool
    print("\nTesting calculate_dining_cost tool:")
    restaurant_id = input("Enter restaurant ID (for example R101): ").strip()
    number_of_guests = int(input("Enter number of guests: "))
    result = calculate_dining_cost.invoke({
        "restaurant_id": restaurant_id,
        "number_of_guests": number_of_guests
    })
    print(result)
