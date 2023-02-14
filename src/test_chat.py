import time
import sys
import pandas as pd

from common.embeddings import compute_related_products_from_query
from common.completion import generate_ai_answer

MAX_SECTION_PRODUCTS = 3
SEPARATOR = "\n* "

def load_prompt_from_text_file(file_path: str) -> str:
    """
    Load a prompt from a text file
    """
    with open(file_path, "r") as f:
        prompt = f.read()
    
    return prompt

def load_user_queries_from_csv(file_path: str) -> pd.DataFrame:
    """
    Load user queries from a csv file
    """
    df = pd.read_csv(file_path)
    return df

def transform_prompt(prompt: str, user_query: str, products: str) -> str:
    """
    Replace the prompt with the user's query
    Replace the prompt with recommended products
    """

    prompt = prompt.replace("%QUERY%", user_query)
    prompt = prompt.replace("%PRODUCTS%", products)

    return prompt

def write_ai_answers_to_csv(file_path: str, ai_answers: list[dict[str, str]]):
    """
    Write the AI answers to a csv file
    """
    df = pd.DataFrame(ai_answers)
    df.to_csv(file_path, index=False)

def main(output_file: str):
    # Load the load_prompt_from_text_file
    prompt = load_prompt_from_text_file("prompt.txt")

    # Load the user queries
    df = load_user_queries_from_csv("user_queries.csv")

    # Get the user user queries
    user_queries = df["query"].tolist()

    ai_answers = []
    for user_query in user_queries:
        # Get recommended products for each user query
        recommended_products = compute_related_products_from_query(user_query)

        # Pause execution for 2 seconds to avoid hitting the API rate limit
        time.sleep(2)

        # Take only the top MAX_SECTION_PRODUCTS products
        most_relevant_products = recommended_products[:MAX_SECTION_PRODUCTS]
            
        chosen_products = []
        for product_data in most_relevant_products:
            product_section = product_data["content"]
                
            chosen_products.append(SEPARATOR + product_section.replace("\n", "; "))

        # Transform the prompt
        transformed_prompt = transform_prompt(prompt, user_query, "".join(chosen_products))

        # Generate the AI answer
        ai_answer = generate_ai_answer(transformed_prompt, show_prompt=True)
        print("=====================================\n")
        print(ai_answer)
        print("=====================================\n")
        print("\n\n")

        ai_answers.append({"query": user_query, "answer": ai_answer})

    # Write the AI answers to a csv file
    write_ai_answers_to_csv(output_file, ai_answers)

if __name__ == "__main__":
    # Get the output file path
    output_file = sys.argv[1]

    main(output_file)
