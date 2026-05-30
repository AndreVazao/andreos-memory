import os
from typing import Dict, Any

from core.router.memory_router import router

MEMORY_PATH = os.getenv("ANDREOS_MEMORY", r"C:\ProgramasGodmode\andreos-memory")

class MemoryContextInjector:
    """
    MEMORY OS FINAL LAYER
    ---------------------
    This is the injection layer that transforms raw system memory
    into LLM-ready context payloads.

    It is designed to be embedded into:
    - IDEs (VSCode / Cloud Desktop / Antigravity)
    - AI Agents
    - CLI tools
    - Backend services
    """

    def __init__(self):
        self.router = router

    def inject(self, query: str, max_tokens: int = 2000) -> Dict[str, Any]:
        """
        Main injection pipeline.
        Returns a fully structured context packet for LLM consumption.
        """

        packet = self.router.build_context_packet(
            query=query,
            max_tokens_estimate=max_tokens
        )

        enriched_packet = {
            "system": "ANDREOS_MEMORY_OS",
            "memory_root": MEMORY_PATH,
            "query": query,
            "context": packet["context"],
            "sources": packet["sources"],
            "meta": {
                "engine": "andreos-memory",
                "mode": "context-injection",
                "compression": "light",
                "token_budget": max_tokens
            }
        }

        return enriched_packet

    def inject_minimal(self, query: str) -> str:
        """
        Lightweight injection for fast agents.
        Returns raw context string only.
        """
        packet = self.inject(query)
        return packet["context"]

    def inject_debug(self, query: str) -> Dict[str, Any]:
        """
        Full debug view including relevance analysis.
        """
        packet = self.inject(query)
        explanation = self.router.explain_relevance(query)

        return {
            **packet,
            "debug": explanation
        }

    def stream_injection(self, query: str):
        """
        Stream memory injection for real-time agents.
        """
        for chunk in self.router.live_memory_feed(query):
            yield {
                "type": "memory_stream",
                "payload": chunk
            }


# Global singleton
injector = MemoryContextInjector()


if __name__ == "__main__":
    print("[MEMORY INJECTOR] Initializing final layer...")

    test_query = "system sync architecture"

    i = MemoryContextInjector()
    result = i.inject_debug(test_query)

    print("\n--- CONTEXT ---\n")
    print(result["context"])

    print("\n--- SOURCES ---\n")
    print(result["sources"])

    print("\n--- DEBUG ---\n")
    print(result["debug"])
