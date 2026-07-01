import ollama

def call_llm(prompt):
    response = ollama.chat(
        model="llama3.1:8b",
        messages=[{"role": "user", "content": prompt}],
        format="json",
        options={"num_ctx": 8192}
    )
    return response["message"]["content"]
