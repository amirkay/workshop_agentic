# 🧠 Agentic Systems Workshop

Build intelligent AI agents using **LangGraph**, **LangChain**, and **Streamlit**.

This workshop teaches you how to design and implement agentic systems through a practical fitness coaching application. You'll progressively build from a single agent to a multi-agent orchestrated system, learning core architectural patterns along the way.

---

## 🎯 What You'll Build

A **fitness coaching system** with AI agents that:
- Calculate nutrition requirements and provide dietary advice
- Design workout plans and training recommendations
- Intelligently route requests between specialized agents

**Focus**: Architecture and reasoning, not infrastructure or deployment.

---

## 🚀 Quick Start

### Prerequisites
- Docker & Docker Compose (available in the wsl on your ISIMA computers) or Python 3.11+
- Git
- OpenAI API key (provided during the workshop)

### Option A: Docker (Recommended)

```bash
# Clone the repository
git clone <REPO_URL>
cd agentic-workshop
```

Next create .env file in your project folder and create a variable OPENAI_API_KEY=sk-..

To get the api key value please go to this website: 
[HERE](https://eu.onetimesecret.com/secret/2hduz5j1mujtr28al17si9tjqb93w8d)

The passphrase will be provided during the workshop.


Next you can start the application.
If you are on an ISIMA computer, you need to type this command in your terminal for docker to start 

```bashtext
docker-rootless-init.sh
```
Then simply run the docker compose file :
```bash
docker compose up
```

Open your browser at **http://localhost:8501** to access the app.

### Option B: Local Python Environment

```bash
# Clone the repository
git clone <REPO_URL>
cd agentic-workshop

# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create environment file
echo "OPENAI_API_KEY=sk-..." > .env

# Run the application
streamlit run app.py
```

---

## 📚 Core Concepts

### 🤖 What is an Agent?

An agent combines:
- A language model with reasoning capabilities
- A clearly defined role and system prompt
- Optional tools it can invoke
- The ability to decide when and how to use those tools

In this workshop, each agent is implemented as a LangGraph workflow.

### 📝 System Prompts as Architecture

System prompts define:
- The agent's role and responsibilities
- Expected behavior and boundaries
- How to interact with tools
- Response formatting and style

**Key insight**: Prompts are architectural components, not just text.

### 🧩 LangGraph Workflows

LangGraph enables explicit reasoning models through:
- **State**: Conversation history and shared context
- **Nodes**: Agents or tool execution points
- **Edges**: Control flow and decision logic

A typical agent loop:
1. Call the language model
2. Check if tools are requested
3. Execute tools if needed, otherwise finish
4. Return results to the model or user

Example control flow:
```python
def should_continue(state):
    if last_message.tool_calls:
        return "tools"
    return END
```

### 📦 Graph State

The graph state maintains:
- Complete message history
- Shared context across reasoning steps
- Tool outputs and model responses
- Any custom data needed by your agents

LangGraph makes this state **explicit and inspectable**, enabling better debugging and understanding of agent behavior.

---

## 🏗️ Workshop Structure

### Step 1: Single Agent — Nutritionist

Build your first agent from scratch:
- **Role**: Nutrition advisor
- **Capabilities**: 
  - Calculate maintenance calories using tools
  - Explain nutritional concepts
  - Provide personalized dietary advice
- **Architecture**: One agent = one workflow

**Learning focus**: Agent fundamentals, tool integration, prompt design

### Step 2: Second Agent — Trainer (Your Task)

Extend the system by creating a second independent agent:
- **Role**: Fitness trainer
- **Capabilities**:
  - Design workout programs
  - Recommend training frequency
  - Balance strength vs cardio
  - Align with fitness goals
- **Your task**:
  - Design a dedicated system prompt
  - Reuse the agent creation patterns
  - Build an independent `trainer_agent`

**Learning focus**: Agent specialization, prompt engineering, parallel development

### Step 3: Multi-Agent Orchestration (Final Challenge)

Introduce intelligent request routing:
- **New component**: Orchestrator agent
- **Role**: Delegate requests to specialized agents
- **Key pattern**: Agents exposed as tools to other agents

The orchestrator:
1. Receives user requests
2. Analyzes intent
3. Routes to the appropriate specialist (nutrition or training)
4. Returns the final response

**HINTS**
- Transforming an agent into a tool can be a simple invoke on the agent itself. (Which you already know how to do)
- An orchestrator could be an agent, with sub-agents as tools and a simple orchestrating prompt.

**Learning focus**: Agent composition, delegation patterns, system design

---

## 🎓 Learning Objectives

By completing this workshop, you will understand:

✅ What AI agents truly are and how they work  
✅ Why prompts are architectural design decisions  
✅ How LangGraph models explicit reasoning loops  
✅ When multi-agent orchestration adds value  
✅ How to design clean, maintainable agentic systems  

---



**Ready to build your first agentic system? Let's get started! 🚀**