import numpy as np
import openai
import json
import os

EMBEDDING_MODEL = "text-embedding-ada-002"

open_ai_key = os.environ.get("OPENAI_API_KEY")

openai.api_key = open_ai_key

def get_embedding(text: str, model: str=EMBEDDING_MODEL) -> list[float]:
    # print(f"Getting embedding for {text}")
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

def compute_related_products_from_query(query: str) -> list[dict[str, str]]:
    """
    Compute the related products from the query.
    """
    embeddings = load_embeddings_from_json("data/embeddings.json")
    product_data = load_product_data_from_json("data/product_data.json")
    
    ordered_products = order_products_by_query_similarity(query, embeddings)
    
    # Map the ordered products to the product product_data
    return [product_data[product_name] for _, product_name in ordered_products]
