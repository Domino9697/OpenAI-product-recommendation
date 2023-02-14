import openai
import os

open_ai_key = os.environ.get("OPENAI_API_KEY")

openai.api_key = open_ai_key

COMPLETIONS_MODEL = "text-davinci-003"
COMPLETIONS_API_PARAMS = {
    # We use temperature of 0.0 because it gives the most predictable, factual answer.
    "temperature": 0.5,
    "max_tokens": 300,
    "model": COMPLETIONS_MODEL,
}

def generate_ai_answer(
    prompt: str,
    show_prompt: bool = False
) -> str:
    if show_prompt:
        print(prompt)

    response = openai.Completion.create(
                prompt=prompt,
                **COMPLETIONS_API_PARAMS
            )

    return response["choices"][0]["text"]
