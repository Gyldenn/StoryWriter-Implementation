from llm import LLMClient

from agents.event_seed import EventSeed
from agents.event_validator import EventValidator
from agents.subtasker import SubTasker
from agents.chapter_weaver import ChapterWeaver
from agents.coordinator import Coordinator
from agents.final_writer import FinalWriter

DEFAULT_STORY_CONCEPT = """
A young archaeologist discovers an ancient artifact that manipulates memory.
"""

class Controller:

    def __init__(
        self,
        max_seed_iterations=5,
        max_writer_iterations=5,
        story_concept=DEFAULT_STORY_CONCEPT,
        model_path="./modelo_local/GGUF/modelo.gguf"
    ):
        self.max_seed_iterations = max_seed_iterations
        self.max_writer_iterations = max_writer_iterations
        self.story_concept = story_concept

        # ÚNICA INSTANCIA DEL MODELO
        self.llm = LLMClient(model_path=model_path, n_ctx=2048)

        # Instancia de agentes (todos reciben self.llm)
        self.event_seed = EventSeed(self.llm)
        self.event_validator = EventValidator(self.llm)
        self.subtasker = SubTasker(self.llm)
        self.chapter_weaver = ChapterWeaver(self.llm)
        self.coordinator = Coordinator(self.llm)
        self.final_writer = FinalWriter(self.llm)

    # 1. EVENTO PRINCIPAL
    def generate_events(self, n_events):
        approved = []
        for i in range(n_events):
            event = self.event_seed.generate_initial_event(
                story_concept=self.story_concept,
                index=i,
                previous_events=approved
            )

            for _ in range(self.max_seed_iterations):
                feedback = self.event_validator.validate(event=event, other_events=approved)

                if feedback["valid"]:
                    approved.append(event)
                    break

                event = self.event_seed.revise_event(event=event, feedback=feedback, other_events=approved)
            else:
                approved.append(event)

        return approved

    # 2. SUB-EVENTOS Y CAPÍTULOS
    def expand_and_weave(self, events):
        all_subs = []
        for ev in events:
            subs = self.subtasker.split_into_sub_events(ev)
            all_subs.extend(subs)
        return self.chapter_weaver.assign_to_chapters(all_subs)

    # 3. ESCRITURA FINAL
    def write_story(self, chapters):
        story = ""

        for ch_idx, chapter in enumerate(chapters):
            for subev in chapter.sub_events:

                instructions = self.coordinator.initial_instructions(
                    sub_event=subev,
                    chapter_context=ch_idx
                )

                for _ in range(self.max_writer_iterations):

                    text = self.final_writer.write_sub_event(
                        sub_event=subev,
                        instructions=instructions
                    )

                    validation = self.coordinator.review(
                        text=text,
                        sub_event=subev,
                        chapter_index=ch_idx
                    )

                    if validation["status"] == "approved":
                        story += text + "\n\n"
                        break

                    instructions = validation["rewrite_instructions"]

        return story

    # PIPELINE COMPLETO
    def run(self, n_events=6):
        events = self.generate_events(n_events)
        chapters = self.expand_and_weave(events)
        return self.write_story(chapters)

if __name__ == "__main__":
    print(Controller().run(n_events=6))
