# Project Setup and Agent Instructions

## Environment Setup

### Virtual Environment Creation
- **Windows**: `python -m venv venv`
- **Mac/Linux**: `python3 -m venv venv`

### Activate Virtual Environment
- **Windows**: `venv\Scripts\activate.bat`
- **Mac/Linux**: `source venv/bin/activate`

### Install Dependencies
```bash
pip install -r requirements.txt
```

## Running the Agent

### Navigate to Scripts Folder
```bash
cd scripts
```

### Execute the Agent
```bash
python run_agent.py
```
*Upon execution, the script will prompt you to enter a prompt. Type your question or instruction and press Enter. The agent will then process the input and display the output.*

## Agent Behavior
The agent should:
1. Inject the user's prompt into the prompt input section properly
2. Process the prompt and generate outputs
3. Display the outputs neatly in the display section

## Notes
- Ensure you are in the project root directory when setting up the virtual environment
- The `requirements.txt` file should be present in the project root
- The `run_agent.py` script should be located in the `scripts` folder
- The script uses `input()` to capture the user's prompt; provide your prompt when asked.