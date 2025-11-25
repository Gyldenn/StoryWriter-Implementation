from .base_agent import BaseAgent
import json

INITIAL_EVENT_PROMPT = """
You are an Event Generator.

Your task is to create a new high-level story event for a narrative based on the concept:

{story_concept}

Event index: {index}

Previous approved events:
{previous_events}

You MUST return a valid JSON object:
{{
  "title": "...",
  "description": "...",
  "characters": [...],
  "location": "...",
  "conflict": "..."
}}
"""


REVISION_PROMPT = """
You are an Event Rewriter.

The event below needs revision based on validator feedback.

Event:
{event}

Feedback:
{feedback}

Rewrite the event so that it addresses the feedback while staying consistent with all previously approved events:
{other_events}

Return ONLY a JSON object with the same fields as before.
"""

class EventSeed(BaseAgent):

  def generate_initial_event(self, story_concept, index, previous_events):
    prompt = INITIAL_EVENT_PROMPT.format(
      story_concept=story_concept,
      index=index,
      previous_events=json.dumps(previous_events, indent=2)
    )
    raw = self.call_llm(prompt)

    try:
      return json.loads(raw)
    except:
      return {"title": "Invalid JSON Event", "raw": raw}

  def revise_event(self, event, feedback, other_events):
    prompt = REVISION_PROMPT.format(
      event=json.dumps(event, indent=2),
      feedback=json.dumps(feedback, indent=2),
      other_events=json.dumps(other_events, indent=2)
    )
    raw = self.call_llm(prompt)

    try:
      return json.loads(raw)
    except:
      return event  # fallback

  def run(self, *args, **kwargs):
    raise NotImplementedError