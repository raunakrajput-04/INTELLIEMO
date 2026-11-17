import os
import sys
import base64
from pathlib import Path
import docx
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

PROJECT_ROOT = Path(__file__).resolve().parent.parent
TEMPLATE_PATH = r"C:\Users\rauna\.gemini\antigravity\brain\dc960050-0706-42ed-880e-2df861b6b5e6\.user_uploaded\media_1794926326383_fa7e7a35.docx"
OUTPUT_DOCX = PROJECT_ROOT / "INTELLIEMO_Project_Report.docx"
OUTPUT_PDF = PROJECT_ROOT / "INTELLIEMO_Project_Report.pdf"
OUTPUT_HTML = PROJECT_ROOT / "INTELLIEMO_Project_Report.html"
LOGO_PATH = PROJECT_ROOT / "vu_logo.png"

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
    tcPr.append(tcMar)

def add_heading(doc, text, level=1):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(12)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.keep_with_next = True
    run = p.add_run(text)
    run.font.name = "Georgia"
    run.font.bold = True
    if level == 1:
        run.font.size = Pt(16)
        run.font.color.rgb = RGBColor(16, 42, 77)
    elif level == 2:
        run.font.size = Pt(13)
        run.font.color.rgb = RGBColor(27, 67, 120)
    else:
        run.font.size = Pt(11.5)
        run.font.color.rgb = RGBColor(40, 40, 40)
    return p

def add_body_p(doc, text="", bold_prefix=None, space_after=4):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = 1.15
    if bold_prefix:
        r_pre = p.add_run(bold_prefix)
        r_pre.font.name = "Georgia"
        r_pre.font.size = Pt(11)
        r_pre.font.bold = True
        r_pre.font.color.rgb = RGBColor(30, 30, 30)
    if text:
        r_text = p.add_run(text)
        r_text.font.name = "Georgia"
        r_text.font.size = Pt(11)
        r_text.font.color.rgb = RGBColor(50, 50, 50)
    return p

def add_bullet(doc, title, body):
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Inches(0.25)
    p.paragraph_format.space_before = Pt(1)
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.line_spacing = 1.15
    r_bullet = p.add_run("• ")
    r_bullet.font.name = "Georgia"
    r_bullet.font.bold = True
    r_bullet.font.color.rgb = RGBColor(16, 42, 77)
    r_title = p.add_run(title)
    r_title.font.name = "Georgia"
    r_title.font.bold = True
    r_title.font.size = Pt(10.5)
    r_body = p.add_run(body)
    r_body.font.name = "Georgia"
    r_body.font.size = Pt(10.5)
    r_body.font.color.rgb = RGBColor(50, 50, 50)
    return p

def add_code_block(doc, code_str, filename=""):
    if filename:
        p_fn = doc.add_paragraph()
        p_fn.paragraph_format.space_before = Pt(8)
        p_fn.paragraph_format.space_after = Pt(2)
        p_fn.paragraph_format.keep_with_next = True
        r_fn = p_fn.add_run(f"Source: {filename}")
        r_fn.font.name = "Consolas"
        r_fn.font.size = Pt(9.5)
        r_fn.font.bold = True
        r_fn.font.color.rgb = RGBColor(16, 42, 77)

    table = doc.add_table(rows=1, cols=1)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    cell = table.rows[0].cells[0]
    cell.width = Inches(6.5)
    set_cell_background(cell, "F4F6F9")
    set_cell_margins(cell, top=120, bottom=120, left=160, right=160)
    
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(0)
    p.paragraph_format.line_spacing = 1.05
    run = p.add_run(code_str.strip())
    run.font.name = "Consolas"
    run.font.size = Pt(8.5)
    run.font.color.rgb = RGBColor(35, 45, 60)
    
    doc.add_paragraph().paragraph_format.space_after = Pt(4)

