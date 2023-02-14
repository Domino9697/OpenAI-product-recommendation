

import numpy as np
import openai
import tiktoken
import json

COMPLETIONS_MODEL = "text-davinci-003"
EMBEDDING_MODEL = "text-embedding-ada-002"

MAX_SECTION_PRODUCTS = 3
SEPARATOR = "\n* "
ENCODING = "cl100k_base"  # encoding for text-embedding-ada-002

COMPLETIONS_API_PARAMS = {
    # We use temperature of 0.0 because it gives the most predictable, factual answer.
    "temperature": 0.5,
    "max_tokens": 300,
    "model": COMPLETIONS_MODEL,
}

encoding = tiktoken.get_encoding(ENCODING)
separator_len = len(encoding.encode(SEPARATOR))

def get_embedding(text: str, model: str=EMBEDDING_MODEL) -> list[float]:
    print(f"Getting embedding for {text}")
    result = openai.Embedding.create(
      model=model,
      input=text
    )

    return result["data"][0]["embedding"]

def vector_similarity(x: list[float], y: list[float]) -> float:
    """
    Returns the similarity between two vectors.
    
    Because OpenAI Embeddings are normalized to length 1, the cosine similarity is the same as the dot product.
    """
    return np.dot(np.array(x), np.array(y))

def order_products_by_query_similarity(query: str, contexts: dict[str, np.array]) -> list[tuple[float, str]]:
    """
    Find the query embedding for the supplied query, and compare it against all of the pre-calculated document embeddings
    to find the most relevant sections. 
    
    Return the list of document sections, sorted by relevance in descending order.
    """
    query_embedding = get_embedding(query)
    
    document_similarities = sorted([
        (vector_similarity(query_embedding, doc_embedding), doc_name) for doc_name, doc_embedding in contexts.items()
    ], reverse=True)
    
    return document_similarities

def load_embeddings_from_json(json_file: str) -> dict[str, np.array]:
    """
    Load the embeddings from the JSON file and transform them into numpy arrays.
    """
    with open(json_file, "rb") as f:
        embeddings = json.loads(f.read().decode("utf-8"))

        # transform all of the embeddings into numpy arrays
        embeddings = {k: np.array(v) for k, v in embeddings.items()}
        
        return embeddings

def load_product_data_from_json(json_file: str) -> dict[str, dict[str, str]]:
    """
    Load the product data from the JSON file.
    """
    with open(json_file, "rb") as f:
        product_data = json.loads(f.read().decode("utf-8"))
        
        return product_data

def construct_prompt(user_input: str, context_embeddings: dict, product_data: dict[str, dict[str, str]]) -> str:
    """
    Fetch relevant 
    """
    most_relevant_products = order_products_by_query_similarity(user_input, context_embeddings)
    
    # Take only the top MAX_SECTION_PRODUCTS products
    most_relevant_products = most_relevant_products[:MAX_SECTION_PRODUCTS]

    chosen_products = []
    chosen_product_names = []
     
    for _, product_name in most_relevant_products:
        print(f"Adding product {product_name}")
        product_section = product_data[product_name]["content"]
        print(f"Product section: {product_section}")
            
        chosen_product_names.append(product_name)
        chosen_products.append(SEPARATOR + product_section.replace("\n", "; "))
            
    # Useful diagnostic information
    print(f"Selected {len(chosen_products)} document sections:")
    print("\n".join(chosen_product_names))

    chosen_products = "".join(chosen_products)
    
    prompt = f"""The following is a conversation between a personal shopper for a luxury brand in ecommerce named AI and a Human. The AI is helpful, creative, clever, and very friendly.
        Human: {user_input}

        The AI searches and comes back with the following products:
        {chosen_products}

        The AI now recommends the best product to the client in the list only if the product matches the user's preferences. The AI tries to convince the client that the product matches the client's preferences by best describing the products based on these preferences.

        AI:
    """
    
    return prompt

def answer_query_with_context(
    query: str,
    product_data: dict[str, dict[str, str]],
    product_embeddings: dict,
    show_prompt: bool = False
) -> str:
    prompt = construct_prompt(
        query,
        product_embeddings,
        product_data
    )
    
    if show_prompt:
        print(prompt)

    response = openai.Completion.create(
                prompt=prompt,
                **COMPLETIONS_API_PARAMS
            )

    return response["choices"][0]["text"]

if __name__ == "__main__":
    embeddings = load_embeddings_from_json("embeddings.json")
    # order the document sections by similarity to the query
    query = "I am someone who loves walking in the street."

    product_data = load_product_data_from_json("product_data.json")

    answer = answer_query_with_context(query, product_data, embeddings, show_prompt=True)

    print(answer)
