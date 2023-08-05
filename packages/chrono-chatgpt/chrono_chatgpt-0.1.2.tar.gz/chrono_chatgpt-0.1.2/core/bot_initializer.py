from revChatGPT.V3 import ChatbotCLI

def initialize(settings)-> ChatbotCLI:
    chatbot = ChatbotCLI(
        api_key=settings["api_key"],
        system_prompt=settings["base_prompt"],
        proxy=settings["proxy"],
        temperature=settings["temperature"],
        top_p=settings["top_p"],
        reply_count=settings["reply_count"],
        engine=settings["model"],

    )
    return chatbot

