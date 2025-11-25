import json
from agents.base_agent import BaseAgent

SUBTASKER_PROMPT = """
You are a Sub-Event Decomposer.

Your goal is to break one high-level story event into 3–7 smaller sub-events.

Each sub-event:
{{
  "id": "...",
  "parent_event": "...",
  "description": "...",
  "purpose": "...",
  "characters": [...],
  "location": "..."
}}

Return ONLY a JSON list.
"""

class SubTasker(BaseAgent):

    def split_into_sub_events(self, event):
        prompt = SUBTASKER_PROMPT + "\n\nMain event:\n" + json.dumps(event, indent=2)

        raw = self.call_llm(prompt)

        try:
            return json.loads(raw)
        except:
            return [{"error": "Invalid JSON", "raw": raw, "parent_event": event.get("title", "?")}]

    def run(self, *args, **kwargs):
        raise NotImplementedError
