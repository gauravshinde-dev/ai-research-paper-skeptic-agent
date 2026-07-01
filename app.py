import streamlit as st
from pdf_utils import extract_text
from skeptic_agent import analyze_paper
import json
import datetime

st.set_page_config(page_title="Research Paper Skeptic Agent", page_icon="🔍")
st.title("🔍 AI Research Paper Skeptic Agent")
st.caption("Upload a research paper and get a critical skeptical review powered by local LLM.")

uploaded = st.file_uploader("Upload a research paper (PDF)", type="pdf")

if uploaded:
    if st.button("Analyze Paper"):
        with open("temp.pdf", "wb") as f:
            f.write(uploaded.read())
        text = extract_text("temp.pdf")
        with st.spinner("Analyzing paper... this may take 30-60 seconds..."):
            result = analyze_paper(text)

        if "error" in result:
            st.error("Could not parse model output.")
            st.text(result.get("raw", ""))
        else:
            st.success("Analysis complete!")

            st.subheader("📌 Main Claim")
            st.info(result["main_claim"])

            st.subheader("🔬 Method Summary")
            st.write(result["method_summary"])

            st.subheader("📊 Evidence for Claims")
            for e in result["evidence_for_claims"]:
                with st.expander(f"Claim: {e['claim'][:80]}..."):
                    st.write(f"**Evidence:** {e['evidence_found']}")
                    color = "green" if e["evidence_strength"] == "strong" else "orange" if e["evidence_strength"] == "moderate" else "red"
                    st.markdown(f"**Strength:** :{color}[{e['evidence_strength']}]")

            st.subheader("⚠️ Limitations")
            for l in result["limitations"]:
                st.warning(l)

            st.subheader("❓ Questions to Ask")
            for q in result["questions_to_ask"]:
                st.write(f"- {q}")

            if result["unsupported_claims"]:
                st.subheader("🚨 Unsupported Claims")
                for u in result["unsupported_claims"]:
                    st.error(u)
            else:
                st.subheader("🚨 Unsupported Claims")
                st.success("No unsupported claims detected.")

            log_entry = {"timestamp": str(datetime.datetime.now()), "filename": uploaded.name, "result": result}
            with open("logs.json", "a") as f:
                f.write(json.dumps(log_entry) + "\n")
            st.caption("Run logged to logs.json")
