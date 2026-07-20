# Day 2 Lab — Autonomous Research AI Agent

An AI agent that researches any topic by searching the web and generating a report.

## Setup

1. Install packages:
   ```
   pip install -r requirements.txt
   ```

2. Create your `.env` file:
   ```
   copy .env.example .env
   ```
   Then open `.env` and add your `OPENAI_API_KEY` and `TAVILY_API_KEY`.

3. Run:
   ```
   python main.py
   ```

## How it works

```
START
  └─> generate_query   (OpenAI turns topic into a search query)
        └─> web_search      (Tavily fetches results)
              └─> evaluate_results  (OpenAI decides: enough info?)
                    │
                    ├── NO  ──> generate_query  (search again, max 3 times)
                    │
                    └── YES ──> generate_report (OpenAI writes the report)
                                      └─> END
```

## Files

| File | Purpose |
|---|---|
| `main.py` | Entry point — loads env, takes input, runs the agent |
| `graph.py` | Wires nodes into a LangGraph workflow |
| `nodes.py` | The four agent steps (query, search, evaluate, report) |
| `state.py` | Shared state passed between nodes |
| `tools.py` | Tavily web search wrapper |
