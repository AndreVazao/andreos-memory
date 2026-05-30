import os
from typing import List, Dict, Any

# Import index engine
from core.index.memory_index_engine import search_memory

MEMORY_PATH = os.getenv("ANDREOS_MEMORY", r"C:\ProgramasGodmode\andreos-memory")

class MemoryRouter:
    """
    Memory Intelligence Router
    --------------------------
    This module acts as the cognitive filtering layer between raw stored memory
    and any external agent (Obsidian, Cloud Desktop, Antigravity, IDEs).

    It decides WHAT is relevant and WHY, based on query intent.
    """

    def __init__(self):
        self.context_cache = {}

    def retrieve_context(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """
        Core retrieval function.
        Returns ranked memory fragments relevant to query.
        """
        raw_results = search_memory(query, limit=limit)

        structured = []
        for score, path, timestamp, snippet in raw_results:
            structured.append({
                "score": score,
                "path": path,
                "timestamp": timestamp,
                "snippet": snippet
            })

        return structured

    def build_context_packet(self, query: str, max_tokens_estimate: int = 2000) -> Dict[str, Any]:
        """
        Builds a compact context packet for AI agents.
        This is the main integration point for LLMs.
        """
        results = self.retrieve_context(query)

        context_blocks = []
        total_chars = 0

        for r in results:
            block = f"[MEMORY]\nPATH: {r['path']}\nTIME: {r['timestamp']}\nCONTENT: {r['snippet']}\n"
            block_size = len(block)

            if total_chars + block_size > max_tokens_estimate * 4:  # rough token estimate
                break

            context_blocks.append(block)
            total_chars += block_size

        packet = {
            "query": query,
            "context": "\n---\n".join(context_blocks),
            "sources": [r["path"] for r in results],
            "count": len(context_blocks)
        }

        return packet

    def explain_relevance(self, query: str) -> Dict[str, Any]:
        """
        Lightweight explanation layer (debug + transparency)
        """
        results = self.retrieve_context(query)

        explanation = []
        for r in results:
            explanation.append({
                "file": r["path"],
                "why_relevant": f"Matched query tokens in stored memory (score={r['score']})",
                "timestamp": r["timestamp"]
            })

        return {
            "query": query,
            "analysis": explanation
        }

    def live_memory_feed(self, query: str):
        """
        Stream-style memory access (future integration with agents)
        """
        results = self.retrieve_context(query)

        for r in results:
            yield {
                "event": "memory_chunk",
                "path": r["path"],
                "content": r["snippet"],
                "score": r["score"]
            }


# Singleton instance for system-wide usage
router = MemoryRouter()


if __name__ == "__main__":
    print("[MEMORY ROUTER] Initializing...")
    test_query = "sync system memory"

    r = MemoryRouter()
    packet = r.build_context_packet(test_query)

    print("\n--- CONTEXT PACKET ---\n")
    print(packet["context"])

    print("\n--- SOURCES ---\n")
    print(packet["sources"])
