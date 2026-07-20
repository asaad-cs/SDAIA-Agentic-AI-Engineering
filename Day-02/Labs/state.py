from typing import TypedDict


class ResearchState(TypedDict):
    topic: str          # research topic entered by the user
    query: str          # current search query
    results: list       # accumulated search snippets
    iteration: int      # number of searches done so far
    enough_info: bool   # whether to stop searching
    report: str         # final generated report
