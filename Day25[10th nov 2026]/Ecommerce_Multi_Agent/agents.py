from agent_framework.openai import OpenAIChatCompletionClient

from tools import calculate_order_total, search_products


def create_inventory_agent(chat_client: OpenAIChatCompletionClient):
    """Create the agent that searches the product catalog and reports availability."""
    return chat_client.as_agent(
        name="InventoryAgent",
        description="Finds products and reports their prices and stock availability.",
        instructions=(
            "You are the Inventory Agent for an ecommerce store. "
            "Always call the search_products tool before answering. Search using "
            "the product category or name requested by the customer. Report the "
            "matching products with their IDs, names, prices, ratings, and stock "
            "counts. Do not ask for details already present in the request. "
            "Prepare a concise summary for the next agent. Do not claim that you "
            "cannot search, calculate, or recommend; leave pricing calculations "
            "to the Pricing Agent. Do not invent product information."
        ),
        default_options={"max_tokens": 2048},
        tools=[search_products],
    )


def create_pricing_agent(chat_client: OpenAIChatCompletionClient):
    """Create the agent that checks order totals, stock, and customer budgets."""
    return chat_client.as_agent(
        name="PricingAgent",
        description="Calculates order totals and identifies products within budget.",
        instructions=(
            "You are the Pricing Agent for an ecommerce store. Read the original "
            "customer request and the Inventory Agent's product matches. Extract "
            "the requested quantity and budget from the original request; do not "
            "ask again for information already provided. For each matching "
            "in-stock product, always call calculate_order_total with its product "
            "ID and the requested quantity. Treat each tool response as "
            "authoritative. Compare valid totals with the stated budget and report "
            "which products are affordable. Clearly exclude out-of-stock, "
            "insufficient-stock, and over-budget products. Ask a question only "
            "when the quantity or budget is genuinely missing or unclear. Do not "
            "invent prices, stock, or totals, and do not claim that you cannot use "
            "the pricing tool."
        ),
        default_options={"max_tokens": 2048},
        tools=[calculate_order_total],
    )


def create_recommendation_agent(chat_client: OpenAIChatCompletionClient):
    """Create the agent that recommends the best eligible product."""
    return chat_client.as_agent(
        name="RecommendationAgent",
        description="Recommends the highest-rated product that meets the customer's requirements.",
        instructions=(
            "You are the Recommendation Agent for an ecommerce store. Review the "
            "product details from the Inventory Agent and the stock, quantity, "
            "and budget results from the Pricing Agent. Only consider products "
            "that are in stock in the requested quantity and whose total cost is "
            "within the customer's budget. Recommend the eligible product with "
            "the highest rating. If ratings are equal, recommend the lower-cost "
            "product. Never recommend an unavailable or over-budget product. "
            "Give a short explanation using the product's rating and total cost. "
            "If no product meets all requirements, say so clearly instead of "
            "recommending an alternative that fails them. Do not call tools or ask "
            "the customer to repeat information already present in the conversation. "
            "Always provide a concise final answer based on the preceding agents' "
            "results. Do not invent details."
        ),
        default_options={"max_tokens": 2048},
    )