def build_docx():
    print("Loading base template:", TEMPLATE_PATH)
    doc = docx.Document(TEMPLATE_PATH)
    
    # Update Cover Page Elements
    # P3: [Title of Project]
    doc.paragraphs[3].text = ""
    r = doc.paragraphs[3].add_run("INTELLIEMO: Enterprise-Grade Text Emotion Intelligence & Explainable NLP Engine")
    r.font.name = "Georgia"
    r.font.size = Pt(17)
    r.font.bold = True
    r.font.color.rgb = RGBColor(16, 42, 77)
    doc.paragraphs[3].alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    # P5: S. Y. B. Tech (Dept Name)
    doc.paragraphs[5].text = ""
    r = doc.paragraphs[5].add_run("S. Y. B. Tech (Department of AI/AIML/AIDS)")
    r.font.name = "Georgia"
    r.font.size = Pt(13)
    r.font.bold = True
    doc.paragraphs[5].alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    # P6: Project 1 [Subject Code & Name]
    doc.paragraphs[6].text = ""
    r = doc.paragraphs[6].add_run("Project 1 [Natural Language Processing & Machine Learning]")
    r.font.name = "Georgia"
    r.font.size = Pt(12)
    r.font.bold = True
    doc.paragraphs[6].alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    # P9: By
    doc.paragraphs[9].text = ""
    r = doc.paragraphs[9].add_run("By")
    r.font.name = "Georgia"
    r.font.size = Pt(12)
    r.font.bold = True
    doc.paragraphs[9].alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    # P10: [Name of student (SRN)]
    doc.paragraphs[10].text = ""
    r1 = doc.paragraphs[10].add_run("Raunak Rajput (31252544)\n")
    r1.font.name = "Georgia"
    r1.font.size = Pt(13)
    r1.font.bold = True
    r2 = doc.paragraphs[10].add_run("Ayush Vishwakarma\n")
    r2.font.name = "Georgia"
    r2.font.size = Pt(12)
    r2.font.bold = True
    r3 = doc.paragraphs[10].add_run("Vipul Bhamare")
    r3.font.name = "Georgia"
    r3.font.size = Pt(12)
    r3.font.bold = True
    doc.paragraphs[10].alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    # Table 0: Index Table
    idx_table = doc.tables[0]
    index_data = [
        ("1", "Introduction & Problem Statement", "2"),
        ("2", "Literature Survey & Theoretical Background", "3"),
        ("3", "System Architecture & Methodology", "4"),
        ("4", "Key Source Code & Implementation", "6"),
        ("5", "Results & Experimental Evaluation", "9"),
        ("6", "Discourse & Mixed Emotion Case Studies", "11"),
        ("7", "Conclusion & Future Scope", "12"),
        ("8", "References", "13")
    ]
    
    # Ensure rows
    while len(idx_table.rows) - 1 < len(index_data):
        idx_table.add_row()
        
    for i, (sr, content, page) in enumerate(index_data):
        row = idx_table.rows[i + 1]
        row.cells[0].text = sr
        row.cells[1].text = content
        row.cells[2].text = page
        for c in row.cells:
            c.paragraphs[0].runs[0].font.name = "Georgia"
            c.paragraphs[0].runs[0].font.size = Pt(10.5)
            c.paragraphs[0].runs[0].font.bold = (i in [0, 2, 3, 4, 6])

    # Now clear filler paragraphs between Table 0 and P39, P62, P85
    # Keep P39 (Introduction:), P62 (Code:), P85 (Result:)
    # Because modifying in-place can shift indexes, we will clear filler texts
    for p_i in range(len(doc.paragraphs)):
        if p_i not in [0, 3, 5, 6, 9, 10, 13, 16, 17, 18, 19, 21, 39, 62, 85]:
            doc.paragraphs[p_i].text = ""

    # Style P39, P62, P85
    for p_idx, title in [(39, "1. Introduction:"), (62, "2. Key Source Code & Implementation:"), (85, "3. Experimental Results & Benchmarks:")]:
        p = doc.paragraphs[p_idx]
        p.text = ""
        r = p.add_run(title)
        r.font.name = "Georgia"
        r.font.size = Pt(16)
        r.font.bold = True
        r.font.color.rgb = RGBColor(16, 42, 77)

    # We will append the rich content after each section or at the end
    # Let's append everything cleanly to create a pristine report
    
    # SECTION 1: INTRODUCTION CONTENT
    add_heading(doc, "1.1 Background & Motivation", level=2)
    add_body_p(doc, "In modern natural language processing (NLP), understanding affective human communication remains a vital frontier. While conventional sentiment analysis reduces expressive human language into binary (positive/negative) or ternary polarities, human emotion is fundamentally multidimensional, nuanced, and dynamic. People routinely express mixed sentiments, antecedent contexts, and subtle affective shifts. For instance, customer feedback, mental health self-reports, conversational agents, and employee satisfaction surveys cannot be adequately characterized by simple polarity tags without losing critical nuances.")
    add_body_p(doc, "Recent advancements in transfer learning—specifically Bidirectional Encoder Representations from Transformers (BERT) and its computationally efficient derivative DistilBERT—have enabled sequence models to capture bidirectional linguistic context. However, a persistent challenge in applying neural sequence classifiers to complex discourse is the softmax peakiness problem: a standard single-label classification architecture forces probabilities to sum to 1.0, frequently allowing a single emotionally charged token to drown out legitimate, conflicting clauses.")
    add_body_p(doc, "INTELLIEMO solves this challenge by coupling a fine-tuned transformer classification backbone with a deterministic Discourse-Aware Multi-Emotion Reasoning Engine and an Explainable AI (XAI) Token Attribution Layer.")

    add_heading(doc, "1.2 Problem Statement", level=2)
    add_body_p(doc, "Traditional sentiment and emotion classification architectures fail when applied to real-world compound statements because:")
    add_bullet(doc, "Lack of Discourse Sensitivity: ", "Complex sentences containing contrastive markers (e.g., 'I was overjoyed at first, but after some time I became frustrated and anxious') are collapsed into a single dominant emotion, discarding either the initial experience or the concluding sentiment.")
    add_bullet(doc, "Black-Box Opacity: ", "Deep neural networks do not natively provide transparent justification for why a classification was generated, eroding user trust in sensitive clinical, judicial, or organizational settings.")
    add_bullet(doc, "High Latency & Cloud Dependency: ", "Massive large language models (LLMs) require expensive cloud API calls, introduce high latency, and pose data privacy risks when processing confidential statements.")

    add_heading(doc, "1.3 Project Objectives", level=2)
    add_bullet(doc, "Transformer Fine-Tuning: ", "Fine-tune a lightweight DistilBERT-base-uncased model (67.0M parameters) on the 6-class dair-ai/emotion benchmark to achieve >= 92% classification accuracy with sub-100ms CPU latency.")
    add_bullet(doc, "Discourse-Aware Decomposition: ", "Develop an algorithm that segments sentences along contrastive ('but', 'however') and temporal ('after some time', 'later') boundaries, weighting concluding resolution clauses higher (60-70%) than antecedent clauses.")
    add_bullet(doc, "Explainable AI (XAI): ", "Implement Vectorized Token-Drop Saliency to compute exact counterfactual word contributions in a single batched tensor forward pass.")
    add_bullet(doc, "Full-Stack Deployment: ", "Build an asynchronous FastAPI REST service with SQLite telemetry and an interactive React 19 + TypeScript + Tailwind CSS dashboard.")

    add_heading(doc, "1.4 Emotion Taxonomy (6 Core Dimensions)", level=2)
    add_bullet(doc, "🌟 Joy: ", "Delight, triumph, celebration, excitement, happiness.")
    add_bullet(doc, "💙 Sadness: ", "Grief, disappointment, sorrow, loneliness, depression.")
    add_bullet(doc, "🔥 Anger: ", "Fury, irritation, resentment, indignation, outrage.")
    add_bullet(doc, "⚡ Fear: ", "Anxiety, panic, terror, dread, vulnerability.")
    add_bullet(doc, "💖 Love: ", "Affection, warmth, gratitude, romantic affinity.")
    add_bullet(doc, "💥 Surprise: ", "Astonishment, shock, amazement, sudden discovery.")

    # SECTION 2: ARCHITECTURE & METHODOLOGY
    add_heading(doc, "1.5 System Architecture & Methodology", level=2)
    add_body_p(doc, "The INTELLIEMO pipeline operates through a multi-tier decoupled architecture:")
    add_bullet(doc, "1. Text Preprocessing: ", "Unicode NFKD normalization, entity sanitization (URLs, mentions), negation detection, and punctuation intensity extraction.")
    add_bullet(doc, "2. Discourse Boundary Decomposition: ", "Regex-based clause splitting along contrastive conjunctions and temporal shift markers.")
    add_bullet(doc, "3. Sequence Classification: ", "WordPiece tokenization (max length 128) followed by DistilBERT feed-forward inference generating 6-class probability logits.")
    add_bullet(doc, "4. Weighted Discourse Synthesis: ", "Terminal clauses receive up to 1.8x weighting over antecedent clauses, calculating composite multi-emotion distributions.")
    add_bullet(doc, "5. Vectorized Token Saliency: ", "Batched counterfactual masking evaluating confidence deltas for each token position.")

    # SECTION 3: CODE SNIPPETS
    add_heading(doc, "2. Key Source Code & Implementation", level=1)
    
    add_heading(doc, "2.1 Text Preprocessing & Feature Extraction Engine", level=2)
    code_prep = '''def normalize_text(text: str) -> str:
    """Normalizes text by removing invalid unicode, lowercasing, and expanding contractions."""
    if not text or not isinstance(text, str):
        return ""
    text = unicodedata.normalize("NFKD", text)
    text = text.lower().strip()
    text = re.sub(r"https?://\S+|www\.\S+", "[URL]", text)
    text = re.sub(r"@\w+", "[USER]", text)
    for contraction, expansion in CONTRACTIONS.items():
        text = re.sub(r"\\b" + re.escape(contraction) + r"\\b", expansion, text)
    text = re.sub(r"\\s+", " ", text).strip()
    return text'''
    add_code_block(doc, code_prep, "backend/app/ml/preprocessing.py")

    add_heading(doc, "2.2 DistilBERT Inference & Model Lifecycle Manager", level=2)
    code_model = '''class ModelManager:
    def predict(self, text: str) -> Dict[str, Any]:
        inputs = self.tokenizer(
            text, return_tensors="pt", truncation=True,
            padding=True, max_length=self.max_length
        )
        input_ids = inputs["input_ids"].to(self.device)
        attention_mask = inputs["attention_mask"].to(self.device)

        with torch.no_grad():
            outputs = self.model(input_ids=input_ids, attention_mask=attention_mask)
            probabilities = torch.softmax(outputs.logits, dim=-1)[0].cpu().numpy()

        dominant_idx = int(probabilities.argmax())
        return {
            "dominant_emotion": self.labels[dominant_idx],
            "confidence": round(float(probabilities[dominant_idx]), 4),
            "probabilities": {label: round(float(probabilities[i]), 4) for i, label in enumerate(self.labels)}
        }'''
    add_code_block(doc, code_model, "backend/app/ml/model_loader.py")

    add_heading(doc, "2.3 Discourse-Aware Multi-Emotion Reasoning Engine", level=2)
    code_disc = '''def decompose_and_analyze_emotions(text: str, features: Dict[str, Any]) -> Dict[str, Any]:
    contrastive_pattern = r'\\b(?:but|however|although|though|despite|yet|after\\s+(?:some\\s+time|that|a\\s+while)|later\\s+on|meanwhile)\\b'
    clauses = [c.strip() for c in re.split(contrastive_pattern, text, flags=re.IGNORECASE) if c.strip()]
    if len(clauses) <= 1:
        return model_manager.predict(text)

    combined_scores = {label: 0.0 for label in model_manager.labels}
    total_weights = 0.0
    for clause_idx, clause in enumerate(clauses):
        clause_weight = 1.0 + (0.8 * clause_idx / max(1, len(clauses) - 1))
        total_weights += clause_weight
        sub_probs = model_manager.predict(clause)["probabilities"]
        for label, prob in sub_probs.items():
            combined_scores[label] += prob * clause_weight

    normalized_probs = {k: round(v / total_weights, 4) for k, v in combined_scores.items()}
    sorted_emotions = sorted(normalized_probs.items(), key=lambda x: x[1], reverse=True)
    return {
        "dominant_emotion": sorted_emotions[0][0],
        "secondary_emotion": sorted_emotions[1][0] if sorted_emotions[1][1] >= 0.20 else None,
        "probabilities": normalized_probs,
        "is_mixed_emotion": sorted_emotions[1][1] >= 0.20,
    }'''
    add_code_block(doc, code_disc, "backend/app/services/emotion_service.py")

    add_heading(doc, "2.4 Vectorized Token-Drop Saliency (Explainable AI)", level=2)
    code_xai = '''def explain_prediction(text: str, target_emotion: Optional[str] = None) -> Dict[str, Any]:
    # Single batched forward pass for up to 16 tokens
    batch_size = len(valid_indices)
    batch_input_ids = input_ids.repeat(batch_size, 1)
    batch_attention_mask = attention_mask.repeat(batch_size, 1)

    for row_idx, token_idx in enumerate(valid_indices):
        batch_input_ids[row_idx, token_idx] = pad_id

    with torch.no_grad():
        masked_outputs = model(input_ids=batch_input_ids, attention_mask=batch_attention_mask)
        masked_probs = torch.softmax(masked_outputs.logits, dim=-1)

    token_scores = []
    for row_idx, token_idx in enumerate(valid_indices):
        delta = baseline_score - float(masked_probs[row_idx, target_idx].item())
        token_scores.append({"token": tokens[token_idx].replace("##", ""), "importance": round(delta, 4)})
    return {"target_emotion": target_emotion, "tokens": token_scores}'''
    add_code_block(doc, code_xai, "backend/app/ml/explainability.py")

    # SECTION 4: RESULTS
    add_heading(doc, "3. Results & Experimental Evaluation", level=1)
    
    add_heading(doc, "3.1 Comparative Benchmark Matrix", level=2)
    add_body_p(doc, "Evaluated on 2,000 holdout test samples from the dair-ai/emotion benchmark corpus:")
    
    # Benchmark table
    bm_table = doc.add_table(rows=4, cols=6)
    bm_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    headers = ["Model Architecture", "Accuracy", "Macro F1", "Weighted F1", "Parameters", "Latency"]
    for j, h in enumerate(headers):
        cell = bm_table.rows[0].cells[j]
        cell.text = h
        set_cell_background(cell, "102A4D")
        set_cell_margins(cell, 80, 80, 100, 100)
        p = cell.paragraphs[0]
        p.runs[0].font.name = "Georgia"
        p.runs[0].font.bold = True
        p.runs[0].font.size = Pt(9.5)
        p.runs[0].font.color.rgb = RGBColor(255, 255, 255)
        
    bm_rows = [
        ["DistilBERT (Fine-Tuned)", "92.70%", "88.25%", "92.69%", "67.0 Million", "82.7 ms"],
        ["TF-IDF + Linear SVM", "88.00%", "82.11%", "87.80%", "~50,000 N-grams", "12.4 ms"],
        ["TF-IDF + Logistic Regression", "86.15%", "79.40%", "85.90%", "~50,000 N-grams", "8.2 ms"]
    ]
    for i, row_data in enumerate(bm_rows):
        bg = "FFFFFF" if i % 2 == 0 else "F8FAFC"
        for j, val in enumerate(row_data):
            cell = bm_table.rows[i + 1].cells[j]
            cell.text = val
            set_cell_background(cell, bg)
            set_cell_margins(cell, 70, 70, 100, 100)
            p = cell.paragraphs[0]
            p.runs[0].font.name = "Georgia"
            p.runs[0].font.size = Pt(9)
            if i == 0:
                p.runs[0].font.bold = True
                p.runs[0].font.color.rgb = RGBColor(16, 42, 77)

    doc.add_paragraph().paragraph_format.space_after = Pt(4)

    add_heading(doc, "3.2 Per-Class Emotion Performance Breakdown", level=2)
    pc_table = doc.add_table(rows=7, cols=5)
    pc_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    pc_headers = ["Emotion Class", "Precision", "Recall", "F1-Score", "Test Support"]
    for j, h in enumerate(pc_headers):
        cell = pc_table.rows[0].cells[j]
        cell.text = h
        set_cell_background(cell, "102A4D")
        set_cell_margins(cell, 80, 80, 100, 100)
        p = cell.paragraphs[0]
        p.runs[0].font.name = "Georgia"
        p.runs[0].font.bold = True
        p.runs[0].font.size = Pt(9.5)
        p.runs[0].font.color.rgb = RGBColor(255, 255, 255)
        
    pc_rows = [
        ["Sadness", "96.89%", "96.56%", "96.72%", "581 samples"],
        ["Joy", "94.93%", "94.24%", "94.58%", "695 samples"],
        ["Anger", "92.59%", "92.00%", "92.29%", "275 samples"],
        ["Fear", "90.00%", "88.98%", "89.49%", "224 samples"],
        ["Love", "80.36%", "84.91%", "82.57%", "159 samples"],
        ["Surprise", "78.95%", "69.23%", "73.77%", "66 samples"],
    ]
    for i, row_data in enumerate(pc_rows):
        bg = "FFFFFF" if i % 2 == 0 else "F8FAFC"
        for j, val in enumerate(row_data):
            cell = pc_table.rows[i + 1].cells[j]
            cell.text = val
            set_cell_background(cell, bg)
            set_cell_margins(cell, 70, 70, 100, 100)
            p = cell.paragraphs[0]
            p.runs[0].font.name = "Georgia"
            p.runs[0].font.size = Pt(9)
            if j == 0:
                p.runs[0].font.bold = True

    doc.add_paragraph().paragraph_format.space_after = Pt(4)

    add_heading(doc, "3.3 Discourse & Explainability Case Studies", level=2)
    add_body_p(doc, "Case 1 (Contrastive Transition): 'I was overjoyed at first, but after some time I became frustrated and anxious.'")
    add_bullet(doc, "Standard Baseline: ", "Collapses entirely to Joy (94.1%) due to 'overjoyed'.")
    add_bullet(doc, "INTELLIEMO Output: ", "Dominant: Anger (44.8%), Secondary: Fear (31.2%), Antecedent: Joy (18.5%). Mixed Emotion: True. Narrative: 'Transitioned from joy into anger and fear'.")
    
    add_body_p(doc, "Case 2 (Token-Drop Saliency): 'I was terrified when the engine stalled on the highway.'")
    add_bullet(doc, "'terrified' (Position 2): ", "+0.6421 Saliency (Strong Positive Driver)")
    add_bullet(doc, "'stalled' (Position 7): ", "+0.1834 Saliency (Secondary Threat Indicator)")
    add_bullet(doc, "'engine' (Position 6): ", "+0.0095 Saliency (Neutral Context)")

    # SECTION 5: CONCLUSION & REFERENCES
    add_heading(doc, "4. Conclusion & Future Scope", level=1)
    add_body_p(doc, "INTELLIEMO successfully demonstrates that combining a fine-tuned transformer (DistilBERT) with a deterministic Discourse Reasoning Engine resolves the critical softmax peakiness problem in NLP. Achieving 92.70% accuracy with sub-100ms CPU latency and vectorized explainability proves that production-grade affective intelligence can run completely locally with high trust and privacy.")
    add_body_p(doc, "Future scope includes multimodal speech/facial emotion integration and expanding to the 28-class GoEmotions psychological taxonomy.")

    add_heading(doc, "5. References", level=1)
    refs = [
        "Vaswani, A., et al. (2017). Attention Is All You Need. NeurIPS 2017.",
        "Sanh, V., et al. (2019). DistilBERT: smaller, faster, cheaper and lighter. arXiv:1910.01108.",
        "Saravia, E., et al. (2018). CARER: Contextualized Affect Representations for Emotion Recognition. EMNLP 2018.",
        "Ribeiro, M. T., et al. (2016). 'Why Should I Trust You?': Explaining the Predictions of Any Classifier. ACM KDD 2016.",
        "Tiangolo, S. (2020). FastAPI Framework. https://fastapi.tiangolo.com"
    ]
    for r_text in refs:
        p_ref = doc.add_paragraph()
        p_ref.paragraph_format.space_before = Pt(2)
        p_ref.paragraph_format.space_after = Pt(4)
        run_ref = p_ref.add_run(r_text)
        run_ref.font.name = "Georgia"
        run_ref.font.size = Pt(10)

    print("Saving Word document to:", OUTPUT_DOCX)
    doc.save(str(OUTPUT_DOCX))
    print("Word document saved successfully.")

if __name__ == "__main__":
    build_docx()
