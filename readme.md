# Emotional vs Logical Chatbot

A dual-personality chatbot built with LangGraph that intelligently routes conversations to either an empathetic therapist agent or a logical assistant agent based on the nature of your message.

## Overview

This chatbot uses a classifier to analyze incoming messages and determine whether they require an emotional or logical response. Based on this classification, the message is routed to the appropriate specialized agent:

- **Therapist Agent**: Provides emotional support, validates feelings, and helps process emotions
- **Logical Agent**: Delivers factual, evidence-based responses with clear logical reasoning

## Features

- **Intelligent Message Classification**: Automatically determines the nature of your query
- **Dual Agent Architecture**: Specialized responses based on message type
- **State Management**: Maintains conversation context using LangGraph
- **Powered by Claude 3.5 Sonnet**: Uses Anthropic's advanced language model

## Prerequisites

- Python 3.8 or higher
- An Anthropic API key

## Installation

1. Clone this repository or download the code

2. Install required dependencies:
```bash
pip install langgraph langchain langchain-anthropic python-dotenv pydantic
```

3. Create a `.env` file in the project root and add your Anthropic API key:
```
ANTHROPIC_API_KEY=your_api_key_here
```

## Usage

Run the chatbot from the command line:

```bash
python main.py
```

Once running, simply type your messages at the prompt:

```
Message: I'm feeling really stressed about work lately
Assistant: [Empathetic therapist response]

Message: What's the capital of France?
Assistant: [Factual logical response]

Message: exit
Bye
```

Type `exit` to quit the chatbot.

## How It Works

The application uses a graph-based workflow with the following nodes:

1. **Classifier Node**: Analyzes the user's message and classifies it as either "emotional" or "logical"
2. **Router Node**: Directs the conversation flow based on classification
3. **Therapist Agent**: Handles emotional/therapeutic conversations
4. **Logical Agent**: Handles factual/logical queries

### Message Classification

Messages are classified as:
- **Emotional**: Requests for emotional support, therapy, feelings, or personal problems
- **Logical**: Requests for facts, information, logical analysis, or practical solutions

## Project Structure

```
.
├── main.py          # Main application file
├── .env             # Environment variables (API keys)
└── README.md        # This file
```

## Configuration

The chatbot uses Claude 3.5 Sonnet by default. You can modify the model by changing the initialization in `main.py`:

```python
llm = init_chat_model(
    "anthropic:claude-3-5-sonnet-latest"
)
```

## Example Interactions

**Emotional Query:**
```
Message: I had a fight with my best friend and I don't know what to do
Assistant: [Empathetic response addressing feelings and providing emotional support]
```

**Logical Query:**
```
Message: How does photosynthesis work?
Assistant: [Factual explanation with scientific details]
```

## Dependencies

- `langgraph`: Graph-based workflow orchestration
- `langchain`: LLM framework and utilities
- `pydantic`: Data validation and structured outputs
- `python-dotenv`: Environment variable management

## Limitations

- The chatbot does not maintain conversation history between sessions
- Classification is performed on individual messages without full conversation context
- Requires an active internet connection and valid API key

## Contributing

Feel free to fork this project and submit pull requests for improvements such as:
- Adding conversation history persistence
- Implementing multi-turn context awareness
- Adding additional specialized agents
- Enhancing the classification logic

## License

This project is open source and available for educational and personal use.

## Support

For issues related to:
- LangGraph: Visit [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- Anthropic API: Visit [Anthropic Documentation](https://docs.anthropic.com/)

---

**Note**: Always ensure your API keys are kept secure and never committed to version control.