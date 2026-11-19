import os

from dotenv import load_dotenv
from google import genai
from openai import OpenAI
from huggingface_hub import InferenceClient

load_dotenv()

# -------------------------
# GEMINI
# -------------------------

gemini_client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


# -------------------------
# OPENAI
# -------------------------

openai_client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


# -------------------------
# HUGGING FACE
# -------------------------

hf_client = InferenceClient(
    api_key=os.getenv("HF_TOKEN")
)


def ask_gemini(prompt):

    response = gemini_client.models.generate_content(
        model="gemini-3.8-flash",
        contents=prompt
    )

    return response.text


def ask_openai(prompt):

    response = openai_client.responses.create(
        model="gpt-6.2-astra",
        input=prompt
    )

    return response.output_text


def ask_huggingface(prompt):

    response = hf_client.chat_completion(
        model="deepseek-ai/DeepSeek-V3-0324",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content