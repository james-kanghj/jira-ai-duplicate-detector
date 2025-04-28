import numpy as np
from openai import OpenAI
from config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)

def get_embedding(text):
    response = client.embeddings.create(
        model="text-embedding-ada-002",
        input=[text]
    )
    return np.array(response.data[0].embedding)