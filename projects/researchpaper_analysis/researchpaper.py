"""
InsightEngine Pro — Multimodal Research Auditor
Run with: streamlit run app.py
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json
import io
import re
import time
import random
import hashlib
from datetime import datetime

# ── Page config (MUST be first Streamlit call) ──────────────────────────────
st.set_page_config(
    layout="wide",
    page_title="InsightEngine Pro",
    page_icon="🔬",
    initial_sidebar_state="expanded",
)

# ── Inject custom CSS ────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Syne:wght@400;600;700;800&family=Inter:wght@300;400;500&display=swap');

:root {
  --bg:         #0a0c14;
  --surface:    #111420;
  --surface2:   #181c2e;
  --border:     #252a40;
  --accent:     #5b8af0;
  --accent2:    #a78bfa;
  --accent3:    #34d399;
  --warn:       #f59e0b;
  --danger:     #f87171;
  --text:       #e2e8f0;
  --muted:      #64748b;
  --mono:       'Space Mono', monospace;
  --sans:       'Syne', sans-serif;
  --body:       'Inter', sans-serif;
}

html, body, [data-testid="stApp"] {
  background: var(--bg) !important;
  color: var(--text) !important;
  font-family: var(--body);
}

/* Hide Streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }
[data-testid="stDecoration"] { display: none; }

/* Custom scrollbar */
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: var(--bg); }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 2px; }

/* ── Hero banner ── */
.hero {
  background: linear-gradient(135deg, #0d1117 0%, #131929 50%, #0d1117 100%);
  border: 1px solid var(--border);
  border-radius: 16px;
  padding: 28px 36px;
  margin-bottom: 24px;
  position: relative;
  overflow: hidden;
}
.hero::before {
  content: '';
  position: absolute;
  top: -60px; right: -60px;
  width: 220px; height: 220px;
  background: radial-gradient(circle, rgba(91,138,240,0.15) 0%, transparent 70%);
  border-radius: 50%;
}
.hero-title {
  font-family: var(--sans);
  font-size: 2.1rem;
  font-weight: 800;
  background: linear-gradient(90deg, #5b8af0, #a78bfa, #34d399);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  margin: 0 0 6px 0;
  letter-spacing: -0.5px;
}
.hero-sub {
  font-family: var(--mono);
  font-size: 0.72rem;
  color: var(--muted);
  letter-spacing: 2px;
  text-transform: uppercase;
}

/* ── Metric cards ── */
.metric-row { display: flex; gap: 12px; margin: 16px 0; }
.metric-card {
  flex: 1;
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 16px 20px;
  position: relative;
}
.metric-card .label {
  font-family: var(--mono);
  font-size: 0.62rem;
  color: var(--muted);
  letter-spacing: 1.5px;
  text-transform: uppercase;
  margin-bottom: 8px;
}
.metric-card .value {
  font-family: var(--sans);
  font-size: 1.8rem;
  font-weight: 700;
  color: var(--text);
}
.metric-card .badge {
  position: absolute;
  top: 14px; right: 14px;
  font-size: 1.2rem;
}
.metric-card .delta {
  font-size: 0.72rem;
  color: var(--accent3);
  margin-top: 4px;
}

/* ── Section headers ── */
.section-head {
  font-family: var(--sans);
  font-size: 1rem;
  font-weight: 700;
  color: var(--text);
  letter-spacing: 0.3px;
  margin: 20px 0 12px 0;
  display: flex;
  align-items: center;
  gap: 8px;
}
.section-head::after {
  content: '';
  flex: 1;
  height: 1px;
  background: var(--border);
}

/* ── Claim cards ── */
.claim-card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-left: 3px solid;
  border-radius: 8px;
  padding: 14px 18px;
  margin-bottom: 10px;
  transition: border-color 0.2s;
}
.claim-strong  { border-left-color: #34d399; }
.claim-moderate { border-left-color: #f59e0b; }
.claim-weak    { border-left-color: #f87171; }
.claim-title {
  font-family: var(--mono);
  font-size: 0.8rem;
  color: var(--text);
  margin-bottom: 6px;
}
.claim-meta {
  font-size: 0.72rem;
  color: var(--muted);
}

/* ── Reference pill ── */
.ref-pill {
  display: inline-block;
  background: var(--surface2);
  border: 1px solid var(--border);
  border-radius: 20px;
  padding: 4px 12px;
  font-family: var(--mono);
  font-size: 0.68rem;
  color: var(--muted);
  margin: 3px;
}
.ref-fresh { border-color: #34d399; color: #34d399; }
.ref-mid   { border-color: #f59e0b; color: #f59e0b; }
.ref-stale { border-color: #f87171; color: #f87171; }

/* ── Chat bubble ── */
.chat-user {
  background: var(--accent);
  color: #fff;
  padding: 10px 16px;
  border-radius: 16px 16px 4px 16px;
  margin: 8px 0 8px 40px;
  font-size: 0.85rem;
}
.chat-ai {
  background: var(--surface2);
  border: 1px solid var(--border);
  color: var(--text);
  padding: 10px 16px;
  border-radius: 16px 16px 16px 4px;
  margin: 8px 40px 8px 0;
  font-size: 0.85rem;
  line-height: 1.55;
}
.chat-label {
  font-family: var(--mono);
  font-size: 0.6rem;
  color: var(--muted);
  letter-spacing: 1px;
  text-transform: uppercase;
  margin-bottom: 4px;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
  background: var(--surface) !important;
  border-right: 1px solid var(--border) !important;
}
[data-testid="stSidebar"] * { color: var(--text) !important; }

/* ── Tab styling ── */
[data-testid="stTabs"] [role="tab"] {
  font-family: var(--mono) !important;
  font-size: 0.75rem !important;
  letter-spacing: 0.5px;
}

/* ── Streamlit elements override ── */
.stButton > button {
  background: var(--surface2) !important;
  border: 1px solid var(--border) !important;
  color: var(--text) !important;
  font-family: var(--mono) !important;
  font-size: 0.72rem !important;
  border-radius: 6px !important;
  transition: border-color 0.2s, background 0.2s !important;
}
.stButton > button:hover {
  border-color: var(--accent) !important;
  background: rgba(91,138,240,0.1) !important;
}
.stTextInput input, .stTextArea textarea {
  background: var(--surface2) !important;
  border: 1px solid var(--border) !important;
  color: var(--text) !important;
  font-family: var(--body) !important;
  border-radius: 8px !important;
}
div[data-testid="stAlert"] {
  background: var(--surface2) !important;
  border: 1px solid var(--border) !important;
  border-radius: 8px !important;
}
.stProgress > div > div {
  background: linear-gradient(90deg, var(--accent), var(--accent2)) !important;
}

/* ── Barcode container ── */
.barcode-wrap {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 10px;
  padding: 16px;
  margin: 12px 0;
}
.barcode-label {
  font-family: var(--mono);
  font-size: 0.62rem;
  color: var(--muted);
  letter-spacing: 2px;
  text-transform: uppercase;
  margin-bottom: 10px;
}

/* ── Status badge ── */
.badge {
  display: inline-block;
  padding: 2px 10px;
  border-radius: 20px;
  font-family: var(--mono);
  font-size: 0.65rem;
  letter-spacing: 0.5px;
}
.badge-green { background: rgba(52,211,153,0.15); color: #34d399; border: 1px solid rgba(52,211,153,0.3); }
.badge-yellow { background: rgba(245,158,11,0.15); color: #f59e0b; border: 1px solid rgba(245,158,11,0.3); }
.badge-red { background: rgba(248,113,113,0.15); color: #f87171; border: 1px solid rgba(248,113,113,0.3); }
.badge-blue { background: rgba(91,138,240,0.15); color: #5b8af0; border: 1px solid rgba(91,138,240,0.3); }

/* ── Knowledge graph placeholder ── */
.kg-node {
  display: inline-block;
  background: var(--surface2);
  border: 1px solid var(--accent);
  border-radius: 20px;
  padding: 5px 14px;
  font-family: var(--mono);
  font-size: 0.7rem;
  color: var(--accent);
  margin: 4px;
}
.kg-edge {
  font-family: var(--mono);
  font-size: 0.65rem;
  color: var(--muted);
  padding: 2px 8px;
}

/* ── Fingerprint / hash display ── */
.fingerprint {
  font-family: var(--mono);
  font-size: 0.65rem;
  color: var(--accent3);
  letter-spacing: 1px;
  word-break: break-all;
  background: var(--surface2);
  border: 1px solid var(--border);
  border-radius: 6px;
  padding: 8px 12px;
  margin-top: 8px;
}

/* ── Timeline ── */
.timeline-item {
  display: flex;
  gap: 14px;
  margin-bottom: 14px;
  align-items: flex-start;
}
.timeline-dot {
  width: 10px; height: 10px;
  border-radius: 50%;
  background: var(--accent);
  margin-top: 4px;
  flex-shrink: 0;
}
.timeline-content { flex: 1; }
.timeline-date {
  font-family: var(--mono);
  font-size: 0.65rem;
  color: var(--muted);
}
.timeline-text { font-size: 0.82rem; color: var(--text); }
</style>
""", unsafe_allow_html=True)

