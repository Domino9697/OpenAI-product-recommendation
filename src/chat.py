from common.embeddings import compute_related_products_from_query
from common.completion import generate_ai_answer

MAX_SECTION_PRODUCTS = 3
SEPARATOR = "\n* "

def construct_prompt(user_input: str, user_labels: list[str], recommended_products: list[dict[str, str]]) -> str:
    """
    Fetch relevant 
    """
    # Take only the top MAX_SECTION_PRODUCTS products
    most_relevant_products = recommended_products[:MAX_SECTION_PRODUCTS]

    chosen_products = []
     
    for product_data in most_relevant_products:
        product_section = product_data["content"]
            
        chosen_products.append(SEPARATOR + product_section.replace("\n", "; "))
            
    chosen_products = "".join(chosen_products)
    
    prompt = f"""The following is a conversation between a personal shopper for a luxury brand in ecommerce named AI and a Human. The AI is helpful, creative, clever, and very friendly.
        The Human presents a picture that represents their preferences. The image contains the following labels:
        {user_labels}

        Human: {user_input}

        The AI searches and comes back with the following products:
        {chosen_products}

        The AI now recommends the best product to the client in the list only if the product matches the user's preferences. The AI tries to convince the client that the product matches the client's preferences by best describing the products based on these preferences.

        AI:
    """
    
    return prompt

def handler(event, _):
    print("\n========================================\n")
    user_input = event.get('prompt')
    user_labels = event.get('labels')
    print(f"Query: {user_input}")
    print(f"Labels: {user_labels}")
    print("\n========================================\n")
    print("\n=================PROMPT=================\n")

    # Build the query input
    user_query = f"{user_input} {', '.join(user_labels)}"
    most_relevant_products = compute_related_products_from_query(user_query)

    prompt = construct_prompt(user_input, user_labels, most_relevant_products)

    answer = generate_ai_answer(prompt, show_prompt=True)
    print("\n========================================\n")

    print("\n================ANSWER==================\n")
    print(answer)
    print("\n========================================\n")


if __name__ == "__main__":
    handler({
        "prompt": "I want to buy a new pair of shoes",
        "labels": ["shoe", "footwear"]
    }, None)
