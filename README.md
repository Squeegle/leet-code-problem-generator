# AI Agent with Ollama and LangChain

This project implements an AI agent using a locally hosted Llama model through Ollama and LangChain.

## Prerequisites

1. Install [Ollama](https://ollama.ai/) on your system
2. Pull the Llama2 model:
   ```bash
   ollama pull llama2
   ```

## Setup

1. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the example script:
```bash
python agent.py
```

## Features

- Uses Ollama to run Llama2 model locally
- Implements a basic agent with tools
- Maintains conversation history
- Includes example tools for:
  - Knowledge base search (placeholder)
  - Getting current time

## Customization

You can customize the agent by:
1. Adding new tools in the `_create_tools` method
2. Modifying the system prompt in `_create_agent`
3. Using different Ollama models by changing the `model_name` parameter

## Note

Make sure Ollama is running in the background before using the agent. You can start Ollama with:
```bash
ollama serve
``` 