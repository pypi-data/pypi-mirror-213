
import openai
from database_manager import DatabaseManager

class Generator:
    def __init__(self, engine="gpt-3.5-turbo", api_key=""):
        self.engine = engine
        self.api_key = api_key
        openai.api_key = api_key
        self.conversation_log = []
        self.db_manager = DatabaseManager()
        
    def display_info(self):
        print("Engine: " + self.engine + '\n' +
              "API Key: " + self.api_key)
    
    def base_generation(self, prompt, memory=False, token=300, temperature=0.5):
        self.conversation_log.append({"role": "user", "content": prompt})
        response = openai.ChatCompletion.create(
            model=self.engine,
            messages=self.conversation_log,
            max_tokens=token,
            temperature=temperature,
        )
        response_content = response.choices[0].message.content.strip()
        if memory:
            self.conversation_log.append({"role": "system", "content": response_content})
        else:
            self.conversation_log.pop()
        return response_content

    def multi_generation(self, prompt, number=1, memory=False):
        responses = [self.base_generation(prompt, memory) for _ in range(number)]
        return responses
