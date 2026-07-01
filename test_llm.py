from llm_client import call_llm

result = call_llm('Return JSON with one field: {"status": "ok"}')
print(result)
