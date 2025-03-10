from groq import Groq
from .chatgptapi_translator import ChatGPTAPI
from os import linesep
from itertools import cycle


GROQ_MODEL_LIST = [
    "gemma2-9b-it",
    "llama-3.3-70b-versatile",
    "llama-3.1-8b-instant",
    "llama-guard-3-8b",
    "llama3-8b-8192",
    "llama3-70b-8192",
    "mixtral-8x7b-32768",
    "gemma-7b-it",
    "qwen-qwq-32b",
    "mistral-saba-24b",
    "qwen-2.5-32b",
    "deepseek-r1-distill-qwen-32b",
    "deepseek-r1-distill-llama-70b-specdec",
    "deepseek-r1-distill-llama-70b",
    "llama-3.3-70b-specdec",
]


class GroqClient(ChatGPTAPI):
    def rotate_model(self):
        if not self.model_list:
            model_list = list(set(GROQ_MODEL_LIST))
            print(f"Using model list {model_list}")
            self.model_list = cycle(model_list)
        self.model = next(self.model_list)

    def create_chat_completion(self, text):
        self.groq_client = Groq(api_key=next(self.keys))

        content = f"{self.prompt_template.format(text=text, language=self.language, crlf=linesep)}"
        sys_content = self.system_content or self.prompt_sys_msg.format(crlf="\n")

        messages = [
            {"role": "system", "content": sys_content},
            {"role": "user", "content": content},
        ]

        if self.deployment_id:
            return self.groq_client.chat.completions.create(
                engine=self.deployment_id,
                messages=messages,
                temperature=self.temperature,
                azure=True,
            )
        return self.groq_client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=self.temperature,
        )
