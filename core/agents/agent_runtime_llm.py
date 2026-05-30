from typing import Dict, Any

from core.injector.memory_context_injector import injector
from core.llm.brain import brain


class LLMAgentRuntime:
    """
    Real cognitive multi-agent runtime.
    Uses LLMBrain instead of simulation.
    """

    def __init__(self):
        self.brain = brain

    def execute(self, task: str) -> Dict[str, Any]:
        # 1. Memory injection
        context = injector.inject(task)
        context_text = context.get("context", "")

        # 2. Planning (LLM)
        plan = self.brain.plan(task, context_text)

        # 3. Coding (LLM)
        code = self.brain.code(task, context_text, plan)

        # 4. Review (LLM)
        review = self.brain.review(task, code)

        return {
            "task": task,
            "context": context_text,
            "plan": plan,
            "code": code,
            "review": review,
            "sources": context.get("sources", [])
        }


# Global runtime
llm_runtime = LLMAgentRuntime()


if __name__ == "__main__":
    result = llm_runtime.execute("optimize memory routing system")

    print("\n--- PLAN ---\n", result["plan"])
    print("\n--- CODE ---\n", result["code"])
    print("\n--- REVIEW ---\n", result["review"])
