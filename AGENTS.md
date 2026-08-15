# Agent Execution Instructions

When the user provides a prompt, follow these steps in order to set up and run the agent:

## 1. Environment Setup
- Create virtual environment:
  - Windows: `python -m venv venv`
  - Mac/Linux: `python3 -m venv venv`
- Activate virtual environment:
  - Windows: `venv\Scripts\activate.bat`
  - Mac/Linux: `source venv/bin/activate`
- Install dependencies: `pip install -r requirements.txt`

## 2. Navigate to Scripts Folder
```bash
cd scripts
```

## 3. Prepare User Prompt
- Capture the user's injected prompt.
- Ensure the prompt is properly formatted for input to `run_agent.py`.

## 4. Run the Agent
Execute the agent script with the user's prompt:
```bash
python run_agent.py "<USER_PROMPT>"
```
*(If the script expects the prompt via stdin or another method, adjust accordingly.)*

## 5. Display Output
- Capture the output from `run_agent.py`.
- Present the output neatly to the user in the display section.

## Notes
- Ensure you are in the project root before starting the setup.
- The virtual environment should be activated before installing dependencies and running the script.
- If any step fails, stop and report the error to the user.
- After execution, you may deactivate the virtual environment (optional).
