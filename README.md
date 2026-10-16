# Agentic AI Labs

Two hands-on Python labs for learning how LLM agents use tools. Both examples
use fictional, in-memory data and do not perform real-world actions.

## Requirements

- Python 3.10 or newer
- An OpenRouter API key to run either LLM-backed agent

Install each lab's requirements separately. The examples use separate
dependencies so you only need to install the lab you want to try.

## Lab 1: ReAct agent

This lab demonstrates a ReAct (Reason, Act, Observe) loop implemented directly
with the Anthropic SDK using OpenRouter. The library assistant can search a
small book catalog and check book availability.

From the repository root, create a local environment file from the placeholder
template and add your own key:

```powershell
Copy-Item agentic_ai_lab\lab1_react_agent\.env.example agentic_ai_lab\lab1_react_agent\.env
```

Edit `agentic_ai_lab\lab1_react_agent\.env`, replacing
`YOUR_OPENROUTER_API_KEY_HERE` with your key. Do not commit `.env`.

Install and run:

```powershell
python -m pip install -r agentic_ai_lab\lab1_react_agent\requirements.txt
python -m agentic_ai_lab.lab1_react_agent.main
```

Pass a question as an argument:

```powershell
python -m agentic_ai_lab.lab1_react_agent.main "Find fantasy books and check The Hobbit"
```

## Lab 2: Custom agent with tools

This lab creates a LangChain agent and supplies custom plant-care and watering
calculation tools. The agent chooses tools based on the question.

Create the environment file and add your own key:

```powershell
Copy-Item agentic_ai_lab\lab2_custom_agent_tools\.env.example agentic_ai_lab\lab2_custom_agent_tools\.env
```

Edit `agentic_ai_lab\lab2_custom_agent_tools\.env`, replacing
`YOUR_OPENROUTER_API_KEY_HERE` with your key. Do not commit `.env`.

Install and run:

```powershell
python -m pip install -r agentic_ai_lab\lab2_custom_agent_tools\requirements.txt
python -m agentic_ai_lab.lab2_custom_agent_tools.main
```

Pass a question as an argument:

```powershell
python -m agentic_ai_lab.lab2_custom_agent_tools.main "How should I care for basil?"
```

## Run tests

The unit tests cover both labs' tool logic and the Lab 1 ReAct orchestration
with a fake model response. They do not need an API key or network access.

```powershell
python -m unittest discover -s agentic_ai_lab -p "test_*.py" -v
```

## Lab structure

```text
agentic_ai_lab/
    lab1_react_agent/
        agent.py          # ReAct model/tool loop
        tools.py          # Library catalog tools and schemas
        main.py           # Command-line entry point
        .env.example      # Placeholder configuration
        requirements.txt
        test_agent.py
        test_tools.py
    lab2_custom_agent_tools/
        agent.py          # LangChain model/tool orchestration
        tools.py          # Custom LangChain tool definitions
        logic.py          # Plant-care data and calculations
        main.py           # Command-line entry point
        .env.example      # Placeholder configuration
        requirements.txt
        test_logic.py
```
