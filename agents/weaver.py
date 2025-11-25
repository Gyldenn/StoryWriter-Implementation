from .base_agent import BaseAgent
import json


PROMPT = """
You are an event weaver. Given N events, create a coherent outline that specifies order, possible short cause-effect connections 
and tone labels. Return JSON: {{ "outline": [... events ...] }}
Events: {events}
"""

class Weaver(BaseAgent):
    def __init__(self, llm_client):
        super().__init__(llm_client, "Weaver", PROMPT)

    def run(self, events: list):
        prompt = self.prompt_template.format(events=json.dumps(events))
        raw = self.call_llm(prompt, max_tokens=512, temperature=0.6)
        try:
            return json.loads(raw)
        except Exception:
            return {"raw": raw}
