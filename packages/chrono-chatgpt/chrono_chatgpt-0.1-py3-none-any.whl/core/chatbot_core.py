from core.internet_module import InternetModule
import settings.setting_loader as setting_loader
import core.bot_initializer as bot_initializer
import logging


class ChatBotCore:
    def __init__(self):
        bot_settings = setting_loader.load()
        self.bot = bot_initializer.initialize(bot_settings)
        self.chatbot = self.bot
        #self.mode_path = "C:\\Users\\Terre\\Development\\_Experiments\\ChatGPT\\src\\revChatGPT\\config\\modes.json"
        self.mode_path = "settings\\modes.json"
        self.internet_module = InternetModule(self.bot)
        self.prompt_wrapper = lambda s: s

        self.internet_enabled = False
        self.is_internet_config_loaded = False

    def load_process_file_config(self):
        self.bot.load(self.mode_path, "conversation")


    def enable_default(self):
        self.prompt_wrapper = lambda prompt: f'{prompt}'

    def enable_internet(self):
        self.prompt_wrapper = lambda prompt: f'This is a prompt from a user to a chatbot: "{prompt}". Respond with "none" if it is directed at the chatbot or cannot be answered by an internet search. Otherwise, respond with a possible search query to a search engine. Do not write any additional text. Make it as minimal as possible'
        self.internet_enabled = True

    def enable_process_file(self):
        self.prompt_wrapper = lambda prompt: f"This is a file containing the filename of the file and file content from a user to a chatbot: {prompt}, do not talk about yourself, do not respond conversationally, and do not explain. just reply ok"

    def load_config(self):
        if not self.is_internet_config_loaded:
            self.bot.load(self.mode_path, "conversation")
            self.internet_enabled = True
            logging.info("internet config loaded!")
            self.is_internet_config_loaded = True


    def get_token_count(self, convo_id: str = "default") -> int:
        return self.chatbot.get_token_count(convo_id)

    def get_max_tokens(self, convo_id: str) -> int:
        return self.chatbot.get_max_tokens(convo_id)

    def ask_core(
        self,
        prompt: str,
        role: str = "user",
        convo_id: str = "default",
        temperature = 0,
        **kwargs,
    ) -> str:
        output="None"
        prompt_wrapper = self.prompt_wrapper
        if prompt_wrapper is not None:
            prompt = prompt_wrapper(prompt)

        if self.internet_enabled:
            output = self.internet_module.ask_using_internet(prompt, role, convo_id, temperature=temperature)
        else:
            output = self.internet_module.ask_default(prompt=prompt, role=role, convo_id=convo_id)
        return output

    def ask(self, prompt: str, role: str = "user", convo_id: str = "default", temperature=0, **kwargs) -> str:
        max_depth = 10
        for _ in range(max_depth):
            result = self.ask_core(prompt, role, convo_id, temperature)
            if "response" in result:
                return result["response"]
        return None

    def ask_stream(
        self,
        prompt: str,
        role: str = "user",
        convo_id: str = "default",
        **kwargs,
    ) -> str:
        return self.chatbot.ask_stream(prompt, role, convo_id, **kwargs)

    def rollback(self, n: int = 1, convo_id: str = "default") -> None:
        self.chatbot.rollback(n, convo_id)

    def reset(self, convo_id: str = "default", system_prompt: str = None) -> None:
        self.chatbot.reset(convo_id, system_prompt)

    def save(self, file: str, *keys: str) -> None:
        self.chatbot.save(file, *keys)

    def load(self, file: str, *keys: str) -> None:
        self.chatbot.load(file, *keys)
