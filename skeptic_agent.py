import json
from llm_client import call_llm

PROMPT = """You are a skeptical research reviewer. Analyze the given paper critically.

Return ONLY valid JSON with this exact structure:
{{
  "main_claim": "the central argument of the paper in one sentence",
  "method_summary": "how they tested or proved their claim",
  "evidence_for_claims": [
    {{
      "claim": "a specific claim made in the paper",
      "evidence_found": "exact supporting text or method from the paper",
      "evidence_strength": "strong or moderate or weak or none"
    }}
  ],
  "limitations": ["limitation 1", "limitation 2"],
  "questions_to_ask": ["critical question 1", "critical question 2"],
  "unsupported_claims": ["any claim made without clear evidence in the text"]
}}

Rules:
- Do not invent evidence not in the text
- If a claim has no evidence, add it to unsupported_claims
- Be specific, reference actual details from the paper
- Return ONLY JSON, no extra text

Paper text:
{paper_text}"""

def analyze_paper(paper_text):
    if len(paper_text) > 8000:
        paper_text = paper_text[:8000]
    prompt = PROMPT.format(paper_text=paper_text)
    response = call_llm(prompt)
    try:
        return json.loads(response)
    except json.JSONDecodeError:
        return {{"error": "Could not parse output", "raw": response}}
