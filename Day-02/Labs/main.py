import os
import logging
from dotenv import load_dotenv

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logging.getLogger("httpx").setLevel(logging.WARNING)  # suppress OpenAI HTTP logs
logger = logging.getLogger(__name__)

load_dotenv()  # must run before importing nodes (which creates the OpenAI client)

from graph import build_graph


def main():
    logger.info("Starting Research Agent")

    load_dotenv()
    logger.info("Environment loaded successfully")

    missing = [k for k in ("OPENAI_API_KEY", "TAVILY_API_KEY") if not os.environ.get(k)]
    if missing:
        logging.error(f"Missing API key(s): {', '.join(missing)}")
        logging.error("Create a .env file and add your keys.")
        return

    logger.info("API keys found: OPENAI_API_KEY, TAVILY_API_KEY")

    topic = input("\nResearch topic: ").strip()
    if not topic:
        return

    logger.info(f"Research topic: {topic}")
    logger.info("Starting graph execution")

    try:
        result = build_graph().invoke({
            "topic": topic,
            "query": "",
            "results": [],
            "iteration": 0,
            "enough_info": False,
            "report": "",
        })
    except Exception as e:
        logging.error(f"Unexpected error during graph execution: {e}")
        raise

    logger.info("Research Agent completed successfully")

    print("\n" + "=" * 50)
    print("  RESEARCH REPORT")
    print("=" * 50)
    print(result["report"])


if __name__ == "__main__":
    main()
