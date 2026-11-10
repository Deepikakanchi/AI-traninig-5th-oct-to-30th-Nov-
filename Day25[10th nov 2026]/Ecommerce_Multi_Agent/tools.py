import json
import re
from pathlib import Path
from agent_framework import tool


def _format_inr(amount: int) -> str:
    return f"₹{_format_indian_grouping(str(amount))}"


def _format_indian_grouping(digits: str) -> str:
    if len(digits) <= 3:
        return digits
    groups = [digits[-3:]]
    digits = digits[:-3]
    while digits:
        groups.append(digits[-2:])
        digits = digits[:-2]
    return ",".join(reversed(groups))


def build_customer_report(customer_request: str) -> str:
    """Build a factual inventory, pricing, and recommendation report."""
    request = customer_request.casefold()
    products = get_products_data()

    requested_category = next(
        (
            product["category"]
            for product in products
            if re.search(
                rf"\b{re.escape(product['category'].casefold().rstrip('s'))}s?\b",
                request,
            )
        ),
        None,
    )
    matching_products = [
        product for product in products
        if requested_category is not None
        and product["category"].casefold() == requested_category.casefold()
    ]

    quantity_match = re.search(
        r"\b(\d+)\s+(?:of\s+)?(?:units?|pieces?|pcs?|laptops?|smartphones?|phones?|"
        r"tablets?|monitors?|headphones?|printers?|keyboards?|mice|mouses?)\b",
        request,
    )
    quantity = int(quantity_match.group(1)) if quantity_match else None

    budget_match = re.search(
        r"(?:₹|INR\b|Rs\.?)\s*([\d,]+)",
        customer_request,
        re.IGNORECASE,
    )
    if budget_match is None:
        budget_match = re.search(
            r"\bbudget\b[^\d]{0,20}([\d,]+)",
            customer_request,
            re.IGNORECASE,
        )
    budget = (
        int(budget_match.group(1).replace(",", ""))
        if budget_match
        else None
    )

    lines = ["--- Inventory Agent ---"]
    if requested_category is None:
        lines.append("Could not identify a product category in the request.")
    elif not matching_products:
        lines.append(f"No products found in category: {requested_category}.")
    else:
        lines.append(f"Matching products ({requested_category}):")
        for product in matching_products:
            lines.append(
                f"- {product['id']} | {product['name']} | "
                f"Price: {_format_inr(product['price_inr'])} | "
                f"Available stock: {product['stock']} | Rating: {product['rating']}/5"
            )

    lines.append("\n--- Pricing Agent ---")
    if quantity is None:
        lines.append("Quantity requested: not specified.")
    else:
        lines.append(f"Quantity requested: {quantity} per product.")
    if budget is None:
        lines.append("Budget: not specified.")
    else:
        lines.append(f"Budget: {_format_inr(budget)}.")

    eligible_products: list[tuple[dict, int]] = []
    if quantity is not None and budget is not None:
        for product in matching_products:
            total = product["price_inr"] * quantity
            affordable = product["stock"] >= quantity and total <= budget
            if affordable:
                eligible_products.append((product, total))
            status = (
                "Within budget"
                if affordable
                else (
                    "Insufficient stock"
                    if product["stock"] < quantity
                    else "Over budget"
                )
            )
            lines.append(
                f"- Product ID: {product['id']} | Quantity: {quantity} | "
                f"Calculated total: {_format_inr(total)} | Budget validation: {status}"
            )
        selected_ids = ", ".join(
            product["id"] for product, _ in eligible_products
        )
        lines.append(
            f"Selected product IDs within budget: {selected_ids or 'None'}."
        )
    else:
        lines.append("Budget validation requires both a quantity and a budget.")

    lines.append("\n--- Recommendation Agent ---")
    if quantity is None or budget is None:
        lines.append("Cannot recommend yet; provide the missing quantity or budget.")
    elif not eligible_products:
        lines.append("No in-stock product meets the requested quantity and budget.")
    else:
        product, total = max(
            eligible_products,
            key=lambda item: (item[0]["rating"], -item[1]),
        )
        lines.extend(
            [
                f"Recommended product: {product['name']} (ID: {product['id']})",
                f"Price and quantity: {_format_inr(product['price_inr'])} x "
                f"{quantity} = {_format_inr(total)}",
                f"Customer rating: {product['rating']}/5",
                "Reason: Highest-rated product that is in stock and within budget.",
            ]
        )

    return "\n".join(lines)


def get_products_data():
    file_path = Path(__file__).parent / "products.json"
    with open(file_path, "r") as file:
        return json.load(file)


@tool
def search_products(query: str) -> str:
    """Find products by name or category."""
    query = query.strip().casefold()

    if not query:
        return "Please enter a product name or category."

    matches = []

    for product in get_products_data():
        if query in product["name"].casefold() or query in product["category"].casefold():
            matches.append(
                f"ID: {product['id']}, Name: {product['name']}, "
                f"Price: INR {product['price_inr']}, Stock: {product['stock']}, "
                f"Rating: {product['rating']}"
            )

    if not matches:
        return f"No products found for '{query}'."

    return "\n".join(matches)


@tool
def calculate_order_total(product_id: str, quantity: int) -> str:
    """Calculate an order total when enough stock is available."""
    if not isinstance(quantity, int) or isinstance(quantity, bool) or quantity <= 0:
        return "Quantity must be a positive whole number."

    for product in get_products_data():
        if product["id"].casefold() == product_id.strip().casefold():
            if quantity > product["stock"]:
                return (
                    f"Only {product['stock']} units of {product['name']} are in stock; "
                    f"you requested {quantity}."
                )

            total = product["price_inr"] * quantity
            return f"Total for {quantity} x {product['name']}: INR {total}."

    return f"No product found with ID '{product_id}'."


if __name__ == "__main__":
    print("Search by category:")
    print(search_products.func("Laptop"))

    print("\nSearch with no matches:")
    print(search_products.func("Unknown product"))

    print("\nCalculate a valid order:")
    print(calculate_order_total.func("P101", 2))

    print("\nCheck insufficient stock:")
    print(calculate_order_total.func("P101", 100))

    print("\nCheck invalid quantity:")
    print(calculate_order_total.func("P101", 0))

    print("\nCheck unknown product ID:")
    print(calculate_order_total.func("P999", 1))