# ── Session state init ────────────────────────────────────────────────────────
for key, default in {
    "target_page": 1,
    "analysis_done": False,
    "chat_history": [],
    "paper_data": None,
    "api_key": "",
}.items():
    if key not in st.session_state:
        st.session_state[key] = default

# ── Helpers ──────────────────────────────────────────────────────────────────

def get_llm(api_key: str):
    from langchain_openai import ChatOpenAI
    return ChatOpenAI(model="gpt-4o-mini", temperature=0.3, api_key=api_key)


def call_claude(prompt: str, api_key: str) -> str:
    try:
        llm = get_llm(api_key)
        from langchain_core.messages import HumanMessage
        resp = llm.invoke([HumanMessage(content=prompt)])
        return resp.content
    except Exception as e:
        return f"[API Error: {e}]"


def analyze_pdf_locally(paper_text: str) -> dict:
    """Analyze uploaded PDF text locally without any API key."""
    import re as _re

    lines = [l.strip() for l in paper_text.splitlines() if l.strip()]
    words = paper_text.split()

    # Title: first non-trivial line
    title = next((l for l in lines if len(l) > 10), "Untitled Paper")

    # Abstract: text after 'abstract' keyword
    abstract_match = _re.search(r'abstract[:\s]+(.{100,600})', paper_text, _re.IGNORECASE | _re.DOTALL)
    abstract_summary = abstract_match.group(1).replace('\n', ' ').strip()[:400] if abstract_match else " ".join(words[:80])

    # Key sentences (highlights) — sentences with numbers/results
    sentences = _re.split(r'(?<=[.!?])\s+', paper_text.replace('\n', ' '))
    result_sents = [s.strip() for s in sentences if _re.search(r'\d+\.?\d*\s*(%|accuracy|result|achieve|outperform|propose|novel|improve)', s, _re.IGNORECASE) and 20 < len(s) < 300]

    # Claims from result sentences
    claims = []
    for s in result_sents[:6]:
        strength = "Strong" if _re.search(r'\d+\.\d+%|p\s*<|significant', s, _re.IGNORECASE) else "Moderate"
        claims.append({"text": s[:120], "page_hint": 1, "strength": strength, "rationale": "Extracted from paper text"})
    if not claims:
        claims = [{"text": s[:120], "page_hint": 1, "strength": "Moderate", "rationale": "Extracted from paper text"} for s in sentences[2:6] if len(s) > 30]

    # Key contributions — sentences with 'propose', 'introduce', 'present', 'novel'
    contrib_sents = [s.strip() for s in sentences if _re.search(r'\b(propose|introduce|present|novel|contribution|we develop|we design)', s, _re.IGNORECASE) and 20 < len(s) < 250]
    key_contributions = list(dict.fromkeys(contrib_sents[:4])) or ["See full paper for contributions."]

    # Limitations
    lim_match = _re.search(r'(limitation|future work|drawback|constraint)[s]?[:\s]+(.{30,500})', paper_text, _re.IGNORECASE | _re.DOTALL)
    limitations = []
    if lim_match:
        lim_text = lim_match.group(2).replace('\n', ' ').strip()
        limitations = [s.strip() for s in _re.split(r'[.;]', lim_text) if len(s.strip()) > 20][:4]
    if not limitations:
        limitations = ["Limitations not explicitly stated in the extracted text."]

    # Methodology keywords
    method_keywords = ["dataset", "model", "training", "evaluation", "experiment", "baseline", "architecture", "preprocessing"]
    method_counts = {k.title(): max(1, len(_re.findall(k, paper_text, _re.IGNORECASE))) for k in method_keywords}
    top_methods = sorted(method_counts.items(), key=lambda x: -x[1])[:5]
    total_m = sum(v for _, v in top_methods)
    methodology_breakdown = {
        "labels": [k for k, _ in top_methods],
        "values": [round(v / total_m * 100) for _, v in top_methods]
    }

    # Sentiment barcode — simple keyword scan per sentence chunk
    pos_words = set(["improve","achieve","outperform","novel","effective","accurate","significant","better","superior","robust"])
    neg_words = set(["limitation","fail","error","drawback","challenge","difficult","poor","lack","issue","problem"])
    chunks = sentences[:30]
    barcode = []
    for s in chunks:
        sl = s.lower()
        if any(w in sl for w in pos_words): barcode.append("positive")
        elif any(w in sl for w in neg_words): barcode.append("negative")
        else: barcode.append("objective")
    barcode = (barcode + ["objective"] * 30)[:30]

    # References — find year patterns near author-like text
    ref_matches = _re.findall(r'([A-Z][a-z]+(?:\s+(?:et al\.?|and|&)\s+[A-Z][a-z]+)?)[,\s]+\(?([12][0-9]{3})\)?', paper_text)
    references = []
    seen = set()
    for citation, year in ref_matches[:8]:
        key = citation.strip()
        if key not in seen:
            seen.add(key)
            yr = int(year)
            age = datetime.now().year - yr
            references.append({"citation": key, "year": yr, "journal": "Unknown", "impact": "High" if age <= 5 else "Medium" if age <= 12 else "Low"})
    if not references:
        references = [{"citation": "References not parsed", "year": 2020, "journal": "Unknown", "impact": "Unknown"}]

    # Scores based on content signals
    evidence_score = min(100, 40 + len(result_sents) * 8)
    novelty_score  = min(100, 30 + len(contrib_sents) * 12)
    repro_score    = min(100, 30 + len(_re.findall(r'\b(code|github|dataset|available|open.source|reproduce)', paper_text, _re.IGNORECASE)) * 10)

    # Entities
    entity_patterns = [
        (r'\b([A-Z][a-zA-Z]+-?[0-9]*)\b', "Method"),
        (r'\b(dataset|corpus|benchmark)\b', "Dataset"),
    ]
    entities = []
    seen_ents = set()
    for pat, etype in entity_patterns:
        for m in _re.finditer(pat, paper_text):
            e = m.group(1)
            if e not in seen_ents and len(e) > 3:
                seen_ents.add(e)
                entities.append({"entity": e, "type": etype})
            if len(entities) >= 8: break
        if len(entities) >= 8: break

    return {
        "title": title,
        "abstract_summary": abstract_summary,
        "evidence_strength_score": evidence_score,
        "evidence_rationale": f"Extracted {len(result_sents)} result-bearing sentences from the paper.",
        "methodology_breakdown": methodology_breakdown,
        "sentiment_barcode": barcode,
        "claims": claims,
        "entities": entities or [{"entity": "N/A", "type": "Other"}],
        "relationships": [],
        "references": references,
        "conflict_of_interest": None,
        "mermaid_flowchart": "graph LR; A[Input] --> B[Model] --> C[Output]",
        "limitations": limitations,
        "novelty_score": novelty_score,
        "reproducibility_score": repro_score,
        "key_contributions": key_contributions,
    }


