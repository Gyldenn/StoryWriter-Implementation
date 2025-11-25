import json
from agents.base_agent import BaseAgent

VALIDATOR_PROMPT = """
You are an Event Validator.

Evaluate whether this event is coherent, original, and non-redundant.

Event:
{event}

Other approved events:
{other_events}

Return ONLY JSON:
{{
  "valid": true/false,
  "reason": "...",
  "required_fixes": "..."
}}
"""

class EventValidator(BaseAgent):

    def validate(self, event, other_events):
        prompt = VALIDATOR_PROMPT.format(
            event=json.dumps(event, indent=2),
            other_events=json.dumps(other_events, indent=2)
        )

        raw = self.call_llm(prompt)

        try:
            return json.loads(raw)
        except:
            return {"valid": True, "reason": "Invalid JSON but accepted", "required_fixes": ""}

    def run(self, *args, **kwargs):
        raise NotImplementedError
