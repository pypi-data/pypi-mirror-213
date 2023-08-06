from database_manager import DatabaseManager
from generator import Generator

class Expander:
    def __init__(self):
        self.generator = Generator()
        self.db_manager = DatabaseManager()

    def base_expansion(self, prompt_parts: list) -> str:
        return "\n\n".join(prompt_parts)

    def expansion_generator(self, user_prompt: str, filename="expansion_generator_prompt.txt") -> list:
        expansion_prompt = self.db_manager.read(2, filename)
        full_prompt = self.base_expansion([expansion_prompt, user_prompt])
        expansion_text = self.generator.base_generation(full_prompt)
        return expansion_text.split("\n")