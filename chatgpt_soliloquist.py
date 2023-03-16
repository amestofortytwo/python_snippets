// Unpolished code to make chatgpt talk to itself. It may help you spark up new ideas or anything else..


import requests
import time

class OpenAIChatbot:
    def __init__(self, api_key):
        self.api_key = api_key
        self.model = 'text-davinci-003'
        self.endpoint = "https://api.openai.com/v1/completions"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }
        self.chat_log = ""

    def generate_text(self, prompt):
        data = {
            "model": self.model,
            "prompt": prompt,
            "max_tokens": 3300,
        }

        response = requests.post(self.endpoint, headers=self.headers, json=data)
        response_json = response.json()
        try:
            text = response_json['choices'][0]['text']
        except:
            print(response_json)
            exit()
        return text

    def chat(self):
        prompt = input('You: \n')
        self.chat_log += f"ME: {prompt}\nAI:"
        response = self.generate_text(self.chat_log)
        print(response)
        self.chat_log += f"{response}\n"
        return response

    def chatcontinued(self, answer):
        prompt = answer
        #self.chat_log += f"ME: {prompt}\nAI:"
        response = self.generate_text(self.chat_log)
        print(response)
        print("--------------------------------------------------------------------------------------")
        self.chat_log += f"{response}\n"

if __name__ == '__main__':
    api_key = ""
    chatbot = OpenAIChatbot(api_key)
    first_reply = chatbot.chat()
    counter = 0
    while True:
        if counter == 10:
            break
        chatbot.chatcontinued(first_reply)
        time.sleep(5) # It seems that with this set to a low number the bot more often replies empty.
        counter += 1
