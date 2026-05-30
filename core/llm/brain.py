import os
from typing import List, Dict, Any

try:
    from openai import OpenAI
except Exception:
    OpenAI = None

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MODEL = os.getenv("ANDREOS_LLM_MODEL", "gpt-4.1-mini")

class LLMBrain:
    """
    Real AI cognition layer.
    Wraps OpenAI (or compatible) LLM API.
    """

    def __init__(self):
        if OpenAI and OPENAI_API_KEY:
            self.client = OpenAI(api_key=OPENAI_API_KEY)
            self.enabled = True
        else:
            self.client = None
            self.enabled = False

    def chat(self, system: str, user: str) -> str:
        if not self.enabled:
            return f"[LLM DISABLED] SYSTEM:\n{system}\nUSER:\n{user}"

        resp = self.client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user}
            ]
        )

        return resp.choices[0].message.content

    def plan(self, task: str, context: str) -> str:
        return self.chat(
            system="You are a planning agent. Break tasks into clear actionable steps.",
            user=f"TASK:\n{task}\n\nCONTEXT:\n{context}"
        )

    def code(self, task: str, context: str, plan: str) -> str:
        return self.chat(
            system="You are a senior software engineer. Produce correct, production-grade code.",
            user=f"TASK:\n{task}\n\nPLAN:\n{plan}\n\nCONTEXT:\n{context}"
        )

    def review(self, task: str, code: str) -> str:
        return self.chat(
            system="You are a strict code reviewer. Find bugs and improvements.",
            user=f"TASK:\n{task}\n\nCODE:\n{code}"
        )


brain = LLMBrain()