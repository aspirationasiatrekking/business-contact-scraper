
from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class SearchResult:
    title: str
    url: str
    snippet: str
    provider: str


class SearchProvider(ABC):

    @abstractmethod
    def search(self, query: str, max_results: int = 10) -> list[SearchResult]:
        pass
