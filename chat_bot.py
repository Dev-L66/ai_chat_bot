import os
from dotenv import load_dotenv
from openai import OpenAI
from transformers import AutoTokenizer
import time

load_dotenv()

my_api_key = os.getenv("GROQ_API_KEY")
access_token = os.getenv("HF_TOKEN")



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

           self.iteration = 0

    def trim_messages(self, max_number=4):
        if len(self.messages) < max_number:
            return
        system_messages = [m for m in self.messages if m["role"] =="system"]
        other_messages = [m for m in self.messages if m["role"] !="system"]
        trimmed_messages = other_messages[-max_number:]

        self.messages= [*system_messages, *trimmed_messages]

    def summarize_messages(self):
        if self.iteration % 5 != 0:
            return

        system_messages = [m for m in self.messages if m["role"] =="system"]
        other_messages = [m for m in self.messages if m["role"] !="system"]

        early_messages, last_messages = (other_messages[0:5],other_messages[5:])
        response = self.client.chat.completions.create(
                model="openai/gpt-oss-20b",
                temperature = 0.5
                messages=[{"role": "system", "content":"Summarize thses messages concisely, keeping key facts and decisions."}
                          ,*early_messages])
        summarized_message = {"role": "system","content":f"""This is summary of five early messages:{response.choices[0].message.content}"""}
        self.messages = [*system_messages, summarized_message, *last_messages]
        print("Summarization was successful")
    
    
    def bot(self,message):
        self.messages.append({"role":"user",
                  "content": message})
        response = self.client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=self.messages,
        stream = True)

        response_text = ""
        for chunk in response:
             if chunk.choices:
               delta = chunk.choices[0].delta.content
               if delta:
                    print(delta, end="", flush=True)
                    response_text += delta
                    time.sleep(0.05)
             if chunk.usage:
              self.total_tokens += chunk.usage.total_tokens
              self.input_tokens += chunk.usage.prompt_tokens
              self.output_tokens += chunk.usage.completion_tokens

        print()
               
 

       
        self.messages.append({"role":"assistant",
                  "content": response_text})

        self.summarize_messages()

        
        return response_text
    

    def chat(self):
        encoding = AutoTokenizer.from_pretrained("gpt2")
        while True:
            self.iteration += 1
            user_query = input("Ask something.... (type q to quit):").strip().lower()
    
            if user_query == "q":
                print("Good Luck")
                break
            token_count = len(encoding.encode(user_query))
            print(token_count)
            if token_count > 10:
                    print("Your prompt exceeded the limit. " \
                    "Try a shorter one, please.")
                    continue

            if self.total_tokens > 3000:
                 print("Unfortunately you exceeded the total token limit for today")
                 break
            
            self.bot(user_query)
            
    
    
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