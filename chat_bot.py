import os
import tiktoken
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

my_api_key = os.getenv("GROQ_API_KEY")


total_tokens = 0

class ChatBot:
    def __init__(self):
           self.client = OpenAI(api_key=my_api_key,
       base_url="https://api.groq.com/openai/v1")

           self.messages = [
     {
          "role": "system",
          "content": """You're a helpful assistant your name is Alexa.
                       Introduce yourself in the first message.
                       Give short helpful answers."""
     }
]

           self.total_tokens = 0
           self.input_tokens = 0
           self.output_tokens = 0

    def bot(self,message):
        self.messages.append({"role":"user",
                  "content": message})
        response = self.client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=self.messages)

        response_text = response.choices[0].message.content
        self.messages.append({"role":"assistant",
                  "content": response_text})

        self.total_tokens += response.usage.total_tokens
        self.input_tokens += response.usage.prompt_tokens
        self.output_tokens += response.usage.completion_tokens
        return response_text

    def chat(self):
        encoding = tiktoken.get_encoding("cl100k_base")
        while True:
            user_query = input("Ask something.... (type q to quit):").strip().lower()
    
            if user_query == "q":
                print("Good Luck")
                break
            token_count = len(encoding.encode(user_query))
            if token_count > 10:
                    print("Your prompt exceeded the limit. Try a shorter one, please.")
                    continue
            answer = self.bot(user_query)
            print(answer)
    
    
    def report(self):
        for message in self.messages:
            print(message)
        print(f"Consumed tokens:{self.total_tokens}")
        print(f"${(self.input_tokens * 0.05 + self.output_tokens * 0.08)/1_000_000}")
    


def main():
    bot = ChatBot()
    bot.chat()
    bot.report()
    

if __name__ == "__main__":
    main()