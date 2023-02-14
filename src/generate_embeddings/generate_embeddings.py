
import numpy as np
import openai
import pandas as pd
import pickle
import tiktoken
import time
import json

COMPLETIONS_MODEL = "text-davinci-003"
EMBEDDING_MODEL = "text-embedding-ada-002"

def get_embedding(text: str, model: str=EMBEDDING_MODEL) -> list[float]:
    print(f"Getting embedding for {text}")
    result = openai.Embedding.create(
      model=model,
      input=text
    )

    # Pause execution for 3 seconds to avoid hitting the API rate limit
    time.sleep(3)

    return result["data"][0]["embedding"]

def compute_doc_embeddings(df: pd.DataFrame) -> dict[str, list[float]]:
    """
    Create an embedding for each row in the dataframe using the OpenAI Embeddings API.
    
    Return a dictionary that maps between each embedding vector and the index of the row that it corresponds to.
    """

    return {
        r["product-name"]: get_embedding(r.content) for _, r in df.iterrows()
    }

def transform_product_data_to_json(df: pd.DataFrame) -> dict[str, dict[str, str]]:
    """
    Transform the product data into a dictionary that maps between the product name and the product data.
    """
    return {
        r["product-name"]: {
            "category": r.category,
            "sub-category": r["sub-category"],
            "brand": r.brand,
            "description": r.description,
            "content": r.content
        } for _, r in df.iterrows()
    }

if __name__ == "__main__":
    df = pd.read_csv("products.csv")

    # filter all empty rows and get 10 rows
    df.dropna(subset=['product-name'], inplace=True)


    # Add a column called content that regroups the title, category, description, sub-category and brand
    df["content"] = "name: " + df["product-name"] + "\n" + "category: " + df["category"] + "\n" + "sub-category: " + df["sub-category"] + "\n" + "brand: " + df["brand"] + "\n" + "description: " + df["description"]

    embeddings = compute_doc_embeddings(df)
    product_data = transform_product_data_to_json(df)

    # Save the embeddings to a JSON file
    with open("embeddings.json", "wb") as f:
        f.write(json.dumps(embeddings, indent=4).encode("utf-8"))

    # Save the product data to a JSON file
    with open("product_data.json", "wb") as f:
        f.write(json.dumps(product_data, indent=4).encode("utf-8"))
