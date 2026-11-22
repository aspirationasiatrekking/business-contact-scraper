
from ddgs import DDGS
from ddgs.exceptions import DDGSException


def search_web(query, max_results=10):
    try:
        with DDGS(timeout=30) as search:
            results = search.text(
                query,
                max_results=max_results,
                region="wt-wt"
            )

        return results

    except DDGSException as error:
        print(f"Search service error: {error}")
        return []

    except Exception as error:
        print(f"Unexpected search error: {error}")
        return []
