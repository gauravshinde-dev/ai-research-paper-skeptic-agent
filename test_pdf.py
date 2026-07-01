from pdf_utils import extract_text

text = extract_text("sample_paper.pdf")
print(text[:1000])
print("Total length:", len(text))
