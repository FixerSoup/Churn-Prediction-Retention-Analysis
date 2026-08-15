---
name: use-visual-mind-maps-for-better-understanding
description: >
  Skill for leveraging visual mind maps located in the
  'visual mindmaps for easy understanding' directory to deepen
  comprehension of the Customer Segmentation and Retention Analysis
  project. Claude should read, interpret, and reference these mind
  maps when answering questions, ensuring explanations are grounded
  in the visualized structure and relationships, leading to more
  accurate and precise results.
---

# Use Visual Mind Maps for Better Understanding — Skill

## 🎯 Skill Purpose

This skill ensures that when Claude works on this project, it actively
considers the visual mind maps stored in  
`Customer Segmntation and retention analysis\visual mindmaps for easy understanding`
to:

- Grasp the high‑level architecture and workflow of the project.
- Understand how data flows from raw input to cleaned data, segmentation,
  modeling, and reporting.
- Recall the relationships between key components (e.g., which scripts
  produce which artifacts, how features are engineered, where models are
  saved).
- Provide answers that are consistent with the visualized logic, reducing
  the chance of overlooking a step or mis‑interpreting a dependency.

## 📂 Where to Find the Mind Maps

All mind‑map files are located under:

```
Customer Segmntation and retention analysis\visual mindmaps for easy understanding\
```

Supported formats (as of this project):

- Markdown (`.md`) – text‑based outlines that can be read directly.
- Images (`.png`, `.jpg`, `.jpeg`) – diagrams that Claude can interpret
  via its vision capabilities (if enabled) or by reading accompanying
  alt‑text/captions.
- Mermaid diagrams (`.mmd`) – if present, Claude can render them
  mentally to understand the flow.

## 🛠️ How to Use the Skill

When you invoke this skill (e.g., via `/use-visual-mind-maps-for-better-understanding`
or when the system automatically loads it because the user’s request
mentions the project), Claude should:

1. **List the files** in the mind‑map directory to know what is available.
2. **Read each file**:
   - For `.md` files: ingest the full content.
   - For image files: if vision is enabled, describe the diagram; otherwise,
     look for any accompanying `.txt` or `.md` file with the same stem that
     contains a description.
   - For `.mmd` files: parse the Mermaid syntax to understand the flowchart.
3. **Synthesize a mental model** of the project based on the mind maps:
   - Identify the sequence: data loading → cleaning → feature engineering
     → clustering → model training → evaluation → report generation.
   - Note where each script (`load_data.py`, `segmentize_customers_by_clustering.py`,
     `train_model.py`, `run_agent.py`, etc.) fits in the flow.
   - Recognize which artifacts are intermediate (e.g., `clean_clustered.csv`,
     `feature_importance.csv`) and which are final outputs (reports, models).
4. **Reference the mind map** in your explanations:
   - When asked about a step, say “As shown in the mind map `X`, …”.
   - When debugging, point to the relevant block in the diagram.
   - When suggesting improvements, relate them to a missing or weak link
     visible in the mind map.
5. **Validate your answer** against the visualized flow:
   - Ensure no step is omitted or reordered incorrectly.
   - Confirm that any script you mention actually exists in the location
     indicated by the mind map.

## 📋 Example Interaction

**User:** “Can you explain how the clustering step feeds into the churn‑prediction model?”

**Claude (using the skill):**  
“Looking at the mind map `project_overview.md` in the visual mindmaps folder,
the flow is:

1. `load_data.py` → raw CSV → `data/raw_data/data.csv`
2. `segmentize_customers_by_clustering.py` → adds cluster labels →  
   `data/cleaned_data/clean_clustered.csv`
3. `train_model.py` reads `clean_clustered.csv`, trains the RandomForest
   pipeline, and saves it to `models/churn_prediction_pipeline.pkl`.

Thus, the clustering step produces the `clean_clustered.csv` file that
the model‑training script consumes directly. This ensures the model is
trained on data that already includes the cluster identifier as a feature.”

## 📝 Quality Rules

- Always verify that the mind‑map file you reference actually exists;
  if a file is missing, fall back to reading the source code or scripts.
- When describing an image, provide a concise textual summary of the
  nodes and edges visible.
- Keep the explanation tied to the visualized flow; avoid introducing
  concepts that are not present in the mind maps unless you explicitly
  label them as extensions or suggestions.
- If the user asks for a detail not covered in the mind maps, you may
  supplement with code inspection, but first state what the mind map shows
  and then note any additional information you found.

## 🔄 Update History

- **2026‑08‑15**: Initial version – defines how to use visual mind maps
  located in `visual mindmaps for easy understanding` to improve
  project comprehension and answer accuracy.

--- 

*Invoke this skill whenever you need a holistic, visual‑grounded
understanding of the project structure, data flow, or component
dependencies.* 