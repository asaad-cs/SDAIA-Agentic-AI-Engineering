import logging
from openai import OpenAI
from state import ResearchState
from tools import tavily_search

logger = logging.getLogger(__name__)

MAX_ITERATIONS = 3

# OpenAI client — created after load_dotenv() runs in main.py
client = OpenAI()


def generate_query(state: ResearchState) -> dict:
    topic = state["topic"]
    iteration = state.get("iteration", 0)

    logger.info("Generating search query...")

    if iteration == 0:
        prompt = f"Generate a concise web search query for: {topic}\nReply with the query only."
    else:
        existing = "\n".join(state.get("results", []))[:800]
        prompt = (
            f"Topic: {topic}\nInfo gathered so far:\n{existing}\n\n"
            f"Generate a more specific follow-up search query. Reply with the query only."
        )

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
    )
    query = response.choices[0].message.content.strip()
    logger.info(f"Generated query: {query}")
    return {"query": query}


def web_search(state: ResearchState) -> dict:
    iteration = state.get("iteration", 0) + 1
    logger.info(f"Starting web search (Iteration {iteration})")
    new_results = tavily_search(state["query"])
    logger.info(f"Retrieved {len(new_results)} search result(s)")
    return {
        "results": state.get("results", []) + new_results,
        "iteration": iteration,
    }


def evaluate_results(state: ResearchState) -> dict:
    logger.info("Evaluating search results")

    if state.get("iteration", 0) >= MAX_ITERATIONS:
        logger.info("Max iterations reached")
        logger.info("Generating final report")
        return {"enough_info": True}

    combined = "\n\n".join(state.get("results", []))[:2000]
    prompt = (
        f"Topic: {state['topic']}\n\nInfo collected:\n{combined}\n\n"
        f"Is there enough information to write a research report? Reply YES or NO only."
    )
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
    )
    answer = response.choices[0].message.content.strip().upper()
    enough = answer.startswith("YES")
    logger.info(f"Enough information: {answer}")
    if enough:
        logger.info("Generating final report")
    else:
        logger.info("Continuing to another search iteration")
    return {"enough_info": enough}


def generate_report(state: ResearchState) -> dict:
    logger.info("Starting report generation")
    combined = "\n\n".join(state.get("results", []))
    prompt = (
        f"Write a research report about: {state['topic']}\n\n"
        f"Based on these search results:\n{combined}\n\n"
        f"Format: Introduction, Key Findings (bullet points), Conclusion."
    )
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5,
    )
    logger.info("Report generated successfully")
    return {"report": response.choices[0].message.content.strip()}
