# AI-Assisted HARA Workflow

--

## System Definition & Functional Decomposition (Human + AI)

**Human Input**  
    +Define system boundaries, functions, operational scenarios (use cases, driving conditions).

**AI Support**
    +Use NLP to analyze system architecture documents, requirements specs, and extract key functional elements.
    +Generate draft functional block diagrams and data flow mappings.

✅ Tools: GPT-based NLP processors, requirement mining tools (e.g., IBM DOORS + AI plugin).

---

## Hazard Identification (AI-Supported Brainstorming)

**Human Input**
    + Use domain expertise to lead a structured brainstorming session (e.g., HAZOP, FMEA).

**AI Support**
    + Suggest potential hazards based on similar system components (leveraging a trained model on incident/hazard databases).
    + Use generative AI to propose hazards from system use cases, abnormal conditions, and edge scenarios.

✅ Example: "Given an ADAS braking system, AI suggests hazards like 'unintended deceleration in tunnel due to GPS signal loss.'"

---

## Risk Estimation & Classification (AI-Augmented Assessment)

**Human Input**
    + Define Severity (S), Exposure (E), and Controllability (C) based on ISO 26262.

**AI Support**
    + Predict preliminary ASIL values based on similar past assessments.
    + Recommend risk levels using machine learning trained on prior HARA data.
    + Flag inconsistencies or missing risk attributes.

✅ Note: AI can suggest but must not decide final ASIL levels—human engineers make that call.

---

## Mitigation Strategy Generation (AI-Aided Recommendations)

**Human Input**
    + Review possible safety goals and functional safety requirements.

**AI Support**
    + Suggest mitigation strategies or safety mechanisms based on the hazard.
    + Recommend architectural changes, redundancy techniques, or software mitigations using a knowledge base.

✅ Example: For a hazard like "loss of steering assist," AI suggests "fallback to mechanical steering + torque reduction."

---

## Documentation & Traceability (AI for Drafting & Linking)
**AI Support**
    + Generate draft HARA tables and reports (ASIL tables, safety goals, and traceability matrices).
    + Automatically link hazard items to system requirements, architecture components, and test cases.

✅ Tools: Use LLMs + document automation tools (e.g., Rasa, Sphinx, LaTeX automation).

---

## Review & Validation (Human-Centric + Explainable AI)

**Human Input**
    + Conduct a formal safety review.
    + Verify traceability, assumptions, and rationale.

**AI Support** 
    + Use explainable AI (XAI) tools to provide reasoning paths for risk estimation.
    + Flag anomalies or deviations from previous similar systems.

---

## Optional Add-ons
Integration with Safety Tools:

Embed the AI workflow within tools like Medini Analyze, PTC Integrity, or Ansys SCADE.

## Closed-Loop Learning

Feed incident reports, field data, or validation feedback back into the AI system to improve future hazard predictions.

--

# Summary Diagram 
``` bash
[ System Definition ]
        ↓
[ Hazard Identification ] ←→ [ AI Suggestion Engine ]
        ↓
[ Risk Estimation (S, E, C) ] ←→ [ AI Risk Predictor ]
        ↓
[ Mitigation Strategy Selection ] ←→ [ AI Knowledge Base ]
        ↓
[ Documentation & Traceability ] ←→ [ AI Drafting & Linking ]
        ↓
[ Human Review & Validation ] ←→ [ Explainable AI Outputs ]
```
