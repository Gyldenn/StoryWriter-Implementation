import json
from agents.base_agent import BaseAgent

CHAPTER_WEAVER_PROMPT = """
You are a Chapter Planner.

Group the following sub-events into chronological narrative chapters.

Output strictly:
{
  "chapters": [
    {
      "chapter_id": 1,
      "summary": "...",
      "sub_events": [...]
    }
  ]
}
"""

class Chapter:
    def __init__(self, chapter_id, summary, sub_events):
        self.chapter_id = chapter_id
        self.summary = summary
        self.sub_events = sub_events

class ChapterWeaver(BaseAgent):

    def assign_to_chapters(self, sub_events):
        prompt = CHAPTER_WEAVER_PROMPT + "\n\nSub-events:\n" + json.dumps(sub_events, indent=2)
        raw = self.call_llm(prompt)

        try:
            parsed = json.loads(raw)
        except:
            return [Chapter(1, "Invalid JSON chapter", sub_events)]

        chapters_data = parsed.get("chapters", [])
        chapters = []

        for ch in chapters_data:
            chapters.append(Chapter(
                chapter_id=ch.get("chapter_id", len(chapters)+1),
                summary=ch.get("summary", ""),
                sub_events=ch.get("sub_events", [])
            ))

        return chapters

    def run(self, *args, **kwargs):
        raise NotImplementedError
