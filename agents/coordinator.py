import json
from agents.base_agent import BaseAgent

INITIAL_INSTRUCTIONS_PROMPT = """
You are the Writing Coordinator.
Provide focused narrative instructions for the writer.

Return ONLY:
{{
  "instructions": "..."
}}
"""

REVIEW_WRITING_PROMPT = """
You are the Writing Reviewer.
Return ONLY:
{{
  "status": "...",
  "issues": "...",
  "rewrite_instructions": "..."
}}
"""

class Coordinator(BaseAgent):

    def initial_instructions(self, sub_event, chapter_context):
        prompt = INITIAL_INSTRUCTIONS_PROMPT.format(
            sub_event=json.dumps(sub_event, indent=2),
            chapter_context=chapter_context
        )
        raw = self.call_llm(prompt)

        try:
            return json.loads(raw).get("instructions", "")
        except:
            return "Write a coherent narrative following the sub-event."

    def review(self, text, sub_event, chapter_index):
        prompt = REVIEW_WRITING_PROMPT.format(
            text=text,
            sub_event=json.dumps(sub_event, indent=2),
            chapter_index=chapter_index
        )
        raw = self.call_llm(prompt)

        try:
            return json.loads(raw)
        except:
            return {
                "status": "needs_revision",
                "issues": "Invalid JSON.",
                "rewrite_instructions": "Rewrite clearly according to the sub-event."
            }

    def run(self, *args, **kwargs):
        raise NotImplementedError