def answer_from_paper(question: str, paper_text: str) -> str:
    """Search paper text for sentences relevant to the question (no API needed)."""
    import re as _re
    q_words = set(_re.findall(r'\b\w{4,}\b', question.lower()))
    sentences = _re.split(r'(?<=[.!?])\s+', paper_text.replace('\n', ' '))
    scored = []
    for s in sentences:
        sl = s.lower()
        score = sum(1 for w in q_words if w in sl)
        if score > 0 and 30 < len(s) < 400:
            scored.append((score, s.strip()))
    scored.sort(key=lambda x: -x[0])
    top = [s for _, s in scored[:4]]
    if top:
        return "Based on the paper:\n\n" + "\n\n".join(f"• {s}" for s in top)
    return "Could not find a relevant answer in the paper text for that question."


def extract_json(text: str) -> dict | list | None:
    """Pull first JSON block out of a string."""
    match = re.search(r"```json\s*([\s\S]+?)\s*```", text)
    if match:
        text = match.group(1)
    try:
        return json.loads(text)
    except Exception:
        return None


def paper_hash(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def color_for_strength(s: str) -> str:
    s = s.lower()
    if "strong" in s:   return "claim-strong"
    if "moderate" in s: return "claim-moderate"
    return "claim-weak"


def strength_emoji(s: str) -> str:
    s = s.lower()
    if "strong" in s:   return "🟢"
    if "moderate" in s: return "🟡"
    return "🔴"


def ref_class(year: int) -> str:
    age = datetime.now().year - year
    if age <= 5:  return "ref-fresh"
    if age <= 12: return "ref-mid"
    return "ref-stale"


# ── Prompt templates ──────────────────────────────────────────────────────────

ANALYSIS_PROMPT = """You are an elite research auditor. Analyze the following research paper text and return ONLY a JSON object with this exact schema — no extra text, no markdown fences outside the JSON:

{{
  "title": "string",
  "abstract_summary": "string (2-3 sentences)",
  "evidence_strength_score": <integer 0-100>,
  "evidence_rationale": "string",
  "methodology_breakdown": {{
    "labels": ["label1","label2",...],
    "values": [<num1>,<num2>,...]
  }},
  "sentiment_barcode": ["positive"|"negative"|"objective", ...],
  "claims": [
    {{"text":"string","page_hint":1,"strength":"Strong|Moderate|Weak","rationale":"string"}}
  ],
  "entities": [
    {{"entity":"string","type":"Method|Finding|Dataset|Institution|Drug|Other"}}
  ],
  "relationships": [
    {{"from":"string","relation":"string","to":"string"}}
  ],
  "references": [
    {{"citation":"string","year":<int>,"journal":"string","impact":"High|Medium|Low|Unknown"}}
  ],
  "conflict_of_interest": "string or null",
  "mermaid_flowchart": "string (valid Mermaid graph LR syntax)",
  "limitations": ["string",...],
  "novelty_score": <integer 0-100>,
  "reproducibility_score": <integer 0-100>,
  "key_contributions": ["string",...]
}}

Paper text (first 6000 chars):
{paper_text}"""


CHAT_PROMPT = """You are an expert research assistant. Answer the user's question based ONLY on the paper content below. Be concise, precise, and cite page numbers or section names when possible.

Paper content:
{paper_text}

Chat history:
{history}

User question: {question}

Answer:"""

# ── Mock data for demo (when no API key) ────────────────────────────────────

DEMO_DATA = {
    "title": "Deep Learning for Carbon Sequestration Prediction in Boreal Forests",
    "abstract_summary": "This paper proposes a transformer-based model to predict carbon sequestration rates in boreal forests using satellite imagery. The model achieves 94.2% accuracy on a held-out test set of 1,200 forest patches. Results suggest AI-driven monitoring could reduce field survey costs by 60%.",
    "evidence_strength_score": 74,
    "evidence_rationale": "Strong quantitative results with clear metrics. However, external validation on non-boreal biomes is absent and sample selection criteria lack detail.",
    "methodology_breakdown": {
        "labels": ["Data Collection", "Model Architecture", "Training", "Evaluation", "Ablation Study"],
        "values": [22, 35, 18, 17, 8]
    },
    "sentiment_barcode": [
        "objective","objective","positive","objective","negative","objective",
        "positive","positive","objective","negative","objective","positive",
        "objective","positive","objective","negative","positive","objective",
        "positive","positive","objective","positive","objective","negative",
        "positive","objective","objective","positive","positive","objective"
    ],
    "claims": [
        {"text": "Model achieves 94.2% prediction accuracy", "page_hint": 5, "strength": "Strong", "rationale": "Backed by 5-fold cross-validation on 1,200 samples with p < 0.001"},
        {"text": "60% reduction in field survey costs", "page_hint": 8, "strength": "Moderate", "rationale": "Based on cost estimates from a single partner institution; not independently verified"},
        {"text": "No significant overfitting observed", "page_hint": 6, "strength": "Moderate", "rationale": "Training vs. validation loss curves shown but held-out test period is only 6 months"},
        {"text": "Outperforms all prior baselines", "page_hint": 7, "strength": "Strong", "rationale": "Comprehensive comparison table against 7 prior methods with statistical significance"},
        {"text": "Generalises to tropical rainforests", "page_hint": 11, "strength": "Weak", "rationale": "Only one small tropical dataset tested; confidence intervals are very wide"},
    ],
    "entities": [
        {"entity": "Vision Transformer (ViT)", "type": "Method"},
        {"entity": "Landsat-8 Imagery", "type": "Dataset"},
        {"entity": "Carbon Flux Network", "type": "Institution"},
        {"entity": "Cross-entropy Loss", "type": "Method"},
        {"entity": "Boreal Forest Patches", "type": "Dataset"},
        {"entity": "CO₂ Sequestration Rate", "type": "Finding"},
        {"entity": "Sentinel-2", "type": "Dataset"},
        {"entity": "Finnish Meteorological Institute", "type": "Institution"},
    ],
    "relationships": [
        {"from": "Vision Transformer (ViT)", "relation": "trained on", "to": "Landsat-8 Imagery"},
        {"from": "Vision Transformer (ViT)", "relation": "predicts", "to": "CO₂ Sequestration Rate"},
        {"from": "Carbon Flux Network", "relation": "provided", "to": "Boreal Forest Patches"},
        {"from": "Finnish Meteorological Institute", "relation": "validated", "to": "CO₂ Sequestration Rate"},
        {"from": "Sentinel-2", "relation": "supplements", "to": "Landsat-8 Imagery"},
    ],
    "references": [
        {"citation": "Vaswani et al., Attention Is All You Need", "year": 2017, "journal": "NeurIPS", "impact": "High"},
        {"citation": "Pan et al., Global Forest Carbon", "year": 2022, "journal": "Nature Climate Change", "impact": "High"},
        {"citation": "Dosovitskiy et al., ViT", "year": 2020, "journal": "ICLR", "impact": "High"},
        {"citation": "Smith & Jones, Remote Sensing Methods", "year": 2011, "journal": "Remote Sensing Environ.", "impact": "Medium"},
        {"citation": "Brown et al., Carbon Accounting", "year": 2015, "journal": "Forest Ecology", "impact": "Medium"},
        {"citation": "Garcia, Satellite Validation Study", "year": 2023, "journal": "arXiv", "impact": "Low"},
        {"citation": "Wilson et al., Boreal Ecology", "year": 2008, "journal": "Ecology Letters", "impact": "Medium"},
        {"citation": "Chen & Liu, Deep Learning Survey", "year": 2021, "journal": "IEEE TPAMI", "impact": "High"},
    ],
    "conflict_of_interest": "Lead author (Dr. A. Nielsen) is a paid scientific advisor to GreenSat Ltd., which sells satellite analysis software. No formal disclosure appears in the paper.",
    "mermaid_flowchart": "graph LR\n    A[Satellite Image Acquisition\nLandsat-8 & Sentinel-2] --> B[Preprocessing\nAtmospheric Correction]\n    B --> C[Patch Extraction\n256×256 tiles]\n    C --> D[Vision Transformer\nViT-B/16]\n    D --> E[Regression Head]\n    E --> F[CO₂ Prediction\nkg C / m² / yr]\n    F --> G[Evaluation\n5-fold CV]\n    G --> H{Accuracy > 90%?}\n    H -->|Yes| I[Deploy to Monitoring API]\n    H -->|No| D",
    "limitations": [
        "Tested exclusively on boreal biomes; tropical generalisability unproven",
        "Ground-truth labels from a single flux-tower network with known gaps",
        "Model latency (2.3s/patch) may limit real-time applications",
        "No uncertainty quantification provided for individual predictions",
    ],
    "novelty_score": 81,
    "reproducibility_score": 63,
    "key_contributions": [
        "First transformer-based architecture applied to pan-boreal carbon flux mapping",
        "A new public benchmark dataset: BorealCarbonBench-1200",
        "Cost-efficiency analysis framework for AI vs. field surveys",
    ],
}

# ── PDF text extraction ───────────────────────────────────────────────────────

def extract_text_from_pdf(pdf_bytes: bytes) -> str:
    try:
        import pypdf
        reader = pypdf.PdfReader(io.BytesIO(pdf_bytes))
        return "\n".join(p.extract_text() or "" for p in reader.pages)
    except Exception:
        return ""

# ── UI Components ─────────────────────────────────────────────────────────────

def render_hero():
    st.markdown("""
    <div class="hero">
      <div class="hero-title">🔬 InsightEngine Pro</div>
      <div class="hero-sub">Multimodal Research Auditor · Evidence Intelligence · AI-Powered</div>
    </div>
    """, unsafe_allow_html=True)


def render_metrics(data: dict):
    ev  = data["evidence_strength_score"]
    nov = data["novelty_score"]
    rep = data["reproducibility_score"]
    refs = data["references"]
    fresh = sum(1 for r in refs if datetime.now().year - r["year"] <= 5)

    def score_color(v):
        if v >= 75: return "#34d399"
        if v >= 50: return "#f59e0b"
        return "#f87171"

    st.markdown(f"""
    <div class="metric-row">
      <div class="metric-card">
        <div class="label">Evidence Strength</div>
        <div class="value" style="color:{score_color(ev)}">{ev}<span style="font-size:1rem;color:var(--muted)">/100</span></div>
        <div class="delta">{"↑ Well-supported" if ev>=70 else "↓ Needs scrutiny"}</div>
        <div class="badge">⚖️</div>
      </div>
      <div class="metric-card">
        <div class="label">Novelty Index</div>
        <div class="value" style="color:{score_color(nov)}">{nov}<span style="font-size:1rem;color:var(--muted)">/100</span></div>
        <div class="delta">{"↑ Highly original" if nov>=70 else "Incremental advance"}</div>
        <div class="badge">💡</div>
      </div>
      <div class="metric-card">
        <div class="label">Reproducibility</div>
        <div class="value" style="color:{score_color(rep)}">{rep}<span style="font-size:1rem;color:var(--muted)">/100</span></div>
        <div class="delta">{"↑ Good" if rep>=70 else "⚠ Gaps exist"}</div>
        <div class="badge">🔁</div>
      </div>
      <div class="metric-card">
        <div class="label">Fresh Citations</div>
        <div class="value" style="color:{score_color(int(fresh/max(len(refs),1)*100))}">{fresh}<span style="font-size:1rem;color:var(--muted)">/{len(refs)}</span></div>
        <div class="delta">≤5 years old</div>
        <div class="badge">📚</div>
      </div>
    </div>
    """, unsafe_allow_html=True)


def render_barcode(sentiments: list):
    color_map = {"positive": "#34d399", "negative": "#f87171", "objective": "#5b8af0"}
    colors = [color_map.get(s, "#5b8af0") for s in sentiments]

    # Build a thin imshow figure
    fig = go.Figure(go.Image(
        z=[[[int(c[1:3],16), int(c[3:5],16), int(c[5:7],16)] for c in colors]],
    ))
    fig.update_layout(
        height=56,
        margin=dict(l=0,r=0,t=0,b=0),
        xaxis=dict(visible=False, showgrid=False),
        yaxis=dict(visible=False, showgrid=False),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
    )
    st.markdown('<div class="barcode-label">🧬 PAPER DNA BARCODE — Emotional Flow (Green=Positive · Blue=Objective · Red=Critical)</div>', unsafe_allow_html=True)
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    # Compact legend
    pos = sentiments.count("positive")
    neg = sentiments.count("negative")
    obj = sentiments.count("objective")
    total = len(sentiments)
    lcol1, lcol2, lcol3 = st.columns(3)
    lcol1.markdown(f'<span class="badge badge-green">🟢 Positive {pos/total*100:.0f}%</span>', unsafe_allow_html=True)
    lcol2.markdown(f'<span class="badge badge-blue">🔵 Objective {obj/total*100:.0f}%</span>', unsafe_allow_html=True)
    lcol3.markdown(f'<span class="badge badge-red">🔴 Critical {neg/total*100:.0f}%</span>', unsafe_allow_html=True)


def render_methodology_chart(breakdown: dict):
    fig = px.pie(
        names=breakdown["labels"],
        values=breakdown["values"],
        hole=0.55,
        color_discrete_sequence=["#5b8af0","#a78bfa","#34d399","#f59e0b","#f87171","#06b6d4"],
    )
    fig.update_traces(textposition='outside', textfont_size=11, textfont_color="#e2e8f0")
    fig.update_layout(
        height=320,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="#e2e8f0",
        showlegend=True,
        legend=dict(
            bgcolor="rgba(0,0,0,0)",
            font=dict(color="#e2e8f0", size=11),
            orientation="v",
        ),
        margin=dict(l=0,r=0,t=20,b=0),
    )
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})


