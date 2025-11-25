import json
from agents.base_agent import BaseAgent

WRITER_PROMPT = """
You are the FinalWriter.
Write 1–3 paragraphs of narrative prose based on:

Sub-event:
{sub_event}

Instructions:
{instructions}

NO JSON. Only story text.
"""

class FinalWriter(BaseAgent):

    def write_sub_event(self, sub_event, instructions):
        prompt = WRITER_PROMPT.format(
            sub_event=json.dumps(sub_event, indent=2),
            instructions=instructions
        )
        raw = self.call_llm(prompt)

        # If model accidentally returns JSON:
        try:
            parsed = json.loads(raw)
            if isinstance(parsed, dict) and "text" in parsed:
                return parsed["text"]
        except:
            pass

        return raw.strip()

    def run(self, *args, **kwargs):
        raise NotImplementedError
