# Project Context: Customer Segmentation and Retention Analysis

## Overview
This project focuses on analyzing customer data to identify distinct segments and understand factors influencing customer retention. The goal is to develop actionable insights that can inform marketing strategies, improve customer engagement, and reduce churn.

## Objectives
- Perform exploratory data analysis (EDA) on customer datasets.
- Apply clustering techniques (e.g., K-Means, hierarchical clustering) to segment customers based on behavior, demographics, and transactional patterns.
- Build predictive models to identify customers at risk of churn.
- Generate visualizations and reports to communicate findings to stakeholders.
- Provide recommendations for targeted retention campaigns.

## Current Status
- **Environment Setup**: Created CLAUDE.md and AGENTS.md files detailing setup and execution instructions for the agent-based workflow.
- **Dependencies**: A `requirements.txt` file is expected to contain necessary Python packages (e.g., pandas, numpy, scikit-learn, matplotlib, seaborn).
- **Scripts**: The `scripts/` directory is intended to house the main agent script (`run_agent.py`) and any supporting modules.
- **Data**: Customer data files (CSV, Excel, or SQL) should be placed in a designated `data/` directory (to be created).
- **Agent Framework**: Instructions are in place for a virtual environment, prompt handling, and execution of `run_agent.py` to process user queries and produce outputs.

## Next Steps
1. **Data Acquisition**: Obtain and place the customer dataset in the `data/` folder.
2. **Requirement Definition**: Finalize the list of Python packages in `requirements.txt`.
3. **Script Development**: Implement `run_agent.py` to:
   - Load and preprocess the data.
   - Execute segmentation and retention analysis based on user prompts.
   - Output results (clusters, churn predictions, visualizations) in a user-friendly format.
4. **Testing**: Run the agent with sample prompts to verify functionality.
5. **Documentation**: Update this CONTEXT.md as milestones are reached.

## Notes
- Ensure the virtual environment is activated before running any scripts.
- The agent is designed to accept a user prompt, process it through the analysis pipeline, and return structured outputs.
- All code should follow best practices for readability, modularity, and reproducibility.

---
*Last updated: 2026-08-15*