def render_claims(claims: list):
    for c in claims:
        cls = color_for_strength(c["strength"])
        em  = strength_emoji(c["strength"])
        st.markdown(f"""
        <div class="claim-card {cls}">
          <div class="claim-title">{em} {c['text']}</div>
          <div class="claim-meta">
            Strength: <b>{c['strength']}</b> &nbsp;·&nbsp; {c['rationale']}
          </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button(f"📌 Jump to page {c['page_hint']}", key=f"claim_{c['text'][:20]}"):
            st.session_state.target_page = c["page_hint"]
            st.rerun()


def render_knowledge_graph(entities: list, relationships: list):
    # Entity type → color
    type_color = {
        "Method": "#5b8af0", "Finding": "#34d399", "Dataset": "#a78bfa",
        "Institution": "#f59e0b", "Drug": "#f87171", "Other": "#64748b",
    }
    # Build plotly scatter network
    import math
    n = len(entities)
    angles = [2*math.pi*i/n for i in range(n)]
    ex = [math.cos(a) for a in angles]
    ey = [math.sin(a) for a in angles]
    entity_idx = {e["entity"]: i for i, e in enumerate(entities)}

    edge_x, edge_y = [], []
    for r in relationships:
        if r["from"] in entity_idx and r["to"] in entity_idx:
            i, j = entity_idx[r["from"]], entity_idx[r["to"]]
            edge_x += [ex[i], ex[j], None]
            edge_y += [ey[i], ey[j], None]

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=edge_x, y=edge_y, mode="lines",
                             line=dict(color="#252a40", width=1.5), hoverinfo="none"))
    for ent, i in entity_idx.items():
        t = entities[i]["type"]
        fig.add_trace(go.Scatter(
            x=[ex[i]], y=[ey[i]],
            mode="markers+text",
            marker=dict(size=16, color=type_color.get(t,"#64748b"), line=dict(color="#0a0c14",width=2)),
            text=[ent], textposition="top center",
            textfont=dict(color="#e2e8f0", size=9, family="Space Mono"),
            hovertemplate=f"<b>{ent}</b><br>Type: {t}<extra></extra>",
            showlegend=False,
        ))
    fig.update_layout(
        height=340,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(17,20,32,1)",
        xaxis=dict(visible=False), yaxis=dict(visible=False),
        margin=dict(l=0,r=0,t=0,b=0),
    )
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    st.markdown("**Relationships detected:**")
    for r in relationships:
        st.markdown(
            f'<span class="kg-node">{r["from"]}</span>'
            f'<span class="kg-edge"> ──{r["relation"]}──▶ </span>'
            f'<span class="kg-node">{r["to"]}</span>',
            unsafe_allow_html=True
        )


def render_references(refs: list):
    now = datetime.now().year
    fresh = [r for r in refs if now - r["year"] <= 5]
    mid   = [r for r in refs if 5 < now - r["year"] <= 12]
    stale = [r for r in refs if now - r["year"] > 12]

    c1, c2, c3 = st.columns(3)
    c1.metric("🟢 Fresh (≤5 yr)", len(fresh))
    c2.metric("🟡 Aging (6-12 yr)", len(mid))
    c3.metric("🔴 Stale (>12 yr)", len(stale))

    # Timeline chart
    years = [r["year"] for r in refs]
    fig = px.histogram(x=years, nbins=15,
                       color_discrete_sequence=["#5b8af0"],
                       labels={"x":"Year","y":"Count"})
    fig.update_layout(
        height=180,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(17,20,32,1)",
        font_color="#e2e8f0",
        margin=dict(l=0,r=0,t=10,b=0),
        xaxis=dict(gridcolor="#252a40"),
        yaxis=dict(gridcolor="#252a40"),
        bargap=0.1,
    )
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    for r in refs:
        cls = ref_class(r["year"])
        st.markdown(
            f'<span class="ref-pill {cls}">📄 {r["citation"]} ({r["year"]}) — {r["journal"]} [{r["impact"]}]</span>',
            unsafe_allow_html=True
        )


def render_mermaid(mermaid_str: str):
    try:
        import streamlit_mermaid as stmd
        stmd.st_mermaid(mermaid_str, height=340)
    except Exception:
        st.code(mermaid_str, language="text")


def render_audio(text: str):
    try:
        from gtts import gTTS
        tts = gTTS(text=text[:500], lang="en", slow=False)
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        fp.seek(0)
        st.audio(fp, format="audio/mp3")
    except Exception as e:
        st.warning(f"Audio generation unavailable: {e}")


def render_fingerprint(pdf_bytes: bytes):
    h = paper_hash(pdf_bytes)
    st.markdown(f"""
    <div style="margin-top:8px">
      <div class="barcode-label">📋 DOCUMENT FINGERPRINT (SHA-256)</div>
      <div class="fingerprint">{h}</div>
    </div>
    """, unsafe_allow_html=True)


def render_pdf(pdf_bytes: bytes, target_page: int):
    try:
        from streamlit_pdf_viewer import pdf_viewer
        pdf_viewer(pdf_bytes, scroll_to_page=target_page, height=640)
    except Exception:
        st.info("Install `streamlit-pdf-viewer` for inline PDF rendering.")
        st.download_button("⬇ Download PDF", pdf_bytes, "paper.pdf", "application/pdf")


def render_coi(coi: str | None):
    if coi:
        st.markdown(f"""
        <div style="background:rgba(248,113,113,0.08);border:1px solid rgba(248,113,113,0.3);
                    border-radius:8px;padding:14px 18px;margin-bottom:12px">
          <div style="font-family:var(--mono);font-size:0.65rem;color:#f87171;
                      letter-spacing:1px;text-transform:uppercase;margin-bottom:6px">
            ⚠ Conflict of Interest Detected
          </div>
          <div style="font-size:0.82rem;color:#e2e8f0">{coi}</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown('<span class="badge badge-green">✓ No COI Detected</span>', unsafe_allow_html=True)


def render_limitations(lims: list):
    for i, l in enumerate(lims, 1):
        st.markdown(f"""
        <div style="display:flex;gap:10px;margin-bottom:8px;align-items:flex-start">
          <span style="font-family:var(--mono);font-size:0.65rem;color:var(--warn);
                       background:rgba(245,158,11,0.1);border:1px solid rgba(245,158,11,0.2);
                       border-radius:4px;padding:1px 7px;flex-shrink:0">L{i}</span>
          <span style="font-size:0.82rem;color:var(--text)">{l}</span>
        </div>
        """, unsafe_allow_html=True)


def render_contributions(contribs: list):
    for c in contribs:
        st.markdown(f"""
        <div style="display:flex;gap:10px;margin-bottom:6px;align-items:flex-start">
          <span style="color:#34d399;flex-shrink:0">✦</span>
          <span style="font-size:0.82rem;color:var(--text)">{c}</span>
        </div>
        """, unsafe_allow_html=True)


# ── Sidebar ───────────────────────────────────────────────────────────────────

with st.sidebar:
    st.markdown("### ⚙️ Configuration")
    api_key = st.text_input("OpenAI API Key", type="password", placeholder="sk-...",
                            help="Leave blank to use built-in demo data")
    st.session_state.api_key = api_key

    st.markdown("---")

    if st.session_state.analysis_done and st.session_state.paper_data:
        data = st.session_state.paper_data
        coi = data.get("conflict_of_interest")
        render_coi(coi)
        st.markdown("---")

    st.markdown("### 💬 Ask the Paper")
    if not st.session_state.analysis_done:
        st.caption("Upload and analyse a paper first.")
    else:
        # Display history
        for msg in st.session_state.chat_history[-6:]:
            role = msg["role"]
            bubble = "chat-user" if role == "user" else "chat-ai"
            label  = "YOU" if role == "user" else "AI AUDITOR"
            st.markdown(f'<div class="chat-label">{label}</div><div class="{bubble}">{msg["content"]}</div>',
                        unsafe_allow_html=True)

        question = st.chat_input("Ask about methodology, limitations…")
        if question:
            st.session_state.chat_history.append({"role":"user","content":question})
            paper_text = st.session_state.get("paper_text","")
            history_str = "\n".join(f"{m['role'].upper()}: {m['content']}"
                                    for m in st.session_state.chat_history[-6:])
            if st.session_state.api_key:
                prompt = CHAT_PROMPT.format(
                    paper_text=paper_text[:5000],
                    history=history_str,
                    question=question,
                )
                answer = call_claude(prompt, st.session_state.api_key)
            elif paper_text.strip():
                answer = answer_from_paper(question, paper_text)
            else:
                answer = "No paper text available. Please upload a PDF and run analysis first."
            st.session_state.chat_history.append({"role":"assistant","content":answer})
            st.rerun()


# ── Main layout ───────────────────────────────────────────────────────────────

render_hero()

pdf_col, analysis_col = st.columns([1, 1], gap="large")

with pdf_col:
    st.markdown('<div class="section-head">📄 Source Document</div>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Upload Research PDF", type="pdf", label_visibility="collapsed")

    run_analysis = False
    pdf_bytes = None

    if uploaded_file:
        pdf_bytes = uploaded_file.getvalue()
        render_fingerprint(pdf_bytes)
        render_pdf(pdf_bytes, st.session_state.target_page)

        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("🚀 Run Full Analysis", use_container_width=True):
                run_analysis = True
        with col_b:
            if st.button("🔄 Reset", use_container_width=True):
                st.session_state.analysis_done = False
                st.session_state.paper_data = None
                st.session_state.chat_history = []
                st.rerun()
    else:
        # Demo mode
        st.info("📂 No PDF uploaded — showing **demo mode** with sample data.", icon="ℹ️")
        if st.button("▶ Load Demo Analysis", use_container_width=True):
            run_analysis = True
            pdf_bytes = b""


# ── Run analysis ──────────────────────────────────────────────────────────────

if run_analysis:
    with st.spinner("🔬 Auditing research paper…"):
        if pdf_bytes:
            paper_text = extract_text_from_pdf(pdf_bytes) if pdf_bytes else ""
            st.session_state["paper_text"] = paper_text
        else:
            paper_text = ""

        if paper_text.strip():
            if st.session_state.api_key:
                prompt = ANALYSIS_PROMPT.format(paper_text=paper_text[:6000])
                raw = call_claude(prompt, st.session_state.api_key)
                data = extract_json(raw)
                if not data:
                    st.warning("AI response parse failed. Using local analysis.")
                    data = analyze_pdf_locally(paper_text)
            else:
                data = analyze_pdf_locally(paper_text)
        else:
            data = DEMO_DATA

        st.session_state.paper_data = data
        st.session_state.analysis_done = True
    st.rerun()


# ── Analysis panel ────────────────────────────────────────────────────────────

with analysis_col:
    if not st.session_state.analysis_done or not st.session_state.paper_data:
        st.markdown("""
        <div style="height:400px;display:flex;align-items:center;justify-content:center;
                    flex-direction:column;gap:16px;color:var(--muted);text-align:center">
          <div style="font-size:3rem">🔬</div>
          <div style="font-family:var(--mono);font-size:0.8rem;letter-spacing:1px">
            AWAITING ANALYSIS
          </div>
          <div style="font-size:0.8rem;max-width:260px">
            Upload a PDF or load the demo to begin the audit
          </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        data = st.session_state.paper_data

        # Title
        st.markdown(f"""
        <div style="background:var(--surface);border:1px solid var(--border);border-radius:10px;
                    padding:16px 20px;margin-bottom:16px">
          <div style="font-family:var(--sans);font-size:1.05rem;font-weight:700;color:var(--text)">
            {data.get('title','Untitled Paper')}
          </div>
          <div style="font-size:0.8rem;color:var(--muted);margin-top:6px">
            {data.get('abstract_summary','')}
          </div>
        </div>
        """, unsafe_allow_html=True)

        # Score cards
        render_metrics(data)

        # ── Tabs ──
        tab_summary, tab_overview, tab_evidence, tab_viz, tab_refs, tab_audio, tab_advanced = st.tabs([
            "📋 Summary", "📊 Overview", "⚖️ Evidence", "🔄 Visuals", "📚 References", "🎧 Audio", "🧠 Deep Dive"
        ])

        with tab_summary:
            # ── Paper Summary ──
            st.markdown('<div class="section-head">📝 Paper Summary</div>', unsafe_allow_html=True)
            st.markdown(f"""
            <div style="background:var(--surface2);border:1px solid var(--border);border-radius:10px;
                        padding:18px 22px;margin-bottom:16px;line-height:1.7">
              <div style="font-size:0.9rem;color:var(--text)">{data.get('abstract_summary','')}</div>
            </div>
            """, unsafe_allow_html=True)

            # ── Highlights ──
            st.markdown('<div class="section-head">🌟 Key Highlights</div>', unsafe_allow_html=True)
            highlights = [
                ("⚖️", "Evidence Strength", f"{data['evidence_strength_score']}/100 — {data.get('evidence_rationale','')}"),
                ("💡", "Novelty", f"{data['novelty_score']}/100"),
                ("🔁", "Reproducibility", f"{data['reproducibility_score']}/100"),
            ]
            for icon, label, val in highlights:
                st.markdown(f"""
            <div style="display:flex;gap:12px;align-items:flex-start;background:var(--surface);
                        border:1px solid var(--border);border-radius:8px;padding:12px 16px;margin-bottom:8px">
              <span style="font-size:1.2rem">{icon}</span>
              <div>
                <div style="font-family:var(--mono);font-size:0.65rem;color:var(--muted);
                            letter-spacing:1px;text-transform:uppercase;margin-bottom:4px">{label}</div>
                <div style="font-size:0.85rem;color:var(--text)">{val}</div>
              </div>
            </div>
            """, unsafe_allow_html=True)

            # ── Important Points ──
            st.markdown('<div class="section-head">📌 Important Points</div>', unsafe_allow_html=True)
            strong_claims = [c for c in data.get('claims', []) if c['strength'] == 'Strong']
            for c in strong_claims:
                st.markdown(f"""
            <div style="display:flex;gap:10px;align-items:flex-start;margin-bottom:8px">
              <span style="color:#34d399;font-size:1rem;flex-shrink:0">●</span>
              <span style="font-size:0.85rem;color:var(--text)">{c['text']}
                <span style="font-size:0.72rem;color:var(--muted)"> — {c['rationale']}</span>
              </span>
            </div>
            """, unsafe_allow_html=True)

            # ── Key Contributions ──
            st.markdown('<div class="section-head">✨ Key Contributions</div>', unsafe_allow_html=True)
            render_contributions(data.get("key_contributions", []))

            # ── Limitations Summary ──
            st.markdown('<div class="section-head">⚠️ Limitations at a Glance</div>', unsafe_allow_html=True)
            render_limitations(data.get("limitations", []))

        with tab_overview:
            st.markdown('<div class="section-head">🧬 Research DNA Barcode</div>', unsafe_allow_html=True)
            render_barcode(data.get("sentiment_barcode", []))

            st.markdown('<div class="section-head">🗺️ Methodology Breakdown</div>', unsafe_allow_html=True)
            render_methodology_chart(data.get("methodology_breakdown", {"labels":[],"values":[]}))

            st.markdown('<div class="section-head">✨ Key Contributions</div>', unsafe_allow_html=True)
            render_contributions(data.get("key_contributions", []))

        with tab_evidence:
            st.markdown(f"""
            <div class="barcode-label" style="margin-bottom:8px">EVIDENCE RATIONALE</div>
            <div style="font-size:0.83rem;color:var(--text);margin-bottom:16px">
              {data.get('evidence_rationale','')}
            </div>
            """, unsafe_allow_html=True)

            st.markdown('<div class="section-head">🔍 Claim Verification</div>', unsafe_allow_html=True)
            render_claims(data.get("claims", []))

            st.markdown('<div class="section-head">⚠ Limitations</div>', unsafe_allow_html=True)
            render_limitations(data.get("limitations", []))

        with tab_viz:
            st.markdown('<div class="section-head">🔄 Methodology Flowchart (Mermaid)</div>', unsafe_allow_html=True)
            render_mermaid(data.get("mermaid_flowchart", "graph LR; A[Start] --> B[End]"))

            st.markdown('<div class="section-head">🕸️ Knowledge Graph</div>', unsafe_allow_html=True)
            render_knowledge_graph(
                data.get("entities", []),
                data.get("relationships", [])
            )

        with tab_refs:
            st.markdown('<div class="section-head">📚 Reference Health Check</div>', unsafe_allow_html=True)
            render_references(data.get("references", []))

        with tab_audio:
            st.markdown('<div class="section-head">🎧 Audio Abstract</div>', unsafe_allow_html=True)
            text_to_speak = data.get("abstract_summary", "No abstract available.")
            st.markdown(f'<div style="font-size:0.83rem;color:var(--muted);margin-bottom:12px">{text_to_speak}</div>',
                        unsafe_allow_html=True)
            if st.button("🔊 Generate Audio Summary", use_container_width=True):
                render_audio(text_to_speak)

            st.markdown('<div class="section-head">📋 Key Contributions Read-Aloud</div>', unsafe_allow_html=True)
            contrib_text = ". ".join(data.get("key_contributions", []))
            if st.button("🔊 Read Contributions", use_container_width=True):
                render_audio(contrib_text)

        with tab_advanced:
            st.markdown('<div class="section-head">🧠 Comparative Radar</div>', unsafe_allow_html=True)
            categories = ["Evidence", "Novelty", "Reproducibility", "Recency", "Methodology"]
            refs = data.get("references", [])
            now = datetime.now().year
            recency = int(sum(1 for r in refs if now - r["year"] <= 5) / max(len(refs),1) * 100)
            values = [
                data["evidence_strength_score"],
                data["novelty_score"],
                data["reproducibility_score"],
                recency,
                min(100, len(data.get("methodology_breakdown",{}).get("labels",[])) * 18),
            ]
            fig = go.Figure(go.Scatterpolar(
                r=values + [values[0]],
                theta=categories + [categories[0]],
                fill="toself",
                fillcolor="rgba(91,138,240,0.15)",
                line=dict(color="#5b8af0", width=2),
                marker=dict(color="#5b8af0"),
            ))
            fig.update_layout(
                polar=dict(
                    bgcolor="rgba(17,20,32,1)",
                    radialaxis=dict(visible=True, range=[0,100], gridcolor="#252a40",
                                   tickfont=dict(color="#64748b", size=9)),
                    angularaxis=dict(gridcolor="#252a40", tickfont=dict(color="#e2e8f0", size=10)),
                ),
                paper_bgcolor="rgba(0,0,0,0)",
                margin=dict(l=40,r=40,t=20,b=20),
                height=300,
                showlegend=False,
            )
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

            st.markdown('<div class="section-head">📈 Evidence vs Novelty Scatter</div>', unsafe_allow_html=True)
            scatter_data = pd.DataFrame({
                "Claim": [c["text"][:35]+"…" for c in data.get("claims", [])],
                "Evidence": [{"Strong":90,"Moderate":55,"Weak":20}.get(c["strength"],50)
                             + random.randint(-5,5) for c in data.get("claims", [])],
                "Strength": [c["strength"] for c in data.get("claims", [])],
            })
            if not scatter_data.empty:
                fig2 = px.bar(scatter_data, x="Claim", y="Evidence",
                              color="Strength",
                              color_discrete_map={"Strong":"#34d399","Moderate":"#f59e0b","Weak":"#f87171"})
                fig2.update_layout(
                    height=220,
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(17,20,32,1)",
                    font_color="#e2e8f0",
                    margin=dict(l=0,r=0,t=0,b=0),
                    xaxis=dict(gridcolor="#252a40", tickfont=dict(size=9)),
                    yaxis=dict(gridcolor="#252a40", range=[0,100]),
                    legend=dict(bgcolor="rgba(0,0,0,0)"),
                    showlegend=True,
                )
                st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar": False})
