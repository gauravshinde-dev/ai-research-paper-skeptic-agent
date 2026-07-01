from pdf_utils import extract_text
from skeptic_agent import analyze_paper
import json

text = extract_text("sample_paper.pdf")
result = analyze_paper(text)
print(json.dumps(result, indent=2))
