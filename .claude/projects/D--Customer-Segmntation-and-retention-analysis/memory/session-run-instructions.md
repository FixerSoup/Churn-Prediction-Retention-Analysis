---
name: session-run-instructions
description: How to run the agent after setup: create venv, activate, install, cd scripts, run run_agent.py with prompt
metadata:
  type: project
---

To run the agent for this project:

1. **Create virtual environment**:
   - Windows: `python -m venv venv`
   - Mac/Linux: `python3 -m venv venv`

2. **Activate virtual environment**:
   - Windows: `venv\Scripts\activate.bat`
   - Mac/Linux: `source venv/bin/activate`

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Navigate to scripts folder**:
   ```bash
   cd scripts
   ```

5. **Run the agent with your prompt**:
   ```bash
   python run_agent.py "<YOUR_PROMPT_HERE>"
   ```
   Replace `<YOUR_PROMPT_HERE>` with the actual prompt you want the agent to process.

**Notes**:
- Ensure you are in the project root directory before starting.
- The virtual environment must be activated before installing dependencies and running the script.
- If the script expects input via stdin or another method, adjust the command accordingly.
- After execution, you may deactivate the virtual environment (optional).
